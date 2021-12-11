# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Python Class to calculate time.

.. moduleauthor:: Diego Dorta <diego.d@variscite.com>
"""

from contextlib import contextmanager
from datetime import timedelta
from time import perf_counter


class Timer:
    def __init__(self):
        """
        Constructor method for the Timer class.
        """
        self.time = 0

    @contextmanager
    def timeit(self):
        """
        Calculates the time and save it in the **time** attribute.
        """
        begin = perf_counter()
        try:
            yield
        finally:
            end = perf_counter()
            self.__convert(end - begin)

    def __convert(self, elapsed):
        """
        Convert time from monotonic to seconds.
        """
        self.time = str(timedelta(seconds=elapsed))
