Getting Started
===============

Environment Setup
-----------------

Host Machine
~~~~~~~~~~~~

1. Install the following packages in the GNU/Linux system:

.. code-block:: console

    # apt install python3 python3-pip

2. Install the required Python packages:

.. code-block:: console

    $ pip3 install opencv-python pillow numpy tensorflow

System on Modules
~~~~~~~~~~~~~~~~~

1. Build the latest Yocto Release available from source code:

* `Variscite Wiki <https://variwiki.com/index.php?title=Yocto_Build_Release&release=RELEASE_HARDKNOTT_V1.1_DART-MX8M-PLUS>`_.


Installation
------------

Build the Package
~~~~~~~~~~~~~~~~~

1. Clone the pyvarml repository:

.. code-block:: console

    $ git clone https://github.com/varijig/pyvarml

2. Build the pyvarml package:

.. code-block:: console

    $ cd pyvarml/
    $ python3 setup.py sdist
    
3. Copy the package to the SoM:

.. code-block:: console

    $ scp dist/<package> root@<IP_ADDRESS>:/home/root
    
4. On the SoM, install the package:

.. code-block:: console

    # pip3 install <package>


Quick Installation using Pypi
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. NOTE::
    Not uploaded yet.

1. Use pip3 tool to install the package located at Pypi repository:

.. code-block:: console

    $ pip3 install pyvarml


Yocto Package Build
-------------------

.. NOTE::
    Not done yet.
