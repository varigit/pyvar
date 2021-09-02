# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

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

    def convert_rgb_to_gray_scale(self, width = None, height = None):
        if width is None:
            sys.exit("Please specify width!")
        if height is None:
            sys.exit("Please specify height!")
        img = cv2.imread(self.image)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.resize(img, (width, height), interpolation = cv2.INTER_LINEAR)
        self.converted = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, 0)
