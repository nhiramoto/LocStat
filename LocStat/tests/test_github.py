"""
Unit test cases for Github module (utils.github.py).
"""

import pytest
from ..utils.github import Github


class TestGithub:

    def test_get_absolute_url(self):
        assert type(Github.get_absolute_url('')) is str, \
            'Returned value is not a string.'
        assert Github.get_absolute_url('foo/bar') \
            == 'https://github.com/foo/bar'
        with pytest.raises(ValueError):
            Github.get_absolute_url(10)
