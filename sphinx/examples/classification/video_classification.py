from pyvarml.engines.tflite import TFLiteInterpreter
from pyvarml.multimedia.video import Video
from pyvarml.utils.label import Label
from pyvarml.utils.overlay import Overlay
from pyvarml.utils.retriever import FTP

ftp = FTP()

if ftp.retrieve_package(category="classification"):
    model_file_path = ftp.model
    label_file_path = ftp.label

labels = Label(label_file_path)
labels.read_labels("classification")

engine = TFLiteInterpreter(model_file_path)

video = Video("path/to/video") # Change here
video.start()
video.set_sizes(engine_input_details=engine.input_details)

draw = Overlay()

while video.loop:
    frame = video.get_frame()
    video.resize_frame(frame)

    engine.set_input(video.frame_resized)
    engine.run_inference()
    engine.get_classification_result()

    output_frame = draw.info(
                        "classification", video.frame_original,
                        engine.result, labels.list, engine.inference_time,
                        model_file_path, video.video)

    video.show_frame("Video Classification Example", output_frame)

video.destroy()
