# API reference

Local base URL: `http://127.0.0.1:5000`.

| Method | Endpoint | Purpose | Success |
|---|---|---|---|
| GET | `/health` | App and MySQL connectivity | 200, or 503 if DB unavailable |
| GET | `/api/courses` | List available courses | 200 |
| GET | `/api/questions` | List active feedback questions | 200 |
| POST | `/api/feedback` | Submit anonymous numeric ratings | 201 |
| GET | `/api/summary` | Aggregated analysis only | 200 |
| GET | `/export/summary.csv` | Download aggregate report | 200 |

## Submit feedback

Content-Type: `application/json`

```json
{
  "course_id": 1,
  "ratings": [
    {"question_id": 1, "rating": 4},
    {"question_id": 2, "rating": 5},
    {"question_id": 3, "rating": 4},
    {"question_id": 4, "rating": 3}
  ],
  "comment": "The examples were helpful."
}
```

Ratings must be integers from 1 to 5. Exactly one rating is required for each active question. Course and question IDs must exist. Comments are optional and limited to 1000 characters. Invalid payloads return 400; database failures return 503.

## Privacy
Summary averages are suppressed for groups smaller than `MIN_GROUP_SIZE` (default 5). The API never returns raw comments or individual feedback rows. CSV export contains aggregate course/question rows only. Avoid collecting identity fields and do not publish free-text comments.
