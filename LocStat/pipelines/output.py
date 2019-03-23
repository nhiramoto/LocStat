# -*- coding: utf-8 -*-


class TxtFileWriterPipeline(object):

    def process_item(self, item, spider):
        return item

    def close_spider(self, spider):
        """
        After closing the spider serializes the structure of the repository on
            file.
        """
        # file_name = spider.repo_name.strip(' /\t\n').replace('/', '-')
        print(f'The spider finished parsing the "{spider.repo_name}"'
              ' repository.')
        root_dir_item = spider.root_dir_item
        print(f'root_dir_item: {root_dir_item}')


class TxtFileWriter:
    """
    Write the repository representation in the file.
    """

    def __init__(self, file_path):
        self.file_path = file_path

    def __enter__(self):
        self.file = open(self.file_path, 'w')
        return self

    def __exit__(self, *args):
        if self.file and not self.file.closed:
            self.file.close()

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        self._file_path = file_path

    def write(self, root_dir_item):
        if self.file and not self.file.closed:
            pass
