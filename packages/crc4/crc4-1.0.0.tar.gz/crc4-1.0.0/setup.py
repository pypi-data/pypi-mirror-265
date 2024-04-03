#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup the RC4 C module"""

from setuptools import Extension, setup

with open("README.md", "r") as fp:
    long_description: str = fp.read()

setup(
    name="crc4",
    version="1.0.0",
    author="Ari Archer",
    author_email="ari@ari.lt",
    url="https://ari.lt/gh/crc4",
    description="RC4 encryption for Python in C.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: C",
        "Development Status :: 5 - Production/Stable",
        "Topic :: Security :: Cryptography",
        "Typing :: Typed",
    ],
    ext_modules=[
        Extension("crc4", ["crc4.c"]),
    ],
    options={"bdist_wheel": {"universal": True}},
)
