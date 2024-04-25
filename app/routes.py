from flask import render_template, jsonify
from app import app, db
from .models import Word
import random
import os

#Note: Should use get url function in render_template()
#      -> Best not to hardcode the file name

def get_user():
    return {
        'username': 'johndoe',
        'first_name': 'John',
        'last_name': 'Doe',
    }

@app.route('/get-word')
def get_word():
    try:
        word_count = Word.query.count()
        if word_count:
            random_id = random.randint(1, word_count)
            word = Word.query.get(random_id)
            if word:
                return jsonify(word=word.word)
        return jsonify(word="No words available"), 404
    except Exception as e:
        return jsonify(error=str(e)), 500

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

@app.route('/leaderboard')
def leaderboard():
    # Get top 200 from DB
    users = [
        {
            'id': 1,
            'username': 'someranomduser',
            'guessed': 5,
            'score': 25,
            'points_per_guess': 5,
        },
        {
            'id': 1,
            'username': 'someotheruser',
            'guessed': 8,
            'points': 24,
            'points_per_guess': 3,
        },
    ]

    return render_template('leaderboard.html', **get_user(), leaderboard=users * 100)

@app.route('/login')
def login():
    return render_template('login.html', **get_user())

@app.route('/signup')
def signup():
    return render_template('signup.html', **get_user())

@app.route('/guess/<int:id>', methods=["GET"])
def guess(id):
    return render_template('guess.html', **get_user())

@app.route("/guess/<int:id>", methods=["POST"])
def guessForm(id):
    userid  = request.form.get("userguess") # todo: check the user guess
    print(userid)
    return render_template('guess.html', **get_user())

@app.route('/draw')
def draw():
    return render_template('draw.html', **get_user())