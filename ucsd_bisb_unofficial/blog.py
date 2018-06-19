#===============================================================================
# blog.py
#===============================================================================

"""Blog blueprint"""




# Imports ======================================================================

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import current_user
from werkzeug.exceptions import abort

from ucsd_bisb_unofficial.auth import login_required
from ucsd_bisb_unofficial.forms import PostForm
from ucsd_bisb_unofficial.models import get_db, Post




# Blueprint assignment =========================================================

bp = Blueprint('blog', __name__, url_prefix='/blog')




# Functions ====================================================================

@bp.route('/index')
def index():
    db = get_db()
    posts = Post.query.all()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    db = get_db()
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            body=form.post.data,
            author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash('your post is now live!')
        return redirect(url_for('blog.index'))
    return render_template('blog/create.html', form=form)


def get_post(id, check_author=True):
    post = Post.query.filter_by(id=id).first()
    
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    
    if check_author and post.user_id != current_user.id:
        abort(403)
    
    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
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
    post = get_post(id)
    db = get_db()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('blog.index'))
