# Student Feedback Analysis System

A privacy-conscious Flask + MySQL application for collecting course feedback and analyzing aggregate ratings with Pandas, NumPy, and Matplotlib.

## Quick start

1. Install Python 3.10+ and MySQL 8+.
2. Create a database using `database/schema.sql`.
3. Create a virtual environment and install `requirements.txt`.
4. Copy `.env.example` to `.env` and set your MySQL credentials.
5. Run `python seed.py` to add sample courses/questions and synthetic feedback.
6. Run `python app.py` and open http://127.0.0.1:5000.

See `docs/PROJECT_PROPOSAL.md`, `docs/API.md`, and `docs/TESTING.md` for project deliverables. Never commit real credentials or identifiable student feedback. Aggregated results are suppressed for groups with fewer than 5 responses.
