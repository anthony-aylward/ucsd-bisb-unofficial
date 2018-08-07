#===============================================================================
# whisper.py
#===============================================================================

"""Whisper blueprint

Attributes
----------
bp : Blueprint
    blueprint object, see the flask tutorial/documentation:

    http://flask.pocoo.org/docs/1.0/tutorial/views/

    http://flask.pocoo.org/docs/1.0/blueprints/
"""




# Imports ======================================================================

import random
import string

from flask import (
    Blueprint, render_template, request, url_for, flash, redirect, current_app
)
from flask_login import login_required, login_user, logout_user, current_user
from flask_principal import Identity, identity_changed
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse

from ucsd_bisb_unofficial.email import send_whisper_email
from ucsd_bisb_unofficial.forms import (
    LoginForm, SendWhisperEmailForm, NewWhisperUserForm, PostForm
)
from ucsd_bisb_unofficial.models import (
    get_db, Role, User, WhisperUser, WhisperPost
)
from ucsd_bisb_unofficial.principals import whisper_permission, named_permission



# Blueprint assignment =========================================================

bp = Blueprint('whisper', __name__, url_prefix='/whisper')




# Functions ====================================================================

# Routes -----------------------------------------------------------------------

@bp.route('/index')
@login_required
@whisper_permission.require(http_exception=403)
def index():
    """Render the whisper index

    This page collects all whisper posts from the database and displays them.
    """

    db = get_db()
    posts = WhisperPost.query.all()
    return render_template('whisper/index.html', posts=posts)


@bp.route('/confidentiality')
@login_required
@named_permission.require(http_exception=403)
def confidentiality():
    """Render the confidentiality agreement"""

    return render_template('whisper/confidentiality.html')


@bp.route('/anonymize', methods=('GET', 'POST'))
@login_required
@named_permission.require(http_exception=403)
def anonymize():
    """Log out of named account and log in to whisper account
    """

    send_whisper_email_form = SendWhisperEmailForm()
    whisper_login_form = LoginForm()
    if send_whisper_email_form.validate_on_submit():
        send_whisper_email(current_user)
        flash('Please check your email to confirm and continue.')
        return redirect(url_for('whisper.anonymize'))
    if whisper_login_form.validate_on_submit():
        whisper_user = (
            WhisperUser
            .query
            .filter_by(username=whisper_login_form.username.data)
            .first()
        )
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('whisper.anonymize'))
        logout_user()
        login_user(whisper_user)
        return redirect(url_for('whisper.index'))
    return render_template(
        'whisper/anonymize.html',
        title='Anonymize',
        send_whisper_email_form=send_whisper_email_form,
        whisper_login_form=whisper_login_form,
        current_whisper_user=False
    )


@bp.route('/new-whisper-user/<token>', methods=('GET', 'POST'))
@login_required
@named_permission.require(http_exception=403)
def new_whisper_user(token):
    if not current_user.id == User.verify_whisper_token(token):
        flash('Token not verified')
        return redirect(url_for('whisper.anonymize'))
    form = NewWhisperUserForm()
    if form.validate_on_submit():
        username = random_username()
        password = random_password()
        whisper_user = WhisperUser(username=username)
        whisper_user.set_password(password)
        db = get_db()
        db.create_all()
        db.session.add(whisper_user)
        whisper_user.add_role(Role.query.filter_by(name='whisper_user').first())
        db.session.commit()
        logout_user()
        login_user(whisper_user)
        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(whisper_user.id)
        )
        flash(
            'Your username and password for this anonymous account are shown '
            'below. RECORD THESE NOW if you want to modify your posts in the '
            'future.'
        )
        flash(f'USERNAME: {username}')
        flash(f'PASSWORD: {password}')
        return redirect(url_for('whisper.index'))
    return render_template(
        'whisper/new-whisper-user.html',
        title='New Whisper User',
        form=form
    )


@bp.route('/create', methods=('GET', 'POST'))
@login_required
@whisper_permission.require(http_exception=403)
def create():
    """Create a new post
    
    This page includes a PostForm (see `forms.py`). A new post will be added to
    the database based on the form data.
    """

    db = get_db()
    form = PostForm()
    if form.validate_on_submit():
        post = WhisperPost(
            title=form.title.data,
            body=form.body.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('whisper.index'))
    return render_template('whisper/create.html', form=form)


def get_post(id, check_author=True):
    """Retrieve a post from the database
    
    Parameters
    ----------
    id : int
        A post ID.
    check_author : bool
        If True, the ID of the current user will be compared to the ID of the
        post's author. If the current user is not the author of the post, the
        retrieval is aborted.
    
    Returns
    -------
    Post or NoneType
        The post with the given post ID.
    """

    post = WhisperPost.query.filter_by(id=id).first()
    
    if post is None:
        abort(404, f"WhisperPost id {id} doesn't exist.")
    
    if check_author and post.whisper_user_id != current_user.id:
        abort(403)
    
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
@whisper_permission.require(http_exception=403)
def update(id):
    """Update a post

    Retrieves the post with the provided ID and provides a PostForm that can
    be used to edit it.

    Parameters
    ----------
    id : int
        The id of the post to be updated
    """

    post = get_post(id)
    form = PostForm()
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None
        
        if not title:
            error = 'Title is required.'
        
        if error is not None:
            flash(error)
        else:
            post.title = title
            post.body = body
            db = get_db()
            db.session.commit()
            return redirect(url_for('whisper.index'))
    
    return render_template('whisper/update.html', form=form, post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
@whisper_permission.require(http_exception=403)
def delete(id):
    """Delete a post

    Parameters
    ----------
    id : int
        The ID no. of the post to be deleted
    """

    post = get_post(id)
    db = get_db()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('whisper.index'))



# Other ------------------------------------------------------------------------

def random_words(k):
    with open('/usr/share/dict/words', 'r') as f:
        words = f.read().splitlines()
    return random.sample(words, k)


def random_username():
    return ''.join(random_words(2))


def random_password(size=16, chars=string.ascii_letters + string.digits):
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
