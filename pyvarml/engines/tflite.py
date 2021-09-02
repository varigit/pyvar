# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import numpy as np

from tflite_runtime.interpreter import Interpreter

#from pyvarml.utils.timer import Timer

class TFLiteInterpreter:
    def __init__(self, model_file_path=None):
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.result = None

        if model_file_path is None:
            sys.exit("No model file specified!")
        else:
            self.model_file_path = model_file_path

    def start(self):
        self.interpreter = Interpreter(model_path=self.model_file_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def get_dtype(self):
        return self.input_details[0]['dtype']

    def get_height(self):
        return self.input_details[0]['shape'][1]

    def get_width(self):
        return self.input_details[0]['shape'][2]

    def set_image(self, image):
        self.interpreter.set_tensor(self.input_details[0]['index'], image)

    # merge two methods below
    def get_result(self, index, squeeze=False):
        if squeeze:
            return np.squeeze(self.interpreter.get_tensor(self.output_details[index]['index']))
        return self.interpreter.get_tensor(self.output_details[index]['index'])

    def get_mnist_result(self):
        self.result = self.interpreter.tensor(self.interpreter.get_output_details()[0]["index"])()[0]
        return np.argmax(self.result)

    def run_inference(self):
        self.interpreter.invoke()

def run_inference(model_file_path, input_image):
    interpreter = Interpreter(model_path=model_file_path)
    interpreter.allocate_tensors()
    interpreter.set_tensor(interpreter.get_input_details()[0]["index"], input_image)
    interpreter.invoke()
    result = interpreter.tensor(interpreter.get_output_details()[0]["index"])()[0]
    return result
