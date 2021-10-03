Classification Examples
=======================

.. NOTE::
    The classification examples use a starter quantized model from `TensorFlow Lite`_.

.. _TensorFlow Lite: https://www.tensorflow.org/lite/guide/hosted_models

Image Classification Example
----------------------------

1. To create a simple image classification, see the example:

.. literalinclude:: examples/classification/image_classification.py
   :language: python
   :linenos:
   :caption: **Source code**: `image_classification.py`_
   :name: Image Classification Example
   :emphasize-lines: 18

.. _image_classification.py: https://github.com/varjig/pyvarml/blob/master/sphinx/examples/classification/image_classification.py

2. See the result:

+------------------------+------------------------+
| **Example**            | **Example Classified** |
+========================+========================+
| |car|                  | |car-converted|        |
+------------------------+------------------------+

.. |car| image:: examples/classification/media/car.jpg
   :width: 100%
   
.. |car-converted| image:: examples/classification/media/car_classified.jpg
   :width: 100%


Video Classification Example
----------------------------

1. To create a simple video classification, see the example:

.. literalinclude:: examples/classification/video_classification.py
   :language: python
   :linenos:
   :caption: **Source code**: `video_classification.py`_
   :name: Video Classification Example
   :emphasize-lines: 19

.. _video_classification.py: https://github.com/varjig/pyvarml/blob/master/sphinx/examples/classification/video_classification.py

2. See the result:

+------------------------+------------------------+
| **Example**            | **Example Classified** |
+========================+========================+
| |street|               | |street-classified|    |
+------------------------+------------------------+

.. |street| image:: examples/classification/media/street_video.gif
   :width: 100%

.. |street-classified| image:: examples/classification/media/street_classified_video.gif
   :width: 100%

Real Time Classification Example
--------------------------------

1. To create a simple real time classification, see the example:

.. literalinclude:: examples/classification/realtime_classification.py
   :language: python
   :linenos:
   :caption: **Source code**: `realtime_classification.py`_
   :name: Real Time Classification Example
   :emphasize-lines: 20

.. _realtime_classification.py: https://github.com/varjig/pyvarml/blob/master/sphinx/examples/classification/realtime_classification.py

User Interface Example
----------------------


