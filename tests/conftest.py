#===============================================================================
# conftest.py
#===============================================================================

"""Tests for ucsd_bisb_unofficial"""




# Imports ======================================================================

from datetime import datetime
import pytest
from ucsd_bisb_unofficial import create_app
from ucsd_bisb_unofficial.models import get_db, User, Post




#  Classes ======================================================================

class AuthActions(object):
    def __init__(self, client):
        self._client = client
    
    def login(self, username='test', password='test', follow_redirects=False):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password},
            follow_redirects=follow_redirects
        )
    
    def logout(self, follow_redirects=False):
        return self._client.get('/auth/logout', follow_redirects=follow_redirects)




# Functions ====================================================================

@pytest.fixture
def testing_config():
    return {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'MAIL_SERVER': None,
        'SECRET_KEY': 'you-will-never-guess',
        'WTF_CSRF_ENABLED': False
    }


@pytest.fixture
def non_testing_config():
    return {
        'TESTING': False,
        'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'MAIL_SERVER': None
    }


@pytest.fixture
def app(testing_config, request):
    app = create_app(testing_config)
    app_context = app.app_context()
    app_context.push()
    
    def teardown():
        app_context.pop()
    
    request.addfinalizer(teardown)
    return app


@pytest.fixture
def db(app, request):
    db = get_db()
    db.create_all()

    test_user = User(username='test', email='test@test.org')
    other_user = User(username='other', email='other@other.org')
    test_user.set_password('test')
    other_user.set_password('other')

    test_post = Post(
        title='test title',
        body='test\nbody',
        user_id=1,
        timestamp=datetime.strptime('2018-01-01 00:00:00', '%Y-%d-%m %H:%M:%S')
    )

    db.session.add(test_user)
    db.session.add(other_user)
    db.session.add(test_post)
    db.session.commit()

    def teardown():
        db.session.remove()
        db.drop_all()
    
    request.addfinalizer(teardown)
    return db


@pytest.fixture
def empty_db(app):
    db = get_db()
    db.create_all()

    test_user = User(username='test', email='test@test.org')
    test_user.set_password('test')

    db.session.add(test_user)
    db.session.commit()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture
def client(app, db):
    return app.test_client()


@pytest.fixture
def empty_client(app, empty_db):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def empty_auth(empty_client):
    return AuthActions(empty_client)
