# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from pyvarml.dataset.mnist import train_mnist_fashion
from pyvarml.engines.tflite import run_inference
from pyvarml.utils.convert_images import convert_rgb_to_gray_scale
from pyvarml.utils.convert_images import get_result

trained_model = train_mnist_fashion()

with open('mnist_fashion.tflite', "wb") as model_file:
    model_file.write(trained_model[0])
    model_file.close()

print(f"Test loss: {trained_model[1]}")
print(f"Test accuracy: {trained_model[2]}")

input_image = convert_rgb_to_gray_scale("shirt.png", 28, 28)

result = run_inference("mnist_fashion.tflite", input_image)

predict_flashion = get_result(result)

print(f"Predicted Fashion: {predict_flashion}")
print(f"Confidence: {result[predict_flashion]}")
