from pyvar.ml.engines.tflite import TFLiteInterpreter
from pyvar.ml.multimedia.images import Images

image_test = Images("path/to/image") # Change here
image_test.convert_rgb_to_gray_scale(28, 28, True)

foo = TFLiteInterpreter("path/to/model") # Change here

foo.start()
foo.set_input(image_test.converted)
foo.run_inference()

predict_digit = foo.get_mnist_result()

print(f"Predicted Digit: {predict_digit}")
print(f"Confidence: {foo.result[predict_digit]}")
