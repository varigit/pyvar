import threading
import cv2
import numpy as np

import gi
gi.require_versions({'GdkPixbuf': "2.0", 'Gtk': "3.0"})
from gi.repository.GdkPixbuf import Colorspace, Pixbuf
from gi.repository import GLib, Gtk

from pyvarml.engines.tflite import TFLiteInterpreter
from pyvarml.multimedia.helper import Multimedia
from pyvarml.utils.framerate import Framerate
from pyvarml.utils.label import Label
from pyvarml.utils.overlay import Overlay
from pyvarml.utils.retriever import FTP
from pyvarml.utils.resizer import Resizer

SSD_LABELS_LIST = [
    "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train",
    "truck", "boat", "traffic light", "fire hydrant", "stop sign",
    "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
    "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag",
    "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite",
    "baseball bat", "baseball glove", "skateboard", "surfboard",
    "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon",
    "bowl", "banana", "apple", "sandwich", "orange", "broccoli", "carrot",
    "hot dog", "pizza", "donut", "cake", "chair", "couch", "potted plant",
    "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote",
    "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear",
    "hair drier", "toothbrush"]

class ObjectSelection(Gtk.Frame):
    def __init__(self, parent, exclude_list):
        super().__init__()
        self.parent = parent
        self.exclude_list = exclude_list
        labels_list = self.exclude_list.copy()
        labels_list.sort()

        vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vertical_box)

        scrolled_window = Gtk.ScrolledWindow()

        horizontal_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        quit_button = Gtk.Button.new_with_label('Quit')
        quit_button.connect('clicked', self.on_quit_button_clicked)
        back_button = Gtk.Button.new_with_label('Back')
        back_button.connect('clicked', self.on_back_button_clicked)
        horizontal_box.pack_start(back_button, True, True, 10)
        horizontal_box.pack_start(quit_button, True, True, 10)
        vertical_box.pack_start(horizontal_box, False, True, 10)
        vertical_box.pack_start(scrolled_window, True, True, 10)

        vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scrolled_window.add(vertical_box)

        for label in labels_list:
            horizontal_box =  Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
            switch_button = Gtk.Switch()
            switch_button.set_active(False)
            switch_button.connect('notify::active',
                                  self.on_object_switch_activated, label)
            label_name = Gtk.Label.new(label)
            horizontal_box.pack_start(label_name, True, True, 100)
            horizontal_box.pack_start(switch_button, False, True, 100)
            vertical_box.pack_start(horizontal_box, True, True, 10)

    def on_quit_button_clicked(self, button):
        Gtk.main_quit()

    def on_back_button_clicked(self, button):
        self.parent.set_current_page(0)

    def on_object_switch_activated(self, switch, gparam, obj):
        if switch.get_active():
            if obj in self.exclude_list:
                self.exclude_list.remove(obj)
        else:
            if obj not in self.exclude_list:
                self.exclude_list.append(obj)

