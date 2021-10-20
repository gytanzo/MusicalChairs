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
#os.environ.get("DATABASE_URL")
app.secret_key = 'supersecretkey'

db = pymongo.MongoClient(os.environ.get("DATABASE_URL"))
print(db)
accounts = db.accounts.passwords

# Flask delgates this to be current homescreen
@app.route('/', methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect('index.html')
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
            render_template('login.html')
    return render_template('login.html')
        

    

@app.route('/help.html')
def gameSelection():
    return render_template('help.html')

@app.route('/playgame.html')
def gameGame():
    if 'username' in session:
        return render_template('playgame.html')
    return redirect('/')

@app.route('/game2.html')
def gameSelect():
    return render_template('game2.html')

@app.route('/profile.html')
def gameProfile():
    if 'username' in session:
        return render_template('profile.html')
    return redirect('/')

@app.route('/index.html')
def gameMenu():
    if 'username' in session:
        return render_template('index.html')
    return redirect('/')

 #   
# @app.route('/login')
# def login():
    
#     return render_template('login.html')

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

    # print("dburl:\n")
    # print(pymongo.MongoClient("DATABASE_URL"))
    # print(os.environ.get("DATABASE_URL"))
    # print("all environ vars:\n")
    # print(os.environ)
    # sys.stdout.flush()
    print(db.list_database_names())
    
    app.run(host='0.0.0.0', port=port)
    