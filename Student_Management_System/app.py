from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def reset_db():
    conn = get_db_connection()
    conn.execute('DROP TABLE IF EXISTS students')
    conn.execute('''
    CREATE TABLE students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll TEXT NOT NULL,
        gender TEXT NOT NULL,
        dob TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        address TEXT NOT NULL,
        branch TEXT NOT NULL,
        year TEXT NOT NULL,
        semester TEXT NOT NULL,
        section TEXT NOT NULL,
        enrollment_year INTEGER NOT NULL,
        cgpa TEXT,
        backlogs INTEGER
    )
    ''')
    conn.commit()
    conn.close()
    print("[Database Reset Successfully!]")

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT * FROM students').fetchall()
    conn.close()
    return render_template('index.html', students=students)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        gender = request.form['gender']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        branch = request.form['branch']
        year = request.form['year']
        semester = request.form['semester']
        section = request.form['section']
        enrollment_year = request.form['enrollment_year']
        cgpa = request.form.get('cgpa') or None
        backlogs = request.form.get('backlogs') or 0

        conn = get_db_connection()
        conn.execute('''
            INSERT INTO students (name, roll, gender, dob, email, phone, address, branch, year, semester, section, enrollment_year, cgpa, backlogs)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, roll, gender, dob, email, phone, address, branch, year, semester, section, enrollment_year, cgpa, backlogs))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    student = conn.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()

    if student is None:
        conn.close()
        return 'Student not found!', 404

    if request.method == 'POST':
        name = request.form['name']
        roll = request.form['roll']
        gender = request.form['gender']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        branch = request.form['branch']
        year = request.form['year']
        semester = request.form['semester']
        section = request.form['section']
        enrollment_year = request.form['enrollment_year']
        cgpa = request.form.get('cgpa') or None
        backlogs = request.form.get('backlogs') or 0

        conn.execute('''
            UPDATE students
            SET name = ?, roll = ?, gender = ?, dob = ?, email = ?, phone = ?, address = ?, branch = ?, year = ?, semester = ?, section = ?, enrollment_year = ?, cgpa = ?, backlogs = ?
            WHERE id = ?
        ''', (name, roll, gender, dob, email, phone, address, branch, year, semester, section, enrollment_year, cgpa, backlogs, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))

    conn.close()
    return render_template('edit.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM students WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    reset_db()  
    app.run(debug=True)
