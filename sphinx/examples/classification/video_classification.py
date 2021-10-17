# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from pyvarml.engines.tflite import TFLiteInterpreter
from pyvarml.multimedia.helper import Multimedia
from pyvarml.utils.framerate import Framerate
from pyvarml.utils.label import Label
from pyvarml.utils.overlay import Overlay
from pyvarml.utils.retriever import FTP
from pyvarml.utils.resizer import Resizer

ftp = FTP()

if ftp.retrieve_package(category="classification"):
    model_file_path = ftp.model
    label_file_path = ftp.label
    video_file_path = ftp.video

labels = Label(label_file_path)
labels.read_labels("classification")

engine = TFLiteInterpreter(model_file_path)

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

    video.show("Video Classification Example", output_frame)

video.destroy()
