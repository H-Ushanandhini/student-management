from flask import Flask, session, redirect, url_for, render_template, request
from flask_bcrypt import Bcrypt
from db import get_connection
app=Flask(__name__)
app.secret_key='mykey123'
bcrypt=Bcrypt(app)

#register route
@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        hashed_pw=bcrypt.generate_password_hash(password).decode('utf-8')
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute('INSERT INTO users(username, password) VALUES (%s, %s)',(username, hashed_pw))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods= ['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        conn=get_connection()
        cursor=conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username= %s',(username,))
        user=cursor.fetchone()
        conn.close()

        if user and bcrypt.check_password_hash(user[2],password):
            session['username']= username
            return redirect(url_for('dashboard'))
        else:
            error='wrong user or password!'
            return render_template('login.html', error=error)
    return render_template('login.html')
    
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html',username= session['username'])

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__=='__main__':
    app.run(debug=True ,port=5001)