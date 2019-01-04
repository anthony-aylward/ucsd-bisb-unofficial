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

from datetime import datetime
from flask import (
    Blueprint, render_template, request, url_for, flash, redirect, current_app,
    g
)
from flask_login import login_required, login_user, logout_user, current_user
from flask_principal import Identity, identity_changed
from werkzeug.exceptions import abort
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.urls import url_parse

from ucsd_bisb_unofficial.email import send_whisper_email
from ucsd_bisb_unofficial.forms import (
    LoginForm, SendWhisperEmailForm, NewWhisperUserForm, PostForm, CommentForm
)
from ucsd_bisb_unofficial.models import (
    get_db, Role, User, WhisperUser, WhisperPost, WhisperComment
)
from ucsd_bisb_unofficial.principals import whisper_permission, named_permission
from ucsd_bisb_unofficial.uploads import documents, images



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
    page = request.args.get('page', 1, type=int)
    posts = (
        WhisperPost.query
        .order_by(WhisperPost.timestamp.desc())
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    )
    next_url = (
        url_for('whisper.index', page=posts.next_num)
        if posts.has_next
        else None
    )
    prev_url = (
        url_for('whisper.index', page=posts.prev_num)
        if posts.has_prev
        else None
    )
    for post in posts.items:
        post.preview = post.body[:128] + (len(post.body) > 128) * '...'
    return render_template(
        'whisper/index.html',
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


@bp.route('/confidentiality')
@login_required
@named_permission.require(http_exception=403)
def confidentiality():
    """Render the confidentiality agreement"""

    return render_template('whisper/confidentiality.html')


@bp.route('/info')
@login_required
@named_permission.require(http_exception=403)
def info():
    """Render the information page"""

    return render_template('whisper/info.html')


@bp.route('/anonymize', methods=('GET', 'POST'))
@login_required
@named_permission.require(http_exception=403)
def anonymize():
    """Log out of named account and log in to whisper account
    """

    send_whisper_email_form = SendWhisperEmailForm()
    whisper_login_form = LoginForm()
    if whisper_login_form.validate_on_submit():
        whisper_user = (
            WhisperUser
            .query
            .filter_by(username=whisper_login_form.username.data)
            .first()
        )
        if whisper_user is None or not whisper_user.check_password(
            whisper_login_form.password.data
        ):
            flash('Invalid username or password', 'error')
            return redirect(url_for('whisper.anonymize'))
        logout_user()
        whisper_user.id = int(whisper_user.id) + len(User.query.all())
        login_user(whisper_user)
        return redirect(url_for('whisper.index'))
    elif send_whisper_email_form.validate_on_submit():
        send_whisper_email(current_user)
        flash('Please check your email to confirm and continue.')
        return redirect(url_for('whisper.anonymize'))
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
        whisper_user.id = int(whisper_user.id) + len(User.query.all())
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
        document_filename =  (
            datetime.utcnow().strftime('%Y%m%d-%H%M%S-{}').format(
                documents.save(request.files['document'])
            )
            if request.files.get('document') else None
        )
        image_filename = (
            datetime.utcnow().strftime('%Y%m%d-%H%M%S-{}').format(
                images.save(request.files['image'])
            )
            if request.files.get('image') else None
        )
        post = WhisperPost(
            title=form.title.data,
            body=form.body.data,
            author=current_user,
            document_filename=document_filename,
            document_url=(
                documents.url(document_filename)
                if document_filename else None
            ),
            image_filename=image_filename,
            image_url=(
                images.url(image_filename) if image_filename else None
            )
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('whisper.index'))
    return render_template('whisper/create.html', form=form)


@bp.route('/<int:whisper_post_id>/comment/', methods=('GET', 'POST'))
@login_required
@whisper_permission.require(http_exception=403)
def comment(whisper_post_id):
    """Comment on a post
    
    This page includes a CommentForm (see `forms.py`). A new comment will
    be added to the database based on the form data.
    """
    
    post = get_post(whisper_post_id, check_author=False)
    db = get_db()
    form = CommentForm()
    if form.validate_on_submit():
        comment = WhisperComment(
            body=form.body.data,
            whisper_user_id=current_user.id,
            whisper_post_id=whisper_post_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('your comment is now live!')
        return redirect(url_for('whisper.detail', id=post.id))
    return render_template('whisper/comment.html', form=form, post=post)


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


def get_comment(id, check_author=True):
    """Retrieve a comment from the database
    
    Parameters
    ----------
    id : int
        A comment ID.
    check_author : bool
        If True, the ID of the current user will be compared to the ID of the
        comment's author. If the current user is not the author of the comment,
        the retrieval is aborted.
    
    Returns
    -------
    Comment or NoneType
        The comment with the given comment ID.
    """

    comment = WhisperComment.query.filter_by(id=id).first()
    if comment is None:
        abort(404, f"WhisperComment id {id} doesn't exist.")
    if check_author and comment.user_id != current_user.id:
        abort(403)
    return comment


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

@bp.route('/<int:id>/delete-comment', methods=('GET', 'POST',))
@login_required
@whisper_permission.require(http_exception=403)
def delete_comment(id):
    """Delete a comment

    Parameters
    ----------
    id : int
        The ID no. of the comment to be deleted
    """

    comment = get_comment(id)
    db = get_db()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('whisper.detail', id=comment.whisper_post_id))


@bp.route('/<int:id>/detail')
@login_required
@whisper_permission.require(http_exception=403)
def detail(id):
    """Detail view of a post

    Retrieves the post with the provided ID and renders the detail
    template

    Parameters
    ----------
    id : int
        The id of the post to be viewed
    """

    post = get_post(id, check_author=False)
    comments = WhisperComment.query.filter(WhisperComment.whisper_post_id == id).all()[
        ::-1
    ]
    return render_template(
        'whisper/detail.html',
        post=post,
        comments=comments,
        index_route='whisper.index',
        update_route='whisper.update',
        comment_route='whisper.comment'
    )


@bp.route('/search')
@login_required
@whisper_permission.require(http_exception=403)
def search():
    if not g.search_form.validate():
        return redirect(url_for('whisper.index'))
    page = request.args.get('page', 1, type=int)
    posts, total = WhisperPost.search(
        g.search_form.q.data,
        page,
        current_app.config['POSTS_PER_PAGE']
    )
    next_url = (
        url_for('whisper.search', q=g.search_form.q.data, page=page + 1)
        if total > page * current_app.config['POSTS_PER_PAGE']
        else None
    )
    prev_url = (
        url_for('whisper.search', q=g.search_form.q.data, page=page - 1)
        if page > 1
        else None
    )
    posts = tuple(
        {
            'id': post.id,
            'title': post.title,
            'author': post.author,
            'timestamp': post.timestamp,
            'preview': post.body[:128] + (len(post.body) > 128) * '...',
            'detail_route': 'whisper.detail'
        }
        for post in posts
    )
    return render_template(
        'whisper/search.html',
        title='Search Results',
        posts=posts,
        next_url=next_url,
        prev_url=prev_url
    )



# Other ------------------------------------------------------------------------

def random_words(k):
    """Randomly sample words from the Unix word list

    Parameters
    ----------
    k : int
        The sample size / number of words
    
    Returns
    -------
    list
        The sample of words

    """
    with open('/usr/share/dict/words', 'r') as f:
        words = f.read().splitlines()
    return random.sample(words, k)


def random_username():
    """Generate a username by concatenating two random words
    
    Returns
    -------
    str
        The random username
    """
    
    return ''.join(random_words(2))


def random_password(size=16, chars=string.ascii_letters + string.digits):
    """Generate a random password

    Parameters
    ----------
    size : int
        Length of the password
    chars : str
        The character set to use, by default:
        (string.ascii_letters + string.digits)
    
    Returns
    -------
    str
        A password of the provided length generated from the provided character
        set
    """

    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
