import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from app import create_app, db

class TestWebApp(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.driver.quit()

    def test_signup_login(self):
        # Signup
        self.driver.get('http://localhost:5000/signup')
        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'password').send_keys('testpassword')
        self.driver.find_element(By.NAME, 'submit').click()

        # Login correct
        self.driver.get('http://localhost:5000/login')
        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'password').send_keys('testpassword' + Keys.RETURN)
        self.assertTrue(self.wait.until(EC.text_to_be_present_in_element((By.ID, 'welcome-message'), 'Welcome, testuser')))

        # Login with wrong password
        self.driver.get('http://localhost:5000/login')
        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'password').send_keys('wrongpassword' + Keys.RETURN)
        self.assertTrue(self.wait.until(EC.text_to_be_present_in_element((By.ID, 'error-message'), 'Invalid password')))

        # Login with non-existent user
        self.driver.get('http://localhost:5000/login')
        self.driver.find_element(By.NAME, 'username').send_keys('nonexistent')
        self.driver.find_element(By.NAME, 'password').send_keys('password' + Keys.RETURN)
        self.assertTrue(self.wait.until(EC.text_to_be_present_in_element((By.ID, 'error-message'), 'User does not exist')))

    def test_drawing_and_word_generator(self):
        # Assuming user is logged in and on the drawing page
        self.driver.get('http://localhost:5000/draw')
        start_time = time.time()
        word = self.driver.find_element(By.ID, 'word-display').text
        self.assertIsNotNone(word)  # Check if a word is displayed

        # Drawing action simulated here
        end_time = time.time()
        self.assertLessEqual(end_time - start_time, 60)  # Check that the drawing time is under 60 seconds

    def test_guessing(self):
        # Assuming user is logged in and on the guessing page
        self.driver.get('http://localhost:5000/guess')
        self.driver.find_element(By.NAME, 'guess').send_keys('correctword' + Keys.RETURN)
        self.assertTrue(self.wait.until(EC.text_to_be_present_in_element((By.ID, 'result-message'), 'Correct Guess')))

        self.driver.find_element(By.NAME, 'guess').send_keys('wrongword' + Keys.RETURN)
       

if __name__ == '__main__':
    unittest.main()
