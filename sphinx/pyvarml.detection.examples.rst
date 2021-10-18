Detection Examples
==================

The detection examples use a quantized starter model from `TensorFlow Lite`_.

.. _TensorFlow Lite: https://www.tensorflow.org/lite/examples/object_detection/overview

Image Detection Example
-----------------------

Run the Image Detection Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varjig/pyvarml/raw/master/examples/detection/image_detection.py

.. code-block:: bash

    python3 image_detection.py

2. The output should be similar as the one below:

+--------------------------------+--------------------------------+
| **Image Example**              | **Image Example Detected**     |
+================================+================================+
| |street-people|                | |street-people_detected|       |
+--------------------------------+--------------------------------+

.. |street-people| image:: examples/detection/media/street.png
   :width: 100%

.. |street-people_detected| image:: examples/detection/media/street_detected.png
   :width: 100%

.. literalinclude:: ../examples/detection/image_detection.py
   :language: python
   :linenos:
   :caption: **Image Detection Example Source code**: `image_detection.py`_
   :name: Image Detection Example

.. _image_detection.py: https://github.com/varjig/pyvarml/blob/master/examples/detection/image_detection.py

|
|
|

Video Detection
---------------

Run the Video Detection Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varjig/pyvarml/raw/master/examples/detection/video_detection.py

.. code-block:: bash

    python3 video_detection.py

2. The output should be similar as the one below:

+------------------------------+------------------------------+
| **Video Example**            | **Video Example Detected**   |
+==============================+==============================+
| |street|                     | |street_detected|            |
+------------------------------+------------------------------+

.. |street| image:: examples/detection/media/street_video.gif
   :width: 100%

.. |street_detected| image:: examples/detection/media/street_detected_video.gif
   :width: 100%

.. literalinclude:: ../examples/detection/video_detection.py
   :language: python
   :linenos:
   :caption: **Video Detection Example Source code**: `video_detection.py`_
   :name: Video Detection Example

.. _video_detection.py: https://github.com/varjig/pyvarml/blob/master/examples/detection/video_detection.py

|
|
|

Real Time Detection
-------------------

Run the Real Time Detection Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varjig/pyvarml/raw/master/examples/detection/realtime_detection.py

.. code-block:: bash

    python3 realtime_detection.py
    
.. literalinclude:: ../examples/detection/realtime_detection.py
   :language: python
   :linenos:
   :caption: **Real Time Detection Example Source code**: `realtime_detection.py`_
   :name: Real Time Detection Example

.. _realtime_detection.py: https://github.com/varjig/pyvarml/blob/master/examples/detection/realtime_detection.py
