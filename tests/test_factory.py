#===============================================================================
# test_factory.py
#===============================================================================

"""Test factory"""




# Imports ======================================================================

from ucsd_bisb_unofficial import create_app




# Functions ====================================================================

def test_config(testing_config, non_testing_config):
    assert not create_app(non_testing_config).testing
    assert create_app(testing_config).testing
