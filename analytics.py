from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RATING_LABELS = [1, 2, 3, 4, 5]

def summarize_feedback(rows, min_group_size=5):
    df = pd.DataFrame(rows)
    if df.empty or "rating" not in df.columns:
        return {"overall": None, "by_course": [], "by_question": [], "distribution": [{"rating": r, "count": 0} for r in RATING_LABELS], "total_responses": 0}
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df[df["rating"].between(1, 5)].copy()
    if df.empty:
        return {"overall": None, "by_course": [], "by_question": [], "distribution": [{"rating": r, "count": 0} for r in RATING_LABELS], "total_responses": 0}

    total = int(len(df))
    overall = round(float(np.mean(df["rating"].to_numpy(dtype=float))), 2) if total >= min_group_size else None
    def grouped(keys, name_key):
        result = df.groupby(keys, dropna=False).agg(responses=("rating", "size"), average_rating=("rating", "mean")).reset_index()
        result["average_rating"] = result["average_rating"].round(2)
        result["average_rating"] = result.apply(lambda row: row["average_rating"] if row["responses"] >= min_group_size else None, axis=1)
        return result.to_dict("records")
    by_course = grouped(["course_id", "course_name"], "course_name") if {"course_id", "course_name"}.issubset(df.columns) else []
    by_question = grouped(["question_id", "question_text"], "question_text") if {"question_id", "question_text"}.issubset(df.columns) else []
    counts = df["rating"].value_counts().reindex(RATING_LABELS, fill_value=0)
    return {
        "overall": overall, "by_course": by_course, "by_question": by_question,
        "distribution": [{"rating": int(r), "count": int(c)} for r, c in counts.items()],
        "total_responses": total,
    }

def create_charts(rows, output_dir, min_group_size=5):
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(rows)
    if df.empty or "rating" not in df.columns:
        return []
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df[df["rating"].between(1, 5)]
    if df.empty:
        return []
    created = []
    counts = df["rating"].value_counts().reindex(RATING_LABELS, fill_value=0)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar([str(r) for r in RATING_LABELS], counts.values)
    ax.set(title="Feedback Rating Distribution", xlabel="Rating (1 = low, 5 = high)", ylabel="Number of responses")
    fig.tight_layout()
    path = output / "rating_distribution.png"; fig.savefig(path, dpi=140); plt.close(fig); created.append(path.name)

    if {"course_name", "rating"}.issubset(df.columns):
        grouped = df.groupby("course_name")["rating"].agg(["mean", "count"])
        grouped = grouped[grouped["count"] >= min_group_size]
        if not grouped.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.bar(grouped.index.astype(str), grouped["mean"])
            ax.set(title="Average Rating by Course", xlabel="Course", ylabel="Average rating (1–5)")
            ax.set_ylim(0, 5); ax.tick_params(axis="x", rotation=20)
            fig.tight_layout()
            path = output / "course_averages.png"; fig.savefig(path, dpi=140); plt.close(fig); created.append(path.name)

    if {"question_text", "rating"}.issubset(df.columns):
        grouped = df.groupby("question_text")["rating"].agg(["mean", "count"])
        grouped = grouped[grouped["count"] >= min_group_size]
        if not grouped.empty:
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.barh(grouped.index.astype(str), grouped["mean"])
            ax.set(title="Average Rating by Question", xlabel="Average rating (1–5)", ylabel="Feedback question")
            ax.set_xlim(0, 5); fig.tight_layout()
            path = output / "question_averages.png"; fig.savefig(path, dpi=140); plt.close(fig); created.append(path.name)
    return created
