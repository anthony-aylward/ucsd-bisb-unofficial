#===============================================================================
# protected.py
#===============================================================================

"""Serve protected files"""




# Imports ======================================================================

import os

from flask import Blueprint, send_from_directory, current_app
from flask_login import login_required



# Blueprint assignment =========================================================

bp = Blueprint('protected', __name__, url_prefix='/protected')




# Functions ====================================================================

@bp.route('/<path:filename>')
@login_required
def protected(filename):
    return send_from_directory(
        os.path.join(current_app.instance_path, 'protected'),
        filename
    )