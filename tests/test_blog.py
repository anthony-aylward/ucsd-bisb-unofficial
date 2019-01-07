#===============================================================================
# test_blog.py
#===============================================================================

"""Test blog"""




# Imports ======================================================================

import pytest
from ucsd_bisb_unofficial.models import get_db, Post




# Functions ====================================================================

def test_index(client, auth, db):
    response = client.get('/blog/index', follow_redirects=True)
    assert b"Log In" in response.data
    assert b"Register" in response.data
    
    auth.login()
    response = client.get('/blog/index')
    print(response.data)
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
    response = client.post(path, follow_redirects=True)
    assert b'Please log in to access this page.' in response.data


def test_author_required(app, client, auth, db):
    # change the post author to another user
    post = Post.query.filter_by(user_id=1).first()
    post.user_id = 2
    db.session.commit()
    
    auth.login()
    # current user can't modify other user's post
    assert client.post('/blog/1/update').status_code == 403
    assert client.post('/blog/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/blog/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', ('/blog/2/update', '/blog/2/delete'))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_create(client, auth):
    auth.login()
    assert client.get('/blog/create').status_code == 200
    response = client.post(
        '/blog/create',
        data={'title': 'created', 'body': 'another test'}
    )
    count = Post.query.count()
    assert count == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/blog/1/update').status_code == 200
    client.post('/blog/1/update', data={'title': 'updated', 'body': ''})
    post = Post.query.filter_by(id=1).first()
    assert post.title == 'updated'


def test_create_validate(client, auth):
    auth.login()
    response = client.post('/blog/create', data={'title': '', 'body': ''})
    assert b'<title>New Post - UCSD BISB Unofficial</title>' in response.data


def test_update_validate(client, auth):
    auth.login()
    response = client.post('/blog/1/update', data={'title': '', 'body': ''})
    assert b'Title is required.' in response.data


def test_delete(client, auth, app, db):
    auth.login()
    response = client.post('/blog/1/delete')
    assert response.headers['Location'] == 'http://localhost/blog/index'
    post = Post.query.filter_by(id=1).first()
    assert post is None
