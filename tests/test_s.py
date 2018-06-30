#!/usr/bin/env python3
from ucsd_bisb_unofficial.models import User

def test_password_hashing():
    u = User(username='susan')
    u.set_password('cat')
    assert not u.check_password('dog')
    assert u.check_password('cat')
