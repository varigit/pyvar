Quick Multimedia Examples
=========================

Multimedia Examples
-------------------

Convert Image
~~~~~~~~~~~~~

1. To convert an image to gray scale, see the example:

.. literalinclude:: ../examples/multimedia/convert_grayscale.py
   :language: python
   :linenos:
   :caption: **Source code**: `convert_grayscale.py`_
   :name: Convert Image
   :emphasize-lines: 3

.. _convert_grayscale.py: https://github.com/varjig/pyvarml/blob/master/examples/multimedia/convert_grayscale.py

2. The output is similar to the one below:

.. code-block:: console

    Shape: (100, 100)

+-----------------------+-----------------------+
| **Original**          | **Converted**         |
+=======================+=======================+
| |dogs|                | |dogs-converted|      |
+-----------------------+-----------------------+

.. |dogs| image:: examples/multimedia/media/dogs.jpg
   :width: 100%
   
.. |dogs-converted| image:: examples/multimedia/media/dogs-converted.jpg
   :width: 30%
