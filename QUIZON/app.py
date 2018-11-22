from flask import Flask, render_template, request, redirect, url_for, session
import db_utils
import numpy
from collections import defaultdict
import os

app = Flask(__name__)


@app.route('/')
@app.route('/login.html', methods = ['GET', 'POST'])
def login():
	return render_template('login.html')


@app.route('/home_page.html')
def home_page():
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

if __name__ == '__main__':
    db = db_utils.db(database="quizon", user="root", password="root", host="localhost")
    app.run()
