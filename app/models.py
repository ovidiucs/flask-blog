from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, lm




# Define a class that represents our users in the database
# This class inherits from  a base model classes
# Models > Classes > Associated with entities within a database.
# The hardest part was finding the right SQLAlchemy data types and picking a
# length for our String fields in the database. Using our models is also extremely
# simple, thanks to the SQLAlchemy query syntax

class User(UserMixin, db.Model):
    """
    Inherit from a user mixin class.
    Methods > or implement your own methods
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)

    username = db.Column(db.String(16), index=True, unique=True)
    password_hash = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(username, password):
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    def __repr__(self):
        return '<User {0}>'.format(self.username)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))
