# Data dictionary

## courses
| Column | Type | Meaning |
|---|---|---|
| course_id | INT PK | Internal course key |
| course_code | VARCHAR(20) UNIQUE | Display code |
| course_name | VARCHAR(150) | Course title |
| instructor_label | VARCHAR(100), nullable | Non-personal faculty label for demo/catalog use |
| semester | VARCHAR(40) | Semester or cohort label |
| created_at | TIMESTAMP | Record creation time |

## feedback_questions
| Column | Type | Meaning |
|---|---|---|
| question_id | INT PK | Question key |
| question_text | VARCHAR(255) | Rating prompt |
| is_active | BOOLEAN | Whether question is included in the current form |
| display_order | INT | Form order |

## feedback
| Column | Type | Meaning |
|---|---|---|
| feedback_id | BIGINT PK | Individual stored rating row |
| course_id | INT FK | References courses.course_id |
| question_id | INT FK | References feedback_questions.question_id |
| rating | TINYINT UNSIGNED | Validated integer from 1 to 5 |
| comment_text | VARCHAR(1000), nullable | Optional comment; not shown publicly |
| submitted_at | TIMESTAMP | Submission timestamp |

The schema intentionally does not store student names, email addresses, student IDs, or IP addresses. A single form submission creates one row per question, so the dashboard's “Total ratings” is the number of question-level rating rows, not the number of completed forms.
