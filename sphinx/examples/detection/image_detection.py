from pyvarml.engines.tflite import TFLiteInterpreter
from pyvarml.multimedia.images import Images
from pyvarml.utils.label import Label
from pyvarml.utils.overlay import Overlay
from pyvarml.utils.retriever import FTP

ftp = FTP()

if ftp.retrieve_package(category="detection"):
    model_file_path = ftp.model
    label_file_path = ftp.label

labels = Label(label_file_path)
labels.read_labels("detection")

engine = TFLiteInterpreter(model_file_path)

image_test = Images("path/to/image") # Change here
image_test.resize(engine_input_details=engine.input_details)

engine.set_image(image_test.resized)
engine.run_inference()
engine.get_detection_result()

draw = Overlay()

output_image = draw.info(
                    "detection", image_test.image_original,
                    engine.result, labels.list, engine.inference_time,
                    model_file_path, image_test.image)

image_test.show("Image Detection Example", output_image)
