## API Documentation

The API documentation can be generated using [sphinx][sphinx_page]. Please
follow the below steps to build the documentation:

1. Clone the `pyvarml` repository:

```bash
$ git clone https://github.com/varjig/pyvarml.git
```

2. Install the required packages:

```bash
$ apt install python3-sphinx
$ pip3 install sphinx_press_theme
```

3. Build the API in the HTML format:

```bash
$ cd sphinx/
$ make html
```

4. Open the HTML page:

```bash
$ firefox _build/html/index.html
```

[sphinx_page]: https://www.sphinx-doc.org/en/master/
