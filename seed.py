from app import bcrypt
from app import app, db
from app.models import User, Word, Sketch, GuessSession

# Function to read words from file
def read_words_from_file(filepath):
    with open(filepath, 'r') as file:
        words = [line.strip() for line in file]
    return words

with app.app_context():
    # Drop all existing tables
    db.drop_all()
    # Create all tables
    db.create_all()

    # Creating test users
    user1 = User(
        username="user1",
        email="user1@example.com",
        first_name="user",
        last_name="one",
        pwd=bcrypt.generate_password_hash("Pass1234!").decode('utf-8'),
    )
    user2 = User(
        username="user2",
        email="user2@example.com",
        first_name="user",
        last_name="two",
        pwd=bcrypt.generate_password_hash("Pass123!").decode('utf-8'),
    )

    # Read words from the file
    words = read_words_from_file('app/static/words/words.txt')

    # Create Word objects
    word_objects = [Word(word=word) for word in words]

    # Create example blank sketch
    sketch1 = Sketch(sketch_path="app/static/sketches/blank.png", user_id=1, word_id=1)

    # Add users and words to the database session
    db.session.add_all([user1, user2, sketch1] + word_objects)
    db.session.commit()

    print("Database seeded!")
