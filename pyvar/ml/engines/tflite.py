# Copyright 2021-2023 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
Module: TFLiteInterpreter
Platform: Unix/Yocto
Synopsis: This module provides a class, TFLiteInterpreter, to manage and
facilitate the usage of TensorFlow Lite inference engine. It encompasses
functions for model loading, data preparation, inference running, and result
interpretation. Additionally, it also handles various model types and offers
multi-threading support for better performance.

Usage:
from pyvar.ml.engines.tflite import TFLiteInterpreter

# Initialize interpreter with model and other settings
interpreter = TFLiteInterpreter(model_path, num_threads, ext_delegate)

# Setup input and run inference
interpreter.set_input(input_image)
interpreter.run_inference()

# Retrieve results
results = interpreter.get_result(category)

Author: Diego Dorta <diego.d@variscite.com>
Copyright: 2021-2023 Variscite LTD
License: BSD-3-Clause
"""

import os
import sys
from multiprocessing import cpu_count
from typing import Optional, List

import numpy as np

try:
    from tflite_runtime.interpreter import Interpreter
    from tflite_runtime.interpreter import load_delegate
except ImportError:
    sys.exit("No TensorFlow Lite Runtime module found!")

from pyvar.ml.config import CLASSIFICATION
from pyvar.ml.config import DETECTION
from pyvar.ml.utils.timer import Timer

# Constants
EXT_DELEGATE_PATH = "/usr/lib/libvx_delegate.so"
DEFAULT_CONFIDENCE = 0.5
DEFAULT_K = 3


class TFLiteInterpreter:
    """
    Class to handle TensorFlow Lite inference engine.

    :param model_file_path: Path to the machine learning model.
    :param num_threads: Number of threads.
    :param ext_delegate: External delegate.
    """
    def __init__(self, model_file_path: Optional[str] = None,
                 num_threads: int = 1,
                 ext_delegate: Optional[List] = None,
                 ext_delegate_path: str = EXT_DELEGATE_PATH):

        if not os.path.isfile(model_file_path):
            raise ValueError("Must pass a valid model file path.")

        if not model_file_path.endswith(".tflite"):
            raise TypeError(f"Expects {model_file_path} to be a '.tflite' file.")

        if not isinstance(num_threads, int) or num_threads < 1:
            raise ValueError("num_threads must be an integer greater than 0.")

        if num_threads > cpu_count():
            raise ValueError(f"num_threads can't be greater than {cpu_count()}.")

        ext_delegate_options = {}
        if ext_delegate is None:
            ext_delegate = [load_delegate(ext_delegate_path, ext_delegate_options)]

        self.model_file_path = model_file_path
        self.interpreter = Interpreter(model_path=self.model_file_path,
                                       experimental_delegates=ext_delegate,
                                       num_threads=num_threads)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.interpreter.invoke()
        self.result = None
        self.inference_time = None
        self.k = DEFAULT_K
        self.confidence = DEFAULT_CONFIDENCE
        self.output_image = None

    def set_k(self, k: int) -> None:
        """
        Set the number of top results to be obtained.

        :param k: Number of top results.
        :raises ValueError: If k is less than 1.
        """
        if k < 1:
            raise ValueError("k must be at least 1.")
        self.k = k

    def set_confidence(self, confidence: float) -> None:
        """
        Set the confidence threshold for results.

        :param confidence: Confidence threshold.
        :raises ValueError: If confidence is not between 0 and 1.
        """
        if not 0 <= confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1.")
        self.confidence = confidence

    def get_dtype(self) -> np.dtype:
        """
        Get the data type of the model input.

        :return: Data type of the model input.
        """
        return self.input_details[0]['dtype']

    def get_height(self) -> int:
        """
        Get the height of the model input.

        :return: Height of the model input.
        :raises IndexError: If input shape does not have at least two dimensions.
        """
        if len(self.input_details[0]['shape']) < 2:
            raise IndexError("Input shape does not have at least two dimensions.")
        return self.input_details[0]['shape'][1]

    def get_width(self) -> int:
        """
        Get the width of the model input.

        :return: Width of the model input.
        :raises IndexError: If input shape does not have at least three dimensions.
        """
        if len(self.input_details[0]['shape']) < 3:
            raise IndexError("Input shape does not have at least three dimensions.")
        return self.input_details[0]['shape'][2]

    def set_input(self, image: np.ndarray) -> None:
        """
        Set the image/frame into the input tensor to be inferred.

        :param image: Image to be inferred.
        :raises TypeError: If image is not an ndarray.
        """
        if not isinstance(image, np.ndarray):
            raise TypeError("Image must be a numpy ndarray.")
        tensor_index = self.input_details[0]['index']
        self.interpreter.set_tensor(tensor_index, image)

    def get_output(self, index: int, squeeze: bool = False) -> np.ndarray:
        """
        Get the result after running the inference.

        :param index: Index of the result.
        :param squeeze: Determines if the result should be squeezed or not.
        :return: Result tensor. If 'squeeze' is True, dimensions of size 1 are removed.
        :raises IndexError: If the provided index is out of range.
        """
        if index >= len(self.output_details):
            raise IndexError("Index out of range in output_details")

        tensor = self.interpreter.get_tensor(self.output_details[index]['index'])

        if squeeze:
            return np.squeeze(tensor)
        return tensor

    def _get_classification_result(self):
        """
        Classifies the results based on the model output.
        Updates the result attribute with tuples of class indices and their corresponding scores.
        """
        output = self.get_output(0, squeeze=True)
        top_k = output.argsort()[-self.k:][::-1]
        self.result = [(i, float(output[i] / 255.0)) for i in top_k]

    def _get_detection_result(self):
        """
        Detects the classes based on the model output.
        Updates the result attribute with dictionaries containing class indices and their positions.
        """
        positions = self.get_output(0, squeeze=True)
        classes = self.get_output(1, squeeze=True)
        scores = self.get_output(2, squeeze=True)
        self.result = [{'pos': positions[idx], '_id': classes[idx]} for idx, score in enumerate(scores) if score > self.confidence]

    def get_result(self, category: Optional[str] = None) -> None:
        """
        Get the result from the output details.

        :param category: Model category (classification or detection).
        :raises ValueError: If category is None or unsupported.
        """
        if category is None:
            raise ValueError("Category must not be None.")

        if category == CLASSIFICATION:
            self._get_classification_result()
        elif category == DETECTION:
            self._get_detection_result()
        else:
            raise ValueError(f"Unsupported category: {category}")

    def run_inference(self) -> None:
        """
        Runs inference on the image/frame set in the set_input() method and sets the inference time.

        :raises RuntimeError: If no input has been set before invoking this method.
        """
        if not self.interpreter.get_input_details():
            raise RuntimeError("No input set. Please call set_input() before run_inference().")

        timer = Timer()
        with timer.timeit():
            self.interpreter.invoke()

        self.inference_time = timer.time
