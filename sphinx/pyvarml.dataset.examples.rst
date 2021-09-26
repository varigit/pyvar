Quick Dataset Examples
======================

Dataset Examples
----------------

Training MNIST Handwritten Digits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. To train a simple MNIST to recognize handwritten digits, see the example:

.. code-block:: python

    from pyvarml.dataset.mnist import train_mnist_digit

    foo = train_mnist_digit()

    with open('mnist_digit.tflite', "wb") as model_file:
        model_file.write(foo[0])
        model_file.close()

    print(f"Test loss: {foo[1]}")
    print(f"Test accuracy: {foo[2]}")

2. The output is similar to the one below:

.. code-block:: console

    Test loss: 0.07373514771461487
    Test accuracy: 0.9776999950408936

Testing MNIST Handwritten Digits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. To test the above model, see the example:

.. code-block:: python

    from pyvarml.engines.tflite import TFLiteInterpreter
    from pyvarml.utils.helper import Images
    
    image_test = Images("zero.png")
    image_test.convert_rgb_to_gray_scale(28, 28, True)
    
    foo = TFLiteInterpreter("mnist_digit.tflite")

    foo.start()
    foo.set_image(image_test.converted)
    foo.run_inference()

    predict_digit = foo.get_mnist_result()

    print(f"Predicted Digit: {predict_digit}")
    print(f"Confidence: {foo.result[predict_digit]}")

2. The output is similar to the one below:

.. code-block:: console

    Predicted Digit: 0
    Confidence: 8.820571899414062
