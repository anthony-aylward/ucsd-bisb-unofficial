#===============================================================================
# login.py
#===============================================================================

"""Instantiation of the LoginManager (see Flask-Login: 
http://flask-login.readthedocs.io/en/latest/#configuring-your-application )

Attributes
----------
login : LoginManager
    The login manager
"""




# Imports ======================================================================

from flask_login import LoginManager
from ucsd_bisb_unofficial.models import User, WhisperUser




# Initialization ===============================================================

login = LoginManager()




# Functions ====================================================================

@login.user_loader
def load_user(id):
    """The load_user function required by the login manager
    
    This tells the login manager how to load a user. In this case, the user
    is retrieved from the database by ID no.

    Parameters
    ----------
    id
        The ID no. of the user to be loaded
    
    Returns
    -------
    User | WhisperUser
        The user to be loaded
    """
    id = int(id)
    user_count = len(User.query.all())
    if id > user_count:
        return WhisperUser.query.get(id - user_count)
    return User.query.get(id)
