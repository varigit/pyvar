Quick Dataset Examples
======================

Dataset Examples
----------------

Training MNIST Handwritten Digits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. To train a simple MNIST to recognize handwritten digits, see the example:

.. literalinclude:: ../../../examples/ml/mnist/train.py
   :language: python
   :linenos:
   :caption: **Source code**: `train.py`_
   :name: Training MNIST Example

.. _train.py: https://github.com/varjig/pyvar/blob/master/examples/ml/mnist/train.py

2. The output is similar to the one below:

.. code-block:: console

    Test loss: 0.07373514771461487
    Test accuracy: 0.9776999950408936

Testing MNIST Handwritten Digits
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. To test the above model, see the example:

.. literalinclude:: ../../../examples/ml/mnist/test.py
   :language: python
   :linenos:
   :caption: **Source code**: `test.py`_
   :name: Testing MNIST Example
   :emphasize-lines: 4, 7

.. _test.py: https://github.com/varjig/pyvar/blob/master/examples/ml/mnist/test.py

2. The output is similar to the one below:

+------------------------+
| **Example**            |
+========================+
| |number|               |
+------------------------+

.. code-block:: console

    Predicted Digit: 0
    Confidence: 8.820571899414062

.. |number| image:: ../../examples/ml/mnist/media/zero.png
   :width: 20%
