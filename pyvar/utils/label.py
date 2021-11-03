# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Label Class

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
    .. note:: 10/15/2021 [diego.d] First Version Released
"""

import re

CLASSIFICATION = "classification"
DETECTION = "detection"

class Label:
    """
    Python Class to read the labels file from Machine Learning models.

    :ivar labels_file: storages the path of the labels model file.
    :ivar list: storages the read labels from the model file.
    """
    def __init__(self, labels_file_path=None):
        self.labels_file = labels_file_path
        self.list = []

    def read_labels(self, category=None):
        """
        Method to read the labels file and save the result in list attribute.

        Args:
            category (str): storages the model category.

        Note:
             **category**: choose between classification or detection.

        Returns:
            If **success** returns **True**, if **not** returns **False**.
        """
        if self.labels_file is None:
            return False
        if category is None:
            return False
        else:
            with open(self.labels_file, 'r', encoding='utf-8') as f:
                if category is CLASSIFICATION:
                    self.list = [line.strip() for line in f.readlines()]
                elif category is DETECTION:
                    p = re.compile(r'\s*(\d+)(.+)')
                    lines = (p.match(line).groups() for line in f.readlines())
                    self.list =  {int(num): text.strip() for num, text in lines}
                f.close()
        return True
