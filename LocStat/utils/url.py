class Url:
    """
    This module implements useful methods that manipulate urls, used in the
        project.
    """

    _github_main_page_url = 'https://github.com'
    _googlecache_urlprefix = 'http://webcache.googleusercontent.com/search?q='

    @staticmethod
    def github_url(relative_url):
        """
        Get the absolute url from the repository relative url
            hosted on Github
        """
        if type(relative_url) is str:
            return f'{Url._github_main_page_url}/{relative_url}'
        else:
            raise ValueError('relative_url must be a string.')

    @staticmethod
    def cached(url):
        """
        Get the google cached version of url
        """
        if type(url) is str:
            return f'{Url._googlecache_urlprefix}{url}'
        else:
            raise ValueError('url must be a string.')
