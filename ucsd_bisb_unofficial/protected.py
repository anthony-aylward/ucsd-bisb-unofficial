#===============================================================================
# protected.py
#===============================================================================

"""Serve protected files"""




# Imports ======================================================================

import os

from flask import send_from_directory
from flask_login import login_required



# Blueprint assignment =========================================================

bp = Blueprint('jumbotron', __name__)




# Functions ====================================================================

@bp.route('/protected/<path:filename>')
@login_required
def protected(filename):
    return send_from_directory(
        os.path.join(current_app.instance_path, 'protected'),
        filename
    )