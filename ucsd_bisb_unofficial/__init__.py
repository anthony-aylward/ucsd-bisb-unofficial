#===============================================================================
# __init__.py
#===============================================================================

"""Initialization

This file contains the application factory for the ucsd_bisb_unofficial app.
"""




# Imports ======================================================================

import os

from flask import Flask
from flask_login import login_required
from flask_uploads import configure_uploads



# Functions ====================================================================

def create_app(test_config=None):
    """The application factory function

    This function creates and configures the Flask application object. For
    more on application factories, see the Flask documentation/tutorial:

    http://flask.pocoo.org/docs/1.0/tutorial/factory/

    http://flask.pocoo.org/docs/1.0/patterns/appfactories/

    Parameters
    ----------
    test_config : dict
        A dictionary containing configuration parameters for use during unit
        testing. If this parameter is `None`, the configuration will be loaded
        from `config.py` in the instance folder.

    Returns
    -------
    Flask
        A flask app
    """

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
    
    from ucsd_bisb_unofficial.models import (
        db, migrate, Role, get_db, Post, WhisperPost
    )
    from ucsd_bisb_unofficial.login import login
    from ucsd_bisb_unofficial.email import mail
    from ucsd_bisb_unofficial.principals import principals
    from ucsd_bisb_unofficial.errors import forbidden
    from ucsd_bisb_unofficial.misaka import md
    from ucsd_bisb_unofficial.fts import fts
    
    for ext in db, login, mail, principals, md, fts:
        ext.init_app(app)
    migrate.init_app(app, db)
    login.login_view = 'auth.login'

    for error, handler in ((403, forbidden),):
        app.register_error_handler(403, forbidden)
    
    from ucsd_bisb_unofficial import (
        auth, blog, jumbotron, protected, lab, career, tech, whisper,
        residency, ta, search, seminars, mental_health, news, stats, committee,
        gbic, fellowships, townhall, settings, courses, td, exam, anti_racism,
        outreach
    )
    for bp in (
        auth.bp, blog.bp, jumbotron.bp, protected.bp, lab.bp, career.bp,
        tech.bp, whisper.bp, residency.bp, ta.bp, search.bp, seminars.bp,
        mental_health.bp, news.bp, stats.bp, committee.bp, gbic.bp,
        fellowships.bp, townhall.bp, settings.bp, courses.bp, td.bp, exam.bp,
        anti_racism.bp, outreach.bp
    ):
        app.register_blueprint(bp)
    
    from ucsd_bisb_unofficial import uploads
    app.register_blueprint(uploads.uploads_mod)

    app.add_url_rule('/', endpoint='auth.login')

    from ucsd_bisb_unofficial.uploads import documents, images
    configure_uploads(app, documents)
    configure_uploads(app, images)

    @app.before_first_request
    def populate_databse():
        with app.app_context():
            db = get_db()
            db.create_all()
            commit = False
            for name, description in (
                ('admin', 'site administrator'),
                ('whisper_user', 'whisper app user'),
                ('named_user', 'named user')
            ):
                if not Role.query.filter_by(name=name).first():
                    role = Role(name=name, description=description)
                    db.session.add(role)
                    commit = True
            if commit:
                db.session.commit()
    
    @app.before_first_request
    def reindex():
        with app.app_context():
            Post.reindex()
            WhisperPost.reindex()
    
    return app
