# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Class to handle TensorFlow Lite inference engine.

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
"""

import os
import sys

import numpy as np

try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    sys.exit("No TensorFlow Lite Runtime module found!")

from pyvar.ml.config import CLASSIFICATION
from pyvar.ml.config import DETECTION
from pyvar.ml.utils.timer import Timer

class TFLiteInterpreter:
    """
    :ivar interpreter: TensorFlow Lite interpreter;
    :ivar input_details: input details from model;
    :ivar output_details: output details from inference;
    :ivar result: results from inference;
    :ivar inference_time: inference time;
    :ivar model_file_path: path to the machine learning model;
    :ivar k: number of top results;
    :ivar confidence: confidence score, default is 0.5.
    """
    def __init__(self, model_file_path=None):
        """
        Constructor method for the TensorFlow Lite class.
        """
        if not os.path.isfile(model_file_path):
            raise ValueError("Must pass a labels file")
        if not model_file_path.endswith(".tflite"):
            raise TypeError(f"Expects {model_file_path} to be a text file")
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
        Set the image/frame into the input tensor to be inferenced.
        """
        tensor_index = self.input_details[0]['index']
        self.interpreter.set_tensor(tensor_index, image)

    def get_output(self, index, squeeze=False):
        """
        Get the result after running the inference.

        Args:
            index (int): index of the result
            squeeze (bool): result is squeezed or not.

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

    def get_result(self, category=None):
        """
        Get the result from the output details.

        Args:
            category (str): model category (classification or detection);

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

    def run_inference(self):
        """
        Runs inference on the image/frame set in the set_input() method.
        """
        self.interpreter.invoke() # ignores the warm-up time.
        timer = Timer()
        with timer.timeit():
            self.interpreter.invoke()
        self.inference_time = timer.time
