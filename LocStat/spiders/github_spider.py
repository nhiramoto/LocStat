# -*- coding: utf-8 -*-
# vim: syntax=python :

# Crawler para extrair informações do Github

import scrapy

class GithubSpider(scrapy.Spider):
    name = 'github_spider'
