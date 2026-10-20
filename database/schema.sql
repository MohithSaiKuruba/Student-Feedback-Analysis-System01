CREATE DATABASE IF NOT EXISTS student_feedback
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE student_feedback;

CREATE TABLE IF NOT EXISTS courses (
  course_id INT AUTO_INCREMENT PRIMARY KEY,
  course_code VARCHAR(20) NOT NULL UNIQUE,
  course_name VARCHAR(150) NOT NULL,
  instructor_label VARCHAR(100) NULL,
  semester VARCHAR(40) NOT NULL DEFAULT 'Current',
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedback_questions (
  question_id INT AUTO_INCREMENT PRIMARY KEY,
  question_text VARCHAR(255) NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT TRUE,
  display_order INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS feedback (
  feedback_id BIGINT AUTO_INCREMENT PRIMARY KEY,
  course_id INT NOT NULL,
  question_id INT NOT NULL,
  rating TINYINT UNSIGNED NOT NULL,
  comment_text VARCHAR(1000) NULL,
  submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_feedback_course FOREIGN KEY (course_id) REFERENCES courses(course_id),
  CONSTRAINT fk_feedback_question FOREIGN KEY (question_id) REFERENCES feedback_questions(question_id),
  CONSTRAINT chk_feedback_rating CHECK (rating BETWEEN 1 AND 5),
  INDEX idx_feedback_course_question (course_id, question_id),
  INDEX idx_feedback_submitted (submitted_at)
);

INSERT IGNORE INTO courses (course_code, course_name, instructor_label, semester) VALUES
('CS201','Database Management Systems','Faculty A','Semester 3'),
('CS202','Python Programming','Faculty B','Semester 3'),
('CS203','Data Structures','Faculty C','Semester 3'),
('CS204','Web Technologies','Faculty D','Semester 3');

INSERT INTO feedback_questions (question_text, display_order)
SELECT 'How clearly were concepts explained?', 1
WHERE NOT EXISTS (SELECT 1 FROM feedback_questions WHERE question_text='How clearly were concepts explained?');
INSERT INTO feedback_questions (question_text, display_order)
SELECT 'How useful were the learning materials?', 2
WHERE NOT EXISTS (SELECT 1 FROM feedback_questions WHERE question_text='How useful were the learning materials?');
INSERT INTO feedback_questions (question_text, display_order)
SELECT 'How engaging were the classes?', 3
WHERE NOT EXISTS (SELECT 1 FROM feedback_questions WHERE question_text='How engaging were the classes?');
INSERT INTO feedback_questions (question_text, display_order)
SELECT 'How confident do you feel applying what you learned?', 4
WHERE NOT EXISTS (SELECT 1 FROM feedback_questions WHERE question_text='How confident do you feel applying what you learned?');
