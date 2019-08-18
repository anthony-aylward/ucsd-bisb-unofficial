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

from flask import Blueprint, render_template, current_app
from flask_login import current_user, login_required
from werkzeug.exceptions import abort

from ucsd_bisb_unofficial.principals import named_permission
from ucsd_bisb_unofficial.models import get_db, User




# Blueprint assignment =========================================================

bp = Blueprint('gbic', __name__, url_prefix='/gbic')




# Functions ====================================================================

def is_registered(email):
    return bool(User.query.filter_by(email=email).first())


def signed_whisper_nda(email):
    user = User.query.filter_by(email=email).first()
    if user is None:
        return False
    else:
        return user.confidentiality_agreed


@bp.route('/index')
@login_required
@named_permission.require(http_exception=403)
def index():
    """Render the gbic index"""
    status = {
        office: {
            'email': email,
            'is_registered': is_registered(email),
            'signed_whisper_nda': signed_whisper_nda(email)
        }
        for office, email in current_app.config['GBIC_EMAILS']
    }

    return render_template(
        'gbic/index.html',
        **status
    )
