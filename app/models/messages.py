"""
Database classes for roles table

"""

from app.db import db
# from jinja2 import Markup
# from werkzeug.security import generate_password_hash
# from math import ceil
from datetime import datetime, timedelta
from sqlalchemy.dialects.postgresql import JSON

ROLE_USER = 0
ROLE_ADMIN = 1


class Messages(db.Model):
    """
    Class for handling Users-Messages relationship.

    """
    __tablename__ = 'messages'

    id = db.Column('id', db.Integer, primary_key=True)
    # one user can have many messages.
    sender_username = db.Column(db.Integer, db.ForeignKey('users.username'))
    message = db.Column(JSON)
    backup_1 = db.Column('backup_1', db.String(50))


    def __init__(self, sender_username, message_json):
        self.sender_username = sender_username
        self.message = message_json

    # Flask-Login Methods start
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

