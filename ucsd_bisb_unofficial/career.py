#===============================================================================
# career.py
#===============================================================================

"""Career blueprint

Attributes
----------
bp : Blueprint
    blueprint object, see the flask tutorial/documentation:

    http://flask.pocoo.org/docs/1.0/tutorial/views/

    http://flask.pocoo.org/docs/1.0/blueprints/
"""




# Imports ======================================================================

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from ucsd_bisb_unofficial.forms import PostForm
from ucsd_bisb_unofficial.models import get_db, Post
from ucsd_bisb_unofficial.principals import named_permission
from ucsd_bisb_unofficial.blog import get_post as get_post




# Blueprint assignment =========================================================

bp = Blueprint('career', __name__, url_prefix='/career')




# Functions ====================================================================

@bp.route('/index')
@login_required
@named_permission.require(http_exception=403)
def index():
    """Render the career index"""
    
    db = get_db()
    posts = Post.query.filter(Post.tag == 'career').all()
    return render_template('career/index.html')


@bp.route('/example_position')
@login_required
@named_permission.require(http_exception=403)
def example_position():
    """Render the example position"""

    return render_template('career/example-position.html')


@bp.route('/create', methods=('GET', 'POST'))
@login_required
@named_permission.require(http_exception=403)
def create():
    """Create a new post
    
    This page includes a PostForm (see `forms.py`). A new post will be added to
    the database based on the form data.
    """

    db = get_db()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            body=form.body.data,
            author=current_user,
            tag='career'
        )
        db.session.add(post)
        db.session.commit()
        flash('your post is now live!')
        return redirect(url_for('lab.index'))
    return render_template('blog/create.html', form=form)


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
@named_permission.require(http_exception=403)
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
            return redirect(url_for('career.index'))
    
    return render_template('blog/update.html', form=form, post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
@named_permission.require(http_exception=403)
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
    return redirect(url_for('career.index'))
