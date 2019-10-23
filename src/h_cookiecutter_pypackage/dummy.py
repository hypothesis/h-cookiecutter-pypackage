"""
A dummy package to test that we can import this during unit tests
"""

import os

from pkg_resources import resource_filename


def get_dummy():
    """A dummy function to call to check"""
    return "dummy"


def data_exists(filename):
    """Check whether local package files exist, for testing purposes"""
    return os.path.exists(resource_filename("h_cookiecutter_pypackage", filename))
