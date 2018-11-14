from flask import Flask, render_template, request, redirect, url_for
import db_utils
import os

app = Flask(__name__)


@app.route('/')
@app.route('/index.html', methods=['GET','POST'])
def home_page():
    if request.method == 'POST':
            data = request.form
            #print(data)
            hashedPassword = ph.hash(data["password"])
            db.insert('users',username=data["username"],passwd=hashedPassword,firstname=data["firstname"],lastname=data["lastname"],email=data["emailid"],phone=data["phone"])
    return render_template('index.html')


if __name__ == '__main__':
    db = db_utils.db(database="forsale", user="root", password="root", host="localhost")
    app.run()
