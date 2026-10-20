# Test plan and report template

Run automated analytics tests from the project root:

```bash
pytest -q
```

## Cases to execute
| ID | Scenario | Input/action | Expected result |
|---|---|---|---|
| T01 | Normal analysis | Five valid ratings of 4 | Mean is 4.00; distribution count for rating 4 is 5 |
| T02 | Empty dataset | Analyze empty list | No crash; zero response count; no average |
| T03 | Small group | Four ratings in one group, threshold 5 | Average suppressed |
| T04 | Boundary low | Rating = 1 | Accepted |
| T05 | Boundary high | Rating = 5 | Accepted |
| T06 | Invalid rating | Rating = 0 or 6 | Submission rejected with 400/form error |
| T07 | Missing answer | Omit an active question | Submission rejected |
| T08 | Invalid course | Unknown course ID | Submission rejected |
| T09 | Long comment | More than 1000 characters | Submission rejected |
| T10 | Database offline | Stop MySQL and request /health | 503 response, no credentials leaked |
| T11 | CSV export | Request /export/summary.csv | CSV includes aggregate rows, never raw comments |
| T12 | API response privacy | Request /api/summary | No comment field or individual feedback records returned |

## Evidence to attach for submission
Capture screenshots of: dashboard with synthetic data, all three charts, feedback validation message, successful feedback submission, CSV opened in a spreadsheet, `pytest -q` output, and the health endpoint. Fill in actual pass/fail results after running on the demonstration machine; do not claim tests passed unless they were executed.
