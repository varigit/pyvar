# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
:platform: Unix/Yocto
:synopsis: Module with miscellaneous functions for Cortex-M.

.. moduleauthor:: Alifer Moraes <alifer.m@variscite.com>
"""

import os

from .config import *


def is_cm_enabled():
    return True if os.listdir(CM_REMOTEPROC_DIR) else False


def get_module():
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
    return int(_parse_cm_info(module, 'cm_cores'))


def get_cm_dtb(module):
    return _parse_cm_info(module, f'cm_dtb_{get_module()}')


def _parse_cm_info(module, field):
    if not module or not os.path.isfile(CM_CONF_FILE):
        return None

    with open(CM_CONF_FILE, 'r') as f:
        for line in f.readlines():
            if field in line.lower():
                val = line.strip().split('=').pop()

                return val.replace('\"', '')


def list_apps():
    apps_list = []

    if os.path.isdir(CM_FIRMWARE_DIR):
        for file in os.listdir(CM_FIRMWARE_DIR):
            if ".elf" not in file.lower():
                continue

            apps_list.append(file)

    return apps_list
