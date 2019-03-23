# -*- coding: utf-8 -*-
# vim: syntax=python :

"""
Model of itens scraped by the spider.
"""

import scrapy


class FileItem(scrapy.Item):
    name = scrapy.Field()
    amount_lines = scrapy.Field()
    amount_bytes = scrapy.Field()


class DirectoryItem(FileItem):
    is_root = scrapy.Field()
    repository_name = scrapy.Field()
    children = scrapy.Field()

    def update_lines_bytes(self):
        """
        Updates the number of lines and bytes in the subdirectory.
        """
        if 'children' in self.fields and type(self['children']) is list:
            self['amount_lines'] = 0
            self['amount_bytes'] = 0
            for child in self['children']:
                if isinstance(child, DirectoryItem):
                    child.update_lines_bytes()
                self['amount_lines'] += child['amount_lines']
                self['amount_bytes'] += child['amount_bytes']

    def index_extensions(self):
        """
        Creates an index with the total of lines and bytes for each file
          type.
        """
        def index_extensions_recursively(dir_item, index):
            if 'children' in dir_item.fields \
                    and type(dir_item['children']) is list:
                for child in dir_item['children']:
                    if isinstance(child, TextFileItem) \
                            and 'extension' in child.fields \
                            and 'amount_lines' in child.fields \
                            and 'amount_bytes' in child.fields:
                        if child['extension'] in index:
                            index[child['extension']]['amount_lines'] += \
                                child['amount_lines']
                            index[child['extension']]['amount_bytes'] += \
                                child['amount_bytes']
                        else:
                            index[child['extension']] = {
                                'amount_lines': child['amount_lines'],
                                'amount_bytes': child['amount_bytes']
                            }
                    elif isinstance(child, DirectoryItem):
                        index_extensions_recursively(child, index)

        index = {}
        index_extensions_recursively(self, index)
        return index


class TextFileItem(FileItem):
    extension = scrapy.Field()
