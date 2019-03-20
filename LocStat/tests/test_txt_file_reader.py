"""
Unit test cases for repositories.txt file reader (txt_file_reader.py).
"""

import os
import pytest
from ..input_output.txt_file_reader import TxtFileReader


class TestTxtFileReader:

    def test_file_path(self):
        txt_file_reader = TxtFileReader('repositories.txt')
        assert type(txt_file_reader.file_path) is str, \
            'file_path attribute is not a string.'
        assert txt_file_reader.file_path == 'repositories.txt', \
            'file_path attribute doesn\'t receive correct value.'

    def test_file_not_exists(self):
        txt_file_reader = TxtFileReader('notexists.txt')
        with pytest.raises(FileNotFoundError):
            txt_file_reader.get_all()

    def test_get_all_returns_list(self):
        txt_file_reader = TxtFileReader('repositories.txt')
        try:
            repo_urls = txt_file_reader.get_all()
        except:
            pass
        else:
            assert type(repo_urls) is list, 'get_all method doesn\'t return a list.'

    def test_get_all_3_repositories(self):
        file_path = os.path.join('LocStat', 'tests', 'txt_files', '3_repositories.txt')
        txt_file_reader = TxtFileReader(file_path)
        repo_urls = txt_file_reader.get_all()
        assert len(repo_urls) == 3, 'Incorrect number of elements in the returned list.'
        assert all(type(url) is str for url in repo_urls), \
            'Returned list does not contain only strings.'
        assert repo_urls[0] == 'https://github.com/facebook/react'
        assert repo_urls[1] == 'https://github.com/pypa/pipenv'
        assert repo_urls[2] == 'https://github.com/d3/d3'
