#===============================================================================
# models.py
#===============================================================================

"""Databse models"""




# Imports ======================================================================

import jwt

from time import time
from datetime import datetime
from flask import g, current_app
from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash




# Database initialization ======================================================

db = SQLAlchemy()
migrate = Migrate()




# Classes ======================================================================

# Models -----------------------------------------------------------------------

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, default=False, nullable=True)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_reset_password_token(self, expires_in=600):
        return (
            jwt.encode(
                {'reset_password': self.id, 'exp': time() + expires_in},
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            .decode('utf-8')
        )
    
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['reset_password']
        except:
            return
        return User.query.get(id)
    
    def get_confirm_email_token(self, expires_in=600):
        return (
            jwt.encode(
                {'confirm_email': self.id, 'exp': time() + expires_in},
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            .decode('utf-8')
        )
    
    @staticmethod
    def verify_confirm_email_token(token):
        try:
            id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['confirm_email']
        except:
            return
        return User.query.get(id)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Post {self.body}>'




# Functions ====================================================================

def get_db():
    if 'db' not in g:
        g.db = db
    return g.db