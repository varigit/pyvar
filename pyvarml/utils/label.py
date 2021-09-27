# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Label Class

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
    .. note:: 10/15/2021 [diego.d] First Version Released
"""

import re

class Label:
    """
    Python Class to read the labels file.

    :ivar labels_file: variable to storage the labels file path;
    :ivar list: variable to storage the read labels;
    """
    def __init__(self, labels_file_path, category=None):
        self.labels_file = labels_file_path
        self.category = category
        self.list = []
        self.read_labels()

    def read_labels(self):
        """
        Method to read the labels file and save it as a list.
        """
        if self.category is "classification":
            with open(self.labels_file, 'r') as f:
                self.list = [line.strip() for line in f.readlines()]
                f.close()
        elif self.category is "detection":
            p = re.compile(r'\s*(\d+)(.+)')
            with open(self.labels_file, 'r', encoding='utf-8') as f:
                lines = (p.match(line).groups() for line in f.readlines())
                self.list =  {int(num): text.strip() for num, text in lines}
                f.close()
