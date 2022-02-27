# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause
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
