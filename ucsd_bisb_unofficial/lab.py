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
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from ucsd_bisb_unofficial.forms import PostForm
from ucsd_bisb_unofficial.models import get_db, Post




# Blueprint assignment =========================================================

bp = Blueprint('lab', __name__, url_prefix='/lab')




# Functions ====================================================================

@bp.route('/index')
@login_required
def index():
    """Render the lab index"""

    return render_template('lab/index.html')

