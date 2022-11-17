Detection Examples
==================

The detection examples use a quantized starter model from `TensorFlow Lite`_:

* **ssd_mobilenet_v1_1_default_1.zip**.

.. _TensorFlow Lite: https://www.tensorflow.org/lite/examples/object_detection/overview

Image Detection Example
-----------------------

Run the Image Detection Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varigit/pyvar/raw/master/examples/ml/detection/image_detection_tflite.py

.. code-block:: bash

    python3 image_detection_tflite.py

2. The output should be similar as the one below:

+--------------------------------+--------------------------------+
| **Image Example**              | **Image Example Detected**     |
+================================+================================+
| |street-people|                | |street-people_detected|       |
+--------------------------------+--------------------------------+

.. |street-people| image:: ../../examples/ml/detection/media/street.png
   :width: 100%

.. |street-people_detected| image:: ../../examples/ml/detection/media/street_detected.png
   :width: 100%

.. literalinclude:: ../../../examples/ml/detection/image_detection_tflite.py
   :language: python
   :linenos:
   :caption: **Image Detection Example Source code**: `image_detection_tflite.py`_
   :name: Image Detection Example

.. _image_detection_tflite.py: https://github.com/varigit/pyvar/blob/master/examples/ml/detection/image_detection_tflite.py

|
|
|

Video Detection
---------------

Run the Video Detection Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varigit/pyvar/raw/master/examples/ml/detection/video_detection_tflite.py

.. code-block:: bash

    python3 video_detection_tflite.py

2. The output should be similar as the one below:

+------------------------------+------------------------------+
| **Video Example**            | **Video Example Detected**   |
+==============================+==============================+
| |street|                     | |street_detected|            |
+------------------------------+------------------------------+

.. |street| image:: ../../examples/ml/detection/media/street_video.gif
   :width: 100%

.. |street_detected| image:: ../../examples/ml/detection/media/street_detected_video.gif
   :width: 100%

.. literalinclude:: ../../../examples/ml/detection/video_detection_tflite.py
   :language: python
   :linenos:
   :caption: **Video Detection Example Source code**: `video_detection_tflite.py`_
   :name: Video Detection Example

.. _video_detection_tflite.py: https://github.com/varigit/pyvar/blob/master/examples/ml/detection/video_detection_tflite.py

|
|
|

Real Time Detection
-------------------

Run the Real Time Detection Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varigit/pyvar/raw/master/examples/ml/detection/realtime_detection_tflite.py

.. code-block:: bash

    python3 realtime_detection_tflite.py
    
.. literalinclude:: ../../../examples/ml/detection/realtime_detection_tflite.py
   :language: python
   :linenos:
   :caption: **Real Time Detection Example Source code**: `realtime_detection_tflite.py`_
   :name: Real Time Detection Example

.. _realtime_detection_tflite.py: https://github.com/varigit/pyvar/blob/master/examples/ml/detection/realtime_detection_tflite.py