class RealTimeDetection(Gtk.Frame):
    def __init__(self, parent, exclude_list):
        super().__init__()
        self.parent = parent
        self.exclude_list = exclude_list
        self.model_file_path = None
        self.label_file_path = None

        ftp = FTP()

        if ftp.retrieve_package(category="detection"):
            self.model_file_path = ftp.model
            self.label_file_path = ftp.label
            
        labels = Label(self.label_file_path)
        labels.read_labels("detection")
 
        self.labels = labels.list
        
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.pixbuf = None

        vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.add(vertical_box)

        horizontal_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        quit_button = Gtk.Button.new_with_label('Quit')
        quit_button.connect('clicked', self.on_quit_button_clicked)
        objects_button = Gtk.Button.new_with_label('Objects')
        objects_button.connect('clicked', self.on_objects_button_clicked)
        horizontal_box.pack_start(objects_button, True, True, 10)
        horizontal_box.pack_start(quit_button, True, True, 10)
        vertical_box.pack_start(horizontal_box, True, False, 10)

        self.displayed_image = Gtk.Image()
        image_box = Gtk.Box(spacing=5)
        image_box.pack_start(self.displayed_image, True, True, 0)
        vertical_box.pack_start(image_box, True, True, 5)

        horizontal_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)

        inference_time_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        inference_label = Gtk.Label()
        inference_label.set_markup('INFERENCE TIME:')
        self.inference_value_label = Gtk.Label.new(None)
        inference_time_box.pack_start(inference_label, False, True, 10)
        inference_time_box.pack_start(self.inference_value_label, False, False, 10)

        fps_box =  Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        fps_label = Gtk.Label()
        fps_label.set_markup('FPS:')
        self.fps_value_label = Gtk.Label.new(None)
        fps_box.pack_start(fps_label, False, True, 10)
        fps_box.pack_start(self.fps_value_label, False, False, 10)

        horizontal_box.pack_start(inference_time_box, True, True, 10)
        horizontal_box.pack_start(fps_box, True, True, 10)
        vertical_box.pack_start(horizontal_box, True, False, 10)

        self.start_interpreter()
        self.run_application()

    def on_quit_button_clicked(self, button):
        Gtk.main_quit()

    def on_objects_button_clicked(self, button):
        self.parent.set_current_page(1)

    def set_displayed_image(self, image):
        image = cv2.resize(image, (420, 340))
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        height, width = image.shape[:2]
        arr = np.ndarray.tobytes(image)
        self.pixbuf = Pixbuf.new_from_data(
                             arr, Colorspace.RGB, False, 8,
                             width, height, width*3, None, None)
        self.displayed_image.set_from_pixbuf(self.pixbuf)
        self.pixbuf = None

    def run_application(self):
        thread = threading.Thread(target=self.image_detection)
        thread.daemon = True
        thread.start()

    def start_interpreter(self):
        self.engine = TFLiteInterpreter(self.model_file_path)

    def image_detection(self):
        resizer = Resizer()
        resizer.set_sizes(engine_input_details=self.engine.input_details)

        camera = Multimedia("/dev/video1", resolution="vga")
        camera.set_v4l2_config()
        
        framerate = Framerate()

        draw = Overlay()
        draw.inference_time_info = False
        draw.scores_info = True
        draw.extra_info = False
        draw.framerate_info = False
        
        while camera.loop:
            with framerate.fpsit():
                frame = camera.get_frame()
                resizer.resize_frame(frame)

                self.engine.set_input(resizer.frame_resized)
                self.engine.run_inference()

                positions = self.engine.get_output(0, squeeze=True)
                classes = self.engine.get_output(1, squeeze=True)
                scores = self.engine.get_output(2, squeeze=True)
                
                result = []
                for idx, score in enumerate(scores):
                    if score > 0.5 and (self.labels[classes[idx]] not in self.exclude_list):
                        result.append({'pos': positions[idx], '_id': classes[idx]})
                
                output_frame = draw.info(category="detection",
                                         image=resizer.frame,
                                         top_result=result,
                                         labels=self.labels,
                                         inference_time=None,
                                         model_name=None,
                                         source_file=camera.dev.name,
                                         fps=None)

            GLib.idle_add(self.inference_value_label.set_text,
                          (f"{self.engine.inference_time}"))
            GLib.idle_add(self.fps_value_label.set_text,
                          (f"{int(framerate.fps)}"))
            GLib.idle_add(self.set_displayed_image, (output_frame))

class UserInterfaceDetectionExample(Gtk.Window):
    def __init__(self):
        super().__init__(title='User Interface Detection Example')
        self.fullscreen()
        exclude_list = SSD_LABELS_LIST.copy()

        container = Gtk.Notebook()
        container.set_show_tabs(False)
        self.add(container)

        realtime_page = RealTimeDetection(container, exclude_list)
        container.append_page(realtime_page)

        label_selection_page = ObjectSelection(container, exclude_list)
        container.append_page(label_selection_page)

if __name__ == "__main__":
    app = UserInterfaceDetectionExample()
    app.connect('delete-event', Gtk.main_quit)
    app.show_all()
    Gtk.main()
