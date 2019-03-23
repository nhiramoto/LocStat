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


class TextFileItem(FileItem):
    extension = scrapy.Field()
