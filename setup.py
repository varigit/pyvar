# Copyright 2021 Variscite LTD
# SPDX-License-Identifier: BSD-3-Clause

import os
from setuptools import setup, find_packages

this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name="pyvarml",
      version="0.0.1",
      description="Variscite Python API for ML Applications",
      long_description=long_description,
      long_description_content_type='text/markdown',
      url = 'https://github.com/dorta/pyvarml',
      author="Diego Dorta",
      author_email="diego.d@variscite.com",
      license="BDS-3-Clause",
      packages=find_packages(),
      zip_safe=False,
      keywords = ['variscite', 'ai', 'ml', 'API'],
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Operating System :: Other OS',
        'Programming Language :: Python :: 3.7'
      ])