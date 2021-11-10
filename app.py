# Flask quick set-up based off official flask documentation
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
import pymongo
from pymongo import MongoClient
from flask import Flask, request, redirect, flash, session
from flask import render_template, render_template_string
from datetime import date, datetime
from operator import itemgetter
import os
import sys
import bcrypt
import json

app = Flask(__name__)

# Secret Key necessary to use for Flask Sessions, created as environment variable "SECRET_KEY"
#app.secret_key = os.environ.get("SECRET_KEY")

app.secret_key = 'supersecretkey'

# Connect to database, database url stored in environment variable
#db = pymongo.MongoClient(os.environ.get("DATABASE_URL"))
db = pymongo.MongoClient("mongodb+srv://Admin:6ek9T4OusBWEWu1G@musicalchairs.3wxqw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority&ssl=true&ssl_cert_reqs=CERT_NONE")
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
        # Find if account exists
        if not accounts.find_one({'name': username}):
            flash('wrong username or password')
            return render_template('login.html')
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

@app.route('/endofgame.html')
def endofgame():
    return render_template('endofgame.html')

@app.route('/gameselection.html')
def gameSelection():
    return render_template('gameselection.html')

@app.route('/playgame.html')
def gamePage():
    return render_template('playgame.html')

@app.route('/endlessgame.html')
def endlessGame():
    return render_template('endlessgame.html')

"""
TODO: Create leaderboard HTML Page.
This was written in advance and anticipation. Tested by running in main() and checking print statements
"""

@app.route('/leaderboard.html')
def leaderboard():
    if 'username' in session:
        # Set up base values n = names, d = dates, hs = hiscore
        hs, n, d = [], [], []
        for i in range(0, 10):
            hs.append(0)
            n.append('No placement')
            d.append('MM/DD/YY')
        # Collect all scores documents
        allScores = db.accounts.scores
        # Below statement finds all documents then proceeds to sort them by highscore: score
        highestScores = allScores.find().sort('highscore.score', -1)
        # Logic for grabbing top ten scores / or til end of document
        counter, limit = 0, 0
        length = allScores.count()
        if length > 10:
            limit = 10
        else:
            limit = length
        # Add top ten documents to arrays
        while counter < limit:
            n[counter] = highestScores[counter]['name']
            d[counter] = highestScores[counter]['highscore']['date']
            hs[counter] = highestScores[counter]['highscore']['score']
            counter = counter + 1
        # Another monstrous return statement. Returning template AND top ten scores with names and dates
        return render_template('leaderboard.html',
                               n1=n[0], n2=n[1], n3=n[2], n4=n[3], n5=n[4], n6=n[5], n7=n[6], n8=n[7], n9=n[8], n10=n[9],
                               d1=d[0], d2=d[1], d3=d[2], d4=d[3], d5=d[4], d6=d[5], d7=d[6], d8=d[7], d9=d[8], d10=d[9],
                               hs1=hs[0], hs2=hs[1], hs3=hs[2], hs4=hs[3], hs5=hs[4], hs6=hs[5], hs7=hs[6], hs8=hs[7], hs9=hs[8], hs10=hs[9])
    else:
        return render_template('login.html')

@app.route('/profile.html')
def profilePage():
    if 'username' in session:
        # Logic for displaying recent games/high score
        scores = [0, 0, 0, 0, 0]
        games = ["None", "None", "None", "None", "None"]
        hi_score = "Play a game!"
        colScores = db.accounts.scores
        user_exists = colScores.find_one({'name': session['username']})
        if user_exists:
            curScores = colScores.find({'name': session['username']})[0]['scores']
            hi_score = colScores.find({'name': session['username']})[0]['highscore']['score']
            i = 0
            while i < len(curScores) and i < 5:
                games[i] = curScores[i].get('date')
                scores[i] = curScores[i].get('score')
                i = i + 1
        # This may look monstrous, but it is just passing variables to HTML. Unfortunately we pass a lot of variables.
        # This renders the profile.html and passes the past five games with their dates, plus the hi-score
        return render_template('profile.html', game_one=games[0], game_two=games[1], game_three=games[2], game_four=games[3], game_five=games[4],
                               score_one=scores[0], score_two=scores[1], score_three=scores[2], score_four=scores[3],
                               score_five=scores[4], hi_score=hi_score)
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
        if username == '' or password == '':
            flash("Invalid credentials!")
            return render_template('signup.html')
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

# Receiving final score from game via POST
@app.route('/store/<string:score>', methods=['POST'])
def storeScore(score):
    score = json.loads(score)
    print(score)
    colScores = db.accounts.scores
    curDate = datetime.now().strftime("%m/%d/%Y at %H:%M:%S") # Get current time to record game date
    user_exists = colScores.find_one({'name': session['username']})
    if not user_exists:
        newScores = {"name": session['username'],
                     "scores": [{"date": curDate, "score": score}],
                     "highscore": {"date": curDate, "score": score}}
        colScores.insert_one(newScores)
    else:
        curScores = colScores.find({'name': session['username']})[0]['scores']
        newScore = {"date": curDate, "score": score}
        curScores.insert(0, newScore)
        # Update scores list with most recent game
        colScores.update_one({'name': session['username']}, {'$set': {'scores': curScores}})
        # Update high score if necessary
        if score > colScores.find({'name': session['username']})[0]['highscore']['score']:
            colScores.update_one({'name': session['username']}, {'$set': {'highscore': {'date': curDate, 'score': score}}})
    # Return status message to affirm POST received.
    return 'Score received!'

# Referenced from 442 slides on Docker/Heroku deployment and live demo
if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 8000
    app.run(host='0.0.0.0', port=port)
    