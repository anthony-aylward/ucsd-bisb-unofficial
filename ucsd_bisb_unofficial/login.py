#===============================================================================
# login.py
#===============================================================================

"""Miguel Grinberg's Flask Mega-Tutorial"""




# Imports ======================================================================

from flask_login import LoginManager
from ucsd_bisb_unofficial.models import User




# Initialization ===============================================================

login = LoginManager()




# Functions ====================================================================

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
