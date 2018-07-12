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




# Blueprint assignment =========================================================

bp = Blueprint('tech', __name__, url_prefix='/tech')




# Functions ====================================================================

@bp.route('/index')
@login_required
def index():
    """Render the tech index"""

    return render_template('tech/index.html')
