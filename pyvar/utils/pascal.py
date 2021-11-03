# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Pascal Class

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
    .. note:: 10/15/2021 [diego.d] First Version Released
"""

import numpy as np


def create_pascal_label_colormap():
    """
    Creates a label colormap used in PASCAL VOC segmentation benchmark.

    Returns:
    A Colormap for visualizing segmentation results.
    """
    colormap = np.zeros((256, 3), dtype=int)
    indices = np.arange(256, dtype=int)

    for shift in reversed(range(8)):
        for channel in range(3):
            colormap[:, channel] |= ((indices >> channel) & 1) << shift
        indices >>= 3

    return colormap


def label_to_color_image(label):
    """
    Adds color defined by the dataset colormap to the label.
    
    Args:
    label: A 2D array with integer type, storing the segmentation label.
    
    Returns:
    A 2D array with floating type. The element of the array is the color indexed by the corresponding element in the input label to the PASCAL color map.
    
    Raises:
    ValueError: If label is not of rank 2 or its value is larger than color map maximum entry.
    """
    if label.ndim != 2:
        raise ValueError('Expect 2-D input label')
    colormap = create_pascal_label_colormap()
    if np.max(label) >= len(colormap):
        raise ValueError('label value too large.')
    return colormap[label]
