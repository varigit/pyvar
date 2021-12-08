# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Class to handle overlay on single images and frames.

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
"""

import colorsys
import random

import cv2
import numpy as np

from pyvar.ml.config import CLASSIFICATION
from pyvar.ml.config import DETECTION
from pyvar.ml.utils.config import FONT, INF_TIME_MSG, FPS_MSG

class Overlay:
    """
    :ivar inference_time_info: shows the inference time on image/frame;
    :ivar scores_info: shows the scores information on image/frame;
    :ivar extra_info: shows extra info on image/frame;
    :ivar framerate_info: shows framerate on image/frame.
    """
    def __init__(self):
        """
        Constructor method for the Label class.
        """
        self.inference_time_info = True
        self.scores_info = True
        self.extra_info = True
        self.framerate_info = False

    @staticmethod
    def generate_colors(labels):
        hsv_tuples = [(x / len(labels), 1., 1.) for x in range(len(labels))]
        colors = list(
                     map(
                         lambda x: colorsys.hsv_to_rgb(*x), hsv_tuples))
        colors = list(
                     map(
                         lambda x:
                            (int(x[0] * 255),
                             int(x[1] * 255),
                             int(x[2] * 255)), colors))
        random.seed(10101)
        random.shuffle(colors)
        random.seed(None)
        return colors


    def info(
        self, category=None, image=None, top_result=None, labels=None,
        inference_time=None, model_name=None, source_file=None, fps=None):
        """
        Draw information on single images and frames such as inference time,
        scores, model name, and source file.

        Args:
            image (numpy array): original image to overlay the information.
            top_result (list): top results from the inference.
            labels (list): list of the read labels.
            inference_time (str): inference time from TFLiteInterpreter class.
            model_name (str): the model name.
            source_file (str): the source file name.
            fps (float): fpsit from Framerate class.

        Returns:
            The :obj:`numpy.array` image format with the overlayed information.
        """
        inference_position = (3, 20)
        if self.scores_info:
            if category is CLASSIFICATION:
                for idx, (i, score) in enumerate (top_result):
                    label_position = (3, 35 * idx + 60)
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
            elif category is DETECTION:
                colors = self.generate_colors(labels)
                image_height, image_width, _ = image.shape
                for obj in top_result:
                    pos = obj['pos']
                    _id = obj['_id']

                    x1 = int(pos[1] * image_width)
                    x2 = int(pos[3] * image_width)
                    y1 = int(pos[0] * image_height)
                    y2 = int(pos[2] * image_height)

                    top = max(0, np.floor(y1 + 0.5).astype('int32'))
                    left = max(0, np.floor(x1 + 0.5).astype('int32'))
                    bottom = min(image_height, np.floor(y2 + 0.5).astype('int32'))
                    right = min(image_width, np.floor(x2 + 0.5).astype('int32'))

                    label_size = cv2.getTextSize(
                                     labels[_id], FONT['hershey'],
                                     FONT['size'], FONT['thickness'])[0]

                    label_rect_left = int(left - 3)
                    label_rect_top = int(top - 3)
                    label_rect_right = int(left + 3 + label_size[0])
                    label_rect_bottom = int(top - 5 - label_size[1])

                    cv2.rectangle(
                        image, (left, top), (right, bottom),
                        colors[int(_id) % len(colors)], 6)
                    cv2.rectangle(
                        image, (label_rect_left, label_rect_top),
                        (label_rect_right, label_rect_bottom),
                        colors[int(_id) % len(colors)], -1)
                    cv2.putText(
                        image, labels[_id], (left, int(top - 4)),
                        FONT['hershey'], FONT['size'],
                        FONT['color']['black'], FONT['thickness'])

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

        if self.framerate_info:
            fps_msg = f"{FPS_MSG}: {int(fps)}"
            x_offset = image.shape[1] - (cv2.getTextSize(
                                             fps_msg, FONT['hershey'],
                                             0.8, 2)[0][0] + 10)
            cv2.putText(
                image, fps_msg, (x_offset, 25), FONT['hershey'], 0.8,
                FONT['color']['black'], 2, cv2.LINE_AA)
            cv2.putText(
                image, fps_msg, (x_offset, 25), FONT['hershey'], 0.8,
                FONT['color']['white'], 1, cv2.LINE_AA)
        return image
