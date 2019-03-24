# -*- coding: utf-8 -*-

from pipelines import output


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
        if spider.repo_name and spider.root_dir_item:
            spider.logger.info(f'The spider finished parsing the '
                               f'"{spider.repo_name}" repository.')
            file_name = spider.repo_name.strip(' /\t\n').replace('/', '-') \
                + '.txt'
            root_dir_item = spider.root_dir_item
            root_dir_item.update_lines_bytes()
            root_dir_item.update_index()
            with output.TxtFileWriter(file_name) as writer:
                writer.write(root_dir_item)
