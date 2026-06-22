from flask import Flask, render_template,request, redirect,url_for
from db import get_connection
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/add', methods=['POST'])
def add_student():
    name=request.form['name']
    email=request.form['email']
    conn=get_connection()
    cursor= conn.cursor()
    cursor.execute('INSERT INTO students(name, email) VALUES (%s, %s)',(name, email))
    conn.commit()
    conn.close()
    return redirect(url_for('view_students'))

@app.route('/students')
def view_students():
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM students')
    students=cursor.fetchall()
    conn.close()
    return render_template('students.html', students=students)

@app.route('/delete/<int:id>')
def delete_student(id):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute('DELETE FROM students WHERE id= %s', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_students'))

@app.route('/edit/<int:id>', methods=['GET','POST'])
def edit_student(id):
    conn=get_connection()
    cursor=conn.cursor()
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        cursor.execute('UPDATE students SET name= %s, email= %s WHERE id= %s',(name, email, id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_students'))
    cursor.execute('SELECT * FROM students WHERE id= %s', (id,))
    student=cursor.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

if __name__ == '__main__':
    app.run(debug=True,port=5001)
