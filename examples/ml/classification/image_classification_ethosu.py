# Copyright 2021-2023 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
This script performs image classification using the EthosuInterpreter engine.

It performs the following steps:

1. Retrieves the classification package using a HTTPS retriever instance.
2. Loads the labels from the label file.
3. Creates an EthosuInterpreter engine instance and a resizer instance.
4. Resizes the input image to the engine's input size.
5. Runs inference and gets the result.
6. Creates an overlay instance and draws the output image with the
   classification result and other information.
7. Shows the output image using the Multimedia helper.

Example:

To run this script:
    $ python3 image_classification_ethosu.py

Args:
None.

Returns:
None.
"""

from pyvar.ml.engines.ethosu import EthosuInterpreter
from pyvar.ml.utils.label import Label
from pyvar.ml.utils.overlay import Overlay
from pyvar.ml.utils.resizer import Resizer
from pyvar.ml.utils.retriever_https import HTTPS
from pyvar.multimedia.helper import Multimedia

https = HTTPS()

if https.retrieve_package(category="classification"):
    model_file_path = https.model
    label_file_path = https.label
    image_file_path = https.image

labels = Label(label_file_path)
labels.read_labels("classification")

engine = EthosuInterpreter(model_file_path=model_file_path)

resizer = Resizer()
resizer.set_sizes(engine_input_details=engine.input_details)

image = Multimedia(image_file_path)
resizer.resize_image(image.video_src)

engine.set_input(resizer.image_resized)
engine.run_inference()
engine.get_result("classification")

draw = Overlay()

output_image = draw.info(category="classification",
                         image=resizer.image,
                         top_result=engine.result,
                         labels=labels.list,
                         inference_time=engine.inference_time,
                         model_name=model_file_path,
                         source_file=resizer.image_path)

image.show_image("Ethosu: Image Classification", output_image)
