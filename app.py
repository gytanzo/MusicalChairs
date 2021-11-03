# Flask quick set-up based off official flask documentation
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
import pymongo
from pymongo import MongoClient
from flask import Flask, request, redirect, flash, session
from flask import render_template, render_template_string
import os
import sys
import bcrypt

app = Flask(__name__)

# Secret Key necessary to use for Flask Sessions, created as environment variable "SECRET_KEY"
app.secret_key = os.environ.get("SECRET_KEY")

# Connect to database, database url stored in environment variable
db = pymongo.MongoClient(os.environ.get("DATABASE_URL"))
accounts = db.accounts.passwords    # contact passwords collection in db

# Flask delegates this to be current home-screen
# Current homepage: Login Page
@app.route('/', methods=["GET", "POST"])
def login():
    # Below conditional determines if a user is currently logged onto the site/has an active session
    # Sessions is part of Flask documentation, references: https://pythonbasics.org/flask-sessions/
    if 'username' in session:
        return redirect('index.html')
    ##############################################################################################
    if request.method == "POST":
        username = request.form.get("Uname")
        password = request.form.get("Pass").encode('utf-8')
        hashed = accounts.find( {'name': username})[0]['password']
        print("printing hashed password")
        print(hashed)
        if bcrypt.checkpw(password, hashed):
            session['username'] = username
            return redirect('index.html')
        else:
            flash('wrong username or password.')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/help.html')
def helpPage():
    return render_template('help.html')

@app.route('/gameselection.html')
def gameSelection():
    return render_template('gameselection.html')

@app.route('/playgame.html')
def gamePage():
    return render_template('playgame.html')

@app.route('/endlessgame.html')
def endlessGame():
    return render_template('endlessgame.html')

@app.route('/profile.html')
def profilePage():
    if 'username' in session:
        return render_template('profile.html')
    return redirect('/')

@app.route('/index.html')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect('/')

@app.route('/signup.html', methods=["GET", "POST"])
def signup():
    if 'username' in session:
        return redirect('index.html')
    if request.method == "POST":
        username = request.form.get("Uname")
        password = request.form.get("Pass")
        #store to databse if Uname not existing
        
        exists = accounts.find_one({'name': username})
        if not exists:
            # Use BCrypt to encrypt password, then insert into DB
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
            accounts.insert({'name': username, 'password': hashed})
            session['username'] = username
            return redirect('/')
        else:
            flash("Username already exists")
    return render_template('signup.html')

@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        return redirect('/')
    return redirect('index.html')


# Referenced from 442 slides on Docker/Heroku deployment and live demo
if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 8000
    app.run(host='0.0.0.0', port=port)
    