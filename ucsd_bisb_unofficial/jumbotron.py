#===============================================================================
# jumbotron.py
#===============================================================================

"""Jumbotron blueprint"""




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
    return render_template('jumbotron/index.html')
