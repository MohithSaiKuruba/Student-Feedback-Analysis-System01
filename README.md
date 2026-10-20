# Student Feedback Analysis System

A responsive, privacy-conscious Flask + MySQL website for collecting course feedback and analyzing rating patterns with Pandas, NumPy, and Matplotlib.

## Features
- Responsive dashboard, anonymous rating form, and server-side validation for ratings from 1 to 5.
- MySQL courses, questions, and feedback tables with primary/foreign keys and a rating constraint.
- Pandas grouped summaries, NumPy averages/distributions, and three Matplotlib charts: rating distribution, average by course, average by question.
- Aggregate-only CSV export and JSON API.
- Database health endpoint, synthetic demo seed, tests, GitHub Actions workflow, and project documentation.
- Averages are suppressed for groups smaller than five ratings by default.

## Requirements
Python 3.10+, MySQL 8+, and pip.

## Local setup
1. Clone the repository and open its directory.
2. Create/activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```
3. Install dependencies: `pip install -r requirements.txt`
4. Run `database/schema.sql` in MySQL Workbench or the MySQL CLI.
5. Copy `.env.example` to `.env`. Set your local MySQL credentials and a strong random `FLASK_SECRET_KEY`. Never commit `.env`.
6. Optional synthetic demo data: `python seed.py`
7. Start the app: `python app.py`
8. Open `http://127.0.0.1:5000`.

If `/health` fails, confirm MySQL is running, the schema script completed, and the `.env` settings are correct.

## API endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | App/database health |
| GET | `/api/courses` | List courses |
| GET | `/api/questions` | List active questions |
| POST | `/api/feedback` | Submit ratings as JSON |
| GET | `/api/summary` | Aggregated analysis |
| GET | `/export/summary.csv` | Download aggregate CSV |

See [API documentation](docs/API.md) for the request format.

## Analysis and charts
- Ratings are valid only in the inclusive range 1–5.
- Arithmetic mean = sum of valid ratings / count of valid ratings.
- Pandas calculates group summaries; NumPy calculates the overall mean and rating distribution.
- Matplotlib charts include titles, labeled axes, units, and interpretation notes.
- Course/question averages are suppressed below `MIN_GROUP_SIZE` (default 5).
- “Total ratings” means question-level rating records, not completed forms.
- Charts are generated at runtime under `static/generated/` and are ignored by Git.

## Tests
Run `pytest -q`. Current analytics tests cover empty data, valid averages, small-group suppression, and invalid ratings. Database-dependent end-to-end checks should be run against a local MySQL instance; see [testing plan](docs/TESTING.md). Do not claim tests passed until you have run them.

## Project deliverables
- [Project proposal and scope](docs/PROJECT_PROPOSAL.md)
- [Review synopsis](docs/requirements-synopsis.md)
- [ER diagram source](docs/ER_DIAGRAM.md)
- [Data dictionary](docs/DATA_DICTIONARY.md)
- [API reference](docs/API.md)
- [Test plan](docs/TESTING.md)
- [10-minute demo plan](docs/DEMO_PLAN.md)
- [MySQL schema and sample catalog](database/schema.sql)

## Privacy, security and limitations
- No student names, IDs, or email addresses are collected.
- Optional comments are stored but never shown by the dashboard, summary API, or CSV export. Avoid entering personal details in comments.
- Demo data is synthetic and must not be presented as real student opinion.
- Averages describe ratings; they do not prove causes or sentiment.
- This is an educational prototype. Before production deployment, add CSRF protection, authentication/authorization for administration, rate limiting, HTTPS, secret management, and a data-retention policy.
