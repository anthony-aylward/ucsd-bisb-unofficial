#===============================================================================
# townhall.py
#===============================================================================

"""committee blueprint

Attributes
----------
bp : Blueprint
    blueprint object, see the flask tutorial/documentation:

    http://flask.pocoo.org/docs/1.0/tutorial/views/

    http://flask.pocoo.org/docs/1.0/blueprints/
"""




# Imports ======================================================================

from flask import Blueprint, render_template, current_app
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from ucsd_bisb_unofficial.principals import named_permission




# Blueprint assignment =========================================================

bp = Blueprint('townhall', __name__, url_prefix='/townhall')




# Functions ====================================================================

@bp.route('/index')
@login_required
@named_permission.require(http_exception=403)
def index():
    """Render the town hall index"""

    return render_template('townhall/index.html')
