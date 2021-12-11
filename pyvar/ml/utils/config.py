# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import cv2

INF_TIME_MSG = "INFERENCE TIME"
TITLE = "CLASSIFICATION"
FPS_MSG = "FPS"

FONT = {'hershey': cv2.FONT_HERSHEY_SIMPLEX,
        'size': 0.8,
        'color': {'black': (0, 0, 0),
                  'blue': (255, 0, 0),
                  'green': (0, 255, 0),
                  'orange': (0, 127, 255),
                  'red': (0, 0, 255),
                  'white': (255, 255, 255)},
        'thickness': 2}


# FTP Credentials
FTP_HOST = "ftp.variscite.com"
FTP_USER = "customerv"
FTP_PASS = "Variscite1"

# Extensions
TFLITE = "*.tflite"
TXT = "*.txt"
ZIP = ".zip"
JPG = "*.jpg"
PNG = "*.png"
MP4 = "*.mp4"

# Default Packages from FTP
DEFAULT_PACKAGES = {'classification': ["pyvarml/classification/",
                                       "mobilenet_v1_1.0_224_quant.zip"],
                    'detection': ["pyvarml/detection/",
                                  "ssd_mobilenet_v1_1_default_1.zip"],
                    'segmentation': ["pyvarml/segmentation/",
                                     "deeplabv3_mnv2_pascal_quant.zip"]}
