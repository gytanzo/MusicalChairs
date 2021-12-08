# Flask quick set-up based off official flask documentation
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
import pymongo
from pymongo import MongoClient
from flask import Flask, request, redirect, flash, session
from flask import render_template, render_template_string
from flask_pymongo import PyMongo
from datetime import date, datetime
from operator import itemgetter
import os
import sys
import bcrypt
import json
import random

app = Flask(__name__)

# Secret Key necessary to use for Flask Sessions, created as environment variable "SECRET_KEY"
app.secret_key = os.environ.get("SECRET_KEY")
# Setting up MONGO object to set up file share
app.config['MONGO_URI'] = os.environ.get("DATABASE_URL")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # File upload limit: 16MB

# Connect to database, database url stored in environment variable
db = pymongo.MongoClient(os.environ.get("DATABASE_URL"))
accounts = db.accounts.passwords    # contact passwords collection in db
genre_preferences = db.accounts.genre_preferences # user genre preferences to be updated when a new user creates an account
account_avatars = db.accounts.avatars
mongo = PyMongo(app)

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
        if bcrypt.checkpw(password, hashed):
            session['username'] = username
            return redirect('index.html')
        else:
            flash('wrong username or password.')
            return render_template('login.html')
    return render_template('login.html')

@app.route('/search.html', methods=["GET", "POST"])
def search():
    if request.method == "POST":
        user = request.form.get("name")
        if not accounts.find_one({'name': user}):
            flash('User not found! Try another user')
            return render_template('search.html')
        else:
            userStr = '/profile/' + user
            print(userStr)
            return redirect(userStr)
    return render_template('search.html')

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
    preferences = genre_preferences.find({'name': session['username']})[0]["preferences"]
    return render_template('playgame.html', preferences=preferences)

@app.route('/endlessgame.html')
def endlessGame():
    preferences = genre_preferences.find({'name': session['username']})[0]["preferences"]
    return render_template('endlessgame.html', preferences=preferences)

@app.route('/endlessendofgame.html')
def endlessendofgame():
    return render_template('endlessendofgame.html')

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
        length = allScores.count_documents({})
        if length > 10:
            limit = 10
        else:
            limit = length
        # Add top ten documents to arrays
        for x in highestScores:
            n[counter] = x['name']
            d[counter] = x['highscore']['date']
            hs[counter] = x['highscore']['score']
            counter = counter + 1
            if counter == limit:
                break
        # Another monstrous return statement. Returning template AND top ten scores with names and dates
        return render_template('leaderboard.html',
                               u1=n[0], u2=n[1], u3=n[2], u4=n[3], u5=n[4], u6=n[5], u7=n[6], u8=n[7], u9=n[8], u10=n[9],
                               d1=d[0], d2=d[1], d3=d[2], d4=d[3], d5=d[4], d6=d[5], d7=d[6], d8=d[7], d9=d[8], d10=d[9],
                               hs1=hs[0], hs2=hs[1], hs3=hs[2], hs4=hs[3], hs5=hs[4], hs6=hs[5], hs7=hs[6], hs8=hs[7], hs9=hs[8], hs10=hs[9])
    else:
        return render_template('login.html')

@app.route('/endlessleaderboard.html')
def endlessleaderboard():
    if 'username' in session:
        # Set up base values n = names, d = dates, hs = hiscore
        hs, n, d = [], [], []
        for i in range(0, 10):
            hs.append(0)
            n.append('No placement')
            d.append('MM/DD/YY')
        # Collect all scores documents
        allScores = db.accounts.endlessScores
        # Below statement finds all documents then proceeds to sort them by highscore: score
        highestScores = allScores.find().sort('highscore.score', -1)
        # Logic for grabbing top ten scores / or til end of document
        counter, limit = 0, 0
        length = allScores.count_documents({})
        if length > 10:
            limit = 10
        else:
            limit = length
        # Add top ten documents to arrays
        for x in highestScores:
            n[counter] = x['name']
            d[counter] = x['highscore']['date']
            hs[counter] = x['highscore']['score']
            counter = counter + 1
            if counter == limit:
                break

        # Another monstrous return statement. Returning template AND top ten scores with names and dates
        return render_template('endlessleaderboard.html',
                               u1=n[0], u2=n[1], u3=n[2], u4=n[3], u5=n[4], u6=n[5], u7=n[6], u8=n[7], u9=n[8], u10=n[9],
                               d1=d[0], d2=d[1], d3=d[2], d4=d[3], d5=d[4], d6=d[5], d7=d[6], d8=d[7], d9=d[8], d10=d[9],
                               hs1=hs[0], hs2=hs[1], hs3=hs[2], hs4=hs[3], hs5=hs[4], hs6=hs[5], hs7=hs[6], hs8=hs[7], hs9=hs[8], hs10=hs[9])
    else:
        return render_template('login.html')

