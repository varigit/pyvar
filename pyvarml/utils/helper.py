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

from pyvarml.utils.config import FONT, INF_TIME_MSG

class Label:
    """
    Python Class to read the labels file.

    :ivar labels_file: variable to storage the labels file path;
    :ivar list: variable to storage the read labels;
    """
    def __init__(self, labels_file_path):
        self.labels_file = labels_file_path
        self.list = []
        self.read_labels()

    def read_labels(self):
        """
        Method to read the labels file and save it as a list.
        """
        with open(self.labels_file, 'r') as f:
            self.list = [line.strip() for line in f.readlines()]
            f.close()

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
        self.inference_time_info = True
        self.scores_info = True
        self.extra_info = True

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

    def put_info(self, image=None, top_result=None, labels=None,
                       inference_time=None, model_name=None, source_file=None):
        """
        Include information on image/frame: inference time, scores, model name,
        and source file.

        Args:
            image (numpy array): original image to overlay the information.
            top_result (list): top results from the inference.
            labels (list): list of the read labels.
            inference_time (str): inference time from TFLiteInterpreter class.
            model_name (str): the model name.
            source_file (str): the source file name.

        Returns:
            The imagen (numpy array) with the overlayed information.
        """
        if self.scores_info:
            for idx, (i, score) in enumerate (top_result):
                label_position = (3, 35 * idx + 60)
                inference_position = (3, 20)
                cv2.putText(
                    image,
                    f"{labels[i]} - {score:0.4f}",
                    label_position,
                    FONT['hershey'],
                    FONT['size'],
                    FONT['color']['black'],
                    FONT['thickness'] + 2)
                cv2.putText(
                    image,
                    f"{labels[i]} - {score:0.4f}",
                    label_position,
                    FONT['hershey'],
                    FONT['size'],
                    FONT['color']['blue'],
                    FONT['thickness'])

        if self.inference_time_info:
            cv2.putText(
                image, f"{INF_TIME_MSG}: {inference_time}", inference_position,
                FONT['hershey'], 0.5, FONT['color']['black'], 2, cv2.LINE_AA)
            cv2.putText(
                image, f"{INF_TIME_MSG}: {inference_time}", inference_position,
                FONT['hershey'], 0.5, FONT['color']['white'], 1, cv2.LINE_AA)

        if self.extra_info:
            y_offset = image.shape[0] - cv2.getTextSize(
                                            source_file, FONT['hershey'],
                                            0.5, 2)[0][1]
            cv2.putText(
                image, f"source: {source_file}", (3, y_offset), FONT['hershey'],
                0.5, FONT['color']['black'], 2, cv2.LINE_AA)
            cv2.putText(
                image, f"source: {source_file}", (3, y_offset), FONT['hershey'],
                0.5, FONT['color']['white'], 1, cv2.LINE_AA)
            y_offset -= (cv2.getTextSize(
                             model_name, FONT['hershey'], 0.5, 2)[0][1] + 3)
            cv2.putText(
                image, f"model: {model_name}", (3, y_offset), FONT['hershey'],
                0.5, FONT['color']['black'], 2, cv2.LINE_AA)
            cv2.putText(
                image, f"model: {model_name}", (3, y_offset), FONT['hershey'],
                0.5, FONT['color']['white'], 1, cv2.LINE_AA)
        return image
