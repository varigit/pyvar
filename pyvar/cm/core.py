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
    """
    :ivar module: SoM type;
    :ivar core: Cortex-M core being used;
    :ivar tty_rpmsg: virtual port to communicate with rpmsg applications;
    :ivar firmwares: list all the available Cortex-M firmwares;
    """

    def __init__(self, core_n=0, tty_offset=3):
        """
        Constructor method for the Cortex-M class.
        """
        self.module = get_module()
        self._validate_cm()
        self._validate_firmwares()
        self._num_cores = get_cm_cores(self.module)
        self.core = core_n
        self.tty_rpmsg = CM_TTY.format(tty_offset, self.core)
        self._firmware_path = CM_FIRMWARE.format(self.core)
        self._state_path = CM_STATE.format(self.core)

    def __del__(self):
        """
        Destructor method for the Cortex-M class.
        """
        try:
            self._stop()
        except AttributeError:
            pass

    @property
    def core(self):
        """
        Get which Cortex-M core is being used.

        Returns:
            An integer representing the Cortex-M core.
        """
        return self._core

    @core.setter
    def core(self, core_n):
        """
        Set which Cortex-M core is going to be used.

        Args:
            core_n (int): index of the Cortex-M core.
        """
        if core_n >= self._num_cores:
            self._core = 0
        else:
            self._core = core_n

    @property
    def state(self):
        """
        Get the current Cortex-M state.

        Returns:
            A string containing the Cortex-M state.
        """
        if os.path.isfile(self._state_path):
            with open(self._state_path, 'r') as f:
                return f.read().strip()

        return "unavailable"

    @state.setter
    def state(self, new_state):
        """
        Set the Cortex-M state.

        Args:
            new_state (str): the state the Cortex-M is going to be set.
        """
        if (self.state == "offline" and new_state == CM_START) \
           or (self.state == "running" and new_state == CM_STOP):
            with open(self._state_path, 'w') as f:
                f.write(new_state)

    @property
    def firmware(self):
        """
        Get the current Cortex-M firmware.

        Returns:
            A string containing the Cortex-M firmware.
        """
        if os.path.isfile(self._firmware_path):
            with open(self._firmware_path, 'r') as f:
                return f.read().strip()

        return "unavailable"

    @firmware.setter
    def firmware(self, new_firmware):
        """
        Set the Cortex-M firmware.

        Args:
            new_firmware (str): the firmware that is going
            to be loaded into the Cortex-M.
        """
        if os.path.isfile(self._firmware_path):
            with open(self._firmware_path, 'w') as f:
                f.write(new_firmware)

    def run(self, firmware):
        """
        Run a given firmware into the Cortex-M.

        Args:
            firmware (str): the firmware that is going
            to run into the Cortex-M.
        """
        if firmware in self.firmwares:
            self._stop()
            self._load(firmware)
            self._start()
        else:
            print(f"{firmware} is not a valid Cortex-M app.")

    def write(self, message):
        """
        Send a message to a Cortex-M application via virtual serial port.

        Args:
            message (str): message the is going to be sent.
        """
        if os.path.exists(self.tty_rpmsg):
            with serial.Serial(self.tty_rpmsg) as ser:
                msg_len = ser.write(f"{message}\n".encode())
                msg = ser.readline(msg_len).decode().strip()
                print(f"Message read from Cortex-M: {msg}")
        else:
            print(f"Device not found: {self.tty_rpmsg}.")

    def read(self):
        """
        Reads a message from a Cortex-M application via virtual serial port.
        """
        if os.path.exists(self.tty_rpmsg):
            with serial.Serial(self.tty_rpmsg, timeout=10) as ser:
                msg = ser.readline().decode().strip()
                print(f"Message read from Cortex-M: {msg}")
        else:
            print(f"Device not found: {self.tty_rpmsg}.")

    def _validate_cm(self):
        """
        Checks if Cortex-M is available.
        """
        if not is_cm_enabled():
            sys.exit(f"Error: {CM_REMOTEPROC_DIR} not found.\n"
                     f"Please enable remoteproc driver.\n"
                     f"Most likely you need to use the correct"
                     f" device tree, try to run:\n"
                     f"fw_setenv fdt_file {get_cm_dtb(self.module)}"
                     f" && reboot")

    def _validate_firmwares(self):
        """
        Checks which files in the firmware directory
        are valid Cortex-M firmwares.
        """
        self.firmwares = []
        firmwares_list = list_firmwares()

        if self.module == 'dart' or self.module == 'som':
            for firmware in firmwares_list:
                if self.module in firmware.lower():
                    self.firmwares.append(firmware)

    def _start(self):
        """
        Start the Cortex-M application and loads
        the imx_rpms_tty kernel module.
        """
        self.state = CM_START
        subprocess.run(['modprobe', 'imx_rpmsg_tty'])

    def _load(self, firmware):
        """
        Set the Cortex-M firmware.

        Args:
            firmware (str): the firmware that is
            going to be loaded into the Cortex-M.
        """
        self.firmware = firmware

    def _stop(self):
        """
        Stop the Cortex-M application and removes
        the imx_rpms_tty kernel module.
        """
        self.state = CM_STOP
        subprocess.run(['modprobe', 'imx_rpmsg_tty', '-r'])
