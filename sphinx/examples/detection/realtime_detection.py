from pyvarml.engines.tflite import TFLiteInterpreter
from pyvarml.multimedia.realtime import RealTime
from pyvarml.utils.framerate import Framerate
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

camera = RealTime("path/to/device") # Change here
camera.start()
camera.set_sizes(engine_input_details=engine.input_details)

framerate = Framerate()

draw = Overlay()
draw.framerate_info = True

while camera.loop:
    with framerate.fpsit():
        frame = camera.get_frame()
        camera.resize_frame(frame)

        engine.set_input(camera.frame_resized)
        engine.run_inference()
        engine.get_detection_result()

        output_frame = draw.info(
                            "detection", camera.frame_original,
                            engine.result, labels.list, engine.inference_time,
                            model_file_path, camera.camera, framerate.fps)

        camera.show_frame("Video Detection", output_frame)

camera.destroy()
