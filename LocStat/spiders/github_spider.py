# -*- coding: utf-8 -*-

import scrapy


class GithubSpider(scrapy.Spider):
    """
    A web scraper that extracts information from Github pages.
    """
    name = 'github_spider'
    allowed_domains = ['github.com']

    def parse(self, response):
        pass
