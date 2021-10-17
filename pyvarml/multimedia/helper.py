# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import os
import sys

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

import cv2

from pyvarml.multimedia.config import FULL_HD_RESOLUTION
from pyvarml.multimedia.config import HD_RESOLUTION
from pyvarml.multimedia.config import VGA_RESOLUTION
from pyvarml.multimedia.config import LEAKY

class Multimedia:
    def __init__(self, source=None, resolution=None):
        self.video_src = source
        self.resolution = resolution
        self.devices = Devices()
        self.devices.get_video_devices()
        self.sink = None

        if not os.path.isfile(self.video_src):
            self.dev = self.devices.search_device(self.video_src)
            self.dev_caps = self.get_caps()

    def get_caps(self):
        if self.resolution == FULL_HD_RESOLUTION:
            return self.validate_caps(self.dev.full_hd_caps)
        elif self.resolution == VGA_RESOLUTION:
            return self.validate_caps(self.dev.vga_caps)
        else:
            if self.resolution != HD_RESOLUTION:
                print(f"Invalid resolution: {self.resolution}. " \
                        "Trying to use HD resolution instead.")
            return self.validate_caps(self.dev.hd_caps)

    def validate_caps(self, caps):
        if caps:
            return caps
        else:
            print(f"Resolution not supported. Using " \
                   "{self.dev.default_caps.width}x" \
                   "{self.dev.default_caps.height} instead.")
            return self.dev.default_caps

    def set_v4l2_config(self):
        if self.video_src and os.path.isfile(self.video_src):
            pipeline = self.v4l2_video_pipeline(self.video_src)
        else:
            pipeline = self.v4l2_camera_pipeline(
                            width=self.dev_caps.width,
                            height=self.dev_caps.height,
                            device=self.dev.name,
                            framerate=self.dev_caps.framerate)
        self.sink = cv2.VideoCapture(pipeline)

    def v4l2_video_pipeline(self, filesrc):
        return (f"filesrc location={filesrc} ! qtdemux name=d d.video_0 ! " \
                f"decodebin ! queue {LEAKY} ! queue ! imxvideoconvert_g2d ! " \
                f"videoconvert ! appsink")        
        
    def v4l2_camera_pipeline(self, width, height, device, framerate):
        return (f"v4l2src device={device} ! video/x-raw,width={width}," \
                f"height={height},framerate={framerate} ! queue {LEAKY} ! " \
                f"videoconvert ! appsink")

    def get_frame(self):
        check, frame = self.sink.read()
        if check is not True:
            self.destroy()
            sys.exit("Your video device could not capture any image.")
        return frame

    def loop(self):
        if (not self.sink) or (not self.sink.isOpened()):
            sys.exit("Your video device could not be initialized. Exiting...")
        return self.sink.isOpened()

    def save(self, name=None, output_frame=None):
        cv2.imwrite(name, output_frame)

    def show(self, name=None, output_frame=None):
        cv2.imshow(name, output_frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'):
            self.destroy()

    def show_image(self, title=None, image=None):
        cv2.imshow(title, image)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def destroy(self):
        self.sink.release()
        cv2.destroyAllWindows()  

class VideoDevice:
    def __init__(self):
        self.name = None
        self.caps = None
        self.default_caps = None
        self.full_hd_caps = None
        self.hd_caps = None
        self.vga_caps = None

class Caps:
    def __init__(self):
        self.name = None
        self.format = None
        self.width = None
        self.height = None
        self.framerate = None

class Devices:
    def __init__(self):
        self.devices = []

    def get_video_devices(self):
        Gst.init()
        dev_monitor = Gst.DeviceMonitor()
        dev_monitor.add_filter("Video/Source")
        dev_monitor.start()

        for dev in dev_monitor.get_devices():
            video_dev = VideoDevice()
            dev_props = dev.get_properties()
            dev_caps = dev.get_caps()

            name = dev_props.get_string("device.path")
            caps = self.get_device_caps(dev_caps.normalize())
            full_hd_caps, hd_caps, vga_caps = self.get_std_caps(caps)
            default_caps = hd_caps
            if (not default_caps) and caps:
                default_caps = caps[0]

            video_dev.name = name
            video_dev.caps = caps
            video_dev.default_caps = default_caps
            video_dev.full_hd_caps = full_hd_caps
            video_dev.hd_caps = hd_caps
            video_dev.vga_caps = vga_caps
            self.devices.append(video_dev)

        dev_monitor.stop()

    @staticmethod
    def get_device_caps(dev_caps):
        caps_list = []

        for i in range(dev_caps.get_size()):
            if dev_caps.get_structure(i).get_name() != "video/x-raw":
                continue
            caps = Caps()
            caps_struct = dev_caps.get_structure(i)
            caps.name = caps_struct.get_name()
            caps.format = caps_struct.get_string("format")
            caps.width = caps_struct.get_int("width")[1]
            caps.height = caps_struct.get_int("height")[1]
            framerate = ("{}/{}".format(*caps_struct.get_fraction(
                                        "framerate")[1:]))
            caps.framerate = framerate
            caps_list.append(caps)

        return caps_list

    @staticmethod
    def get_std_caps(dev_caps):
        full_hd_caps = None
        hd_caps = None
        vga_caps = None

        for caps in dev_caps:
            if  (caps.width == 1920) and (caps.height == 1080):
                full_hd_caps = caps
            elif (caps.width == 1280) and (caps.height == 720):
                hd_caps = caps
            elif (caps.width == 640) and (caps.height == 480):
                vga_caps = caps

        return full_hd_caps, hd_caps, vga_caps

    def search_device(self, dev_name):
        dev = None
        if dev_name.startswith("/dev/video"):
            for device in self.devices:
                if device.name == dev_name:
                    dev = device
                if not dev:
                    print("The specified video_src was not found. " \
                          "Searching for default video device...")
        if not dev and self.devices:
            dev = self.devices[0]
        elif not dev:
            sys.exit("No video device found. Exiting...")
        print(f"Using {dev.name} as video device")
        return dev
