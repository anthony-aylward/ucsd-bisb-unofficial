#===============================================================================
# models.py
#===============================================================================

"""Databse models

Attributes
----------
db : SQLAlchemy
    The database object (see Flask-SQLAlchemy:
    http://flask-sqlalchemy.pocoo.org/2.3/ )
migrate : Migrate
    The Migrate object (see Flask-Migrate:
    https://flask-migrate.readthedocs.io/en/latest/ )
"""




# Imports ======================================================================

import jwt

from time import time
from datetime import datetime
from flask import g, current_app
from flask_ftscursor import query_index, add_to_index, remove_from_index
from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash




# Database initialization ======================================================

db = SQLAlchemy()
migrate = Migrate()




# Auxiliary tables =============================================================

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

roles_whisper_users = db.Table(
    'roles_whisper_users',
    db.Column('whisper_user_id', db.Integer, db.ForeignKey('whisper_user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)




# Classes ======================================================================

# Mixins -----------------------------------------------------------------------

class SearchableMixin():
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id).desc()), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)




# Models -----------------------------------------------------------------------

class User(UserMixin, db.Model):
    """A user

    Attributes
    ----------
    id : int
    username : str
    email : str
    password_hash : str
    posts
    email_confirmation_sent_on : datetime
    email_confirmed : bool
    email_confirmed_on : datetime
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    email_confirmation_sent_on = db.Column(db.DateTime, nullable=True)
    email_confirmed = db.Column(db.Boolean, default=False, nullable=True)
    email_confirmed_on = db.Column(db.DateTime, nullable=True)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        """String representation of the user
        
        Returns
        -------
        str
            String representation of the user
        """

        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Set the user's password

        Parameters
        ----------
        password : str
            The password to hash
        """

        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check the provided password against the user's database record
        
        Parameters
        ----------
        password : str
            The provided password
        
        Returns
        -------
        bool
            The result of the hash check
        """

        return check_password_hash(self.password_hash, password)
    
    def get_confirm_email_token(self, expires_in=600):
        """Generate an email confirmation token

        Parameters
        ----------
        expires_in : int
            The lifetime of the token in seconds
        
        Returns
        -------
        bytes
            The token
        """

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
        """Verify an email confirmation token

        Parameters
        ----------
        token
            The token to be verified
        
        Returns
        -------
        User or None
            The user corresponding to the token if it is successfully verified,
            otherwise None.
        """
        
        try:
            id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['confirm_email']
        except:
            return
        return User.query.get(id)
    
    def get_whisper_token(self, expires_in=600):
        """Generate a whisper token

        Parameters
        ----------
        expires_in : int
            The lifetime of the token in seconds
        
        Returns
        -------
        bytes
            The token
        """

        return (
            jwt.encode(
                {'whisper': self.id, 'exp': time() + expires_in},
                current_app.config['SECRET_KEY'],
                algorithm='HS256'
            )
            .decode('utf-8')
        )
    
    @staticmethod
    def verify_whisper_token(token):
        """Verify a whisper token

        Parameters
        ----------
        token
            The token to be verified
        
        Returns
        -------
            True if the token is successfully verified, otherwise False.
        """
        
        try:
            id = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )['whisper']
        except:
            return
        return int(id)
    
    def add_role(self, role):
        if not self.has_role(role):
            self.roles.append(role)
    
    def remove_role(self, role):
        if self.has_role(role):
            self.roles.remove(role)
    
    def has_role(self, role):
            return self.roles.filter(
                roles_users.c.role_id == role.id
            ).count() > 0
    
    # def get_reset_password_token(self, expires_in=600):
    #     """Generate a password reset token

    #     Parameters
    #     ----------
    #     expires_in : int
    #         The lifetime of the token in seconds
        
    #     Returns
    #     -------
    #     bytes
    #         The token
    #     """

    #     return (
    #         jwt.encode(
    #             {'reset_password': self.id, 'exp': time() + expires_in},
    #             current_app.config['SECRET_KEY'],
    #             algorithm='HS256'
    #         )
    #         .decode('utf-8')
    #     )
    
    # @staticmethod
    # def verify_reset_password_token(token):
    #     """Verify a password reset token

    #     Parameters
    #     ----------
    #     token
    #         The token to be verified
        
    #     Returns
    #     -------
    #     User or None
    #         The user corresponding to the token if it is successfully verified,
    #         otherwise None.
    #     """

    #     try:
    #         id = jwt.decode(
    #             token,
    #             current_app.config['SECRET_KEY'],
    #             algorithms=['HS256']
    #         )['reset_password']
    #     except:
    #         return
    #     return User.query.get(id)


