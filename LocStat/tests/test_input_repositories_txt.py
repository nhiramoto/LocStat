"""
Unit test cases for repositories.txt file reader (input_repositories_txt.py).
"""

from ..input_output.input_repositories_txt import InputTxt


class TestInputRepositoriesTxt:

    def test_file_path(self):
        inputRepositoriesTxt = InputTxt('repositories.txt')
        assert inputRepositoriesTxt.file_path == 'repositories.txt'
