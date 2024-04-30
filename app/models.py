from app import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    guessed = db.Column(db.Integer, default=0)
    points = db.Column(db.Integer, default=0)

    sketches = db.relationship('Sketch', backref='author', lazy='dynamic')

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String, nullable=False)

    sketches = db.relationship('Sketch', backref='word', lazy='dynamic')

class Sketch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sketch_path = db.Column(db.Text, nullable=False)  # Path to the file storing the sketch
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class GuessSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sketch_id = db.Column(db.Integer, db.ForeignKey('sketch.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)  # Initially null, set when the user makes a correct guess

    # Relation to User
    user = db.relationship('User', backref=db.backref('guess_sessions', lazy='dynamic'))
    # Relation to Sketch
    sketch = db.relationship('Sketch', backref=db.backref('guess_sessions', lazy='dynamic'))
