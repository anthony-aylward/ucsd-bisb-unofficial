#===============================================================================
# principals.py
#===============================================================================

"""Initialization of Flask-Principal objects"""




# Imports ======================================================================

from flask import g
from flask_login import current_user
from flask_principal import (
    Principal, RoleNeed, UserNeed, Permission, identity_loaded
)




# Initialization ===============================================================

principals = Principal()

named_need = RoleNeed('named_user')
whisper_need = RoleNeed('whisper_user')

named_permission = Permission(named_need)
whisper_permission = Permission(whisper_need)




# Functions ====================================================================

@identity_loaded.connect
def on_identity_loaded(sender, identity):
    identity.user = current_user
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

