# Final demonstration plan (10 minutes)

1. **0:00–1:00 — Problem and objective.** Explain why aggregated course feedback helps compare learning experiences and why anonymity matters.
2. **1:00–2:00 — Database.** Show `courses`, `feedback_questions`, and `feedback` tables; point out primary/foreign keys and the 1–5 constraint.
3. **2:00–3:30 — Live form.** Select a synthetic-demo course, submit a valid rating set, and show validation by attempting to submit with a missing rating.
4. **3:30–4:30 — API.** Demonstrate `/health`, `/api/courses`, and a sample `POST /api/feedback` request with a JSON client.
5. **4:30–6:30 — Analysis and charts.** Explain the Pandas group-by, NumPy arithmetic mean and rating distribution, then show rating distribution, course average, and question average charts.
6. **6:30–7:30 — Privacy.** Explain that names/student IDs are not collected, comments are not publicly displayed, and averages are suppressed below the configured threshold.
7. **7:30–8:30 — Export and tests.** Download aggregate CSV and run `pytest -q`; show actual test output.
8. **8:30–10:00 — Findings and limitations.** Describe patterns in the synthetic sample only; explain averages do not establish causes and production deployment needs security review.

## Preparation checklist
- Run schema SQL and seed script before the presentation.
- Use synthetic data only.
- Confirm the dashboard, API and CSV export work.
- Have terminal/test output ready.
- Do not describe generated sample patterns as real student opinion.
