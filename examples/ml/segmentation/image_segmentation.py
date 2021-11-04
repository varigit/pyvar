from pyvar.ml.engines.tflite import TFLiteInterpreter
from pyvar.ml.multimedia.images import Images
from pyvar.ml.utils.overlay import Overlay
from pyvar.ml.utils.retriever import FTP

ftp = FTP()

if ftp.retrieve_package(category="segmentation"):
    model_file_path = ftp.model

engine = TFLiteInterpreter(model_file_path)

image_test = Images("path/to/image") # Change here
image_test.resize(engine_input_details=engine.input_details)

engine.set_input(image_test.resized)
engine.run_inference()
engine.get_segmentation_result(image=image_test.resized_no_dims)

draw = Overlay()
draw.scores_info = False

output_image = draw.info(
                    None, engine.output_image,
                    None, None, engine.inference_time,
                    model_file_path, image_test.image)

image_test.show("Image Semantic Segmentation Example", output_image)
