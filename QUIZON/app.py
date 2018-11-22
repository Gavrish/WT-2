from flask import Flask, render_template, request, redirect, url_for
import db_utils
import os

app = Flask(__name__)


@app.route('/')
@app.route('/login.html')
def login():
	return render_template('login.html')


@app.route('/home_page.html')
def home_page():
    return render_template('home_page.html')


@app.route('/take_quiz.html')
def take_quiz():
	return render_template('take_quiz.html')

if __name__ == '__main__':
    db = db_utils.db(database="quizon", user="root", password="root", host="localhost")
    app.run()
