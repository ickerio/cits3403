from flask import (
    Flask, render_template,
)

app = Flask(__name__)

def get_user():
    return {
        'username': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
    }


@app.route('/')
def index():
    return render_template('index.html', **get_user())

@app.route('/login')
def login():
    return render_template('login.html', **get_user())

@app.route('/find-sketch')
def findSketch():
    return render_template('find-sketch.html', **get_user())

@app.route('/guess-sketch')
def guessSketch():
    return render_template('guess-sketch.html', **get_user())

@app.route('/draw-sketch')
def drawSketch():
    return render_template('draw-sketch.html', **get_user())