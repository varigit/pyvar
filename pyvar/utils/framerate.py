# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Class to get framerate from videos and real time cameras.

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
    .. note:: 10/15/2021 [diego.d] First Version Released
"""

import collections
from contextlib import contextmanager
from time import monotonic

class Framerate:
    def __init__(self):
        self.fps = 0
        self.window = collections.deque(maxlen=30)

    @contextmanager
    def fpsit(self):
        """
        The framerate is storage in the **fps** attribute.
        """
        begin = monotonic()
        try:
            yield
        finally:
            end = monotonic()
            self.window.append(end - begin)
            self.fps = len(self.window) / sum(self.window)
