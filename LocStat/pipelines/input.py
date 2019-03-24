import sys


class TxtFileReader:
    """
    Reads a text file and returns a list of repositories URLs.
    """

    def __init__(self, file_path):
        self._file = None
        self._file_path = file_path

    def __enter__(self):
        self._file = open(self._file_path, 'r')
        return self

    def __exit__(self, *args):
        if self._file and not self._file.closed:
            self._file.close()

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        self._file_path = file_path

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file):
        self._file = file

    @property
    def closed(self):
        if self._file:
            return self._file.closed
        else:
            return True

    def get_all(self):
        """
        Returns a list of all repositories URLs from the file.
        """
        if self._file and not self._file.closed:
            lines = self._file.readlines()
            lines = list(map(lambda s: s.strip('\n'), lines))
            lines = list(filter(lambda s: s, lines))
            return lines
        else:
            return []
