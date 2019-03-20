class Github:

    _main_page_url = 'https://github.com'

    @staticmethod
    def get_absolute_url(relative_url):
        if type(relative_url) is str:
            return f'{Github._main_page_url}/{relative_url}'
        else:
            raise ValueError('relative_url must be a string.')
