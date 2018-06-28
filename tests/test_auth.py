#===============================================================================
# test_auth.py
#===============================================================================

"""Test authentication"""




# Imports ======================================================================

import pytest
from flask import session
from flask_login import current_user
from ucsd_bisb_unofficial.models import User




# Functions ====================================================================

def test_register(client):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register',
        data={
            'username': 'a',
            'email': 'a@a.com',
            'password': 'a',
            'password2': 'a'
        }
    )
    assert 'http://localhost/auth/login' == response.headers['Location']
    a = User.query.filter_by(username='a').first()
    assert a is not None


@pytest.mark.parametrize(
    ('username', 'email', 'password', 'password2'),
    (
        ('', '', '', ''),
        ('a', 'a@a.com', '', ''),
        ('test', 'test@test.org', 'test', 'test'),
    )
)
def test_register_validate_input(
    client,
    username,
    email,
    password,
    password2
):
    response = client.post(
        '/auth/register',
        data={
            'username': username,
            'email': email,
            'password': password,
            'password2': password
        }
    )
    print(response.data)
    assert b'<title>Register - UCSD BISB Unofficial</title>' in response.data


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'
    
    with client:
        client.get('/')
        assert session['user_id'] == '1'
        assert current_user.username == 'test'


@pytest.mark.parametrize(
    ('username', 'password', 'message'),
    (
        ('a', 'test', b'Invalid username or password'),
        ('test','a', b'Invalid username or password'),
    )
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password, follow_redirects=True)
    print(response.data)
    assert message in response.data


def test_logout(client, auth):
    auth.login()
    with client:
        auth.logout()
        assert 'user_id' not in session
