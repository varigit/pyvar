# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import sphinx_press_theme
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

html_theme = 'press'

extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'sphinx.ext.napoleon',
              'sphinx.ext.viewcode',
              'sphinx.ext.extlinks']


release = '0.0.1'
project = 'Variscite LTD'
copyright = '2021-2022 Variscite LTD'
author = 'Variscite LTD'

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_static_path = []

html_show_sourcelink = True

html_logo = 'images/logo.png'

html_favicon = 'images/favicon.png'

html_show_sphinx = False

html_search_language = 'en'
