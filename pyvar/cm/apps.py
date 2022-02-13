# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Class to handle Cortex-M applications.

.. moduleauthor:: Alifer Moraes <alifer.m@variscite.com>
"""

import subprocess
import sys

import serial

from .utils.helper import *


class CortexM:
    def __init__(self, core_n=0):
        self.module = get_module()
        self._validate_cm()
        self._validate_apps()
        self._num_cores = get_cm_cores(self.module)
        self.core = core_n
        self._firmware_path = CM_FIRMWARE.format(self.core)
        self._state_path = CM_STATE.format(self.core)

    def __del__(self):
        try:
            self._stop()
        except AttributeError:
            pass

    @property
    def core(self):
        return self._core

    @core.setter
    def core(self, core_n):
        if core_n >= self._num_cores:
            self._core = 0
        else:
            self._core = core_n

    @property
    def state(self):
        if os.path.isfile(self._state_path):
            with open(self._state_path, 'r') as f:
                return f.read().strip()

        return "unavailable"

    @state.setter
    def state(self, new_state):
        if (self.state == "offline" and new_state == CM_START) \
           or (self.state == "running" and new_state == CM_STOP):
            with open(self._state_path, 'w') as f:
                f.write(new_state)

    @property
    def firmware(self):
        if os.path.isfile(self._firmware_path):
            with open(self._firmware_path, 'r') as f:
                return f.read().strip()

        return "unavailable"

    @firmware.setter
    def firmware(self, new_firmware):
        if os.path.isfile(self._firmware_path):
            with open(self._firmware_path, 'w') as f:
                f.write(new_firmware)

    def run(self, app):
        if app in self.apps:
            self._stop()
            self._load(app)
            self._start()
        else:
            print(f"{app} is not a valid Cortex-M app.")

    @staticmethod
    def write(message):
        if os.path.exists(CM_TTY):
            with serial.Serial(CM_TTY) as ser:
                len = ser.write(f"{message}\n".encode())
                msg = ser.readline(len).decode().strip()
                print(f"Message read from Cortex-M: {msg}")
        else:
            print(f"Device not found: {CM_TTY}.")

    @staticmethod
    def read():
        if os.path.exists(CM_TTY):
            with serial.Serial(CM_TTY, timeout=10) as ser:
                msg = ser.readline().decode().strip()
                print(f"Message read from Cortex-M: {msg}")
        else:
            print(f"Device not found: {CM_TTY}.")

    def _validate_cm(self):
        if not is_cm_enabled():
            sys.exit(f"Error: {CM_REMOTEPROC_DIR} not found.\n"
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
        self.state = CM_START
        subprocess.run(['modprobe', 'imx_rpmsg_tty'])

    def _load(self, app):
        self.firmware = app

    def _stop(self):
        self.state = CM_STOP
        subprocess.run(['modprobe', 'imx_rpmsg_tty', '-r'])
