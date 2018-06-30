#===============================================================================
# auth.py
#===============================================================================

"""Authentication blueprint"""




# Imports ======================================================================

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from ucsd_bisb_unofficial.db import get_db




# Blueprint assignment =========================================================

bp = Blueprint('auth', __name__)




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


@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = (
            db
            .execute('SELECT * FROM user WHERE username = ?', (username,))
            .fetchone()
        )
        
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('blog.index'))
        
        flash(error)
    
    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = (
            get_db()
            .execute('SELECT * FROM user WHERE id = ?', (user_id,))
            .fetchone()
        )


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view
