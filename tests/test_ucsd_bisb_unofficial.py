#===============================================================================
# test_ucsd_bisb_unfficial.py
#===============================================================================

"""Testing example"""



# Imports ======================================================================

import flask
import pytest

from contextlib import contextmanager
from flask_login import current_user




# Functions ====================================================================

def test_empty_db(empty_auth, empty_client, empty_db):
    """Start with a blank database."""
    
    client = empty_client
    auth = empty_auth
    auth.login()
    response = client.get('/blog/index')
    print(response.data)
    assert b'Edit' not in response.data


def login(client, auth, username='test', password='test'):
    return auth.login(
        username=username,
        password=password,
        follow_redirects=True
    )


def logout(client, auth):
    return auth.logout(follow_redirects=True)


def test_login_logout(client, auth):
    """Make sure login and logout works."""

    response = login(client, auth)
    assert b'<h1 class="display-3">It takes a village</h1>' in response.data

    response = logout(client, auth)
    print(response.data)
    assert b'<a href="/auth/login">Log In</a>' in response.data

    response = login(client, auth, username='testx')
    assert b'Invalid username or password' in response.data

    response = login(client, auth, password='testx')
    assert b'Invalid username or password' in response.data


def test_messages(client, auth):
    """Test that messages work."""

    login(client, auth)
    response = client.post(
        '/blog/create',
        data=dict(
            title='<Hello>',
            body='<strong>HTML</strong> allowed here'
        ),
        follow_redirects=True
    )
    response = client.get('/blog/index')
    assert b'No entries here so far' not in response.data
    assert b'&lt;Hello&gt;' in response.data
    assert b'&lt;strong&gt;HTML&lt;/strong&gt; allowed here' in response.data


def test_app_request_context(app):
    with app.test_request_context('/?name=Peter'):
        assert flask.request.path == '/'
        assert flask.request.args['name'] == 'Peter'


def test_test_client(app):
    with app.test_client() as c:
        response = c.get('/?tequila=42')
        assert flask.request.args['tequila'] == '42'