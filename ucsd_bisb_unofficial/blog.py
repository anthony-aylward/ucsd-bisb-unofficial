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

from datetime import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    current_app
)
from flask_login import current_user, login_required
from werkzeug.exceptions import abort
from ucsd_bisb_unofficial.forms import PostForm, CommentForm
from ucsd_bisb_unofficial.models import get_db, Post, Comment
from ucsd_bisb_unofficial.principals import named_permission
from ucsd_bisb_unofficial.uploads import documents, images




# Blueprint assignment =========================================================

bp = Blueprint('blog', __name__, url_prefix='/blog')




# Functions ====================================================================

@bp.route('/index')
@login_required
@named_permission.require(http_exception=403)
def index():
    """Render the blog index

    This page collects all posts from the database and displays them.
    """

    db = get_db()
    page = request.args.get('page', 1, type=int)
    posts = (
        Post.query
        .filter(Post.tag == 'blog')
        .order_by(Post.timestamp.desc())
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)
    )
    next_url = (
        url_for('blog.index', page=posts.next_num)
        if posts.has_next
        else None
    )
    prev_url = (
        url_for('blog.index', page=posts.prev_num)
        if posts.has_prev
        else None
    )
    for post in posts.items:
        post.preview = post.body[:128] + (len(post.body) > 128) * '...'
    return render_template(
        'blog/index.html',
        posts=posts.items,
        next_url=next_url,
        prev_url=prev_url
    )


def construct_create_route(blueprint, tag):
    @blueprint.route('/create', methods=('GET', 'POST'))
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
            post = Post(
                title=form.title.data,
                body=form.body.data,
                author=current_user,
                tag=tag,
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
            flash('your post is now live!')
            return redirect(url_for(f'{tag}.index'))
        return render_template(f'blog/create.html', form=form)
    return create


def construct_comment_route(blueprint, tag):
    @blueprint.route('/<int:post_id>/comment/', methods=('GET', 'POST'))
    @login_required
    @named_permission.require(http_exception=403)
    def comment(post_id):
        """Comment on a post
        
        This page includes a CommentForm (see `forms.py`). A new comment will
        be added to the database based on the form data.
        """
        
        post = get_post(post_id)
        db = get_db()
        form = CommentForm()
        if form.validate_on_submit():
            comment = Comment(
                body=form.body.data,
                user_id=current_user.id,
                post_id=post_id
            )
            db.session.add(comment)
            db.session.commit()
            flash('your comment is now live!')
            return redirect(
                url_for(f'{tag}.detail', id=post.id)
            )
        return render_template('blog/comment.html', form=form, post=post)
    return comment


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

    comment = Comment.query.filter_by(id=id).first()
    if comment is None:
        abort(404, f"Comment id {id} doesn't exist.")
    if check_author and comment.user_id != current_user.id:
        abort(403)
    return comment


def construct_update_route(blueprint, tag):
    @blueprint.route('/<int:id>/update', methods=('GET', 'POST'))
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
                return redirect(url_for(f'{tag}.index'))
        return render_template(
            'blog/update.html',
            form=form,
            post=post,
            delete_route=f'{tag}.delete'
        )
    return update


def construct_delete_route(blueprint, tag):
    @blueprint.route('/<int:id>/delete', methods=('POST',))
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
        return redirect(url_for(f'{tag}.index'))
    return delete


def construct_delete_comment_route(blueprint, tag):
    @blueprint.route('/<int:id>/delete-comment', methods=('GET', 'POST',))
    @login_required
    @named_permission.require(http_exception=403)
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
        return redirect(url_for(f'{tag}.detail', id=comment.post_id))
    return delete_comment


def construct_detail_route(blueprint, tag):
    @blueprint.route('/<int:id>/detail')
    @login_required
    @named_permission.require(http_exception=403)
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
        db = get_db()
        comments = Comment.query.filter(Comment.post_id == id).all()[::-1]
        return render_template(
            'blog/detail.html',
            post=post,
            comments=comments,
            index_route=f'{tag}.index',
            update_route=f'{tag}.update',
            comment_route=f'{tag}.comment'
        )
    return detail


create = construct_create_route(bp, 'blog')
update = construct_update_route(bp, 'blog')
delete = construct_delete_route(bp, 'blog')
detail = construct_detail_route(bp, 'blog')
comment = construct_comment_route(bp, 'blog')
delete_comment = construct_delete_comment_route(bp, 'blog')
