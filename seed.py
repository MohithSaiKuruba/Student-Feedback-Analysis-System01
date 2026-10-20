"""Seed synthetic feedback for demonstration only; never use real student data here."""
import random
from app import create_app
from db import get_connection, fetch_all

def main():
    app = create_app()
    with app.app_context():
        courses = fetch_all("SELECT course_id FROM courses")
        questions = fetch_all("SELECT question_id FROM feedback_questions WHERE is_active=1")
        if not courses or not questions:
            raise SystemExit("Run database/schema.sql first.")
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM feedback")
            if cur.fetchone()[0]:
                print("Feedback already exists; skipping to avoid duplicate demo rows.")
                return
            random.seed(42)
            for course in courses:
                for _ in range(12):
                    for question in questions:
                        rating = max(1, min(5, int(round(random.gauss(3.8, 0.9)))))
                        cur.execute("INSERT INTO feedback (course_id, question_id, rating) VALUES (%s,%s,%s)",
                                    (course["course_id"], question["question_id"], rating))
            conn.commit()
            print("Inserted synthetic demo feedback.")
        finally:
            conn.close()

if __name__ == "__main__":
    main()
