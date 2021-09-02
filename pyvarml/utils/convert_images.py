# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import cv2
import numpy as np

def convert_rgb_to_gray_scale(image_path, height, width):
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (28, 28), interpolation = cv2.INTER_LINEAR)
    img = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, 0)
    return img
    
def get_result(result):
    return np.argmax(result)
