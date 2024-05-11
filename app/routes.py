from flask import render_template, jsonify, flash, redirect, url_for, session, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager, bcrypt
from app.models import Word, User, Sketch, GuessSession
from app.forms import login_form, signup_form
import random
import time
import base64
import os
from datetime import datetime

#Potential Issues
# did not include the has_guessed boolean in index() sketches[], might be ok?
# the timing of 30s for /guess probs wont work if someone has bad load times
# should use more specific session variable names for /guess timings

#Error
"""
guessed_session = GuessSession.query.filter_by(user_id=current_user.id, sketch_id=sketch.id).first()
AttributeError: 'AnonymousUserMixin' object has no attribute 'id'

"""

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@app.route('/')
def index():
    sketches = []

    # Fetch sketches from the database
    all_sketches = Sketch.query.all()

    for sketch in all_sketches:
        guessed_session = GuessSession.query.filter_by(user_id=current_user.id, sketch_id=sketch.id).first()

        if guessed_session:
            time_taken = guessed_session.end_time - guessed_session.start_time
            time_taken_str = f"{time_taken.seconds} seconds"
            sketches.append({'id': sketch.id, 'username': sketch.author.username, 'date': time_taken_str})
        else:
            sketches.append({'id': sketch.id, 'username': sketch.author.username, 'date': None})

    # Sort sketches so unguessed ones appear first
    sketches.sort(key=lambda x: x['date'] is None, reverse=True)

    return render_template('index.html', sketches=sketches)

@app.route('/leaderboard')
@login_required
def leaderboard():
    # Fetch the leaderboard, ensuring it's in descending order by points
    leaderboard = db.session.execute(
        db.select(User).order_by(User.points.desc()).limit(200)
    ).scalars().all()  # Make sure to convert to list if necessary

    # Calculate the rank of the current user
    current_user_rank = next(
        (index + 1 for index, user in enumerate(leaderboard) if user.id == current_user.id),
        None
    )

    return render_template('leaderboard.html', leaderboard=leaderboard, current_user_rank=current_user_rank)

@app.route('/login', methods=("GET", "POST"))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = login_form()

    if form.validate_on_submit():
        try:
            user = db.session.execute(db.select(User).where(User.email == form.email.data).limit(1)).scalar()
            if bcrypt.check_password_hash(user.pwd, form.pwd.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Invalid usnermae or password!", "danger")
        except Exception as e:
            flash(e, "danger")

    return render_template('auth.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=("GET", "POST"))
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = signup_form()

    if form.validate_on_submit():
        try:
            new_user = User(
                username = form.username.data,
                email = form.email.data,
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                pwd = bcrypt.generate_password_hash(form.pwd.data),
            )
    
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))
        except Exception as e:
            flash(e, "danger")

    return render_template('auth.html', form=form)


# TODO: redo with Flask-Forms, as per above 


@app.route('/guess/<int:id>', methods=["GET"])
@login_required
def guess(id):
    sketch = Sketch.query.get(id)   
    # if the sketch doesn't exist, return 404 error
    if not sketch:
        abort(404)
    # Pass the sketch data to the template
    return render_template('guess.html', sketch=sketch)



TIME_LIMIT = 30

@app.route("/guess/<int:id>", methods=["POST"])
def guessForm(id):
    user_guess = request.form.get("userguess")
    sketch = Sketch.query.get(id)
    user = User.query.get(session.get('user_id'))

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
            points = int((remaining_seconds) * 100)
            user.points += points
            db.session.commit()
        else:
            feedback_message = "Incorrect guess! Keep trying."

    return jsonify(feedback_message=feedback_message, submit_disabled=submit_disabled, points=points)


@app.route('/draw')
@login_required
def draw():
    return render_template('draw.html')

@app.route('/begin-draw', methods=["GET"])
@login_required
def begin_draw():
    try:
        word_count = Word.query.count()
        if word_count:
            random_id = random.randint(1, word_count)
            word = Word.query.get(random_id)
            if word:
                # start drawing session
                session['draw_start_time'] = time.time()
                session['draw_word'] = word.word  # Store the word in the session
                return jsonify(status="success", word=word.word)
        return jsonify(status="error", message="No words available"), 404
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500
    
@app.route('/submit-draw', methods=["POST"])
@login_required
def submit_draw():
    if 'draw_start_time' not in session or 'draw_word' not in session:
        return jsonify(status="error", message="Session not started or corrupted"), 400
    
    elapsed_time = time.time() - session['draw_start_time']
    if elapsed_time > 33: # allowing 3s buffer for bad network delay
        return jsonify(status="error", message="Time expired"), 400
    
    # Decode and save the image
    image_data = request.json.get('image')
    if not image_data:
        return jsonify(status="error", message="No image data provided"), 400
    
    # Strip header from data URL
    header, encoded = image_data.split(',', 1)
    data = base64.b64decode(encoded)
    
    directory = "app/static/sketches"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Check if the canvas is blank
    blankpath = os.path.join(directory, "blank.png")
    with open(blankpath, "rb") as f:
        blankdata = f.read()
        if data == blankdata:
            return jsonify(status="error", message="Blank canvas provided"), 400

    filename = f"{current_user.id}_{int(time.time())}.png"
    filepath = os.path.join(directory, filename)
    
    # Save the file
    with open(filepath, "wb") as f:
        f.write(data)
    
    # Get word_id
    word_id = Word.query.filter_by(word=session['draw_word']).first().id   

    # Create a database entry
    sketch = Sketch(sketch_path=filepath, user_id=current_user.id, word_id=word_id) # this could be wrong
    db.session.add(sketch)
    db.session.commit()
    
    return jsonify(status="success", message=f"Submitted successfully in {elapsed_time:.2f} seconds", word=session['draw_word']) # this could be wrong

