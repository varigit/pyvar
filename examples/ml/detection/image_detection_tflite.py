# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
This script performs object detection using the TFLiteInterpreter engine.

It performs the following steps:

1. Retrieves the detection package using a HTTPS retriever instance.
2. Loads the labels from the label file.
3. Creates an TFLiteInterpreter engine instance and a resizer instance.
4. Resizes the input image to the engine's input size.
5. Runs inference and gets the detection result.
6. Creates an overlay instance and draws the output image with the
   detection result and other information.
7. Shows the output image using the Multimedia helper.

Example:

To run this script:
    $ python3 object_detection_tflite.py

Args:
None.

Returns:
None.
"""

from argparse import ArgumentParser

from pyvar.ml.engines.tflite import TFLiteInterpreter
from pyvar.ml.utils.label import Label
from pyvar.ml.utils.overlay import Overlay
from pyvar.ml.utils.resizer import Resizer
from pyvar.ml.utils.retriever_https import HTTPS
from pyvar.multimedia.helper import Multimedia

https = HTTPS()
parser = ArgumentParser()
parser.add_argument('--num_threads', type=int)
args = parser.parse_args()
args.num_threads = 2

if https.retrieve_package(category="detection"):
    model_file_path = https.model
    label_file_path = https.label
    image_file_path = https.image

labels = Label(label_file_path)
labels.read_labels("detection")

engine = TFLiteInterpreter(model_file_path=model_file_path,
                           num_threads=args.num_threads)

resizer = Resizer()
resizer.set_sizes(engine_input_details=engine.input_details)

image = Multimedia(image_file_path)
resizer.resize_image(image.video_src)

engine.set_input(resizer.image_resized)
engine.run_inference()
engine.get_result("detection")

draw = Overlay()

output_image = draw.info(category="detection",
                         image=resizer.image,
                         top_result=engine.result,
                         labels=labels.list,
                         inference_time=engine.inference_time,
                         model_name=model_file_path,
                         source_file=resizer.image_path)

image.show_image("TFLite: Image Detection", output_image)
