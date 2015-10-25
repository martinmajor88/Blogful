import os
class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost:8080/blogful"
    DEBUG = True
    SECRET_KEY = os.environ.get("BLOGFUL_SECRET_KEY", "")

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:mypass@localhost:5432/blogful-test"
    DEBUG = False
    SECRET_KEY = "Not secret"

class TravisConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://localhost:5432/blogful-test"
    DEBUG = False
    SECRET_KEY = "Not secret"
