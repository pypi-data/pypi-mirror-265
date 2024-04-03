from setuptools import setup, find_packages
import codecs
import os

path = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(path, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.2'
DESCRIPTION = 'Simple JSON Config Parser for Python.'
LONG_DESCRIPTION = 'Simple JSON Config Parser for Python that allows creation, modification, and deletion of multiple JSON configuration files.'

# Setting up
setup(
    name="SimpleJsonConfigParser",
    version=VERSION,
    author="TPosty",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'configuration'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
