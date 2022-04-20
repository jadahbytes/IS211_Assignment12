DROP TABLE IF EXISTS

CREATE TABLE students (
  student_id INTEGER PRIMARY KEY AUTOINCREMENT,
  firstname TEXT NOT NULL,
  lastname TEXT NOT NULL,
);

CREATE TABLE quizzes (
  quiz_id INTEGER PRIMARY KEY AUTOINCREMENT,
  subject TEXT NOT NULL,
  total_questions TEXT NOT NULL,
  date_given
);

CREATE TABLE student_scores (
  student_id INTEGER NOT NULL,
  quiz_id INTEGER NOT NULL,
  score INTEGER NOT NULL
);
