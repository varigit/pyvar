# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Class to retrieve packages from Variscite FTP server.

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
"""

import ftplib
import glob
import os
import shutil
import sys

from pyvar.config import CACHEDIR
from pyvar.ml.config import CLASSIFICATION
from pyvar.ml.config import DETECTION
from pyvar.ml.config import SEGMENTATION
from pyvar.ml.utils.config import FTP_HOST, FTP_USER, FTP_PASS
from pyvar.ml.utils.config import DEFAULT_PACKAGES
from pyvar.ml.utils.config import TFLITE, TXT, ZIP, JPG, PNG, MP4

class FTP:
    """
    **This class can be used as reference only. It is not for production-ready.**
    """
    def __init__(self, host=None, user=None, passwd=None):
        """
        Constructor method for the FTP class.
        """
        self.host = FTP_HOST if host is None else host
        self.user = FTP_USER if user is None else user
        self.passwd = FTP_PASS if passwd is None else passwd
        self.cachedir = CACHEDIR
        self.retrieved_package = None
        self.model = None
        self.label = None
        self.image = None
        self.video = None
        try:
            self.ftp = ftplib.FTP(self.host, self.user, self.passwd)
            try:
                os.mkdir(self.cachedir)
            except:
                pass
        except ftplib.all_errors as error:
            sys.exit(error)
            
    def retrieve_package(
        self, package_dir=None, package_filename=None, category=None):
        """
        Retrieve package from the FTP server.
        
        Args:
            package_dir (str): package directory;
            package_filename (str): model package file name;
            category (str): model category (classification or detection).
        
        Returns:
            True if the package file was downloaded successfully. False if not.
        """
        if category is not None:
            if category is CLASSIFICATION:
                package_dir = DEFAULT_PACKAGES[CLASSIFICATION][0]
                package_filename = DEFAULT_PACKAGES[CLASSIFICATION][1]
            elif category is DETECTION:
                package_dir = DEFAULT_PACKAGES[DETECTION][0]
                package_filename = DEFAULT_PACKAGES[DETECTION][1]
            elif category is SEGMENTATION:
                package_dir = DEFAULT_PACKAGES[SEGMENTATION][0]
                package_filename = DEFAULT_PACKAGES[SEGMENTATION][1]

        package_file = os.path.join(self.cachedir, package_filename)
        try:
            self.ftp.cwd(package_dir)
            with open(package_file, "wb") as f:
                r = self.ftp.retrbinary(f"RETR {package_filename}", f.write)
                if not r.startswith("226 Transfer complete"):
                    os.remove(package_file)
                    return False
                else:
                    self.retrieved_package = package_file
                    self.ftp.cwd("/")
        except:
            return False

        if self.retrieved_package.endswith(ZIP):
            package_name_path = self.retrieved_package[:-4]
            try:
                shutil.unpack_archive(self.retrieved_package, self.cachedir)
                self.get_package_names(package_name_path, category)
                os.remove(self.retrieved_package)
            except:
                return False
        self.disconnect()
        return True

    def disconnect(self):
        """
        Send a quit command to the server and close the connection.        
        """
        self.ftp.quit()

    def get_package_names(self, package_name_path, category):
        """
        Get the model and label names from the downloaded package.        
        """
        model_list = glob.glob(os.path.join(package_name_path, TFLITE))
        self.model = model_list[0]
        label_list = glob.glob(os.path.join(package_name_path, TXT))
        self.label = label_list[0]
        if category is CLASSIFICATION:
            image_list = glob.glob(os.path.join(package_name_path, JPG))
            self.image = image_list[0]
        if category is DETECTION:
            image_list = glob.glob(os.path.join(package_name_path, PNG))
            self.image = image_list[0]
        video_list = glob.glob(os.path.join(package_name_path, MP4))
        self.video = video_list[0]
