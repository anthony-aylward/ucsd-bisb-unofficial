#===============================================================================
# test_factory.py
#===============================================================================

"""Test factory"""




# Imports ======================================================================

from ucsd_bisb_unofficial import create_app




# Functions ====================================================================

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello, World!'

