# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Video Class

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
    .. note:: 10/15/2021 [diego.d] First Version Released
"""

import cv2
import numpy as np

class Video:
    def __init__(self, video_file_path):
        self.video = video_file_path
        self.video_capture = None
        self.frame_original = None
        self.frame_resized = None
        self.width = None
        self.height = None
        
    def start(self):
        pipeline = f"filesrc location={self.video} ! " \
                    "qtdemux name=d d.video_0 ! " \
                    "decodebin ! queue leaky=downstream max-size-buffers=1 ! " \
                    "queue ! imxvideoconvert_g2d ! " \
                    "videoconvert ! appsink"
        pipeline = self.video # testing on host
        self.video_capture =  cv2.VideoCapture(pipeline)
        return True
    
    def destroy(self):
        self.video_capture.release()
        cv2.destroyAllWindows()        
    
    def loop(self):
        return self.video_capture.isOpened()
    
    def show_frame(self, name=None, output_frame=None):
        cv2.imshow(name, output_frame)
        cv2.waitKey(1)        
    
    def get_frame(self):
        check, frame = self.video_capture.read()
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
