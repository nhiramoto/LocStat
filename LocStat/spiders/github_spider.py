# -*- coding: utf-8 -*-

import re
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import TimeoutError, TCPTimedOutError

from .. import items
from ..utils.url import Url


class GithubSpider(scrapy.Spider):
    """
    A web scraper that extracts information from public repositories of the
        corresponding pages in Github.
    To prevent confusion between pages, each instance of the spider analyzes
        only one repository.
    """
    name = 'github_spider'

    def __init__(self, repo_name=None, *args, **kwargs):
        """
        GithubSpider receives the repository name in the user/repository format
            in the constructor.
        """
        super(GithubSpider, self).__init__(*args, **kwargs)
        self.root_dir_item = {}
        repo_name = 'nhtoshiaki/LocStat'
        if repo_name is not None:
            self.repo_name = repo_name
            self.url = Url.github_url(repo_name)
        else:
            self.logger.critical('No repository set, make sure the repository'
                                 'is set before running the spider.')

    def start_requests(self):
        if self.url is not None:
            yield scrapy.Request(url=self.url, callback=self.parse,
                                 errback=self.errback)

    @property
    def root_dir_item(self):
        return self._root_dir_item

    @root_dir_item.setter
    def root_dir_item(self, root_dir_item):
        self._root_dir_item = root_dir_item

    @property
    def repo_name(self):
        return self._repo_name

    @repo_name.setter
    def repo_name(self, repo_name):
        if repo_name is not None:
            self._repo_name = repo_name
            self.url = Url.github_url(repo_name)

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url

    def errback(self, failure):
        if failure.check(HttpError):
            url = failure.value.response.url
            status = failure.value.response.status
            if status == 404:
                self.logger.error(f'Page "{url}" not found.')
        elif failure.check(TimeoutError, TCPTimedOutError):
            url = failure.request.url
            self.logger.error(f'Connection error on {url}, make sure the '
                              'address is reachable.')

    def parse(self, response):
        """
        Check whether the page exists, whether it contains a list of files
            or not and triggers the corresponding parse method.
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
            parent['children'].append(dir_item)
        # Check if the page has the current file name,
        #   otherwise it is the root directory of the repository.
        file_name = response.css(
            '.repository-content .breadcrumb .final-path::text').get()
        if file_name is None:
            dir_item['name'] = ''
            dir_item['is_root'] = True
            dir_item['repository_relurl'] = self.repo_name
            dir_item['repository_name'] = self.repo_name.split('/')[1]
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
            self.root_dir_item = dir_item
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
