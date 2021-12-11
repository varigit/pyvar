# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Class to handle labels file from Machine Learning models.

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
"""

import os
import re

from pyvar.ml.config import CLASSIFICATION
from pyvar.ml.config import DETECTION


class Label:
    """
    :ivar labels_file: path to the labels file.
    :ivar list: list with the labels from the label file.
    """
    def __init__(self, labels_file_path=None):
        """
        Constructor method for the Label class.
        """
        if not os.path.isfile(labels_file_path):
            raise ValueError("Must pass a labels file")
        if not labels_file_path.endswith(".txt"):
            raise TypeError(f"Expects {labels_file_path} to be a text file")
        self.labels_file = labels_file_path
        self.list = []

    def read_labels(self, category=None):
        """
        Reads Machine Learning labels file and save the result as a list.

        Args:
            category (str): model category (classification or detection).

        Returns:
            True if the labels file was read successfully.
        """
        if category is None:
            raise TypeError("Must specify the category")
        else:
            with open(self.labels_file, 'r', encoding='utf-8') as f:
                if category is CLASSIFICATION:
                    self.list = [line.strip() for line in f.readlines()]
                elif category is DETECTION:
                    p = re.compile(r'\s*(\d+)(.+)')
                    lines = (p.match(line).groups() for line in f.readlines())
                    self.list = {int(num): text.strip() for num, text in lines}
                f.close()
        return True
