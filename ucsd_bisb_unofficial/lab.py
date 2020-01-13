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
from ucsd_bisb_unofficial.markdown_table import markdown_table




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
    
    quarter = request.args.get('quarter', 'fall-2019', type=str)
    rotation_db = RotationDatabase(current_app.config['ROTATION_DATABASE_CSV'])
    for column_name, json_file_path in current_app.config[
        'ROTATION_DATABASE_JSON'
    ].items():
        rotation_db.add_json(
            column_name,
            json_file_path
        )

    def markdown_link(col, text):
        return '[{}]({})'.format(
            text,
            url_for('protected.protected', filename=rotation_db.dict[name][col])
        )

    for name in rotation_db.dict.keys():
        for col in 10, 11, 12, 13, 14, 15:
            if rotation_db.dict[name][col]:
                rotation_db.dict[name][col] = markdown_link(
                    col, 'Proposal' if col % 2 == 0 else 'Report'
                )
    quarter_to_columns = {
        'fall-2018': (1, 2, 14, 15, 22), 'winter-2019': (3, 4, 16, 17, 22),
        'spring-2019': (5, 6, 18, 19, 22), 'summer-2019': (7, 8, 22),
        'fall-2019': (9, 10, 20, 21, 22)
    }
    return render_template(
        'lab/rotations.html',
        table=rotation_db.markdown_table(*quarter_to_columns[quarter]),
        quarter=quarter
    )


@bp.route('/profs')
@login_required
@named_permission.require(http_exception=403)
def profs():
    """Render the faculty database"""

    dept = request.args.get('dept', 'bio', type=str)
    return render_template(
        'lab/profs.html',
        table=markdown_table(current_app.config['PROFS_CSV'][dept]),
        dept=dept
    )
