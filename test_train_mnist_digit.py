# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from pyvarml.dataset.mnist import train_mnist_digit
from pyvarml.engines.tflite import run_inference
from pyvarml.utils.convert_images import convert_rgb_to_gray_scale
from pyvarml.utils.convert_images import get_result

'''
The train_mnist_digit() function returns a tuple containing:
position -> [0] = trained model
position -> [1] = test loss
position -> [2] = test accuracy
'''
trained_model = train_mnist_digit()

with open('mnist.tflite', "wb") as model_file:
    model_file.write(trained_model[0])
    model_file.close()

print(f"Test loss: {trained_model[1]}")
print(f"Test accuracy: {trained_model[2]}")

'''
The convert_rgb_to_gray_scale() function returns a converted gray scale image:
'''
input_image = convert_rgb_to_gray_scale("zero.png", 28, 28)

result = run_inference("mnist.tflite", input_image)

predict_digit = get_result(result)

print(f"Predicted Digit: {predict_digit}")
print(f"Confidence: {result[predict_digit]}")

