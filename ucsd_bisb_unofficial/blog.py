#===============================================================================
# blog.py
#===============================================================================

"""Blog blueprint

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




# Blueprint assignment =========================================================

bp = Blueprint('blog', __name__, url_prefix='/blog')




# Functions ====================================================================

@bp.route('/index')
@login_required
def index():
    """Render the blog index

    This page collects all posts from the database and displays them.
    """

    db = get_db()
    posts = Post.query.all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
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
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('your post is now live!')
        return redirect(url_for('blog.index'))
    return render_template('blog/create.html', form=form)


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

    post = Post.query.filter_by(id=id).first()
    
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    
    if check_author and post.user_id != current_user.id:
        abort(403)
    
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
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
            return redirect(url_for('blog.index'))
    
    return render_template('blog/update.html', form=form, post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
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
    return redirect(url_for('blog.index'))
