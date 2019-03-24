# -*- coding: utf-8 -*-

import items


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

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, file):
        self._file = file

    @property
    def closed(self):
        if self.file:
            return self.file.closed
        else:
            return True

    def write(self, root_dir_item):
        if self.file and not self.file.closed:
            self.file.write(f'Repositório: '
                            f'{root_dir_item["repository_relurl"]}\n')
            self.file.write(f'Total de linhas: '
                            f'{root_dir_item["amount_lines"]}\n')
            self.file.write(f'Total de bytes: '
                            f'{root_dir_item["amount_bytes"]}\n')
            self.file.write('\n')
            self.write_extension_statistic(root_dir_item)
            self.file.write('\n')
            self.write_tree_structure(root_dir_item)

    def write_extension_statistic(self, root_dir_item):
        """
        Writes the table with the number of lines and bytes for each file
          extension.
        """
        if self.file and not self.file.closed:
            self.file.write(f'{"Extensão":<10} | {"Linhas":^15} | '
                            f'{"Bytes":^15}\n')
            self.file.write(f'{"":=<11}|{"":=^17}|{"":=^16}\n')
            if 'index' in root_dir_item:
                for ext, info in root_dir_item['index'].items():
                    if len(ext) == 0:
                        ext = '<outros>'
                    amount_lines, amount_bytes = 0, 0
                    perc_lines, perc_bytes = 0, 0
                    if 'amount_lines' in info:
                        amount_lines = info['amount_lines']
                    if 'amount_bytes' in info:
                        amount_bytes = info['amount_bytes']
                    if 'amount_lines' in root_dir_item and \
                            root_dir_item['amount_lines'] != 0:
                        perc_lines = int(100 * amount_lines
                                         / root_dir_item['amount_lines'])
                    if 'amount_bytes' in root_dir_item and \
                            root_dir_item['amount_bytes'] != 0:
                        perc_bytes = int(100 * amount_bytes
                                         / root_dir_item['amount_bytes'])
                    self.file.write(f'{ext:<10} | {amount_lines:>7} '
                                    f'({perc_lines:>3} %) | '
                                    f'{amount_bytes:>6} '
                                    f'({perc_bytes:>3} %)\n')

    def write_tree_structure(self, root_dir_item):
        """
        Writes the repository file structure.
        """
        def _tree_structure(file_item, depth):
            """
            Recursive function to create the file structure.
            """
            structure = ''
            for i in range(depth - 1):
                structure += '|   '
            structure += '|-- '
            if 'name' in file_item:
                if isinstance(file_item, items.DirectoryItem):
                    structure += f'[{file_item["name"]}]\n'
                    if 'children' in file_item \
                            and type(file_item['children']) is list:
                        for child in file_item['children']:
                            structure += \
                                _tree_structure(child, depth + 1)
                elif isinstance(file_item, items.TextFileItem):
                    structure += f'{file_item["name"]}'
                    if 'amount_lines' in file_item:
                        structure += f' ({file_item["amount_lines"]} linhas)'
                    structure += '\n'
            return structure

        if self.file and not self.file.closed:
            structure = ''
            if 'repository_name' in root_dir_item:
                structure += f'[{root_dir_item["repository_name"]}]\n'
            if 'children' in root_dir_item and type(root_dir_item['children'])\
                    is list:
                for child in root_dir_item['children']:
                    structure += _tree_structure(child, 1)
            self.file.write(structure)
