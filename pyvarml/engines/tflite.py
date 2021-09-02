# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from tflite_runtime.interpreter import Interpreter

#from pyvarml.utils.timer import Timer

def run_inference(model_file_path, input_image):
    interpreter = Interpreter(model_path=model_file_path)
    interpreter.allocate_tensors()
    interpreter.set_tensor(interpreter.get_input_details()[0]["index"], input_image)
    interpreter.invoke()
    result = interpreter.tensor(interpreter.get_output_details()[0]["index"])()[0]
    return result
