User Interface Examples
=======================

Detection User Interface
------------------------

Run the Detection User Interface Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Retrieve the example, and execute it on the SoM:

.. code-block:: bash

    curl -LJO https://github.com/varigit/pyvar/raw/master/examples/ml/detection/ui_detection.py

.. code-block:: bash

    python3 ui_detection.py

2. The output should be similar as the one below:

+--------------------------------+
| **User Interface Example**     |
+================================+
| |ui_objects|                   |
+--------------------------------+

.. |ui_objects| image:: ../../examples/ml/detection/media/ui_objects.png
   :width: 100%

+--------------------------------+
| **User Interface Options**     |
+================================+
| |ui_options|                   |
+--------------------------------+

.. |ui_options| image:: ../../examples/ml/detection/media/ui_options.png
   :width: 100%
   
+--------------------------------+
| **User Interface Detected**    |
+================================+
| |ui_objects_detected|          |
+--------------------------------+

.. |ui_objects_detected| image:: ../../examples/ml/detection/media/ui_objects_detected.png
   :width: 100%

.. literalinclude:: ../../../examples/ml/detection/ui_detection.py
   :language: python
   :linenos:
   :caption: **User Interface Detection Example Source code**: `ui_detection.py`_
   :name: User Interface Detection Example

.. _ui_detection.py: https://github.com/varigit/pyvar/blob/master/examples/ml/detection/ui_detection.py
