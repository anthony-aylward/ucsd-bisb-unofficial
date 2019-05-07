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
from ucsd_bisb_unofficial.blog import (
    get_post, construct_create_route, construct_update_route,
    construct_delete_route, construct_detail_route, construct_comment_route,
    construct_delete_comment_route
)




# Blueprint assignment =========================================================

bp = Blueprint('career', __name__, url_prefix='/career')




# Functions ====================================================================

@bp.route('/index')
@login_required
@named_permission.require(http_exception=403)
def index():
    """Render the career index"""
    
    db = get_db()
    posts = Post.query.filter(Post.tag == 'career').all()[::-1]
    for post in posts:
        post.preview = post.body[:256]
    return render_template('career/index.html', posts=posts)


@bp.route('/example_position')
@login_required
@named_permission.require(http_exception=403)
def example_position():
    """Render the example position"""

    return render_template('career/example-position.html')


@bp.route('/companies')
@login_required
@named_permission.require(http_exception=403)
def companies():
    """Render the company databse"""

    return render_template(
        'career/companies.html',
        table=markdown_table(current_app.config['COMPANIES_CSV']),
        dept=dept
    )



create = construct_create_route(bp, 'career')
update = construct_update_route(bp, 'career')
delete = construct_delete_route(bp, 'career')
detail = construct_detail_route(bp, 'career')
comment = construct_comment_route(bp, 'career')
delete_comment = construct_delete_comment_route(bp, 'career')