class Post(SearchableMixin, db.Model):
    """A post

    Attributes
    ----------
    id : int
    title : str
    body : str
    timestamp : datetime
    user_id : int
    tag : str
    """

    __searchable__ = ('body', 'title')

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.String(80000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tag = db.Column(db.String(128))
    document_filename = db.Column(db.String, default=None)
    document_url = db.Column(db.String, default=None)
    image_filename = db.Column(db.String, default=None)
    image_url = db.Column(db.String, default=None)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def __repr__(self):
        """String representation of the post
        
        Returns
        -------
        str
            String representation of the post
        """
        
        return f'<Post {self.body}>'


class Comment(db.Model):
    """A comment

    Attributes
    ----------
    id : int
    body : str
    timestamp : datetime
    post_id : int
    user_id : int
    """

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(80000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        """String representation of the comment
        
        Returns
        -------
        str
            String representation of the comment
        """
        
        return f'<Comment {self.body}>'


class Role(db.Model):
    """A role

    Attributes
    ----------
    id : int
    name : str
    description : str
    """

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __repr__(self):
        """String representation of the role
        
        Returns
        -------
        str
            String representation of the role
        """

        return f'<Role {self.name}>'


class WhisperUser(UserMixin, db.Model):
    """A user

    Attributes
    ----------
    id : int
    username : str
    password_hash : str
    whisper_posts
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    whisper_posts = db.relationship('WhisperPost', backref='author', lazy='dynamic')
    roles = db.relationship(
        'Role',
        secondary=roles_whisper_users,
        backref=db.backref('whisper_users', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        """String representation of the user
        
        Returns
        -------
        str
            String representation of the user
        """

        return f'<WhisperUser {self.username}>'
    
    def set_password(self, password):
        """Set the user's password

        Parameters
        ----------
        password : str
            The password to hash
        """

        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check the provided password against the user's database record
        
        Parameters
        ----------
        password : str
            The provided password
        
        Returns
        -------
        bool
            The result of the hash check
        """

        return check_password_hash(self.password_hash, password)
    
    def add_role(self, role):
        if not self.has_role(role):
            self.roles.append(role)
    
    def remove_role(self, role):
        if self.has_role(role):
            self.roles.remove(role)
    
    def has_role(self, role):
            return self.roles.filter(
                roles_whisper_users.c.role_id == role.id
            ).count() > 0


class WhisperPost(db.Model):
    """A whisper post

    Attributes
    ----------
    id : int
    title : str
    body : str
    timestamp : datetime
    whisper_user_id : int
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128))
    body = db.Column(db.String(80000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    whisper_user_id = db.Column(db.Integer, db.ForeignKey('whisper_user.id'))

    def __repr__(self):
        """String representation of the post
        
        Returns
        -------
        str
            String representation of the post
        """

        return f'<WhisperPost {self.body}>'


class WhisperComment(db.Model):
    """A whisper comment

    Attributes
    ----------
    id : int
    body : str
    timestamp : datetime
    whisper_post_id : int
    whisper_user_id : int
    """

    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(80000))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    whisper_post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    whisper_user_id = db.Column(db.Integer)

    def __repr__(self):
        """String representation of the comment
        
        Returns
        -------
        str
            String representation of the comment
        """
        
        return f'<WhisperComment {self.body}>'




# Functions ====================================================================

def get_db():
    """Retrieve the database from the application context
    
    Returns
    -------
    SQLAlchemy
        The database object
    """

    if 'db' not in g:
        g.db = db
    return g.db




# Events =======================================================================

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
