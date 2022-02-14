# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from pyvar.cm.core import CortexM

cortex = CortexM()

print("Available Cortex-M apps:")
for firmware in cortex.firmwares:
    print(firmware)

for firmware in cortex.firmwares:
    if "cm_rpmsg_lite_str_echo" in firmware:
        print("Running cm_rpmsg_lite_str_echo...")
        cortex.run(firmware)
        break

while True:
    msg = input(str("Write a message to the Cortex-M: "))
    cortex.write(msg)

    if msg == "quit":
        break
