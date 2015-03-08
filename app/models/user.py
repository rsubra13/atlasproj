"""
Database class for the UserManagement

"""

from app.db import db
from werkzeug.security import generate_password_hash
from datetime import datetime

ROLE_USER = 0
ROLE_ADMIN = 1


class User(db.Model):
    """
    Class for handling user data.

    """
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(50), unique=True, index=True)
    password = db.Column('password', db.String(80))
    email = db.Column('email', db.String(50), unique=True, index=True)
    institution = db.Column('institution', db.String(60))
    backup_1 = db.Column('backup_1', db.String(50))

    def __init__(self, username, password, email, institution):
        self.username = username
        self.set_password(password)
        self.email = email
        self.registered_on = datetime.utcnow()
        self.institution = institution

    # Flask-Login Methods start
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    # Flask Login methods end
    def __repr__(self):
        return '<User %r>' % (self.name)

    def as_dict(self):
        '''
        Return an individual User as a dictionary.
        '''
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'registered_on': self.registered_on,
            'institution': self.institution,
        }

    def set_password(self, password):
        self.password = generate_password_hash(password)