@app.route('/profile.html')
def profilePage():
    if 'username' in session:
        # Get URL for avatar stored in mongo
        avi_loc = account_avatars.find_one({'name': session['username']})
        avi = avi_loc['avatar_name']
        print(avi)
        # Logic for displaying recent games/high score
        scores = [0, 0, 0, 0, 0]
        games = ["None", "None", "None", "None", "None"]
        hi_score = "Play a game!"
        colScores = db.accounts.scores
        user_exists = colScores.find_one({'name': session['username']})
        if user_exists:
            preferences = genre_preferences.find({'name': session['username']})[0]["preferences"]
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
                               score_five=scores[4], hi_score=hi_score, preferences=preferences, avatar=avi)
    return redirect('/')

@app.route('/index.html')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect('/')

# Logic for viewing another person's profile page
@app.route('/profile/<string:username>', methods=["GET", "POST"])
def otherProfile(username):
    # Get the URL stored in mongo for their avatar
    avi_loc = account_avatars.find_one({'name': username})
    avi = avi_loc['avatar_name']
    # If it is someone's own profile, redirect them to their profile
    if 'username' in session:
        if session['username'] == username:
            return redirect('/profile.html')
    # Logic for attempting to view a non-existing profile
    exists = accounts.find_one({'name': username})
    if not exists:
        return render_template('nonuser.html')
    # Logic for existing user, show their profile
    else:
        # Fetch account information (reused from profile page)
        scores = [0, 0, 0, 0, 0]
        games = ["None", "None", "None", "None", "None"]
        colScores = db.accounts.scores
        curScores = colScores.find({'name': username})[0]['scores']
        hi_score = colScores.find({'name': username})[0]['highscore']['score']
        i = 0
        while i < len(curScores) and i < 5:
            games[i] = curScores[i].get('date')
            scores[i] = curScores[i].get('score')
            i = i + 1
        return render_template('otherprofile.html', username=username, g1=games[0], g2=games[1], g3=games[2],
                               g4=games[3], g5=games[4], s1=scores[0], s2=scores[1], s3=scores[2], s4=scores[3],
                               s5=scores[4], hiscore=hi_score, avatar=avi)

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
            preferences = [True, True, True, True, True]
            genre_preferences.insert_one({'name': username, 'preferences': preferences})
            # Upon creation of a new account, create an entry for an avatar for them.
            account_avatars.insert({'name': username, 'avatar_name': "default.jpg"})
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
@app.route('/store/<string:score>', methods=['POST', 'GET'])
def storeScore(score):
    score = json.loads(score)
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

@app.route('/endlessStore/<string:score>', methods=['POST', 'GET'])
def storeEndlessScore(score):
    score = json.loads(score)
    print(score)
    colScores = db.accounts.endlessScores
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
    
# Posting user genre preferences
@app.route('/prefpush/<string:preferences>', methods=['POST', 'GET'])
def postPreferences(preferences):
    # Accepts string in format "True,True,True,True,True"
    new_preferences = json.loads(preferences)
    genre_preferences.update_one({'name': session['username']}, {'$set': {'preferences': new_preferences}})
    return 'Preferences updated!'

# This is all referenced from https://www.youtube.com/watch?v=DsgAuceHha4
@app.route('/aviupload', methods=['POST'])
def aviupload():
    if 'username' in session:
        if 'avatar' in request.files:
            avatar = request.files['avatar']
            # Check if the file is valid and only an image
            if not avatar.filename.endswith(('.png', '.jpg', '.jpeg')):
                return 'Not a valid filetype'
            # Renaming the avatar and saving to mongo
            avatar_name = session['username'] + '_' + avatar.filename
            mongo.save_file(avatar_name, avatar)
            # For some reason on Heroku, an md5 hash is NOT generated, causing crashes.
            # For the sake of needing a hotfix, I will generate it and manually add it...
            randHash = str(random.getrandbits(128))
            imgDB = db.myFirstDatabase.fs.files
            avi = imgDB.find({'filename': avatar_name})[0]
            keys = avi.keys()
            if 'md5' in keys:
                imgDB.update_one({'filename': avatar_name}, {'$add': {'md5': randHash}})
            # Replace current avatar with new one
            account_avatars.update_one({'name': session['username']}, {'$set': {'avatar_name': avatar_name}})
        return redirect('/profile.html')
    return redirect('/')

# Testing purposes: Direct link to file to verify it was uploaded
# is also used as a route to DB to show off profile photo in HTML (it is the URL)
@app.route('/file/<filename>')
def showFile(filename):
    return mongo.send_file(filename)

# Referenced from 442 slides on Docker/Heroku deployment and live demo
if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 8000
    app.debug = True
    app.run(host='0.0.0.0', port=port)
    