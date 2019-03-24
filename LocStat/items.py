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
    repository_relurl = scrapy.Field()
    repository_name = scrapy.Field()
    # Index of extensions and your amount of lines and bytes.
    index = scrapy.Field()
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

    def update_index(self):
        """
        Creates an index with the total of lines and bytes for each file
          type.
        """
        def index_extensions_recursively(item, index):
            if isinstance(item, TextFileItem) \
                    and 'extension' in item \
                    and 'amount_lines' in item \
                    and 'amount_bytes' in item:
                if item['extension'] in index:
                    index[item['extension']]['amount_lines'] += \
                        item['amount_lines']
                    index[item['extension']]['amount_bytes'] += \
                        item['amount_bytes']
                else:
                    index[item['extension']] = {
                        'amount_lines': item['amount_lines'],
                        'amount_bytes': item['amount_bytes']
                    }
            elif isinstance(item, DirectoryItem):
                if 'children' in item \
                        and type(item['children']) is list:
                    for child in item['children']:
                        index_extensions_recursively(child, index)

        index = {}
        index_extensions_recursively(self, index)
        self['index'] = index


class TextFileItem(FileItem):
    extension = scrapy.Field()
