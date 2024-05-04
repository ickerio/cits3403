from flask import render_template, jsonify, request, session
from app import app, db
from app.models import Word, User, GuessSession
from datetime import datetime, timedelta
import random

# Time limit for guessing in seconds
TIME_LIMIT = 30

# Note: Should use get url function in render_template()
# -> Best not to hardcode the file name

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
    session['start_time'] = datetime.now()
    return render_template('guess.html', **get_user())

@app.route("/guess/<int:id>", methods=["POST"])
def guessForm(id):
    user_guess = request.form.get("userguess")
    sketch = Sketch.query.get(id)
    user = get_user()

    feedback_message = ""
    submit_disabled = False

    # Check if the time limit for guessing has expired
    if 'start_time' not in session:
        session['start_time'] = datetime.now()

    elapsed_time = datetime.now() - session['start_time']
    remaining_seconds = TIME_LIMIT - elapsed_time.total_seconds()

    if remaining_seconds <= 0:
        feedback_message = "Time's up! Please try again."
        submit_disabled = True
    else:
        # Check if the user's guess matches the word associated with the sketch
        if user_guess.lower() == sketch.word.word.lower():
            feedback_message = "Correct! Good job!"
            submit_disabled = True
            # Calculate points based on the formula: (seconds remaining / guess attempts) x 100
            guess_attempts = int(request.form.get('guessAttempts'))
            if guess_attempts == 0:
                guess_attempts = 1  # Prevent division by zero
            points = int((remaining_seconds / guess_attempts) * 100)
            user.points += points
            db.session.commit()
        else:
            feedback_message = "Incorrect guess! Keep trying."
            # Record the incorrect submission
            guess_session = GuessSession(user_id=user.id, sketch_id=sketch.id)
            db.session.add(guess_session)
            db.session.commit()

    return jsonify(feedback_message=feedback_message, submit_disabled=submit_disabled)

@app.route('/draw')
def draw():
    return render_template('draw.html', **get_user())
