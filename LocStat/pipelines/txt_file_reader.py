import sys
from ..utils.url import Url


class TxtFileReader:
    """
    Reads a text file and returns a list of repositories URLs.
    """

    def __init__(self, file_path):
        self._file_path = file_path
        self._file = open(self._file_path, 'r')

    @property
    def file_path(self):
        return self._file_path

    def get_all(self):
        """
        Returns a list of all repositories URLs from the file.
        """
        repo_urls = []
        with self._file as file:
            for line in file:
                rel_url = line.strip(' \t\n/')
                repo_urls.append(Url.github_url(rel_url))
        return repo_urls
