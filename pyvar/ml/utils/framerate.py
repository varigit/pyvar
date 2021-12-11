# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Class to calculate framerate from videos and real time cameras devices.

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
"""

import collections
from contextlib import contextmanager
from time import perf_counter


class Framerate:
    def __init__(self):
        """
        Constructor method for the Framerate class.
        """
        self.fps = 0
        self.window = collections.deque(maxlen=30)

    @contextmanager
    def fpsit(self):
        """
        Calculates the frames per second and save it in the **fps** attribute.
        """
        begin = perf_counter()
        try:
            yield
        finally:
            end = perf_counter()
            self.window.append(end - begin)
            self.fps = len(self.window) / sum(self.window)
