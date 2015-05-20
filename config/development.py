import os

DEBUG = False
TESTING = True
SECRET_KEY = 'top secret'
SQLALHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
    os.path.dirname(__file__), '../data-dev.sqlite3')
