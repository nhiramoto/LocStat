# -*- coding: utf-8 -*-
# vim: syntax=python :

# Model dos itens recuperados pelos Spiders

import scrapy


class LocstatItem(scrapy.Item):
    pass


class FileItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    size_bytes = scrapy.Field()


class DirectoryItem(FileItem):
    pass


class TextFileItem(FileItem):
    pass


class BinaryFileItem(FileItem):
    pass
