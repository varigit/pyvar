# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import collections
from contextlib import contextmanager
from time import monotonic

class Framerate:
    def __init__(self):
        self.fps = 0
        self.window = collections.deque(maxlen=30)

    @contextmanager
    def fpsit(self):
        begin = monotonic()
        try:
            yield
        finally:
            end = monotonic()
            self.window.append(end - begin)
            self.fps = len(self.window) / sum(self.window)
