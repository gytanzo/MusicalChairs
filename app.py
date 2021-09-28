# Flask quick set-up based off official flask documentation
# https://flask.palletsprojects.com/en/2.0.x/quickstart/
from flask import Flask
from flask import render_template, render_template_string
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else 8000
    app.run(host='0.0.0.0', port=port)