#===============================================================================
# search.py
#===============================================================================

"""Search functionality"""




# Imports ======================================================================

import sqlite3

from flask import (
    Blueprint, current_app, g, request, redirect, render_template, url_for
)
from flask_login import current_user, login_required
from ucsd_bisb_unofficial.models import Post
from ucsd_bisb_unofficial.forms import SearchForm




# Blueprint assignment =========================================================

bp = Blueprint('search', __name__, url_prefix='/search')




# Functions ====================================================================

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('jumbotron.index'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(
        g.search_form.q.data,
        page,
        current_app.config['POSTS_PER_PAGE']
    )
    next_url = (
        url_for('search.search', q=g.search_form.q.data, page=page + 1)
        if total > page * current_app.config['POSTS_PER_PAGE']
        else None
    )
    prev_url = (
        url_for('search.search', q=g.search_form.q.data, page=page - 1)
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
            'detail_route': f'{post.tag}.detail'
        }
        for post in posts
    )
    return render_template(
        'search/search.html',
        title='Search Results',
        posts=posts,
        next_url=next_url,
        prev_url=prev_url
    )
