# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Class to handle TensorFlow Lite inference engine.

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
    .. note:: 10/15/2021 [diego.d] First Version Released
"""

import numpy as np

try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    sys.exit("No TensorFlow Lite Runtime module found!")

from pyvarml.utils.timer import Timer

class TFLiteInterpreter:
    """
    **Constructor**

    Specify the TensorFlow Lite model, otherwise it fails.
    """
    def __init__(self, model_file_path=None):
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.result = None
        self.inference_time = None

        if model_file_path is None:
            sys.exit("No model file specified!")
        else:
            self.model_file_path = model_file_path

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

    # merge two methods below
    def get_result(self, index, squeeze=False):
        """
        Get the result after running the inference.

        Args:
            index: index of the result
            squeeze: if the result is squeeze or not.

        Returns:
            if **squeeze**, return **squeeze**
            if **not**, return **not squeeze**
        """
        if squeeze:
            return np.squeeze(self.interpreter.get_tensor(self.output_details[index]['index']))
        return self.interpreter.get_tensor(self.output_details[index]['index'])

    def get_mnist_result(self):
        """
        Get the MNIST result.

        Returns:
            The digits result.
        """
        self.result = self.interpreter.tensor(self.interpreter.get_output_details()[0]["index"])()[0]
        return np.argmax(self.result)

    def run_inference(self):
        """
        Run the inference on the image/frame set in the set_image() method.
        """
        timer = Timer()
        with timer.timeit():
            self.interpreter.invoke()
        self.inference_time = timer.time

def run_inference(model_file_path, input_image):
    """
    Run the inference quickly.

    Args:
        model_file_path: path to the TensorFlow Lite.
        input_image: path to the image/frame to the inferenced.

    Returns:
        The result of the inference.
    """
    interpreter = Interpreter(model_path=model_file_path)
    interpreter.allocate_tensors()
    interpreter.set_tensor(interpreter.get_input_details()[0]["index"], input_image)
    interpreter.invoke()
    result = interpreter.tensor(interpreter.get_output_details()[0]["index"])()[0]
    return result
