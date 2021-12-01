Getting Started
===============

Before getting started with pyvar package and learning more about its core and
examples, it is important to mention that one of the main focus of this package
is to allow the users to explore multiple Machine Learning (*ML*) applications use
cases by using displays, cameras, and user interfaces capabilities.

Hardware
--------

Recommended System on Modules (SoMs)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To achieve the best possible performance on the ML applications, it is
recommended to use the System on Modules powered by the i.MX8M Plus processor
from NXP. Check the SoMs below:

+-----------------------+-----------------------+
| `VAR-SOM-MX8M-PLUS`_  | `DART-MX8M-PLUS`_     |
+=======================+=======================+
| |var-mplus|           | |dart-mplus|          |
+-----------------------+-----------------------+

.. _VAR-SOM-MX8M-PLUS: https://www.variscite.com/product/system-on-module-som/cortex-a53-krait/var-som-mx8m-plus-nxp-i-mx-8m-plus/

.. |var-mplus| image:: images/var-som-mx8m-plus.png
   :width: 65%

.. _DART-MX8M-PLUS: https://www.variscite.com/product/system-on-module-som/cortex-a53-krait/dart-mx8m-plus-nxp-i-mx-8m-plus/

.. |dart-mplus| image:: images/dart-mx8m-plus.png
   :width: 60%

Neural Processing Unit (NPU)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The above SoMs have a dedicated unit to deal with ML inference process called
Neural Processing Unit provided by Verisilicon. This compute engine delivers
up to 2.3 Tera Operations Per Second (*TOPS*) and handles 8-bit fixed-point operations
models, allowing the user to achieve the highest performance during the inference process.

* For more information about the NPU, please check this `page`_.

.. _page: https://www.nxp.com/products/processors-and-microcontrollers/arm-processors/i-mx-applications-processors/i-mx-8-processors/i-mx-8m-plus-arm-cortex-a53-machine-learning-vision-multimedia-and-industrial-iot:IMX8MPLUS

The pyvar package is not tied to the NPU only, you can use any other SoM from the
i.MX8 family with the ML API, what changes is that the inference process runs
on the GPU/CPU instead of the NPU itself. Check the other SoMs below:

* `Other Systems on Modules`_

.. _Other Systems on Modules: https://www.variscite.com/products/system-on-module-som/?cpu_name=NXP%20iMX8

Supported Cameras
~~~~~~~~~~~~~~~~~

The pyvar package supports on its multimedia API the following cameras:

* `VCAM-5640S-DUO`_
* `VCAM-AR0821N`_
    * To use the Basler one, please see this `tutorial`_.

.. _VCAM-5640S-DUO: https://www.variscite.com/product/accessories/vcam-5640s-duo/

.. _VCAM-AR0821N: https://www.variscite.com/product/accessories/vcam-ar0821b-camera-board/

.. _tutorial: https://variwiki.com/index.php?title=MX8_Basler_Camera_NXP


Software
--------

Setting Up the BSP
~~~~~~~~~~~~~~~~~~

1. Build the latest `Yocto Release`_ with **Wayland** + **X11** features using **fsl-image-qt5 image**.

.. _Yocto Release: https://variwiki.com/

2. Flash the built image into the SD Card, boot the board, then go to next section.


Python Package Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install the pyvar package using pip3 via Pypi:

.. code-block:: console

    root@imx8mp-var-dart:~# pip3 install pyvar

1.1 To make sure that pyvar is installed, run the following command to check:

.. code-block:: console

    root@imx8mp-var-dart:~# python3
    Python 3.9.5 (default, May  3 2021, 15:11:33) 
    [GCC 10.2.0] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import pyvar
    >>>
