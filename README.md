## Variscite Python API for ML Applications

This repository contains an easy-to-use Python API that helps customers to
develop their own Machine Learning applications to run on Variscite SoMs powered
by the NXP i.MX8M Plus.

### API Documentation

The API documentation can be generated using [sphinx][sphinx_page]. Please
follow the below steps to build the documentation:

1. Clone the `pyvarml` repository:

```bash
$ git clone https://github.com/varjig/pyvarml.git
```

2. Build the API in the HTML format:

```bash
$ cd sphinx/
$ make html
```

3. Open the HTML page:

```bash
$ firefox _build/html/index.html
```

### Build the Package

To learn how to build the package, please refer to the API documentation.

### Development Status: Planning

**0.0.1**
- Python API for Machine Learning.
  
### Copyright and License

Copyright 2021 Variscite LTD. Free use of this software is granted under
the terms of the BSD 3-Clause License.
See [LICENSE](https://github.com/varijig/pyvarml/blob/master/LICENSE.md)
for details.

[sphinx_page]: https://www.sphinx-doc.org/en/master/
