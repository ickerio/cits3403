from datetime import datetime
from flask import render_template, jsonify, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager, bcrypt
from app.models import Word, User, Sketch, GuessSession
from app.forms import login_form, signup_form, ProfileForm
import random
import time
import base64
import os
from math import floor
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from flask import render_template

@app.route('/profile', methods=["GET", "POST"])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_password = form.password.data
        if bcrypt.check_password_hash(current_user.pwd, current_password):
            # Collect potential updates
            first_name = form.first_name.data
            last_name = form.last_name.data
            new_username = form.username.data
            new_email = form.email.data
            new_password = form.new_password.data

            # Check for username conflict
            if new_username != current_user.username and User.query.filter_by(username=new_username).first():
                flash("Username already taken. Please choose a different username.", "danger")
                return render_template('profile.html', form=form)

            # Check for email conflict
            if new_email != current_user.email and User.query.filter_by(email=new_email).first():
                flash("Email already taken. Please choose a different email.", "danger")
                return render_template('profile.html', form=form)

            # All checks passed, proceed with updates
            current_user.first_name = first_name
            current_user.last_name = last_name
            current_user.username = new_username
            current_user.email = new_email

            if new_password:
                current_user.pwd = bcrypt.generate_password_hash(new_password)

            db.session.commit()

            flash("Your profile has been updated successfully.", "success")
        else:
            flash("Your current password is invalid. Changes not saved.", "danger")
    elif request.method == "POST":
        flash("There was an issue updating your profile. Please check your information and try again.", "danger")

    return render_template('profile.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

@app.route('/')
def index():
    sketches_data = []

    # Fetch all sketches from the database
    sketches = Sketch.query.all()

    for sketch in sketches:
        cannot_guess = False
        guessed_correctly = False
        guessed_at = None

        if current_user.is_authenticated:
            # Determine if the current user has guessed and if they are the author
            guess_session = GuessSession.query.filter_by(
                user_id=current_user.id,
                sketch_id=sketch.id
            ).first()

            cannot_guess = guess_session is not None or sketch.user_id == current_user.id
            guessed_correctly = guess_session.guess_correctly if guess_session else None

            # Check and format the guessed_at date if exists
            if guess_session and guess_session.guess_at:
                date_format = "%b %d, %Y" if guess_session.guess_at.year == datetime.now().year else "%b %d, %Y"
                guessed_at = guess_session.guess_at.strftime(date_format)
            else:
                guessed_at = None

        # Format the date properly
        date_format = "%b %d, %Y" if sketch.created_at.year == datetime.now().year else "%b %d, %Y"
        formatted_date = sketch.created_at.strftime(date_format)

        sketches_data.append({
            'id': sketch.id,
            'username': sketch.author.username,
            'date': formatted_date,
            'cannot_guess': cannot_guess,
            'guessed_correctly': guessed_correctly,
            'guessed_at': guessed_at
        })

    return render_template('index.html', sketches=sketches_data)

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

    return render_template('leaderboard.html', leaderboard=leaderboard, current_user_rank=current_user_rank, floor=floor)

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

@app.route('/set-sketch-id/<int:sketch_id>')
@login_required
def set_sketch_id(sketch_id):
    session['sketch_id'] = sketch_id
    return redirect(url_for('guess'))

@app.route('/guess', methods=["GET"])
@login_required
def guess():
    sketch_id = session.get('sketch_id')
    if sketch_id is None:
        # Redirect the user to index or show an error
        return redirect(url_for('index'))
    return render_template('guess.html')

@app.route("/begin-guess", methods=["GET"])
@login_required
def begin_guess():
    sketch_id = session.get('sketch_id')
    if not sketch_id:
        return jsonify({'error': 'Sketch not set'}), 403
    
    sketch = Sketch.query.get_or_404(sketch_id)
    word_to_guess = sketch.word.word  # Accessing the word associated with the sketch
    session['word_to_guess'] = word_to_guess  # Saving the word in the session

    session['num_guesses'] = 0

    #also a GuessSession should be created here?

    image_path = sketch.sketch_path
    try:
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        session['guess_start_time'] = time.time()
        return jsonify({'image_data': 'data:image/png;base64,' + encoded_string, 'word_to_guess': word_to_guess})
    except IOError:
        return jsonify({'error': 'File not found'}), 404

@app.route("/submit-guess", methods=["POST"])
@login_required
def submit_guess():
    if 'guess_start_time' not in session or 'word_to_guess' not in session:
        return jsonify(status="error", message="Session not started or corrupted"), 400
    
    elapsed_time = time.time() - session['guess_start_time']
    if elapsed_time > 33:  # allowing 3s buffer for bad network delay
        return jsonify(status="error", message="Time expired"), 400
    
    guess = request.form.get('userguess')
    if not guess:
        return jsonify({'correct': False, 'message': 'Guess cannot be empty'}), 400

    guess_correct = guess.lower() == session['word_to_guess'].lower() if session['word_to_guess'] else False
    sketch_id = session.get('sketch_id')

    # Check if there's an existing guess session for this user and sketch
    guess_session = GuessSession.query.filter_by(user_id=current_user.id, sketch_id=sketch_id).first()
    if not guess_session:
        # Create a new GuessSession if none exists
        guess_session = GuessSession(
            user_id=current_user.id,
            sketch_id=sketch_id,
            guess_correctly=guess_correct
        )
    else:
        # Update existing GuessSession
        guess_session.guess_correctly = guess_correct
        guess_session.guess_at = db.func.current_timestamp()

    db.session.add(guess_session)
    db.session.commit()

    session['num_guesses'] = session.get('num_guesses', 0) + 1  # update guesses count
    current_user.guessed += 1
    remaining_seconds = 33 - elapsed_time
    if guess_correct:
        current_user.points += int((remaining_seconds / session['num_guesses']) * 100)
    db.session.commit()

    return jsonify({'correct': guess_correct, 'message': 'Guess received'})

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


