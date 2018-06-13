#===============================================================================
# jumbotron.py
#===============================================================================

"""Jumbotron blueprint"""




# Imports ======================================================================

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from ucsd_bisb_unofficial.auth import login_required
from ucsd_bisb_unofficial.db import get_db




# Blueprint assignment =========================================================

bp = Blueprint('jumbotron', __name__, url_prefix='/jumbotron')




# Functions ====================================================================

@bp.route('/')
@login_required
def index():
    return render_template('jumbotron/index.html')
