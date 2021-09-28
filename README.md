## Pyvarml API

This repository contains an easy-to-use Python API that helps customers to
develop their own Machine Learning application on Variscite SoMs powered by
the NXP i.MX8M Plus.

### API Documentation

To generate the API documentation, please follow the above steps:

1. Clone this repository:

    ```bash
    $ git clone https://github.com/varjig/pyvarml.git
    ```

2. Build the API using sphinx:

    ```bash
    $ cd sphinx/
    $ make html
    ```

3. Open the page:

    ```bash
    $ firefox _build/html/index.html
    ```

### Build the Package

1. Run the following command to build the package:

    ```bash
    $ python3 setup.py sdist
    ```

2. Copy the package to the module:

    ```bash
    $ scp dist/<package>.tar.gz root@<IP_ADDRESS>:/home/root
    ```

3. On the SoM, run the following command:

    ```bash
    # pip3 install <package>.tar.gz
    ```

### Development Status: Planning

**0.0.1**
- Python API for Machine Learning.
  
### Copyright and License

Copyright 2021 Variscite LTD. Free use of this software is granted under
the terms of the BSD 3-Clause License.
See [LICENSE](https://github.com/varijig/pyvarml/blob/master/LICENSE.md)
for details.
