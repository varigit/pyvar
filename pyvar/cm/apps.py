# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Class to handle Cortex-M applications.

.. moduleauthor:: Alifer Moraes <alifer.m@variscite.com>
"""

import sys

import serial

from .utils.helper import *


class CortexM:
    def __init__(self):
        self.module = get_module()
        self.state = STATE
        self.firmware = FIRMWARE
        self._validate_cm()
        self._validate_apps()

    def run(self, app):
        if app in self.apps:
            self._stop()
            self._load(app)
            self._start()
        else:
            print(f"{app} is not a valid Cortex-M app.")

    def stop(self):
        self._stop()

    @staticmethod
    def write(message):
        if os.path.exists(TTY):
            with serial.Serial(TTY) as ser:
                len = ser.write(f"{message}\n".encode())
                msg = ser.readline(len).decode().strip()
                print(f"Message read from Cortex-M: {msg}")
        else:
            print(f"Device not found: {TTY}.")

    @staticmethod
    def read():
        if os.path.exists(TTY):
            with serial.Serial(TTY, timeout=10) as ser:
                msg = ser.readline().decode().strip()
                print(f"Message read from Cortex-M: {msg}")
        else:
            print(f"Device not found: {TTY}.")

    def _validate_cm(self):
        if not is_cm_enabled():
            sys.exit(f"Error: {REMOTEPROC_DIR} not found.\n"
                     f"Please enable remoteproc driver.\n"
                     f"Most likely you need to use the correct"
                     f" device tree, try to run:\n"
                     f"fw_setenv fdt_file {get_cm_dtb(self.module)}"
                     f" && reboot")

    def _validate_apps(self):
        self.apps = []
        apps_list = list_apps()

        if self.module == 'dart' or self.module == 'som':
            for app in apps_list:
                if self.module in app.lower():
                    self.apps.append(app)

    def _start(self):
        if os.path.isfile(self.state):
            with open(self.state, 'r+') as f:
                if "offline" in f.read():
                    f.write("start")
                    f.truncate()

            os.system('modprobe imx_rpmsg_tty')

    def _load(self, app):
        if os.path.isfile(self.firmware):
            with open(self.firmware, 'w') as f:
                f.write(app)

    def _stop(self):
        if os.path.isfile(self.state):
            os.system('modprobe imx_rpmsg_tty -r')

            with open(self.state, 'r+') as f:
                if "running" in f.read():
                    f.write("stop")
                    f.truncate()
