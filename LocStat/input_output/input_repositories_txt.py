from ..utils.github import Github


class InputTxt:
    """
    Reads a file and returns a list of repositories URLs.
    """

    def __init__(self, file_path):
        self._file_path = file_path

    @property
    def file_path(self):
        return self._file_path

    def get_all(self):
        """
        Return a list of repositories URLs from the file.
        """
        with open(self._file_path, 'r') as file:
            pass
