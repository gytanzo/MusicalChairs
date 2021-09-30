# Flask quick set-up based off official flask documentation
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
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

# Referenced from 442 slides on Docker/Heroku deployment and live demo
if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 8000
    app.run(host='0.0.0.0', port=port)