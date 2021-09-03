#!/usr/bin/env python3
# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import argparse
import sys

from pyvarml.engines.tflite import TFLiteInterpreter
from pyvarml.utils.helper import Image

parser = argparse.ArgumentParser()

parser.add_argument('--model', help='.tflite model to be executed')          
parser.add_argument('--image', help='image file to be classified')          

args = vars(parser.parse_args())

if args['model'] is None:
    sys.exit("Please, specify the model path")
if args['image'] is None:
    sys.exit("Please, specify the image path")

image_test = Image(args['image'])
image_test.convert_rgb_to_gray_scale(28, 28)

example = TFLiteInterpreter(args['model'])

example.start()
example.set_image(image_test.converted)
example.run_inference()

predict_digit = example.get_mnist_result()
print(f"Predicted Digit: {predict_digit}")
print(f"Confidence: {example.result[predict_digit]}")
print(f"Inference time: {example.inference_time}")
