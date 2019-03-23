"""
Unit test cases for items.py
"""

from .. import items


class TestItems:

    def test_file_item(self):
        file_item = items.FileItem()
        file_item['name'] = 'foo'
        assert file_item['name'] == 'foo', \
            'Attribute "name" from FileItem does not retain the value.'
        file_item['amount_lines'] = 10
        assert file_item['amount_lines'] == 10, \
            'Attribute "amount_lines" from FileItem does not retain the value.'
        file_item['amount_bytes'] = 500
        assert file_item['amount_bytes'] == 500, \
            'Attribute "amount_bytes" from FileItem does not retain the value.'

    def test_directory_item(self):
        dir_item = items.DirectoryItem()
        dir_item['name'] = 'foo'
        assert dir_item['name'] == 'foo', \
            'Attribute "name" from FileItem does not retain the value.'
        dir_item['amount_lines'] = 10
        assert dir_item['amount_lines'] == 10, \
            'Attribute "amount_lines" from FileItem does not retain the value.'
        dir_item['amount_bytes'] = 500
        assert dir_item['amount_bytes'] == 500, \
            'Attribute "amount_bytes" from FileItem does not retain the value.'
        dir_item['is_root'] = True
        assert dir_item['is_root'], \
            'Attribute "is_root" from FileItem does not retain the value.'
        dir_item['repository_name'] = 'repository001'
        assert dir_item['repository_name'] == 'repository001', \
            'Attribute "repository_name" from FileItem does not retain \
            the value.'
        dir_item['children'] = [1, 2, 3]
        assert len(dir_item['children']) == 3 \
            and all([xi == yi for xi, yi in
                    zip(dir_item['children'], [1, 2, 3])]), \
            'Attribute "children" from FileItem does not retain \
            the value.'

    def test_text_file_item(self):
        text_file_item = items.TextFileItem()
        text_file_item['name'] = 'foo'
        assert text_file_item['name'] == 'foo', \
            'Attribute "name" from TextFileItem does not retain the value.'
        text_file_item['amount_lines'] = 10
        assert text_file_item['amount_lines'] == 10, \
            'Attribute "amount_lines" from TextFileItem does not retain \
            the value.'
        text_file_item['amount_bytes'] = 500
        assert text_file_item['amount_bytes'] == 500, \
            'Attribute "amount_bytes" from TextFileItem does not retain \
            the value.'
        text_file_item['extension'] = 'txt'
        assert text_file_item['extension'] == 'txt', \
            'Attribute "extension" from TextFileItem does not retain \
            the value.'
