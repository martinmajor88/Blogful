import os
import unittest
import multiprocessing
import time
from urlparse import urlparse

from werkzeug.security import generate_password_hash
from splinter import Browser

os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session

class TestViews(unittest.TestCase):
    def setUp(self):
        """ Test setup """

        self.browser = Browser("phantomjs")

        Base.metadata.create_all(engine)

        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

        self.process = multiprocessing.Process(target=app.run)
        self.process.start()
        time.sleep(1)

    def simulate_account_creation(self):
        self.browser.visit("http://127.0.0.1:5000/newaccount")
        self.browser.fill("name", "Alice")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        self.browser.fill("password_2", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")

    def test_login_correct(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")

    def test_logout(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        button = self.browser.find_link_by_href('/logout')
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/login")

    def test_add_post(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "alice@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.browser.visit("http://127.0.0.1:5000/post/add")
        self.browser.fill("title", "Title")
        self.browser.fill("content", "Content")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")

    def test_delete(self):
        self.test_login_correct()
        #self.test_add_post()
        self.browser.visit("http://127.0.0.1:5000/post/0/delete")
        #button = self.browser.find_by_tag("button[type=submit]")
        #button.click()
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/")

    def test_login_incorrect(self):
        self.browser.visit("http://127.0.0.1:5000/login")
        self.browser.fill("email", "bob@example.com")
        self.browser.fill("password", "test")
        button = self.browser.find_by_css("button[type=submit]")
        button.click()
        self.assertEqual(self.browser.url, "http://127.0.0.1:5000/login")

    def tearDown(self):
        """ Test teardown """
        # Remove the tables and their data from the database
        self.process.terminate()
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()