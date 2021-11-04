Quick Utils Examples
====================

Utils Examples
--------------

Retrieve from Variscite FTP
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. To retrieve a specific ML model from Variscite's FTP server, see the example:

.. literalinclude:: ../examples/utils/variscite_ftp.py
   :language: python
   :linenos:
   :caption: **Source code**: `variscite_ftp.py`_
   :name: Retrieve from Variscite FTP
   :emphasize-lines: 5

.. _variscite_ftp.py: https://github.com/varjig/pyvarml/blob/master/examples/utils/variscite_ftp.py

2. The output is similar to the one below:

.. code-block:: console

    Model: ~/.cache/pyvarml/mobilenet_v1_1.0_224_quant/mobilenet_v1_1.0_224_quant.tflite
    Label: ~/.cache/pyvarml/mobilenet_v1_1.0_224_quant/labels_mobilenet_quant_v1_224.txt

.. NOTE::
    Check the available model packages file at the `FTP`_  from Variscite.

.. _FTP: ftp://customerv:Variscite1@ftp.variscite.com/pyvarml

Retrieve from Other FTP
~~~~~~~~~~~~~~~~~~~~~~~

1. To retrieve other model packages files from other FTP, see the example:

.. literalinclude:: ../examples/utils/other_ftp.py
   :language: python
   :linenos:
   :caption: **Source code**: `other_ftp.py`_
   :name: Retrieve from Other FTP

.. _other_ftp.py: https://github.com/varjig/pyvarml/blob/master/examples/utils/other_ftp.py

.. IMPORTANT::
    The current version only supports packages in (.zip) format.

Calculate Time
~~~~~~~~~~~~~~

1. To calculate the time, see the example:

.. literalinclude:: ../examples/utils/calculate_time.py
   :language: python
   :linenos:
   :caption: **Source code**: `calculate_time.py`_
   :name: Calculate Time

.. _calculate_time.py: https://github.com/varjig/pyvarml/blob/master/examples/utils/calculate_time.py

2. The output is similar to the one below:

.. code-block:: console
 
    Time: 0:00:03.000196
