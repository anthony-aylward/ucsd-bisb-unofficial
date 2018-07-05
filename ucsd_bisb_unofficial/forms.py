#===============================================================================
# forms.py
#===============================================================================

"""Forms (subclasses of FlaskForm, see Flask-WTF:
http://flask-wtf.readthedocs.io/en/stable/ )
"""




# Imports  =====================================================================

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, TextAreaField
)
from wtforms.validators import (
    ValidationError, DataRequired, Email, EqualTo, Length
)
from ucsd_bisb_unofficial.models import User




# Classes ======================================================================

# Forms ------------------------------------------------------------------------

class LoginForm(FlaskForm):
    """A form for user login credentials

    Attributes
    ----------
    username : StringField
    password : PasswordField
    remember_me : BooleanField
    submit : SubmitField
    """

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    """A form for user registration info

    Attributes
    ----------
    username : StringField
    email : StringField
    password : PasswordField
    password2 : PasswordField
    submit : SubmitField
    """

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class PostForm(FlaskForm):
    """A form for post data
    
    Attributes
    ----------
    title : StringField
    body : TextAreaField
    """

    title = StringField('Title', validators=[DataRequired()])
    body = TextAreaField(
        'Say something',
        validators=[
            DataRequired(),
            Length(min=1, max=140)
        ]
    )
    submit = SubmitField('Submit')


class ResetPasswordRequestForm(FlaskForm):
    """A form for a password reset request

    Attributes
    ----------
    username : StringField
    email : StringField
    submit : SubmitField
    """

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


class ResetPasswordForm(FlaskForm):
    """A form for providing a new password

    Attributes
    ----------
    password : PasswordField
    password2 : PasswordField
    """

    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password',
        validators=[DataRequired(), EqualTo('password')]
    )
    submit = SubmitField('Request Password Reset')