import os, unittest
from app import app, db, bcrypt
from app.models import User, Sketch, Word, GuessSession
from datetime import datetime, timedelta
from config import TestConfig

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        user1 = User(
            username = "user1",
            email = "user1@example.com",
            first_name = "user",
            last_name = "one",
            pwd = bcrypt.generate_password_hash("Pass1234!"),
        )

        user2 = User(
            username = "user2",
            email = "user2@example.com",
            first_name = "user",
            last_name = "two",
            pwd = bcrypt.generate_password_hash("Pass123!"),
        )

        #word1 = Word(word="apple")
        #word2 = Word(word="banana")

        #sketch1 = Sketch(sketch_path="path/to/sketch1.png", user=user1, word=word1)
        #sketch2 = Sketch(sketch_path="path/to/sketch2.png", user=user2, word=word2)

        #session1 = GuessSession(user=user1, sketch=sketch1)
        #session2 = GuessSession(user=user2, sketch=sketch2)

        db.session.add_all([user1, user2])#, word1, word2, sketch1, sketch2, session1, session2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_details(self):
        user = User.query.get(1)
        self.assertEqual(user.username, "user1")
        self.assertEqual(user.email, "user1@example.com")
        self.assertTrue(bcrypt.check_password_hash(user.pwd, "Pass1234!"))
        self.assertFalse(bcrypt.check_password_hash(user.pwd, "Pass123!"))

    #def test_sketch_relationship(self):
    #    sketch = Sketch.query.get(1)
    #    self.assertEqual(sketch.user.username, "user1")
    #   self.assertEqual(sketch.word.word, "apple")

    #def test_guess_session(self):
    #    session = GuessSession.query.get(1)
    #    self.assertEqual(session.user.username, "user1")
    #    self.assertEqual(session.sketch.sketch_path, "path/to/sketch1.png")

if __name__ == "__main__":
    unittest.main()
