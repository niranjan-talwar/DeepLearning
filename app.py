import subprocess
from flask import Flask, render_template,request,redirect,url_for,session
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import streamlit as st
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import pymysql

app = Flask(__name__)
app.secret_key = 'xyzsdfg'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'user-system'

mysql = MySQL(app)




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s AND password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']
            mesage = 'Logged in successfully !'
            return render_template('checkout-form.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
            
                
    return render_template('index.html', mesage = mesage)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form and 'security-question' in request.form and 'security-answer' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        question = request.form['security-question']
        answer = request.form['security-answer']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s, % s, % s)', (userName, email, password, question, answer,))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
   
    return render_template('index.html', mesage = mesage)

@app.route('/transaction', methods =['GET', 'POST'])
def transaction():
    if request.method == 'POST' and 'firstname' in request.form and 'email' in request.form and 'address' in request.form and 'city' in request.form and 'state' in request.form and 'zip' in request.form and 'cardname' in request.form and 'cardnumber' in request.form and 'expmonth' in request.form and 'expyear' in request.form and 'cvv' in request.form and 'latitude' in request.form and 'longitude' in request.form:
        userName = request.form['firstname']
        email = request.form['email']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        zipi = request.form['zip']
        cname=request.form['cardname']
        cnumber = request.form['cardnumber']
        emonth = request.form['expmonth']
        eyear = request.form['expyear']
        cvv = request.form['cvv']
        lat = request.form['latitude']
        lon = request.form['longitude']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO transaction VALUES (% s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s, % s)', (lat, lon, userName, email, address, city, zipi, state, cname, cnumber, emonth, cvv, eyear))
        mysql.connection.commit()
        mesage = 'You have successfully initiated transaction !'
    return redirect(url_for('checking'))

@app.route('/security', methods=['POST'])
def security():
    email=request.form.get('email')
    answer=request.form.get('security-answer')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT Answer FROM user WHERE email = % s', (email, ))
    result = cursor.fetchone()
    ans=result['Answer']
    msg='security question verified'
    if ans:
        if ans==answer:
            return render_template('success1.html', msg=msg) 
        else:
            return render_template('failure1.html', msg=msg)
    else:
        return 'user not found'
    

@app.route('/failure')
def failure():
    return render_template('failure.html')

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout-form.html')

@app.route('/checking', methods=['POST','GET'])
def checking():
    subprocess.Popen(['streamlit','run','pyth.py'])
    return 'Streamlit app is running'



if __name__ == "__main__":
    app.run()