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

if ftp.retrieve_package(category="detection"):
    model_file_path = ftp.model
    label_file_path = ftp.label

labels = Label(label_file_path)
labels.read_labels("detection")

engine = TFLiteInterpreter(model_file_path)

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

        camera.show("Video Detection", output_frame)

camera.destroy()
