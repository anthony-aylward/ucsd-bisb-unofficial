#===============================================================================
# auth.py
#===============================================================================

"""Authentication blueprint"""




# Imports ======================================================================

import functools

from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import current_user, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse

from ucsd_bisb_unofficial.forms import (
    LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm
)
from ucsd_bisb_unofficial.models import get_db, User
from ucsd_bisb_unofficial.email import (
    send_password_reset_email, send_confirmation_email
)




# Blueprint assignment =========================================================

bp = Blueprint('auth', __name__, url_prefix='/auth')




# Functions ====================================================================

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for('jumbotron.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db = get_db()
        db.session.add(user)
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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('jumbotron.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@bp.route('/reset_password_request', methods=('GET', 'POST'))
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('jumbotron.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.email == form.email.data:
            send_password_reset_email(user)
            flash(
                'Check your email for the instructions to reset your password'
            )
            return redirect(url_for('auth.login'))
        else:
            flash('Invalid username/email pair')
            return redirect(url_for('auth.reset_password_request'))
    return render_template(
        'auth/reset_password_request.html',
        title='Reset Password',
        form=form
    )


@bp.route('/reset_password/<token>', methods=('GET', 'POST'))
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('jumbotron.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('auth.login'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db = get_db()
        db.session.commit()
        flash('Your password has been reset.')    
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('/confirm/<token>')
def confirm_email(token):
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
