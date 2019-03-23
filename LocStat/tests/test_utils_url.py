"""
Unit test cases for utils.url module.
"""

import pytest
from ..utils.url import Url


class TestUtilsUrl:

    def test_github_url(self):
        assert type(Url.github_url('')) is str, \
            'Returned value is not a string.'
        assert Url.github_url('foo/bar') \
            == 'https://github.com/foo/bar'
        with pytest.raises(ValueError):
            Url.github_url(10)

    def test_cached(self):
        assert type(Url.cached('')) is str, \
            'Returned value is not a string.'
        assert Url.cached('http://foo.bar') \
            == \
            'http://webcache.googleusercontent.com/search?q=http://foo.bar'
        with pytest.raises(ValueError):
            Url.cached(10)
