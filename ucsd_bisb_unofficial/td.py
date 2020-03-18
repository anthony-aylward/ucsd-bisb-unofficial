#===============================================================================
# td.py
#===============================================================================

"""thesis / dissertation blueprint

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
    get_post, construct_index_route, construct_create_route,
    construct_update_route, construct_delete_route, construct_detail_route,
    construct_comment_route, construct_delete_comment_route
)




# Blueprint assignment =========================================================

bp = Blueprint('td', __name__, url_prefix='/td')




# Functions ====================================================================

index = construct_index_route(bp, 'td')
create = construct_create_route(bp, 'td')
update = construct_update_route(bp, 'td')
delete = construct_delete_route(bp, 'td')
detail = construct_detail_route(bp, 'td')
comment = construct_comment_route(bp, 'td')
delete_comment = construct_delete_comment_route(bp, 'td')
