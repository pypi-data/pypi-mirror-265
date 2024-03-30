from setuptools import setup, find_packages
import codecs
import os
import random
import numpy
import datetime
import pandas
import string
import warnings
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
VERSION = '0.1.6'
DESCRIPTION = 'Library to create custom dataframe quickly'
LONG_DESCRIPTION = 'This library will help to create our own custom dataframes quickly. You can populate an int,category and dates column easily'


setup(
    name="quick-df",
    version=VERSION,
    author="Marcel Tino",
    author_email="<marceltino92@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=['pandas','datetime','numpy'],
    keywords=['dataframe','quick'])
