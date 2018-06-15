#===============================================================================
# test_blog.py
#===============================================================================

"""Test blog"""




# Imports ======================================================================

import pytest
from ucsd_bisb_unofficial.db import get_db




# Functions ====================================================================

def test_index(client, auth):
    response = client.get('/blog/index')
    assert b"Log In" in response.data
    assert b"Register" in response.data
    
    auth.login()
    response = client.get('/blog/index')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/blog/1/update"' in response.data


@pytest.mark.parametrize('path', (
    '/blog/create',
    '/blog/1/update',
    '/blog/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()
    
    auth.login()
    # current user can't modify other user's post
    assert client.post('/blog/1/update').status_code == 403
    assert client.post('/blog/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/blog/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/blog/2/update',
    '/blog/2/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/blog/create').status_code == 200
    client.post('/blog/create', data={'title': 'created', 'body': ''})
    
    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM post').fetchone()[0]
        assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/blog/1/update').status_code == 200
    client.post('/blog/1/update', data={'title': 'updated', 'body': ''})
    
    with app.app_context():
       db = get_db()
       post = db.execute('SELECT * FROM post where ID = 1').fetchone()
       assert post['title'] == 'updated'


@pytest.mark.parametrize('path', (
    '/blog/create',
    '/blog/1/update',
))
def test_create_update_validate(client, auth, path):
    auth.login()
    response = client.post(path, data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/blog/1/delete')
    assert response.headers['Location'] == 'http://localhost/blog/index'
    
    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM post WHERE id = 1').fetchone()
        assert post is None

