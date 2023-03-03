#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages
from setuptools import setup

# Package meta-data.
DESCRIPTION = \
"""Simple markov and gillespie models for chemical reactions."""
URL = "https://github.com/harmsm/kinetics_simulator"
EMAIL = "harmsm@gmail.com"
AUTHOR = "Michael J. Harms"
REQUIRES_PYTHON = ">=3.8.0"
VERSION = None

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Load the package's __version__.py module as a dictionary.
about = {}
about['__version__'] = VERSION

# Packages
packages = find_packages()
package_data = {}

# Where the magic happens:
setup(
    name="kinetics_simulator", # Note this is different than "topiary" for PIP package name
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=packages,
    package_data=package_data,
    zip_safe=False,
    include_package_data=True,
    license='MIT',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Science/Research',
      'Programming Language :: Python :: 3.8',
      'Programming Language :: Python :: 3.9',
      'Programming Language :: Python :: 3.10',
    ],
    keywords="biochemistry; kinetics; simulation"
)
