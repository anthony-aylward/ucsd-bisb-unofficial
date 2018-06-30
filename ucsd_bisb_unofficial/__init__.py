#===============================================================================
# __init__.py
#===============================================================================

"""Initialization"""




# Imports ======================================================================

import os

from flask import Flask




# Functions ====================================================================

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    from .models import db, migrate, User
    db.init_app(app)
    migrate.init_app(app, db)

    from .login import login
    login.init_app(app)
    login.login_view = 'auth.login'

    from .email import mail
    mail.init_app(app)
    
    from . import auth
    app.register_blueprint(auth.bp)
    
    from . import blog
    app.register_blueprint(blog.bp)
    
    from . import jumbotron
    app.register_blueprint(jumbotron.bp)

    from . import protected
    app.register_blueprint(protected.bp)

    app.add_url_rule('/', endpoint='auth.login')
    
    return app

