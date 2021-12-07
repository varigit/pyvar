# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from pyvar.ml.engines.armnn import ArmNNInterpreter
from pyvar.ml.utils.label import Label
from pyvar.ml.utils.retriever import FTP
from pyvar.ml.utils.resizer import Resizer
from pyvar.multimedia.helper import Multimedia

ftp = FTP()

if ftp.retrieve_package(category="classification"):
    model_file_path = ftp.model
    label_file_path = ftp.label
    image_file_path = ftp.image

labels = Label(label_file_path)
labels.read_labels("classification")

engine = ArmNNInterpreter(model_file_path, accelerated=True, category="classification")

resizer = Resizer()

image = Multimedia(image_file_path)
resizer.resize_armnn(image.video_src, engine.input_width, engine.input_height)

engine.set_input(resizer.image_resized)

engine.run_inference()

engine.get_result("classification", labels.list)

print(f"Inference time: {engine.inference_time}")
