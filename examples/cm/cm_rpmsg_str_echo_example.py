# Copyright 2022-2023 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

"""
The following code is a Python script that interacts with a Cortex-M
microcontroller using the PyVar library. The script searches for a firmware
called "cm_rpmsg_lite_str_echo" and runs it on the Cortex-M. It then prompts
the user to input a message that will be sent to the Cortex-M and displayed
on its terminal. The program will continue to prompt for input until the user
types "quit".
"""

import sys

from pyvar.cm.core import CortexM


def main():
    cortex = CortexM()
    fw = None

    for firmware in cortex.firmwares:
        if "str_echo" in firmware:
            fw = firmware
            break

    if not fw:
        sys.exit("The cm_rpmsg_lite_str_echo firmware was not found.")

    print(f"Running {fw}...")
    cortex.run(fw)

    while True:
        msg = input(str("Write a message to the Cortex-M: "))
        cortex.write(msg)

        if msg == "quit":
            break


if __name__ == "__main__":
    main()
