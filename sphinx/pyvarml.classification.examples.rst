Classification Examples
=======================

The classification examples use a quantized starter model from `TensorFlow Lite`_.

.. _TensorFlow Lite: https://www.tensorflow.org/lite/guide/hosted_models

Image Classification
--------------------

Run the Image Classification Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varjig/pyvarml/raw/master/examples/classification/image_classification.py

.. code-block:: bash

    python3 image_classification.py

2. The output should be similar as the one below:

+------------------------------+------------------------------+
| **Image Example**            | **Image Example Classified** |
+==============================+==============================+
| |car|                        | |car-converted|              |
+------------------------------+------------------------------+

.. |car| image:: examples/classification/media/car.jpg
   :width: 100%
   
.. |car-converted| image:: examples/classification/media/car_classified.jpg
   :width: 100%

.. literalinclude:: ../examples/classification/image_classification.py
   :language: python
   :linenos:
   :caption: **Image Classification Example Source Code**: `image_classification.py`_
   :name: Image Classification Example

.. _image_classification.py: https://github.com/varjig/pyvarml/blob/master/examples/classification/image_classification.py

|
|
|

Video Classification
--------------------

Run the Video Classification Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varjig/pyvarml/raw/master/examples/classification/video_classification.py

.. code-block:: bash

    python3 video_classification.py

2. The output should be similar as the one below:

+------------------------------+------------------------------+
| **Video Example**            | **Video Example Classified** |
+==============================+==============================+
| |street|                     | |street-classified|          |
+------------------------------+------------------------------+

.. |street| image:: examples/classification/media/street_video.gif
   :width: 100%

.. |street-classified| image:: examples/classification/media/street_classified_video.gif
   :width: 100%

.. literalinclude:: ../examples/classification/video_classification.py
   :language: python
   :linenos:
   :caption: **Video Classification Example Source code**: `video_classification.py`_
   :name: Video Classification Example

.. _video_classification.py: https://github.com/varjig/pyvarml/blob/master/examples/classification/video_classification.py

|
|
|

Real Time Classification
------------------------

Run the Real Time Classification Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varjig/pyvarml/raw/master/examples/classification/realtime_classification.py

.. code-block:: bash

    python3 realtime_classification.py

.. literalinclude:: ../examples/classification/realtime_classification.py
   :language: python
   :linenos:
   :caption: **Real Time Classification Example Source code**: `realtime_classification.py`_
   :name: Real Time Classification Example

.. _realtime_classification.py: https://github.com/varjig/pyvarml/blob/master/examples/classification/realtime_classification.py---
