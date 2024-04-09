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
    sketches = [
        {
            'id': 1,
            'username': 'someranomduser',
            'date': '4m ago', # obviously this is a placeholder for better date parsing
            'has_guessed': False,
        },
        {
            'id': 2,
            'username': 'otheruser',
            'date': '7h ago', # obviously this is a placeholder for better date parsing
            'has_guessed': False,
        },
        {
            'id': 3,
            'username': 'anotheruser',
            'date': 'Apr 4', # obviously this is a placeholder for better date parsing
            'has_guessed': True,
        },
        {
            'id': 4,
            'username': 'yetanotheruser',
            'date': 'Dec 12, 2023', # obviously this is a placeholder for better date parsing
            'has_guessed': True,
        }
    ]

    return render_template('index.html', **get_user(), sketches=sketches)

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