# Flask quick set-up based off official flask documentation
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
import pymongo
from pymongo import MongoClient
from flask import Flask
from flask import render_template, render_template_string
import sys

app = Flask(__name__)

# Flask delgates this to be current homescreen
@app.route('/')
def index():
    return render_template('index.html')

# Link to selectgame.html
@app.route('/selection')
def gameSelection():
    return render_template('selectgame.html')

@app.route('/game')
def gameScreen():
    return render_template('game.html')

@app.route('/profile')
def profilePage():
    return render_template('profile.html')

# Referenced from 442 slides on Docker/Heroku deployment and live demo
if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 8000

    client = pymongo.MongoClient("mongodb+srv://Admin:MusicGameAdmins50277@musicalchairs.3wxqw.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test
    print(f"Existing Databases")
    print(client.list_database_names())
    
    # Create test DB
    """accounts = client['accounts']
    col_users = accounts['passwords']
    document = {'name': 'Sample Name', 'password': 'Sample PW'}
    col_users.insert_one(document)
    print(f"\nVerify the New Database")
    print(client.list_database_names())
    print(f"\nCollections in the Database")
    print(accounts.list_collection_names())
    print(f"\nDocuments in the accounts Collection")
    user = col_users.find()
    # Print each Document
    for item in user:
        print(item)
"""
    app.run(host='0.0.0.0', port=port)
    