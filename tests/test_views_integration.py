import os
import unittest
from urlparse import urlparse

from werkzeug.security import generate_password_hash

os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"

from blog import app
from blog import models
from blog.database import Base, engine, session
from splinter import Browser

class TestViews(unittest.TestCase):
    def setUp(self):
        """Test setuo"""
        self.client = app.test_client()
        self.browser = Browser("phantomjs")

        Base.metadata.create_all(engine)

        self.user = models.User(name="Alice", email="alice@example.com",
                                password=generate_password_hash("test"))
        session.add(self.user)
        session.commit()

    def simulate_login(self):
        with self.client.session_transaction() as http_session:
            http_session["user_id"] = str(self.user.id)
            http_session["_fresh"] = True

    def test_add_post(self):
        self.simulate_login()

        response = self.client.post("http://127.0.0.1:5000/post/add", data={
            "title": "Test Post",
            "content": "Test content"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlparse(response.location).path, "/")
        posts = session.query(models.Post).all()
        self.assertEqual(len(posts), 1)

        post = posts[0]
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "Test content")
        self.assertEqual(post.author, self.user)

    #def test_delete_post(self):
        #self.simulate_login()

        #self.client.post("http://127.0.0.1:5000/post/0/delete")
        #button = self.browser.find_by_css("button[type=submit]")
        #button.click()
        #posts = session.query(models.Post).all()
        #self.assertEqual(len(posts), 0)

    def tearDown(self):
        """Test teardown"""
        session.close()
        engine.dispose()
        Base.metadata.drop_all(engine)
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()