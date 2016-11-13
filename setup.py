try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension
from treeprinter.__meta__ import __title__, __version__, __site__, __license__, __author__, __email__, __summary__
import os.path
import re

CLASSIFIERS = filter(None, map(str.strip,
                               """
                               Development Status :: 5 - Production/Stable
                               Intended Audience :: Developers
                               License :: OSI Approved :: BSD License
                               Programming Language :: C
                               Programming Language :: Python :: 2.4
                               Programming Language :: Python :: 2.5
                               Programming Language :: Python :: 2.6
                               Programming Language :: Python :: 2.7
                               Programming Language :: Python :: 3
                               Programming Language :: Python :: 3.2
                               """.splitlines()))


f = open('README.md')
try:
    README = f.read()
finally:
    f.close()


setup(
    name=__title__,
    version=__version__,
    packages=[__title__, __title__ + '.tests', __title__ + '.printers'],
    url=__site__,
    license=__license__,
    author=__author__,
    author_email=__email__,
    description=__summary__,
    long_description=README,
    classifiers=CLASSIFIERS,
    package_data={'treeprinter': ['./README.md']},
)