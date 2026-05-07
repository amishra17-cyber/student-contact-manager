from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            email   TEXT NOT NULL,
            phone   TEXT NOT NULL,
            course  TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    search = request.args.get('search', '')
    if search:
        c.execute("SELECT * FROM students WHERE name LIKE ?", ('%' + search + '%',))
    else:
        c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template('index.html', students=students, search=search)

@app.route('/add', methods=['POST'])
def add():
    name   = request.form['name']
    email  = request.form['email']
    phone  = request.form['phone']
    course = request.form['course']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO students (name, email, phone, course) VALUES (?, ?, ?, ?)",
              (name, email, phone, course))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE id = ?", (id,))
    student = c.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    name   = request.form['name']
    email  = request.form['email']
    phone  = request.form['phone']
    course = request.form['course']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE students SET name=?, email=?, phone=?, course=? WHERE id=?",
              (name, email, phone, course, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)