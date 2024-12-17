# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
This script performs video classification using the TFLiteInterpreter engine.

It performs the following steps:

1. Retrieves the classification package using a HTTPS retriever instance.
2. Loads the labels from the label file.
3. Creates an TFLiteInterpreter engine instance and a resizer instance.
4. Resizes each frame of the input video to the engine's input size.
5. Runs inference and gets the result for each frame.
6. Creates an overlay instance and draws the output image with the
   classification result and other information for each frame.
7. Shows the output video using the Multimedia helper.

Example:

To run this script:
    $ python3 video_classification_tflite.py

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

if https.retrieve_package(category="classification"):
    model_file_path = https.model
    label_file_path = https.label
    video_file_path = https.video

labels = Label(label_file_path)
labels.read_labels("classification")

engine = TFLiteInterpreter(model_file_path=model_file_path,
                           num_threads=args.num_threads)

resizer = Resizer()
resizer.set_sizes(engine_input_details=engine.input_details)

video = Multimedia(video_file_path)
video.set_v4l2_config()

draw = Overlay()

while video.loop:
    frame = video.get_frame()
    resizer.resize_frame(frame)

    engine.set_input(resizer.frame_resized)
    engine.run_inference()
    engine.get_result("classification")

    output_frame = draw.info(category="classification",
                             image=resizer.frame,
                             top_result=engine.result,
                             labels=labels.list,
                             inference_time=engine.inference_time,
                             model_name=model_file_path,
                             source_file=video.video_src)

    video.show("TFLite: Video Classification", output_frame)

video.destroy()
