Multimedia API: Getting Started
===============================

Introduction
------------

The Multimedia API provides a set o classes and functions to provide an easy way
write multimedia applications for the Variscite's SoMs, such as capturing and
displaying images using cameras, playing videos, and so on.

Hardware
--------

Supported Cameras
~~~~~~~~~~~~~~~~~

The pyvar package supports on its `Multimedia API`_ the following cameras:

* `VCAM-5640S-DUO`_;
* `VCAM-AR0821N`_. To use the Basler one, please see this `tutorial`_.

.. _VCAM-5640S-DUO: https://www.variscite.com/product/accessories/vcam-5640s-duo/

.. _VCAM-AR0821N: https://www.variscite.com/product/accessories/vcam-ar0821b-camera-board/

.. _tutorial: https://variwiki.com/index.php?title=MX8_Basler_Camera_NXP

.. _Multimedia API: https://python.variscite.com/multimediaapi/pyvar.multimedia.html

See this quick example to open a camera using the multimedia API:

    .. code-block:: python

        1  # Import the multimedia API from pyvar
        2  from pyvar.multimedia.helper import Multimedia
        3
        4  # Create the object specifying the source (video or camera), and the resolution.
        5  foo = Multimedia(source="/dev/video1", resolution="hd")
        6
        7  # Set the v4l2 configuration.
        8  foo.set_v4l2_config()
        9
        10 # Create a loop to read the frames
        11 while foo.loop:
        12        # Read the frame
        13        frame = foo.get_frame()
        14        # do something with the frame, for instance: ML inference.
        15        ...
        16        # Show the frame
        17        foo.show("Camera Example", frame)
        18
        19 # Destroy the camera object
        20 foo.destroy()

Software
--------

Setting Up the BSP
~~~~~~~~~~~~~~~~~~

#. Build the latest `Yocto Release`_ with **Wayland** + **X11** features using **fsl-image-qt5** image;

    **NOTE**: To use the **fsl-image-gui** image, make sure to add the following lines at your **local.conf** file:

    .. code-block:: bash

        OPENCV_PKGS_imxgpu = " \
           python3-opencv \
        "

        IMAGE_INSTALL_append_mx8 = " \
            ${OPENCV_PKGS} \
        "

.. _Yocto Release: https://variwiki.com/

1. Flash the built image into the SD Card, boot the board, then go to next section.

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
        >>> from pyvar import multimedia
        >>>
