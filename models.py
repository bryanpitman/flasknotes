"""Models for Notes application"""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """creates a new user"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True)
    username = db.Column(
        db.String(20),
        nullable=False)
    password = db.Column(
        db.String(100),
        nullable=False)
    email = db.Column(
        db.String(50),
        unique = True,
        nullable=False)
    first_name = db.Column(
        db.String(30),
        nullable=False)
    last_name = db.Column(
        db.String(30),
        nullable=False)

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password).decode('utf8')

        # return instance of user w/username and hashed pwd
        return cls(username=username,
                password=hashed,
                email=email,
                first_name=first_name,
                last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """
        # will return instnace of user or none
        user = cls.query.filter_by(username=username).one_or_none()

        if user and bcrypt.check_password_hash(user.password, password):
            # return user instance
            return user
        else:
            return False