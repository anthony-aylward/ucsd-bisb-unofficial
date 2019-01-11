#===============================================================================
# lab.py
#===============================================================================

"""Lab blueprint

Attributes
----------
bp : Blueprint
    blueprint object, see the flask tutorial/documentation:

    http://flask.pocoo.org/docs/1.0/tutorial/views/

    http://flask.pocoo.org/docs/1.0/blueprints/
"""




# Imports ======================================================================

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for,
    current_app
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
from ucsd_bisb_unofficial.rotation_database import RotationDatabase




# Blueprint assignment =========================================================

bp = Blueprint('lab', __name__, url_prefix='/lab')




# Functions ====================================================================

index = construct_index_route(bp, 'lab')
create = construct_create_route(bp, 'lab')
update = construct_update_route(bp, 'lab')
delete = construct_delete_route(bp, 'lab')
detail = construct_detail_route(bp, 'lab')
comment = construct_comment_route(bp, 'lab')
delete_comment = construct_delete_comment_route(bp, 'lab')

@bp.route('/rotations')
@login_required
@named_permission.require(http_exception=403)
def rotations():
    """Render the rotation database"""
    quarter = request.args.get('quarter', 'all', type=str)
    quarter_columns_dict = {
        'all': (),
        'fall-2018': (1, 2),
        'winter-2019': (3, 4),
        'spring-2019': (5, 6)
    }
    rotation_db = RotationDatabase(current_app.config['ROTATION_DATABASE_CSV'])
    columns = quarter_columns_dict[quarter]
    table = rotation_db.markdown_table(*columns)
    return render_template('lab/rotations.html', table=table, quarter=quarter)
