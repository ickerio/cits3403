import os
import unittest
from io import BytesIO
from app import create_app, db, bcrypt
from app.models import User, Sketch, Word, GuessSession
from datetime import datetime
from config import TestConfig
import base64
from PIL import Image


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        with self.app.app_context():
            db.create_all()
            self.add_test_data()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def add_test_data(self):
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

        word1 = Word(word="apple")
        word2 = Word(word="banana")

        db.session.add_all([user1, user2, word1, word2])
        db.session.commit()

        sketch1 = self.create_mock_sketch(user_id=user1.id, word_id=word1.id)
        sketch2 = self.create_mock_sketch(user_id=user2.id, word_id=word2.id)

        db.session.add_all([sketch1, sketch2])
        db.session.commit()

    def create_mock_sketch(self, user_id, word_id):
        img = Image.new('RGB', (100, 100), color=(73, 109, 137))
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        sketch_path = f"app/static/sketches/{user_id}_{word_id}.png"
        if not os.path.exists(os.path.dirname(sketch_path)):
            os.makedirs(os.path.dirname(sketch_path))
        with open(sketch_path, 'wb') as f:
            f.write(img_byte_arr)
        return Sketch(sketch_path=sketch_path, user_id=user_id, word_id=word_id)


class TestUserDetails(TestSetup):
    def test_user_details(self):
        user = User.query.filter_by(username="user1").first()
        self.assertEqual(user.username, "user1")
        self.assertEqual(user.email, "user1@example.com")
        self.assertEqual(user.first_name, "user")
        self.assertEqual(user.last_name, "one")
        self.assertTrue(bcrypt.check_password_hash(user.pwd, "Pass1234!"))
        self.assertFalse(bcrypt.check_password_hash(user.pwd, "Pass123!"))


class TestUserRegistration(TestSetup):
    def test_user_registration(self):
        response = self.client.post('/signup', data=dict(
            username='newuser',
            email='newuser@example.com',
            first_name='New',
            last_name='User',
            pwd='Password123!',
            cpwd='Password123!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
        new_user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(new_user)


class TestUserLoginLogout(TestSetup):
    def test_user_login(self):
        response = self.client.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logout', response.data)

    def test_user_login_invalid_password(self):
        response = self.client.post('/login', data=dict(
            email='user1@example.com',
            pwd='WrongPassword!'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password!', response.data)

    def test_user_logout(self):
        self.client.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)


class TestPages(TestSetup):
    def test_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_leaderboard_page(self):
        self.client.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        response = self.client.get('/leaderboard')
        self.assertEqual(response.status_code, 200)


class TestGuessing(TestSetup):
    def test_guess_page(self):
        self.client.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        self.client.get('/set-sketch-id/1')
        response = self.client.get('/guess')
        self.assertEqual(response.status_code, 200)

    def test_begin_guess(self):
        self.client.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        self.client.get('/set-sketch-id/1')
        response = self.client.get('/begin-guess')
        self.assertEqual(response.status_code, 200)

    def test_submit_guess(self):
        self.client.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        self.client.get('/set-sketch-id/1')
        self.client.get('/begin-guess')
        response = self.client.post('/submit-guess', data=dict(
            userguess='apple'
        ))
        self.assertEqual(response.status_code, 200)


class TestDrawing(TestSetup):
    def test_draw_page(self):
        self.client.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        response = self.client.get('/draw')
        self.assertEqual(response.status_code, 200)

    def test_begin_draw(self):
        self.client.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        response = self.client.get('/begin-draw')
        self.assertEqual(response.status_code, 200)

    def test_submit_draw(self):
        self.client.post('/login', data=dict(
            email='user1@example.com',
            pwd='Pass1234!'
        ), follow_redirects=True)
        self.client.get('/begin-draw')
        image_data = 'data:image/png;base64,' + base64.b64encode(b'test_image_data').decode('utf-8')
        response = self.client.post('/submit-draw', json=dict(image=image_data))
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
