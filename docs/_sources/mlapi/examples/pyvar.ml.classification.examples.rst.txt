Classification Examples
=======================

The classification examples use a quantized starter model from `TensorFlow Lite`_:

* i.MX 8M Plus:
    * mobilenet_v1_1.0_224_quant.tflite
    * mobilenet_v2_1.0_224_quant.tflite

.. _TensorFlow Lite: https://www.tensorflow.org/lite/guide/hosted_models

Image Classification
--------------------

Run the Image Classification Example on MPlus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varigit/pyvar/raw/master/examples/ml/classification/image_classification_tflite.py

.. code-block:: bash

    python3 image_classification_tflite.py

2. The output should be similar as the one below:

+------------------------------+------------------------------+
| **Image Example**            | **Image Example Classified** |
+==============================+==============================+
| |car-plus|                   | |car-converted-plus|         |
+------------------------------+------------------------------+

.. |car-plus| image:: ../../examples/ml/classification/media/car.jpg
   :width: 100%
   
.. |car-converted-plus| image:: ../../examples/ml/classification/media/car_classified.jpg
   :width: 100%

.. literalinclude:: ../../../examples/ml/classification/image_classification_tflite.py
   :language: python
   :linenos:
   :caption: **Image Classification Example Source Code for MPlus**: `image_classification_tflite.py`_
   :name: Image Classification Example MPlus

.. _image_classification_tflite.py: https://github.com/varigit/pyvar/blob/master/examples/ml/classification/image_classification_tflite.py

|
|
|

Video Classification
--------------------

Run the Video Classification Example on MPlus
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varigit/pyvar/raw/master/examples/ml/classification/video_classification_tflite.py

.. code-block:: bash

    python3 video_classification_tflite.py

2. The output should be similar as the one below:

+------------------------------+------------------------------+
| **Video Example**            | **Video Example Classified** |
+==============================+==============================+
| |street-plus|                | |street-classified-plus|     |
+------------------------------+------------------------------+

.. |street-plus| image:: ../../examples/ml/classification/media/street_video.gif
   :width: 100%

.. |street-classified-plus| image:: ../../examples/ml/classification/media/street_classified_video.gif
   :width: 100%

.. literalinclude:: ../../../examples/ml/classification/video_classification_tflite.py
   :language: python
   :linenos:
   :caption: **Video Classification Example Source code for MPlus**: `video_classification_tflite.py`_
   :name: Video Classification Example MPlus

.. _video_classification_tflite.py: https://github.com/varigit/pyvar/blob/master/examples/ml/classification/video_classification_tflite.py

|
|
|

Real Time Classification
------------------------

Run the Real Time Classification Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varigit/pyvar/raw/master/examples/ml/classification/realtime_classification_tflite.py

.. code-block:: bash

    python3 realtime_classification_tflite.py

.. literalinclude:: ../../../examples/ml/classification/realtime_classification_tflite.py
   :language: python
   :linenos:
   :caption: **Real Time Classification Example Source code**: `realtime_classification_tflite.py`_
   :name: Real Time Classification Example

.. _realtime_classification_tflite.py: https://github.com/varigit/pyvar/blob/master/examples/ml/classification/realtime_classification_tflite.py
