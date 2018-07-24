#===============================================================================
# errors.py
#===============================================================================

"""errors"""




# Imports  =====================================================================

from flask import render_template
from ucsd_bisb_unofficial.models import get_db





# Functions ====================================================================

def forbidden(error):
    return render_template('errors/403.html'), 403
