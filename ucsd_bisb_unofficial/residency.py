#===============================================================================
# residency.py
#===============================================================================

"""Residency blueprint

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
    construct_delete_route, construct_detail_route
)




# Blueprint assignment =========================================================

bp = Blueprint('residency', __name__, url_prefix='/residency')




# Functions ====================================================================

@bp.route('/index')
@login_required
@named_permission.require(http_exception=403)
def index():
    """Render the residency index"""
    
    db = get_db()
    posts = Post.query.filter(Post.tag == 'residency').all()[::-1]
    for post in posts:
        post.preview = post.body[:256]
    return render_template('residency/index.html', posts=posts)


create = construct_create_route(bp, 'residency')
update = construct_update_route(bp, 'residency')
delete = construct_delete_route(bp, 'residency')
detail = construct_detail_route(bp, 'residency')
