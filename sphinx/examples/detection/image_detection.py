# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from pyvarml.engines.tflite import TFLiteInterpreter
from pyvarml.multimedia.helper import Multimedia
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

image = Multimedia("media/street.png")
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

image.show_image("Image Detection Example", output_image)
