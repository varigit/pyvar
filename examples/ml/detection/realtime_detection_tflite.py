# Copyright 2021-2023 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
This script performs real-time object detection using the TFLiteInterpreter
engine.

It performs the following steps:

1. Retrieves the detection package using a HTTPS retriever instance.
2. Loads the labels from the label file.
3. Creates an TFLiteInterpreter engine instance and a resizer instance.
4. Resizes each frame of the input video from a camera to the engine's input size.
5. Runs inference and gets the result for each frame.
6. Creates an overlay instance and draws the output image with the
   detection result and other information for each frame.
7. Shows the output video with the detection results using the Multimedia helper.

Example:

To run this script:
    $ python3 realtime_detection_tflite.py

Args:
None.

Returns:
None.
"""

from argparse import ArgumentParser

from pyvar.ml.engines.tflite import TFLiteInterpreter
from pyvar.ml.utils.framerate import Framerate
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

labels = Label(label_file_path)
labels.read_labels("detection")

engine = TFLiteInterpreter(model_file_path=model_file_path,
                           num_threads=args.num_threads)

resizer = Resizer()
resizer.set_sizes(engine_input_details=engine.input_details)

camera = Multimedia("/dev/video1", resolution="vga")
camera.set_v4l2_config()

framerate = Framerate()

draw = Overlay()
draw.framerate_info = True

while camera.loop:
    with framerate.fpsit():
        frame = camera.get_frame()
        resizer.resize_frame(frame)

        engine.set_input(resizer.frame_resized)
        engine.run_inference()
        engine.get_result("detection")

        output_frame = draw.info(category="detection",
                                 image=resizer.frame,
                                 top_result=engine.result,
                                 labels=labels.list,
                                 inference_time=engine.inference_time,
                                 model_name=model_file_path,
                                 source_file=camera.dev.name,
                                 fps=framerate.fps)

        camera.show("TFLite: Real Time Detection", output_frame)

camera.destroy()
