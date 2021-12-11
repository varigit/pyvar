# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import cv2
import numpy as np
import threading

import gi
gi.require_versions({'GdkPixbuf': "2.0", 'Gtk': "3.0"})
from gi.repository.GdkPixbuf import Colorspace, Pixbuf
from gi.repository import GLib, Gtk

from pyvar.ml.engines.tflite import TFLiteInterpreter
from pyvar.ml.utils.label import Label
from pyvar.ml.utils.overlay import Overlay
from pyvar.ml.utils.resizer import Resizer
from pyvar.ml.utils.retriever import FTP
from pyvar.multimedia.helper import Multimedia

SSD_LABELS_LIST = ["person", "backpack", "umbrella", "handbag", "tie",
                   "suitcase", "bottle", "wine glass", "cup", "fork", "knife",
                   "spoon", "chair", "potted plant", "laptop", "mouse",
                   "remote", "keyboard", "cell phone", "book", "banana",
                   "apple", "sandwich", "orange", "clock", "vase", "scissors"]


class RealTimeDetection(Gtk.Window):
    def __init__(self, detection_list):
        super().__init__()
        self.fullscreen()
        self.set_border_width(2)
        self.detection_list = detection_list
        self.model_file_path = None
        self.label_file_path = None

        ftp = FTP()

        if ftp.retrieve_package(category="detection"):
            self.model_file_path = ftp.model
            self.label_file_path = ftp.label

        labels = Label(self.label_file_path)
        labels.read_labels("detection")

        self.labels = labels.list

        self.engine = None
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.pixbuf = None

        horizontal_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.add(horizontal_box)

        scrolled_window = Gtk.ScrolledWindow()
        horizontal_box.pack_start(scrolled_window, True, True, 0)

        vertical_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        scrolled_window.add(vertical_box)

        for label in self.detection_list:
            toggle_button = Gtk.ToggleButton(label=f'{label}')
            toggle_button.set_active(True)
            toggle_button.connect('toggled', self.on_object_toggled, label)
            vertical_box.pack_start(toggle_button, True, True, 0)

        self.displayed_image = Gtk.Image()
        horizontal_box.pack_start(self.displayed_image, True, True, 0)

        self.start_interpreter()
        self.run_application()

    def on_object_toggled(self, button, obj):
        if button.get_active():
            if obj not in self.detection_list:
                self.detection_list.append(obj)
        else:
            if obj in self.detection_list:
                self.detection_list.remove(obj)

    def set_displayed_image(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        height, width = image.shape[:2]
        arr = np.ndarray.tobytes(image)
        self.pixbuf = Pixbuf.new_from_data(
            arr, Colorspace.RGB, False, 8,
            width - 10, height - 10, width * 3, None, None)
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

        camera = Multimedia("/dev/video0", resolution="vga")
        camera.set_v4l2_config()

        draw = Overlay()
        draw.inference_time_info = False
        draw.scores_info = True
        draw.extra_info = False
        draw.framerate_info = False

        while camera.loop:
            frame = camera.get_frame()
            resizer.resize_frame(frame)

            self.engine.set_input(resizer.frame_resized)
            self.engine.run_inference()

            positions = self.engine.get_output(0, squeeze=True)
            classes = self.engine.get_output(1, squeeze=True)
            scores = self.engine.get_output(2, squeeze=True)

            result = []
            for idx, score in enumerate(scores):
                if score > 0.5 and (self.labels[classes[idx]] in self.detection_list):
                    result.append({'pos': positions[idx], '_id': classes[idx]})

            output_frame = draw.info(category="detection",
                                     image=resizer.frame,
                                     top_result=result,
                                     labels=self.labels,
                                     inference_time=None,
                                     model_name=None,
                                     source_file=camera.dev.name,
                                     fps=None)

            GLib.idle_add(self.set_displayed_image, output_frame)


if __name__ == "__main__":
    detection_list = SSD_LABELS_LIST.copy()
    app = RealTimeDetection(detection_list)
    app.connect('delete-event', Gtk.main_quit)
    app.show_all()
    Gtk.main()
