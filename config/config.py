__author__ = 'ovidiucs'
import os

DEBUG = True
SECRET_KEY = 'top secret'
SQLALCHEMY_DATABASE_URI = 'sqllite:///' + os.path.join(
    os.path.dirname(__file__), '../data-dev.sqlite3')
