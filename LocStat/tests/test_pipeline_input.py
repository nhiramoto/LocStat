"""
Unit test cases for txt file reader (pipelines.input.TxtFileReader).
"""

import pytest
from unittest import mock
from ..pipelines.input import TxtFileReader


class TestTxtFileReader:

    file_content = (
        'foo/bar\n'
        'lorem/ipsum\n'
        'another/repo'
    )

    @pytest.fixture
    def reader(self):
        with mock.patch('builtins.open', new=mock.mock_open(
                read_data=TestTxtFileReader.file_content)):
            return TxtFileReader('repositories.txt')

    def test_open(self):
        with mock.patch('builtins.open',
                        new=mock.mock_open()) as m:
            with TxtFileReader('repositories.txt'):
                m.assert_called_with('repositories.txt', 'r')

    def test_file_path(self, reader):
        with mock.patch('builtins.open', new=mock.mock_open(
                read_data=TestTxtFileReader.file_content)):
            with TxtFileReader('repositories.txt') as reader:
                assert type(reader.file_path) is str, \
                    'file_path attribute is not a string.'
                assert reader.file_path == 'repositories.txt', \
                    'file_path attribute doesn\'t receive correct value.'

    def test_get_all_returns_list(self, reader):
        with mock.patch('builtins.open', new=mock.mock_open(
                read_data=TestTxtFileReader.file_content)):
            with TxtFileReader('repositories.txt') as reader:
                repo_urls = reader.get_all()
                assert type(repo_urls) is list, \
                    'get_all method doesn\'t return a list.'
