# -*- coding: utf-8 -*-

import scrapy
from .. import items


class GithubSpider(scrapy.Spider):
    """
    A web scraper that extracts information from public repositories of the
        corresponding pages in Github.
    Each instance of the spider analyzes only one repository
    """
    name = 'github_spider'

    def parse(self, response):
        """
        Check whether the page exists, whether it contains a list of files
            or not and triggers the corresponding method.
        """
        repository_content = response.css('.repository-content')
        if repository_content:
            file_wrap = repository_content.css('.file-wrap')
            if file_wrap:
                self.parse_file_list(response)
            else:
                self.parse_file_content(response)
        else:
            pass

    def parse_file_list(self, response):
        """
        Parses the page containing file list.
        """
        dir_item = items.DirectoryItem()
        # Check if parent directory exists, if so add to list of subfiles
        if 'parent' in response.meta:
            parent = response.meta['parent']
            parent.children.append(dir_item)
        # Check if the page has the current file name,
        #   otherwise it is the root directory of the repository.
        file_name = response.css(
            '.repository-content .breadcrumb .final-path::text').get()
        if file_name is None:
            dir_item.name = ''
            dir_item.is_root = True
            dir_item.repository_name = response.css(
                '.repohead .public [itemprop="name"] a::text').get()
        else:
            dir_item.name = file_name
            dir_item.is_root = False
            dir_item.repository_name = None
        # Creates list of subfiles
        dir_item.children = []

        file_wrap = response.css('.repository-content .file-wrap')
        file_list_a = \
            file_wrap.css('.files .js-navigation-item .content a').getall()
        for a in file_list_a:
            # Creates new request for each file link
            request = response.follow(a, callback=self.parse)
            # Passes the current directory as parent
            request.meta['parent'] = dir_item
            yield request

        yield dir_item

    def parse_file_content(self, response):
        """
        Parses the page that contains the content of a file.
        """
        pass
