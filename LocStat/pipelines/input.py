class TxtFileReader:
    """
    Reads a text file and returns a list of repositories URLs.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.file = open(self.file_path, 'r')
        return self

    def __exit__(self, *args):
        if self.file and not self.file.closed:
            self.file.close()

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        self._file_path = file_path

    @property
    def closed(self):
        if self.file:
            return self.file.closed
        else:
            return True

    def get_all(self):
        """
        Returns a list of all repositories URLs from the file.
        """
        repo_urls = []
        if self.file and not self.file.closed:
            for line in self.file:
                rel_url = line.strip(' \t\n/')
                repo_urls.append(rel_url)
        return repo_urls
