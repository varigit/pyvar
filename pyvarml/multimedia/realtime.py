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
    """
    Python Class to handle real time input.

    :ivar camera: storages the path of the device (e.g.: /dev/video1)
    :ivar camera_capture: storages the device capture from OpenCV.
    :ivar frame_original: storages the original frame.
    :ivar frame_resized: storages the resized frame.
    :ivar width: frame width.
    :ivar height: frame height.
    """
    def __init__(self, device):
        self.camera = device
        self.camera_capture = None
        self.frame_original = None
        self.frame_resized = None
        self.width = None
        self.height = None
        
    def start(self):
        """
        Creates the pipeline to open camera.

        Returns:
            if **success**, return **True**
        """
        pipeline = f"v4l2src device={self.camera} ! " \
                   "video/x-raw,width=640,height=480," \
                   "framerate=30/1 ! queue leaky=downstream " \
                   "max-size-buffers=1 ! videoconvert ! " \
                   "appsink"
        self.camera_capture = cv2.VideoCapture(pipeline)
        return True
    
    def destroy(self):
        """
        Release the camera capture and destroy all windows.
        """
        self.camera_capture.release()
        cv2.destroyAllWindows()        
    
    def loop(self):
        """
        Check if camera is opened.
        """
        return self.camera_capture.isOpened()
    
    def show_frame(self, name=None, output_frame=None):
        """
        Show frame on the window.

        Args:
            name (str): name of the window frame.
            output frame: frame to be showed.
        """
        cv2.imshow(name, output_frame)
        cv2.waitKey(1)        
    
    def get_frame(self):
        """
        Get/read one frame from camera.

        Returns:
            if **success**, return frame
            if **not**, return **False**
        """
        check, frame = self.camera_capture.read()
        if check is not True:
            return False
        return frame
        
    def set_sizes(self, engine_input_details=None):
        """
        Set the width and height sizes to resize the frame.

        Args:
            engine_input_details: input details from TensorFlow Lite model.
        """
        if engine_input_details is not None:
            _, self.height, self.width, _ = engine_input_details[0]['shape']
    
    
    def resize_frame(self, frame, width=None, height=None, expand_dims=False):
        """
        Resize the frame.

        Args:
            frame: frame to be resized.
            width (int): frame width.
            height (int): frame height.

        Returns:
            None. The resized frame is storaged at frame_resized attribute.
        """
        if width is not None:
            self.width = width
        if height is not None:
            self.height = height
            
        self.frame_original = frame
        
        self.frame_resized = cv2.resize(frame, (self.width, self.height))
        if expand_dims:
            self.frame_resized = np.expand_dims(self.frame_resized, axis = 0)
