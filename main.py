from flask import Flask,render_template,request,redirect,session
import mysql.connector
import os

app=Flask(__name__)
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost",user="root",password="raghav@#8959",port='3306',database="raghavg")
cursor=conn.cursor()


@app.route('/')
def login():
     return render_template('login.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('main_page.html')
    else:
        return redirect('/')

@app.route('/questions')
def questions():
     return render_template('que_ans.html')

@app.route('/admin')
def admin():
     return render_template('admin.html')



@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')

    cursor.execute("""SELECT * FROM `userr` WHERE `email` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/add_user',methods=['POST'])
def add_user():
    name=request.form.get('uname')
    email=request.form.get('uemail')
    password=request.form.get('upassword')
    cursor.execute("""INSERT INTO `userr` (`user_id`,`name`,`email`,`password`) VALUES
    (NULL,'{}','{}','{}')""".format(name,email,password))
    conn.commit()
    cursor.execute("""SELECT * FROM `userr` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/home')

@app.route('/login_admin' ,methods=['POST'])
def login_admin():
    username=request.form.get('vusername')
    password=request.form.get('vpassword')

    cursor.execute("""SELECT * FROM `adminr` WHERE `username` LIKE '{}' AND `password` LIKE '{}'"""
                   .format(username,password))
    uusers=cursor.fetchall()
    if len(uusers)>0:
        session['user_id']=uusers[0][0]
        return "welcome admin"
    else:
        return ('/')


@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')

@app.route('/securityque')
def securityque():
    return redirect('/questions')

@app.route('/adminpage')
def adminpage():
    return redirect('/admin')



if __name__=="__main__":
    app.run(debug=True)