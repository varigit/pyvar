# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Class to  manipulate images/frames.

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
    .. note:: 10/15/2021 [diego.d] First Version Released
"""

import sys

import cv2
import numpy as np

class Image:
    def __init__(self, image_file=None):
        if image_file is None:
            sys.exit("No image specified!")
        else:
            self.image = image_file    
        self.converted = None     

    def convert_rgb_to_gray_scale(self, width=None, height=None, expand_dims=True):
        """
        Convert RGB images/frames to gray scale.

        Args:
            width (int): image width
            height (int): image height
            expand_dims (bool): expand dimensions

        The gray scale image/frame is storage in the **converted** attribute.
        """
        if width is None:
            sys.exit("Please specify width!")
        if height is None:
            sys.exit("Please specify height!")
        img = cv2.imread(self.image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (width, height), interpolation = cv2.INTER_LINEAR)
        self.converted = np.expand_dims(np.array(
                            img, dtype=np.float32) / 255.0, 0) if expand_dims else img
