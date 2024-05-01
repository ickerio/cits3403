from flask import render_template, jsonify, request
from app import app, db
from app.models import Word, User, GuessSession
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
    leaderboard = db.session.execute(db.select(User).order_by(User.points).limit(200)).scalars()
    return render_template('leaderboard.html', **get_user(), leaderboard=leaderboard)

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
    user_guess = request.form.get("userguess")
    sketch = Sketch.query.get(id)
    user = get_user()

    submit_disabled = False  #initialize submit button state

    #check if the user's guess matches the word associated with the sketch
    if user_guess.lower() == sketch.word.word.lower():
        guess_session = GuessSession.query.filter_by(user_id=user.id, sketch_id=sketch.id).first()

        if guess_session: #if this is not first attempt
            feedback_message = "Correct! Good Job"
            submit_disabled = True  # Disable submit button after correct guess
            user.points += 2  # Increment points for correct guess on second attempt
        else:
            guess_session = GuessSession(user_id=user.id, sketch_id=sketch.id)
            db.session.add(guess_session)
            db.session.commit()

            feedback_message = "Fantastic! You got it correct on the first try"
            submit_disabled = True  # Disable submit button after correct guess on first attempt
            user.points += 5  # Increment points for correct guess on first attempt
    else:
        guess_session = GuessSession.query.filter_by(user_id=user.id, sketch_id=sketch.id).first()

        if guess_session:
            feedback_message = "Incorrect! Sorry you have no more guesses"
            submit_disabled = True  # Disable submit button after incorrect guess on second attempt
        else:
            guess_session = GuessSession(user_id=user.id, sketch_id=sketch.id)
            db.session.add(guess_session)
            db.session.commit()

            feedback_message = "Wrong guess! Don't worry you have one more chance left. Choose wisely"

    db.session.commit()  # Save the updated user points

    return render_template('guess.html', **get_user(), feedback_message=feedback_message, sketch_path=sketch.sketch_path, submit_disabled=submit_disabled)

@app.route('/draw')
def draw():
    return render_template('draw.html', **get_user())
