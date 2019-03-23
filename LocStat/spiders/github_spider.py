# -*- coding: utf-8 -*-

import re
import scrapy
from .. import items


class GithubSpider(scrapy.Spider):
    """
    A web scraper that extracts information from public repositories of the
        corresponding pages in Github.
    Each instance of the spider analyzes only one repository
    """
    name = 'github_spider'
    start_urls = ['https://github.com/nhtoshiaki/LocStat']

    def parse(self, response):
        """
        Check whether the page exists, whether it contains a list of files
            or not and triggers the corresponding method.
        """
        repository_content = response.css('.repository-content')
        if repository_content:
            self.logger.info(f'{response.url} is a repository page!')
            file_wrap = repository_content.css('.file-wrap')
            if file_wrap:
                self.logger.info(f'{response.url} contains list of files.')
                results = self.parse_file_list(response)
                if results is not None:
                    yield from results
            else:
                self.logger.info(f'{response.url} is the content of a file.')
                results = self.parse_file_content(response)
                if results is not None:
                    yield from results

    def parse_file_list(self, response):
        """
        Parses the page containing file list.
        """
        # Create a directory item
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
            dir_item['name'] = ''
            dir_item['is_root'] = True
            dir_item['repository_name'] = response.css(
                '.repohead .public [itemprop="name"] a::text').get()
        else:
            dir_item['name'] = file_name
            dir_item['is_root'] = False
            dir_item['repository_name'] = None
        # Creates list of subfiles
        dir_item['children'] = []

        file_wrap = response.css('.repository-content .file-wrap')
        file_list_href =\
            file_wrap.css('.files .js-navigation-item .content a::attr(href)')\
            .getall()
        for href in file_list_href:
            # Build the absolute url
            next_page = response.urljoin(href)
            # Creates new request for each file link
            request = scrapy.Request(next_page, callback=self.parse)
            # Passes the current directory as parent
            request.meta['parent'] = dir_item
            yield request

        # Only returns the root directory
        if dir_item['is_root']:
            yield dir_item
        else:
            return None

    def parse_file_content(self, response):
        """
        Parses the page that contains the content of a file.
        """
        repository_content = response.css('.repository-content')
        # Takes the file name of the current page
        file_name = \
            repository_content.css('.breadcrumb .final-path::text') \
            .get().strip(' \t\n')
        # Check if the file_name has letters before and after the dot
        if re.fullmatch(r'\w+\.\w+', file_name):
            # If so then extract the file extension
            ext_match = re.match(r'\w+\.(\w+)', file_name)
            extension = ext_match.group(1)
        else:
            # Otherwise, use empty string
            extension = ''
        # Takes the amount of lines and bytes in the file header
        file_info = \
            repository_content.css('.Box .Box-header .text-mono::text') \
            .getall()
        # Extracts the first integer number from each string in the list
        file_info = list(map(
            lambda field: int(re.findall(r'(\d+)', field)[0]),
            file_info))

        # Create a file item
        text_file_item = items.TextFileItem()
        text_file_item['name'] = file_name
        text_file_item['amount_lines'] = file_info[0]
        text_file_item['amount_bytes'] = file_info[1]
        text_file_item['extension'] = extension
        # Check if parent directory exists, if so add to list of subfiles
        if 'parent' in response.meta:
            parent = response.meta['parent']
            parent['children'].append(text_file_item)
        return None
