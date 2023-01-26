# Copyright 2023 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from argparse import ArgumentParser

from pyvar.ml.engines.ethosu import EthosuInterpreter
from pyvar.ml.utils.label import Label
from pyvar.ml.utils.overlay import Overlay
from pyvar.ml.utils.resizer import Resizer
from pyvar.ml.utils.retriever import FTP
from pyvar.multimedia.helper import Multimedia

ftp = FTP()
parser = ArgumentParser()
args = parser.parse_args()

if ftp.retrieve_package(category="classification"):
    model_file_path = ftp.model
    label_file_path = ftp.label
    image_file_path = ftp.image

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
