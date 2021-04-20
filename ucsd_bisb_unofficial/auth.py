#===============================================================================
# auth.py
#===============================================================================

"""Authentication blueprint

Attributes
----------
bp : Blueprint
    blueprint object, see the flask tutorial/documentation:

    http://flask.pocoo.org/docs/1.0/tutorial/views/

    http://flask.pocoo.org/docs/1.0/blueprints/
"""




# Imports ======================================================================

from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    current_app
)
from flask_login import current_user, login_user, logout_user
from flask_principal import AnonymousIdentity, Identity, identity_changed
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse

from ucsd_bisb_unofficial.forms import (
    LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
)
from ucsd_bisb_unofficial.models import get_db, User, Role
from ucsd_bisb_unofficial.email import send_confirmation_email
from ucsd_bisb_unofficial.rotation_database import RotationDatabase




# Blueprint assignment =========================================================

bp = Blueprint('auth', __name__, url_prefix='/auth')




# Functions ====================================================================

@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user
    
    If the current user is already logged in, they will be redirected to the
    index page.

    Otherwise, the registration page will be rendered. It includes a
    RegistrationForm (see `forms.py`).
    
    If the supplied email is on the approved email list (and does not already
    have an account, see models.User), a new user will be created from the form
    data and added to the database. There it will await confirmation (see
    `confirm_email`)
    """

    if current_user.is_authenticated:
        return redirect(url_for('jumbotron.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.email.data not in current_app.config['APPROVED_EMAILS']:
            flash(
                'Sorry, that email is not on the approved list. If you are a '
                f'BISB student, contact {current_app.config["ADMINS"][0]} '
                'to get your email approved for registration.'
            )
            return redirect(url_for('auth.login'))
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db = get_db()
        db.create_all()
        db.session.add(user)
        user.add_role(Role.query.filter_by(name='named_user').first())
        db.session.commit()
        send_confirmation_email(user)
        flash(
            'Thanks for registering!  Please check your email to '
            'confirm your email address.'
        )
        return redirect(url_for('auth.login'))
    return render_template(
        'auth/register.html',
        title='Register',
        form=form
    )


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in to the site

    If the current user is already logged in, they will be redirected to the
    index page.

    Otherwise, the login page will be rendered. It includes a LoginForm (see
    `forms.py`). Supplying valid credentials will allow the user to log in.
    """

    if current_user.is_authenticated:
        return redirect(url_for('jumbotron.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or any(
            (
                not user.check_password(form.password.data),
                not user.email_confirmed
            )
        ):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id)
        )
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('jumbotron.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Log In', form=form)


@bp.route('/demo')
def demo():
    """Demo of site functionality"""

    quarter = request.args.get('quarter', 'fall-2019', type=str)
    if quarter == 'fall-2019':
        rotation_db = RotationDatabase(current_app.config['ROTATION_DATABASE_2019_CSV'])
    elif quarter == 'fall-2020':
        rotation_db = RotationDatabase(current_app.config['ROTATION_DATABASE_2020_CSV'])
    else:
        rotation_db = RotationDatabase(current_app.config['ROTATION_DATABASE_CSV'])
    for column_name, json_file_path in current_app.config[
        'ROTATION_DATABASE_2019_JSON' if quarter == 'fall-2019' else
        'ROTATION_DATABASE_2020_JSON' if quarter == 'fall-2020' else
        'ROTATION_DATABASE_JSON'
    ].items():
        rotation_db.add_json(
            column_name,
            json_file_path
        )

    def markdown_link(col, text):
        return '[{}]({})'.format(
            text,
            url_for('protected.protected', filename=rotation_db.dict[name][col])
        )

    for name in rotation_db.dict.keys():
        for col in (2, 3) if (quarter in ('fall-2019', 'fall-2020')) else (10, 11, 12, 13, 14, 15):
            if rotation_db.dict[name][col]:
                rotation_db.dict[name][col] = markdown_link(
                    col, 'Proposal' if col % 2 == 0 else 'Report'
                )
    quarter_to_columns = {
        'fall-2018': (1, 2, 10, 11, 16), 'winter-2019': (3, 4, 12, 13, 16),
        'spring-2019': (5, 6, 14, 15, 16), 'fall-2019': (0, 1, 2, 3, 4),
        'fall-2020': (0, 1, 2, 3, 4)
    }
    return render_template(
        'auth/demo.html',
        table=rotation_db.markdown_table(*quarter_to_columns[quarter]),
        quarter=quarter
    )


@bp.route('/logout')
def logout():
    """Log out the current user"""

    logout_user()
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity()
    )
    return redirect(url_for('auth.login'))


@bp.route('/confirm/<token>')
def confirm_email(token):
    """Email confirmation page

    If the current user is already logged in, they will be redirected to the
    index page.

    This function renders the page liked to by the registration confirmation
    email. It includes a message about the success or failure of the
    confirmation.

    Parameters
    ----------
    token
        The JSON web token
    """

    if current_user.is_authenticated:
        return redirect(url_for('jumbotron.index'))
    user = User.verify_confirm_email_token(token)
    if not user:
        flash('Strange, no account found.', 'error')
    if user.email_confirmed:
        flash('Account already confirmed. Please login.', 'info')
    else:
        user.email_confirmed = True
        user.email_confirmed_on = datetime.utcnow()
        db = get_db()
        db.session.add(user)
        db.session.commit()
        flash('Thank you for confirming your email address!')
    return redirect(url_for('auth.login'))


# @bp.route('/reset_password_request', methods=('GET', 'POST'))
# def reset_password_request():
#     """Request a password reset

#     If the current user is already logged in, they will be redirected to the
#     index page.

#     Otherwise, the reset password page will be rendered. It includes a
#     ResetPasswordRequestForm (see `forms.py`). Submitting a valid
#     username-email pair will cause a password reset email to be sent.
#     """

#     if current_user.is_authenticated:
#         return redirect(url_for('jumbotron.index'))
#     form = ResetPasswordRequestForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user and user.email == form.email.data:
#             send_password_reset_email(user)
#             flash(
#                 'Check your email for the instructions to reset your password'
#             )
#             return redirect(url_for('auth.login'))
#         else:
#             flash('Invalid username/email pair')
#             return redirect(url_for('auth.reset_password_request'))
#     return render_template(
#         'auth/reset_password_request.html',
#         title='Reset Password',
#         form=form
#     )


# @bp.route('/reset_password/<token>', methods=('GET', 'POST'))
# def reset_password(token):
#     """Reset a user's password
    
#     If the current user is already logged in, they will be redirected to the
#     index page.

#     This function renders the page linked to by the password reset email. The
#     link includes a JSON web token as a variable component of the URL. If the
#     token cannot be verified, the user is redirected to the login page.

#     If the token is verified, the user's password will be reset according to
#     the data entered into the included ResetPasswordForm (see `forms.py`).

#     Parameters
#     ----------
#     token
#         the JSON web token
#     """

#     if current_user.is_authenticated:
#         return redirect(url_for('jumbotron.index'))
#     user = User.verify_reset_password_token(token)
#     if not user:
#         return redirect(url_for('auth.login'))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         user.set_password(form.password.data)
#         db = get_db()
#         db.session.commit()
#         flash('Your password has been reset.')    
#         return redirect(url_for('auth.login'))
#     return render_template('auth/reset_password.html', form=form)
