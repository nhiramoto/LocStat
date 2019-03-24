#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from spiders.github_spider import GithubSpider
from pipelines.input import TxtFileReader


def main():
    try:
        with TxtFileReader('repositories.txt') as reader:
            # Takes the list of URLs from the file
            urls = reader.get_all()
            # Remove urls starting with #
            urls = list(filter(lambda s: not s.startswith('#'), urls))
            print(f'Parsing the repositories: {" ".join(urls)}.')
            process = CrawlerProcess(get_project_settings())
            for url in urls:
                process.crawl(GithubSpider, repo_name=url)
            process.start()
            print('Parse completed.')
    except FileNotFoundError:
        print('File repositories.txt not found.', file=sys.stderr)
    except Exception as e:
        print(f'Error while opening file: {e}', file=sys.stderr)


if __name__ == '__main__':
    main()
