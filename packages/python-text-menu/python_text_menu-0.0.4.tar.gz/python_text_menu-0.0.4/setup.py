import codecs
import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding='utf-8') as fh:
    long_description = '\n' + fh.read()

VERSION = '0.0.4'
DESCRIPTION = 'Basic text menu for console'
LONG_DESCRIPTION = long_description

setup(
    name='python_text_menu',
    version=VERSION,
    author='Macaya25 (Andres Macaya)',
    author_email='afmacaya@miuandes.cl',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'menu', 'cli'],
)
