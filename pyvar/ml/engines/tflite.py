# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Engine Class

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
"""

import sys

import cv2
import numpy as np
from PIL import Image

try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    sys.exit("No TensorFlow Lite Runtime module found!")

from pyvar.ml.config import CLASSIFICATION
from pyvar.ml.config import DETECTION
from pyvar.ml.utils.timer import Timer
from pyvar.ml.utils.pascal import label_to_color_image

class TFLiteInterpreter:
    """
    Class to handle TensorFlow Lite inference engine.

    :ivar interpreter: storages the TensorFlow Lite interpreter;
    :ivar input_details: storages the input details from model;
    :ivar output_details: storages the output details from inference;
    :ivar result: storages the results from inference;
    :ivar inference_time: storages the inference time;
    :ivar model_file_path: storages the model file path;
    :ivar k: number of top results;
    :ivar confidence: confidence score, default is 0.5.
    """
    def __init__(self, model_file_path=None):
        self.model_file_path = model_file_path
        self.interpreter = Interpreter(model_path=self.model_file_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.result = None
        self.inference_time = None
        self.k = 3
        self.confidence = 0.5
        self.output_image = None

    def set_k(self, k):
        """
        Set the k results attribute.
        """
        self.k = k

    def set_confidence(self, confidence):
        """
        Set the confidence results attribute.
        """
        self.confidence = confidence

    def get_dtype(self):
        """
        Get the model type.

        Returns:
            The model type.
        """
        return self.input_details[0]['dtype']

    def get_height(self):
        """
        Get the model height.

        Returns:
            The model height.
        """
        return self.input_details[0]['shape'][1]

    def get_width(self):
        """
        Get the model width.

        Returns:
            The model witdh.
        """
        return self.input_details[0]['shape'][2]

    def set_input(self, image):
        """
        Set the input tensor to be inferenced.

        Returns:
            None.
        """
        tensor_index = self.input_details[0]['index']
        self.interpreter.set_tensor(tensor_index, image)

    def get_output(self, index, squeeze=False):
        """
        Get the result after running the inference.

        Args:
            index: index of the result
            squeeze: if the result is squeezed or not.

        Returns:
            if **squeeze**, return **squeezed**
            if **not**, return **not squeeze**
        """
        if squeeze:
            return np.squeeze(
                      self.interpreter.get_tensor(
                                       self.output_details[index]['index']))
        return self.interpreter.get_tensor(
                                self.output_details[index]['index'])

    def get_segmentation_result(self, image): # need to check this
        """
        Get the result after running the inference on semantic segmentation.

        Args:
            image: resized image with no expand dimensions;

        Returns:
            None. Storages the output image in the attribute.
        """
        output_details = self.interpreter.get_output_details()[0]
        result =  self.interpreter.tensor(output_details['index'])()[0].astype(np.uint8)

        result = result[:self.get_height(), :self.get_width()]
        mask_img = label_to_color_image(result).astype(np.uint8)
        mask_img = Image.fromarray(mask_img)

        self.output_image = Image.blend(image, mask_img, alpha=0.5)
        self.output_image = cv2.cvtColor(np.array(self.output_image), cv2.COLOR_RGB2BGR)

    def get_result(self, category=None):
        """
        Get the result from the output details.

        Args:
            category (str): type of machine learning model.

        Returns:
            if **success**, return **True**
            if **not**, return **False**
        """
        if category is not None:
            if category is CLASSIFICATION:
                output = self.get_output(0, squeeze=True)
                top_k = output.argsort()[-self.k:][::-1]
                self.result = []
                for i in top_k:
                    score = float(output[i] / 255.0)
                    self.result.append((i, score))
                return True
            elif category is DETECTION:
                positions = self.get_output(0, squeeze=True)
                classes = self.get_output(1, squeeze=True)
                scores = self.get_output(2, squeeze=True)
                self.result = []
                for idx, score in enumerate(scores):
                    if score > self.confidence:
                        self.result.append(
                                    {'pos': positions[idx],
                                     '_id': classes[idx]})
                return True
        else:
            return False

    def get_mnist_result(self):
        """
        Get the MNIST result.

        Returns:
            The digits result.
        """
        self.result = self.interpreter.tensor(
                           self.output_details[0]["index"])()[0]
        return np.argmax(self.result)

    def run_inference(self):
        """
        Run inference on the image/frame set in the set_input() method.
        
        Returns:
            None. The inference time is storage in the inference_time attribute.
        """
        self.interpreter.invoke() # ignores the warm-up time.
        timer = Timer()
        with timer.timeit():
            self.interpreter.invoke()
        self.inference_time = timer.time
