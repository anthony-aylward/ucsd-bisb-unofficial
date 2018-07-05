#===============================================================================
# jumbotron.py
#===============================================================================

"""Jumbotron blueprint

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
from flask_login import login_required
from werkzeug.exceptions import abort




# Blueprint assignment =========================================================

bp = Blueprint('jumbotron', __name__)




# Functions ====================================================================

@bp.route('/')
@login_required
def index():
    """Render the index page"""

    return render_template('jumbotron/index.html')
