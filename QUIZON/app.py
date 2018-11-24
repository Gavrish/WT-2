from flask import Flask, render_template, request, redirect, url_for, session
import db_utils
from flask_restful import Resource, Api
import json

from argon2 import PasswordHasher

import numpy
from collections import defaultdict
import os,random

app = Flask(__name__)

api = Api(app)

questions=[]
questionaireLen=0


# @app.route('/login.html', methods = ['GET', 'POST'])
def updateQuestionaire():
	with open('./static/celeb.txt') as f:
	    data = json.load(f)


	randomIndexes=random.sample(range(0, len(data)), len(data)-1)
	for i in range(0,len(data)-1):
		questions.append(data[randomIndexes[i]])

	print(questions)
	return len(data)

currentQuestionIndex=int()
class GetQuestion(Resource):

	def post(self):
		global questions
		global currentQuestionIndex
		global questionaireLen
		nextQuestion={}
		data=request.get_json();
		if(data["questionIndex"]==""):
			questionaireLen=updateQuestionaire()
			nextQuestion["resultsArray"]=[]  #total,correct
			nextQuestion["resultsArray"].extend([questionaireLen,0,0])
		else:
			print	("Hi in next question ",data["currentAnswer"], " ",data["questionIndex"] )
			nextQuestion["resultsArray"]=[]
			if data["currentAnswer"]==questions[data["questionIndex"]]: # correctAnswer
				print("Exec")

				nextQuestion["resultsArray"].append(questionaireLen)
				nextQuestion["resultsArray"].append(int(data["resultsArray"][1])+1)
				nextQuestion["resultsArray"].append(int(data["resultsArray"][2]))




			else:
				nextQuestion["resultsArray"].append(questionaireLen)
				nextQuestion["resultsArray"].append(int(data["resultsArray"][1]))
				nextQuestion["resultsArray"].append(int(data["resultsArray"][2])+1)


		options=random.sample(range(0, 99), 3)
		answerIndex=random.randint(0,3)
		nextQuestion["answer"]=answerIndex;
		nextQuestion["options"]=[]

		for i in range(0, 4):
			if i==answerIndex:
				nextQuestion["options"].append(questions[currentQuestionIndex])
			else:
				nextQuestion["options"].append(questions[options.pop()])

		print(nextQuestion["options"])
		nextQuestion["questionIndex"]=currentQuestionIndex;
		currentQuestionIndex+=1
		return json.dumps(nextQuestion)

api.add_resource(GetQuestion, '/getQuestion')


@app.route('/signup.html', methods = ['GET', 'POST'])
def signup():
	return render_template('signup.html')



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
	# session[username]={}
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
@app.route('/')
@app.route('/login1.html', methods = ['GET', 'POST'])
def login():
	return render_template('login1.html')
if __name__ == '__main__':
    db = db_utils.db(database="quizon", user="postgres", password="a", host="localhost")
    ph = PasswordHasher()
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.run()
