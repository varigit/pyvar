# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Real Time Class

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
    .. note:: 10/15/2021 [diego.d] First Version Released
"""

import cv2
import numpy as np


class RealTime:
    def __init__(self, device):
        self.camera = device
        self.camera_capture = None
        self.frame_original = None
        self.frame_resized = None
        self.width = None
        self.height = None
        
    def start(self):
        pipeline = f"v4l2src device={self.camera} ! " \
                   "video/x-raw,width=640,height=480," \
                   "framerate=30/1 ! queue leaky=downstream " \
                   "max-size-buffers=1 ! videoconvert ! " \
                   "appsink"
        pipeline = 0 # testing on host
        self.camera_capture =  cv2.VideoCapture(pipeline)
        return True
    
    def destroy(self):
        self.camera_capture.release()
        cv2.destroyAllWindows()        
    
    def loop(self):
        return self.camera_capture.isOpened()
    
    def show_frame(self, name=None, output_frame=None):
        cv2.imshow(name, output_frame)
        cv2.waitKey(1)        
    
    def get_frame(self):
        check, frame = self.camera_capture.read()
        if check is not True:
            return False
        return frame
        
    def set_sizes(self, engine_input_details=None):
        if engine_input_details is not None:
            _, self.height, self.width, _ = engine_input_details[0]['shape']
    
    
    def resize_frame(self, frame, width=None, height=None):
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
            
        self.frame_original = frame
        
        self.frame_resized = cv2.resize(frame, (self.width, self.height))
        self.frame_resized = np.expand_dims(self.frame_resized, axis = 0)
