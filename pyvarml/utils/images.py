# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Utils Classes

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
    .. note:: 10/15/2021 [diego.d] First Version Released
"""

import cv2
import numpy as np

from PIL import Image

class Images:
    """
    Python Class to manipulate images (resize, convert, and more).

    :ivar image: variable to storage the original image;
    :ivar converted: variable to storage the converted image;
    :ivar resized: variable to storage the resized image;
    :ivar inference_time_info: enables inference time overlay;
    :ivar scores_info: enables scores overlay;
    :ivar extra_info: enables extra info overlay.
    """
    def __init__(self, image_file=None):
        self.image = image_file
        self.converted = None
        self.resized = None

    def show(self, title=None, image=None):
        """
        Method to show image.

        Args:
            title (str): title of the image;
            image (numpy array): set the image to be showed.
        """
        cv2.imshow(title, image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def save(self, name=None, image=None):
        """
        Method to save image.

        Args:
            name (str): name of the output image;
            image (numpy array): set the image to be saved.
        """
        cv2.imwrite(name, image)

    def resize(self, width=None, height=None,
                     engine_input_details=None, expand_dims=True):
        """
        Method to resize images using Pillow.

        Args:
            width (int): set the new image width to be resized;
            height (int): set the new image height to be resized;
            engine_input_details (list): model input details from TensorFlow.
            expand_dims (bool): expand dimensions.

        Note:
             **engine_input_details**: Use this in case the image model size is unkown.

             **expand_dims**: insert a new axis in the shape of the array, for example: (50, 50) -> (1, 50, 50)

        Returns:
            None. The gray scale image is storage in the **converted** attribute.
        """
        if engine_input_details is not None:
            _, height, width, _ = engine_input_details[0]['shape']
        with Image.open(self.image) as im:
            image = np.array(im)
            image = image[:, :, ::-1].copy()
            self.resized = im.resize((width, height))
            self.resized = np.expand_dims(
                              self.resized,
                              axis = 0) if expand_dims else self.resized
            self.image_original = image

    def convert_rgb_to_gray_scale(self, width=None, height=None,
                                        expand_dims=True):
        """
        Convert RGB images/frames to gray scale.

        Args:
            width (int): image width
            height (int): image height
            expand_dims (bool): expand dimensions

        The gray scale image/frame is storage in the **converted** attribute.
        """
        image = cv2.imread(self.image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image = cv2.resize(
                    image, (width, height), interpolation = cv2.INTER_LINEAR)
        self.converted = np.expand_dims(
                            np.array(
                            image,
                            dtype=np.float32) / 255.0,
                            0) if expand_dims else image



