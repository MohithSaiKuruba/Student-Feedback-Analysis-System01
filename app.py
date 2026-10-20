import csv
import io
import os
from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, Response
from mysql.connector import Error
from config import Config
from db import get_connection, fetch_all, fetch_one
from analytics import summarize_feedback, create_charts

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)

    def feedback_rows():
        return fetch_all("""SELECT f.course_id, c.course_name, f.question_id, q.question_text,
                                   f.rating, f.submitted_at
                            FROM feedback f
                            JOIN courses c ON c.course_id=f.course_id
                            JOIN feedback_questions q ON q.question_id=f.question_id""")

    def insert_answers(course_id, answers, comment):
        questions = fetch_all("SELECT question_id FROM feedback_questions WHERE is_active=1 ORDER BY display_order, question_id")
        valid_ids = {int(q["question_id"]) for q in questions}
        normalized = [(int(a["question_id"]), int(a["rating"])) for a in answers]
        if len(normalized) != len(valid_ids) or {qid for qid, _ in normalized} != valid_ids:
            raise ValueError("Provide exactly one rating for every active question.")
        if any(rating < 1 or rating > 5 for _, rating in normalized):
            raise ValueError("Ratings must be whole numbers from 1 to 5.")
        if len(comment) > 1000:
            raise ValueError("Comment must be 1000 characters or fewer.")
        if not fetch_one("SELECT course_id FROM courses WHERE course_id=%s", (course_id,)):
            raise ValueError("Choose a valid course.")
        conn = get_connection()
        try:
            cursor = conn.cursor()
            for qid, rating in normalized:
                cursor.execute(
                    "INSERT INTO feedback (course_id, question_id, rating, comment_text) VALUES (%s,%s,%s,%s)",
                    (course_id, qid, rating, comment or None),
                )
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @app.get("/health")
    def health():
        try:
            conn = get_connection(); conn.close()
            return jsonify(status="ok", database="connected")
        except Error:
            return jsonify(status="degraded", database="unavailable"), 503

    @app.get("/")
    def dashboard():
        try:
            courses = fetch_all("SELECT course_id, course_code, course_name, semester FROM courses ORDER BY course_name")
            questions = fetch_all("SELECT question_id, question_text FROM feedback_questions WHERE is_active=1 ORDER BY display_order, question_id")
            rows = feedback_rows()
            summary = summarize_feedback(rows, app.config["MIN_GROUP_SIZE"])
            charts = create_charts(rows, os.path.join(app.root_path, "static", "generated"), app.config["MIN_GROUP_SIZE"])
            return render_template("index.html", courses=courses, questions=questions, summary=summary, charts=charts, db_unavailable=False)
        except Error:
            return render_template("index.html", courses=[], questions=[], summary={"overall": None, "by_course": [], "by_question": [], "distribution": [], "total_responses": 0}, charts=[], db_unavailable=True), 503

    @app.post("/feedback")
    def submit_feedback():
        try:
            course_id = request.form.get("course_id", type=int)
            ratings = request.form.getlist("rating")
            if not course_id or not ratings:
                raise ValueError("Choose a course and rate every question.")
            questions = fetch_all("SELECT question_id FROM feedback_questions WHERE is_active=1 ORDER BY display_order, question_id")
            if len(questions) != len(ratings):
                raise ValueError("Please rate every question and submit again.")
            answers = [{"question_id": q["question_id"], "rating": rating} for q, rating in zip(questions, ratings)]
            insert_answers(course_id, answers, request.form.get("comment", "").strip())
            flash("Thank you — your anonymous feedback has been recorded.", "success")
        except (ValueError, TypeError, KeyError) as exc:
            flash(str(exc), "error")
        except Error:
            flash("The database is unavailable. Your feedback was not saved; please try again later.", "error")
        return redirect(url_for("dashboard"))

    @app.get("/api/courses")
    def api_courses():
        try:
            return jsonify(data=fetch_all("SELECT course_id, course_code, course_name, semester FROM courses ORDER BY course_name"))
        except Error:
            return jsonify(error="Database unavailable"), 503

    @app.get("/api/questions")
    def api_questions():
        try:
            return jsonify(data=fetch_all("SELECT question_id, question_text FROM feedback_questions WHERE is_active=1 ORDER BY display_order, question_id"))
        except Error:
            return jsonify(error="Database unavailable"), 503

    @app.post("/api/feedback")
    def api_submit_feedback():
        payload = request.get_json(silent=True) or {}
        try:
            course_id = int(payload.get("course_id", 0))
            answers = payload.get("ratings", [])
            comment = str(payload.get("comment", "")).strip()
            if not course_id or not isinstance(answers, list) or not answers:
                raise ValueError("course_id and a non-empty ratings array are required")
            insert_answers(course_id, answers, comment)
            return jsonify(message="Feedback recorded anonymously"), 201
        except (ValueError, TypeError, KeyError) as exc:
            return jsonify(error=str(exc)), 400
        except Error:
            return jsonify(error="Database unavailable"), 503

    @app.get("/api/summary")
    def api_summary():
        try:
            return jsonify(data=summarize_feedback(feedback_rows(), app.config["MIN_GROUP_SIZE"]))
        except Error:
            return jsonify(error="Database unavailable"), 503

    @app.get("/export/summary.csv")
    def export_summary():
        try:
            summary = summarize_feedback(feedback_rows(), app.config["MIN_GROUP_SIZE"])
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Course", "Question", "Responses", "Average rating (1–5)"])
            for item in summary["by_course"]:
                writer.writerow([item.get("course_name"), "All questions", item.get("responses"), item.get("average_rating") if item.get("average_rating") is not None else "Suppressed"])
            for item in summary["by_question"]:
                writer.writerow(["All courses", item.get("question_text"), item.get("responses"), item.get("average_rating") if item.get("average_rating") is not None else "Suppressed"])
            return Response(output.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=feedback-summary.csv"})
        except Error:
            return jsonify(error="Database unavailable"), 503

    return app

app = create_app()
if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "0") == "1")
