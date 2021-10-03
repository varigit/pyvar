# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Engines Classes

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
    .. note:: 10/15/2021 [diego.d] First Version Released
"""

import sys

import numpy as np

try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    sys.exit("No TensorFlow Lite Runtime module found!")

from pyvarml.utils.timer import Timer

class TFLiteInterpreter:
    """
    Python Class to handle TensorFlow Lite inference engine.

    :ivar interpreter: variable to storage the TensorFlow Lite interpreter;
    :ivar input_details: variable to storage the input details from model;
    :ivar output_details: variable to storage the output details from inference;
    :ivar result: variable to storage the results from inference;
    :ivar inference_time: variable to storage the inference time;
    :ivar model_file_path: variable to storage the model file path.
    """
    def __init__(self, model_file_path=None):
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.result = None
        self.inference_time = None
        self.model_file_path = model_file_path
        self.start()

    def start(self):
        """
        Method to start the TensorFlow lite engine.
        """
        self.interpreter = Interpreter(model_path=self.model_file_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

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

    def set_image(self, image):
        """
        Set the image to be inferenced.
        """
        self.interpreter.set_tensor(self.input_details[0]['index'], image)

    def get_result(self, index, squeeze=False):
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

    def get_classification_result(self, k=3):
        """
        Get the result after running the classification inference.

        Args:
            k (int): number of top results.

        Returns:
            None. The result is storage in the result attribute.
        """
        output_details = self.interpreter.get_output_details()[0]
        output = np.squeeze(self.interpreter.get_tensor(output_details['index']))

        top_k = output.argsort()[-k:][::-1]
        self.result = []
        for i in top_k:
            score = float(output[i] / 255.0)
            self.result.append((i, score))

    def get_detection_result(self, confidence=0.5):
        """
        Get the result after running the detection inference.
        
        Args:
            confidence (float): score confidence, 0.5 is the default one.

        Returns:
            None. The result is storage in the result attribute.
        """
        positions = self.get_result(0, squeeze=True)
        classes = self.get_result(1, squeeze=True)
        scores = self.get_result(2, squeeze=True)

        self.result = []
        for idx, score in enumerate(scores):
            if score > confidence:
                self.result.append({'pos': positions[idx], '_id': classes[idx]})

    def get_mnist_result(self):
        """
        Get the MNIST result.

        Returns:
            The digits result.
        """
        self.result = self.interpreter.tensor(
                         self.interpreter.get_output_details()[0]["index"])()[0]
        return np.argmax(self.result)

    def run_inference(self):
        """
        Run the inference on the image/frame set in the set_image() method.
        
        Returns:
            None. The inference time is storage in the inference_time attribute.
        """
        self.interpreter.invoke()
        timer = Timer()
        with timer.timeit():
            self.interpreter.invoke()
        self.inference_time = timer.time
