Classification Examples
=======================

Image Classification
--------------------

1. To create a simple image classification, see the example:

.. code-block:: python

    from pyvarml.engines.tflite import TFLiteInterpreter
    from pyvarml.utils.helper import Label, Images
    from pyvarml.utils.retriever import FTP
    from pyvarml.utils.timer import Timer

    ftp = FTP()
    package_dir = "pyvarml/classification/"
    package_filename = "mobilenet_v1_1.0_224_quant.zip"

    if ftp.retrieve_package(package_dir, package_filename):
        model_file_path = ftp.model[0]
        label_file_path = ftp.label[0]

    labels = Label(label_file_path)

    engine = TFLiteInterpreter(model_file_path)

    my_image = Images("car.jpg")
    my_image.resize(engine_input_details=engine.input_details)

    engine.set_image(my_image.resized)
    engine.run_inference()
    engine.get_classification_result()

    output_image = my_image.put_info(
                            my_image.image_original,
                            engine.result,
                            labels.list,
                            engine.inference_time,
                            model_file_path,
                            my_image.image)

    my_image.show("Classification Example", output_image)

+------------------------+------------------------+
| **Example**            | **Example Classified** |
+========================+========================+
| |car|                  | |dogs-converted|       |
+------------------------+------------------------+

.. |car| image:: images/car.jpg
   :width: 100%
   
.. |dogs-converted| image:: images/car_classified.jpg
   :width: 100%


Video Classification
--------------------


Real Time Classification
------------------------


