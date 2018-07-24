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

from flask import Blueprint, render_template
from flask_login import login_required

from ucsd_bisb_unofficial.principals import named_permission




# Blueprint assignment =========================================================

bp = Blueprint('career', __name__, url_prefix='/career')




# Functions ====================================================================

@bp.route('/index')
@login_required
@named_permission.require(http_exception=403)
def index():
    """Render the career index"""

    return render_template('career/index.html')


@bp.route('/example_position')
@login_required
@named_permission.require(http_exception=403)
def example_position():
    """Render the example position"""

    return render_template('career/example-position.html')
