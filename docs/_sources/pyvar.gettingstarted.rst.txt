Getting Started
===============

For Machine Learning API
------------------------

Setting Up the Hardware and the BSP
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. To use the Machine Learning API make sure to have one of the following supported SoMs:

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

2. Follow the quick instructions below to build the latest Yocto Release. 

* For more information on how to build BSP from source code go to the Variscite `Wiki`_ page.
* The API supports `VCAM-5640S-DUO`_ and `VCAM-AR0821N`_. To use the Basler one, please see this `tutorial`_.

.. _Wiki: https://variwiki.com/

.. _tutorial: https://variwiki.com/index.php?title=MX8_Basler_Camera_NXP

.. _VCAM-5640S-DUO: https://www.variscite.com/product/accessories/vcam-5640s-duo/

.. _VCAM-AR0821N: https://www.variscite.com/product/accessories/vcam-ar0821b-camera-board/

2.1 Retrieve the latest revision:

.. code-block:: console

    $ repo init -u https://github.com/varigit/variscite-bsp-platform.git \
                -b fsl-hardknott -m imx-5.10.35-2.0.0-var01.xml
    $ repo sync -j$(nproc)

2.2 Build XWayland GUI demo image, and launch the bitbake to build the image:

.. code-block:: console

    $ MACHINE=imx8mp-var-dart DISTRO=fsl-imx-xwayland . var-setup-release.sh \
                              -b build_xwayland
    $ bitbake fsl-image-qt5

3. Flash the image into the SD Card, boot the board, then go to next section.

Quick Python Package Instalation
--------------------------------

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
