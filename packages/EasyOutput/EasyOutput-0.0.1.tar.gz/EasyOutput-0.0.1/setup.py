from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'Colored messages in the palm of your hand'
LONG_DESCRIPTION = 'A package that allows you to use error, success, and information messages with ease.'

# Setting up
setup(
    name="EasyOutput",
    version=VERSION,
    author="FrankAustin",
    author_email="<frankaustindev808@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['colorama'],
    keywords=['python', 'colored print', 'error message', 'success message', 'colored message'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)