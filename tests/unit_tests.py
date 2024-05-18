import os, unittest
from app import create_app, db
from app.models import User, Sketch, Word, GuessSession
from datetime import datetime, timedelta

class UserTestCase(unittest.TestCase):

    def setUp(self):
        # Setting up an in-memory database for testing
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Creating test data
        user1 = User(username="user1", email="user1@example.com")
        user1.set_password("testpassword1")
        user2 = User(username="user2", email="user2@example.com")
        user2.set_password("testpassword2")

        word1 = Word(word="apple")
        word2 = Word(word="banana")

        sketch1 = Sketch(sketch_path="path/to/sketch1.png", user=user1, word=word1)
        sketch2 = Sketch(sketch_path="path/to/sketch2.png", user=user2, word=word2)

        session1 = GuessSession(user=user1, sketch=sketch1)
        session2 = GuessSession(user=user2, sketch=sketch2)

        db.session.add_all([user1, user2, word1, word2, sketch1, sketch2, session1, session2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_details(self):
        user = User.query.get(1)
        self.assertEqual(user.username, "user1")
        self.assertEqual(user.email, "user1@example.com")
        self.assertTrue(user.check_password("testpassword1"))
        self.assertFalse(user.check_password("testpassword2"))

    def test_sketch_relationship(self):
        sketch = Sketch.query.get(1)
        self.assertEqual(sketch.user.username, "user1")
        self.assertEqual(sketch.word.word, "apple")

    def test_guess_session(self):
        session = GuessSession.query.get(1)
        self.assertEqual(session.user.username, "user1")
        self.assertEqual(session.sketch.sketch_path, "path/to/sketch1.png")

if __name__ == "__main__":
    unittest.main()
