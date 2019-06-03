#===============================================================================
# committee.py
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

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from ucsd_bisb_unofficial.principals import named_permission




# Blueprint assignment =========================================================

bp = Blueprint('gbic', __name__, url_prefix='/gbic')




# Functions ====================================================================

@bp.route('/index')
@login_required
@named_permission.require(http_exception=403)
def index():
    """Render the gbic index"""

    return render_template('gbic/index.html')
