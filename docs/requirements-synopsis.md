# Review synopsis

**Title:** Student Feedback Analysis System  
**Difficulty:** Beginner  
**Stack:** HTML/CSS, Flask, MySQL, Pandas, NumPy, Matplotlib, pytest

**Problem:** Course feedback is hard to compare consistently, and exposing individual responses may compromise privacy.

**Objective:** Collect anonymous 1–5 course ratings, summarize response patterns by course and question, visualize the results, and export aggregate reports.

**Scope:** Course/question catalog, feedback form and JSON API, MySQL storage, rating validation, dashboard, three charts, aggregate CSV, tests and documentation.

**Out of scope:** student accounts, public comments, individual-level reporting, sentiment classification, or causal conclusions.

**Expected output:** total question-level ratings, overall average when the privacy threshold is met, course-wise and question-wise averages, five-category rating distribution, three charts and a CSV report.

**Privacy:** no student identifiers collected; comments are not shown in public reports; averages are suppressed when groups contain fewer than five ratings; demo data is synthetic.

**Formula:** Arithmetic mean = sum of valid ratings / count of valid ratings. Only ratings 1–5 are included.

**Milestones:** Week 1 (21–23 Oct 2026): synopsis, schema, routes, validation and core tests. Week 2 (28–30 Oct 2026): analysis, charts, integration, final documentation and demo.
