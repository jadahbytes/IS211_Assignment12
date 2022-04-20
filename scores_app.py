from flask import Flask, render_template, session, redirect, request, current_app, g, flash
import sqlite3

app = Flask(__name__)


conn = sqlite3.connect('C:/Users/Jadah/IS211_Assignment12/hw12.db')
print("Opened database successfully!")

cur = conn.cursor()

check_username = 'abbott'
check_password = 'elementary'
app.secret_key = '01110011'


# students = {
#     1 : ['John', 'Smith'],
#     2 : ['Jadah', 'Stone'],
#     3 : ['Rusty', 'Goldbaum']
# }
#
# quizzes = {
#     1 : ['Python Basics', 5, 'February, 5, 2015'],
#     2 : ['Power BI Reporting', 15, 'March, 10, 2015']
# }
#
# student_scores = {
#     1 : [1, 1, 85],
#     2 : [1, 2, 100],
#     3 : [3, 2, 99]
# }
# # drop tables @ start of program
# for table in ('students', 'quizzes', 'student_scores'):
#     cur.execute(f'DROP TABLE IF EXISTS {table}')
#
# # create tables
# cur.execute('''CREATE TABLE students (
#             firstname TEXT,
#             lastname TEXT)''')
# print("Table created successfully!")
#
# cur.execute('''CREATE TABLE quizzes (
#             subject TEXT,
#             total_questions TEXT,
#             date_given TEXT)''')
# print("Table created successfully!")
#
# cur.execute('''CREATE TABLE student_scores (
#             student_id INTEGER,
#             quiz_id INTEGER,
#             score INTEGER)''')
# print("Table created successfully!")
#
# def populate_table(dict, table):
#     #add student + quiz data to table
#     for k, v in dict.items():
#         if table == 'students':
#             cur.execute(f'INSERT INTO {table} VALUES (?,?)', (v))
#         else:
#             cur.execute(f'INSERT INTO {table} VALUES (?,?,?)', (v))
#     conn.commit()
#
# populate_table(students, 'students')
# populate_table(quizzes, 'quizzes')
# populate_table(student_scores, 'student_scores')


@app.route('/', methods=['GET'])
def main_page():
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != check_username:
            error = "Incorrect Username! Please try again"
        elif request.form['password'] != check_password:
            error = 'Invalid Password! Please try again.'
        else:
            session['logged_in'] = True
            return redirect('/dashboard')

    return render_template('login.html', error=error)


@app.route('/dashboard', methods=['GET'])
def dashboard():
    conn = sqlite3.connect('hw12.db')
    cur = conn.cursor()
    if session['logged_in'] == True:
        cur.execute('''SELECT rowid,
                        firstname,
                        lastname
                        FROM students''')
        students = cur.fetchall()
        cur.execute('''SELECT rowid,
                        subject,
                        total_questions,
                        date_given
                        FROM quizzes''')
        quizzes = cur.fetchall()
    else:
        error = "You must login to continue."
        return render_template('login.html', error=error)
    return render_template('dashboard.html', students=students, quizzes=quizzes)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    error = None
    conn = sqlite3.connect('hw12.db')
    cur = conn.cursor()
    if session['logged_in'] == True:
        if request.method == 'GET':
            return render_template('newstudent.html')
        elif request.method == 'POST':
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            cur.execute('INSERT INTO students VALUES (?,?)', (firstname, lastname))
            conn.commit()
            print(f'{firstname}, {lastname} added to students table!')
            return redirect('/dashboard')
        else:
            error = "An error occurred. Please try again."
            return render_template('newstudent.html', error=error)
    else:
        error = "You must login to continue."
        return render_template('login.html', error=error)

@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    error = None
    conn = sqlite3.connect('hw12.db')
    cur = conn.cursor()
    if session['logged_in'] == True:
        if request.method == 'GET':
            return render_template('newquiz.html')
        elif request.method == 'POST':
            subject = request.form['subject']
            total_questions = request.form['total_questions']
            date_given = f"{request.form['month_day']}, {request.form['year']}"
            cur.execute('INSERT INTO quizzes VALUES (?,?,?)', (subject, total_questions, date_given))
            conn.commit()
            return redirect('/dashboard')
        else:
            error = "An error occurred. Please try again."
            return render_template('newquiz.html', error=error)
    else:
        error = "You must login to continue."
        return render_template('login.html', error=error)

@app.route('/student/<id>')
def quiz_results(id):
    error = None
    conn = sqlite3.connect('hw12.db')
    cur = conn.cursor()
    if session['logged_in'] == True:
        cur.execute('''SELECT
                        students.firstname || " " || students.lastname as Name,
                        student_scores.rowid,
                        quizzes.subject,
                        student_scores.score
                        FROM student_scores
                        JOIN students
                        ON student_scores.student_id = students.rowid
                        JOIN quizzes
                        ON student_scores.student_id = quizzes.rowid
                        WHERE student_scores.student_id == ?''', id)
        quiz_results = cur.fetchall()
        print(quiz_results)
        if len(quiz_results) != 0:
            return render_template('quizresults.html', results=quiz_results, error=error)
        else:
            error = "No results for selected student."
            return render_template('quizresults.html', results=quiz_results, error=error)

@app.route('/results/add', methods=['GET', 'POST'])
def add_score():
    error = None
    conn = sqlite3.connect('hw12.db')
    cur = conn.cursor()
    if session['logged_in'] == True:
        try:
            if request.method == 'GET':
                cur.execute('''SELECT rowid,
                               firstname || "" || lastname
                               FROM students''')
                students = cur.fetchall()
                cur.execute('''SELECT rowid,
                               subject
                               FROM quizzes''')
                quizzes = cur.fetchall()
                print(students)
                return render_template('newscores.html', students=students, quizzes=quizzes)
            elif request.method == 'POST':
                student = request.form['student']
                quiz = request.form['quiz']
                grade = request.form['grade']
                cur.execute('INSERT INTO student_scores VALUES (?,?,?)', (student, quiz, grade))
                conn.commit()
                return redirect('/dashboard')
        except:
            flash("An error occurred. Please try again.")
            return redirect('/results/add')

if __name__ == "__main__":
    app.run(debug=True)
