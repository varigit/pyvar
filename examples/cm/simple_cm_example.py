# Copyright 2022 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

from time import sleep

from pyvar.cm.apps import CortexM

cortex = CortexM()

print("Available Cortex-M apps:")

for app in cortex.apps:
    print(app)

print("Running cm_rpmsg_lite_str_echo...")

for app in cortex.apps:
    if "cm_rpmsg_lite_str_echo" in app:
        cortex.run(app)
        break

while True:
    msg = input(str("Write a message to the Cortex-M: "))
    cortex.write(msg)

    if msg == "quit":
        break

cortex.stop()