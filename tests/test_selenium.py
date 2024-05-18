import unittest
import threading
import time
import ctypes
import socket
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from app import app, db
from config import TestConfig

def terminate_thread(thread):
    if not thread.is_alive():
        return

    exc = ctypes.py_object(SystemExit)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
    if res == 0:
        raise ValueError("nonexistent thread id")
    elif res > 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

class TestWebApp(unittest.TestCase):

    def setUp(self):
        # Suppress Flask server logs
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)
        
        app.config.from_object(TestConfig)
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

        self.port = find_free_port()
        self.server_thread = threading.Thread(target=app.run, kwargs={'port': self.port, 'use_reloader': False})
        self.server_thread.start()

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)
        self.wait = WebDriverWait(self.driver, 10)

        # Allow some time for the server to start
        time.sleep(1)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        self.driver.quit()
        
        # Stop the Flask server
        terminate_thread(self.server_thread)

    def test_signup(self):
        base_url = f'http://localhost:{self.port}'

        # Navigate to signup page
        self.driver.get(f'{base_url}/signup')
        
        # Wait for the username field to be present
        self.wait.until(EC.presence_of_element_located((By.NAME, 'username')))

        # Fill out the signup form
        self.driver.find_element(By.NAME, 'username').send_keys('testuser')
        self.driver.find_element(By.NAME, 'first_name').send_keys('Test')
        self.driver.find_element(By.NAME, 'last_name').send_keys('User')
        self.driver.find_element(By.NAME, 'email').send_keys('test@example.com')
        self.driver.find_element(By.NAME, 'pwd').send_keys('testpassword')
        self.driver.find_element(By.NAME, 'cpwd').send_keys('testpassword')
        self.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

if __name__ == '__main__':
    unittest.main()
