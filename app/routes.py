from flask import render_template, jsonify, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager, bcrypt
from app.models import Word, User, Sketch
from app.forms import login_form, signup_form
import random
import time
import base64
import os

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, user_id)

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
    return render_template('guess.html')

@app.route("/guess/<int:id>", methods=["POST"])
@login_required
def guessForm(id):
    userid  = request.form.get("userguess") # todo: check the user guess
    print(userid)
    return render_template('guess.html')

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
                session['start_time'] = time.time()
                session['word_to_draw'] = word.word  # Store the word in the session
                return jsonify(status="success", word=word.word)
        return jsonify(status="error", message="No words available"), 404
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500
    
@app.route('/submit-draw', methods=["POST"])
@login_required
def submit_draw():
    if 'start_time' not in session or 'word_to_draw' not in session:
        return jsonify(status="error", message="Session not started or corrupted"), 400
    
    elapsed_time = time.time() - session['start_time']
    if elapsed_time > 33: # allowing 3s buffer for bad network delay
        return jsonify(status="error", message="Time expired"), 400
    
    # Decode and save the image
    image_data = request.json.get('image')
    if not image_data:
        return jsonify(status="error", message="No image data provided"), 400
    
    # Strip header from data URL
    header, encoded = image_data.split(',', 1)
    data = base64.b64decode(encoded)
    
    # Define the directory and filename
    directory = "app/static/sketches"
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    filename = f"{current_user.id}_{int(time.time())}.png"
    filepath = os.path.join(directory, filename)
    
    # Save the file
    with open(filepath, "wb") as f:
        f.write(data)
    
    # Get word_id
    word_id = Word.query.filter_by(word=session['word_to_draw']).first().id   

    # Create a database entry
    sketch = Sketch(sketch_path=filepath, user_id=current_user.id, word_id=word_id) # this could be wrong
    db.session.add(sketch)
    db.session.commit()
    
    return jsonify(status="success", message=f"Submitted successfully in {elapsed_time:.2f} seconds", word=session['word_to_draw']) # this could be wrong
