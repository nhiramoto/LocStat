class Github:

    _main_page_url = 'https://github.com'

    @staticmethod
    def get_absolute_url(relative_url):
        return f'{_main_page_url}/{relative_url}'
