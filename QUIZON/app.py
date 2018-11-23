from flask import Flask, render_template, request, redirect, url_for, session
import db_utils
from argon2 import PasswordHasher
import numpy
from collections import defaultdict
import os

app = Flask(__name__)


@app.route('/')
@app.route('/login1.html', methods = ['GET', 'POST'])
def login():
	return render_template('login1.html')


@app.route('/signup.html', methods = ['GET', 'POST'])
def signup():
	return render_template('signup.html')


# To process login
@app.route('/process_login',methods=['POST'])
def process_login():
    if request.method == 'POST':
        data = request.form
        user = db.query('users',username=data['username'])
        if(len(user) == 1):
            print('Success: valid username')
            password = user[0]['passwd']
            try:
                if(ph.verify(password,data['password'])):
                    print('Success: valid password')
                    print(user[0]['username'])
                    session['username'] = user[0]['username']
                    print(session['username'])
                    return redirect(url_for('home_page'))
            except:
                print('Failure: invalid password')
                return redirect(url_for('login'))
        else:
            print('Failure: invalid username')
            return redirect(url_for('login'))


@app.route('/home_page.html', methods = ['GET', 'POST'])
def home_page():
	if(request.method == 'POST'):
		data = request.form
        #print(data)
		hashedPassword = ph.hash(data["password"])

		db.insert('users',username=data["username"],passwd=hashedPassword,email=data["emailid"], overall= 0)

	username = 'g'
	qid = db.execute_query_string("select qid ,result from user_quiz where username = '"+ username + "'")
	print(qid)
	quiz=[]

	for i in qid:
		d1 =defaultdict()
		id = str( i['qid'])
		qname = db.execute_query_string("select qname from quiz where qid = '"+ id + "'")
		print(qname)
		d1['qid'] = id
		d1['result'] = i['result']
		d1['qname'] = qname[0]['qname']
		quiz.append(d1)
		print(quiz)

	res =[]
	for i in quiz:
		res.append(i['result'])
	
	over = numpy.mean(res)
	print(over)
	return render_template('home_page.html', quiz = quiz, over = over)


@app.route('/take_quiz.html')
def take_quiz():
	return render_template('take_quiz.html')

# Handling logging out
@app.route('/logout.html')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    db = db_utils.db(database="quizon", user="root", password="root", host="localhost")
    ph = PasswordHasher()
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
