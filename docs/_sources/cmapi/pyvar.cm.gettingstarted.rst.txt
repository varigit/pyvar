Cortex-M API: Getting Started
=============================

Introduction
------------

The Cortex-M API provides a set of functions and methods to help run and communicate
with Cortex-M applications from the Cortex-A side.

Software
--------

Setting Up the BSP
~~~~~~~~~~~~~~~~~~

#. Build the latest `Yocto Release`_, make sure to add the following lines at your **local.conf** file:

    .. code-block:: bash

        IMAGE_INSTALL_append = " \
            python3-pip \
        "

.. _Yocto Release: https://variwiki.com/

1. Flash the built image into the SD Card, boot the board, then go to the next section.


Python API Package Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. To install the pyvar API Python package use the pip3 tool to retrieve via Pypi:

    .. code-block:: console

        root@imx8mp-var-dart:~# pip3 install pyvar

2. To make sure that pyvar is installed, run the following command to check:

    .. code-block:: console

        root@imx8mp-var-dart:~# python3
        Python 3.9.5 (default, May  3 2021, 15:11:33)
        [GCC 10.2.0] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>> from pyvar import cm
        >>>

Quick Example
~~~~~~~~~~~~~

See this quick example to run a Cortex-M application using the Cortex-M API:

    .. code-block:: python

        1  # Import the Cortex-M class from pyvar
        2  from pyvar.cm.core import CortexM
        3
        4  # Create the object
        5  cortex = CortexM()
        6
        7  # List all the available applications
        8  cortex.firmwares
        9
        10 # Run the firmware (It must exists in the listed firmwares)
        11 cortex.run("firmware_name")
        12
        13 # Destroy the object
        14 cortex.destroy()
