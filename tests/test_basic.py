import os
import unittest
from app import app, db, bcrypt
from app.models import User, Sketch, Word, GuessSession
from datetime import datetime
from config import TestConfig
import base64

class BasicTests(unittest.TestCase):
    def setUp(self):
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        user1 = User(
            username="user1",
            email="user1@example.com",
            first_name="user",
            last_name="one",
            pwd=bcrypt.generate_password_hash("Pass1234!"),
        )

        user2 = User(
            username="user2",
            email="user2@example.com",
            first_name="user",
            last_name="two",
            pwd=bcrypt.generate_password_hash("Pass123!"),
        )

        word1 = Word(word="apple")
        word2 = Word(word="banana")

        db.session.add_all([user1, user2, word1, word2])
        db.session.commit()

        sketch1 = Sketch(sketch_path="app/static/sketches/6_1715689534.png", user_id=1, word_id=1)
        sketch2 = Sketch(sketch_path="app/static/sketches/4_1714644600.png", user_id=2, word_id=2)

        db.session.add_all([sketch1, sketch2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_details(self):
        user = User.query.get(1)
        self.assertEqual(user.username, "user1")
        self.assertEqual(user.email, "user1@example.com")
        self.assertEqual(user.first_name, "user")
        self.assertEqual(user.last_name, "one"),
        self.assertTrue(bcrypt.check_password_hash(user.pwd, "Pass1234!"))
        self.assertFalse(bcrypt.check_password_hash(user.pwd, "Pass123!"))

    def test_user_registration(self):
        response = self.app.post('/signup', data=dict(
            username='newuser',
            email='newuser@example.com',
            first_name='New',
            last_name='User',
            pwd='Password123!',
            cpwd='Password123!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        new_user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(new_user)

    def test_user_login(self):
        response = self.app.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logout', response.data)

    def test_user_logout(self):
        self.app.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        response = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)

    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_page(self):
        self.app.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        response = self.app.get('/leaderboard')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Leaderboard', response.data)

    def test_guess_page(self):
        self.app.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        self.app.get('/set-sketch-id/1')
        response = self.app.get('/guess') 
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Guess', response.data)

    def test_begin_guess(self):
        self.app.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        self.app.get('/set-sketch-id/1')
        response = self.app.get('/begin-guess')
        self.assertEqual(response.status_code, 200) 
        self.assertIn(b'image_data', response.data)

    def test_submit_guess(self):
        self.app.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        self.app.get('/set-sketch-id/1')
        self.app.get('/begin-guess')
        response = self.app.post('/submit-guess', data=dict(
            userguess='apple'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Guess received', response.data)

    def test_draw_page(self):
        self.app.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        response = self.app.get('/draw')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Draw', response.data)

    def test_begin_draw(self):
        self.app.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        response = self.app.get('/begin-draw')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'success', response.data)

    def test_submit_draw(self):
        self.app.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        self.app.get('/begin-draw')
        image_data = 'data:image/png;base64,' + base64.b64encode(b'test_image_data').decode('utf-8')
        response = self.app.post('/submit-draw', json=dict(image=image_data))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Submitted successfully', response.data)

if __name__ == "__main__":
    unittest.main()
