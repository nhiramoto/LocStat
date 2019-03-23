"""
Unit test cases for txt file reader (pipelines.input.TxtFileReader).
"""

import os
import pytest
from ..pipelines.input import TxtFileReader


class TestTxtFileReader:

    def test_opening_file(self):
        with TxtFileReader('repositories.txt'):
            pass
        with pytest.raises(FileNotFoundError):
            with TxtFileReader('notexists.txt'):
                pass

    def test_closing_file(self):
        file = TxtFileReader('repositories.txt')
        with file:
            pass
        assert file.closed, 'The file is not being closed.'

    def test_file_path(self):
        with TxtFileReader('repositories.txt') as txt_file_reader:
            assert type(txt_file_reader.file_path) is str, \
                'file_path attribute is not a string.'
            assert txt_file_reader.file_path == 'repositories.txt', \
                'file_path attribute doesn\'t receive correct value.'

    def test_get_all_returns_list(self):
        with TxtFileReader('repositories.txt') as txt_file_reader:
            repo_urls = txt_file_reader.get_all()
            assert type(repo_urls) is list, \
                'get_all method doesn\'t return a list.'

    def test_get_all_3_repositories(self):
        file_path = os.path.join(
            'LocStat', 'tests', 'txt_files', '3_repositories.txt')
        with TxtFileReader(file_path) as txt_file_reader:
            repo_urls = txt_file_reader.get_all()
            assert len(repo_urls) == 3, \
                'Incorrect number of elements in the returned list.'
            assert all(type(url) is str for url in repo_urls), \
                'Returned list does not contain only strings.'
            assert repo_urls[0] == 'facebook/react'
            assert repo_urls[1] == 'pypa/pipenv'
            assert repo_urls[2] == 'd3/d3'
