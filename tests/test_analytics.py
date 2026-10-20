from analytics import summarize_feedback

def rows_for(count, rating=4):
    return [{"course_id": 1, "course_name": "Demo", "question_id": 1,
             "question_text": "Clarity", "rating": rating, "submitted_at": "2026-01-01"} for _ in range(count)]

def test_empty_data_returns_empty_summary():
    result = summarize_feedback([], min_group_size=5)
    assert result["total_responses"] == 0
    assert result["overall"] is None
    assert result["by_course"] == []

def test_valid_ratings_are_averaged():
    result = summarize_feedback(rows_for(5, 4), min_group_size=5)
    assert result["overall"] == 4.0
    assert result["by_course"][0]["average_rating"] == 4.0
    assert result["distribution"][3]["count"] == 5

def test_small_group_average_is_suppressed():
    result = summarize_feedback(rows_for(4, 5), min_group_size=5)
    assert result["overall"] is None
    assert result["by_course"][0]["average_rating"] is None

def test_invalid_ratings_are_ignored():
    rows = rows_for(5, 3) + [{"course_id": 1, "course_name": "Demo", "question_id": 1,
                              "question_text": "Clarity", "rating": 9, "submitted_at": "2026-01-01"}]
    result = summarize_feedback(rows, min_group_size=5)
    assert result["total_responses"] == 5
