#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

VERSION = __version__ = "0.0.0"

AUTHOR = "Viral NFT"
AUTHOR_EMAIL = "team@winit.gg"
CLASSIFIERS = [
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Programming Language :: Python :: 3.7",
]
INCLUDE_PACKAGE_DATA = True
INSTALL_REQUIRES = open("requirements.txt").read().splitlines()
KEYWORDS = (
    "viral nft prefect flow dag workflow pipeline data"
)
LONG_DESCRIPTION = open("README.md").read()

setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    classifiers=CLASSIFIERS,
    include_package_data=INCLUDE_PACKAGE_DATA,
    install_requires=INSTALL_REQUIRES,
    keywords=KEYWORDS,
    long_description=LONG_DESCRIPTION,
    name="moap",
    packages=find_packages(include=["src", "src.*"]),
    python_requires=">=3.7",
    version=VERSION,
)
