Quick Utils Examples
====================

Utils Examples
--------------

Retrieve from Variscite FTP
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. To retrieve a specific ML model from Variscite's FTP server, see the example:

.. code-block:: python

    from pyvarml.utils.retriever import FTP

    foo = FTP()

    package_dir = "pyvarml/classification/"
    package_filename = "mobilenet_v1_1.0_224_quant.zip"

    if foo.retrieve_package(package_dir, package_filename):
        print(f"Model: {foo.model}")
        print(f"Label: {foo.label}")

2. The output is similar to the one below:

.. code-block:: console

    Model: ['/home/venus/.cache/pyvarml/mobilenet_v1_1.0_224_quant/mobilenet_v1_1.0_224_quant.tflite']
    Label: ['/home/venus/.cache/pyvarml/mobilenet_v1_1.0_224_quant/labels_mobilenet_quant_v1_224.txt']

.. NOTE::
    Check the available model packages file at the `FTP`_  from Variscite.

.. _FTP: ftp://customerv:Variscite1@ftp.variscite.com/pyvarml

Retrieve from Other FTP
~~~~~~~~~~~~~~~~~~~~~~~

1. To retrieve other model packages files from other FTP, see the example:

.. code-block:: python

    from pyvarml.utils.retriever import FTP

    foo = FTP(host="ftp_host_link", user="ftp_user", passwd="ftp_passwd")
    
    ...

.. IMPORTANT::
    The current version only supports packages in (.zip) format.

Calculate Time
~~~~~~~~~~~~~~

1. To calculate the time, see the example:

.. code-block:: python

    from pyvarml.utils.timer import Timer
    
    foo = Timer()
    with foo.timeit():
        ...
    
    print(f"Time: {foo.time}")

2. The output is similar to the one below:

.. code-block:: console
 
    Time: 0:00:03.000196

Convert Image
~~~~~~~~~~~~~

1. To convert an image to gray scale, see the example:

.. code-block:: python

    from pyvarml.utils.helper import Images

    foo = Images("dogs.jpg")

    foo.convert_rgb_to_gray_scale(100, 100, False)

    print(f"Shape: {foo.converted.shape}")

2. The output is similar to the one below:

.. code-block:: console

    Shape: (100, 100)

+-----------------------+-----------------------+
| **Original**          | **Converted**         |
+=======================+=======================+
| |dogs|                | |dogs-converted|      |
+-----------------------+-----------------------+

.. |dogs| image:: images/dogs.jpg
   :width: 60%
   
.. |dogs-converted| image:: images/dogs-converted.jpg
   :width: 30%
