# -*- coding: utf-8 -*-

from . import output


class LocStatPipeline(object):
    """
    Defines what to do when an item is collected or
        a spider completes the parsing.
    """

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        """
        After closing the spider serializes the structure of the repository on
            file.
        """
        print(f'The spider finished parsing the "{spider.repo_name}"'
              ' repository.')
        if spider and hasattr(spider, 'repo_name') \
                and hasattr(spider, 'root_dir_item'):
            file_name = spider.repo_name.strip(' /\t\n').replace('/', '-') \
                + '.txt'
            root_dir_item = spider.root_dir_item
            root_dir_item.update_lines_bytes()
            root_dir_item.update_index()
            print(f'root_dir_item: {root_dir_item}')
            with output.TxtFileWriter(file_name) as writer:
                writer.write(root_dir_item)
