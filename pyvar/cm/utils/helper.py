# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Module with miscellaneous functions for Cortex-M.

.. moduleauthor:: Alifer Moraes <alifer.m@variscite.com>
"""

import os
import subprocess

from .config import *


def is_cm_enabled():
    """
    Check if the Cortex-M is enabled.

    Returns:
        if **enabled**, return **True**
        if **not**, return **not False**
    """
    return True if os.listdir(CM_REMOTEPROC_DIR) else False


def get_module():
    """
    Get the SoM type.

    Returns:
        A string containing the SoM's type.
    """
    if not os.path.exists(MACHINE):
        return None

    with open(MACHINE, 'r') as machine:
        module = machine.read().lower()

    if "var-som" in module:
        return "som"
    elif "dart-mx8" in module:
        return "dart"
    elif "spear-mx8" in module:
        return "spear"
    else:
        return "unknown"


def get_cm_cores(module):
    """
    Get the number of Cortex-M cores.

    Returns:
        An integer number of cores.
    """
    return int(_parse_cm_info(module, 'cm_cores'))


def get_cm_dtb(module):
    """
    Get the DTB file that enables the Cortex-M.

    Returns:
        A string with the name of the DTB file.
    """
    return _parse_cm_info(module, f'cm_dtb_{get_module()}')


def _parse_cm_info(module, field):
    """
    Get information about the Cortex-M from the variscite-rproc.conf file.

    Args:
        module (str): the SoM type;
        field (str): a field of the variscite-rproc.conf file;

    Returns:
        A string with the required field value.
    """
    if not module or not os.path.isfile(CM_CONF_FILE):
        return None

    with open(CM_CONF_FILE, 'r') as f:
        for line in f.readlines():
            if field in line.lower():
                val = line.strip().split('=').pop()

                return val.replace('\"', '')


def _firmware_check(file):
    """
    Check if a file is a valid Cortex-M firmware.

    Args:
        file (str): path to the file;

    Returns:
        if **is valid**, return **True**
        if **not**, return **not False**
    """
    out = subprocess.run(['file', '-b', file], capture_output=True)
    out = out.stdout.decode().strip().lower()

    return "arm, eabi" in out


def list_firmwares():
    """
    List all the valid Cortex-M firmwares under the firmware directory.

    Returns:
        A list containing the valid firmwares
    """
    firmwares_list = []

    if os.path.isdir(CM_FIRMWARE_DIR):
        for file in os.listdir(CM_FIRMWARE_DIR):
            if _firmware_check(os.path.join(CM_FIRMWARE_DIR, file)):
                firmwares_list.append(file)

    return firmwares_list
