# -*- coding: utf-8 -*-

from __future__ import print_function
from setuptools import setup, find_packages

setup(
    name="distributed-logging",
    version="0.0.2",
    author="mfkifhss",
    author_email="mfkifhss@gmail.com",
    description="Python Framework.",
    license="MIT",
    url="",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=True,
    platforms='any',
    install_requires=[
        "pywin32==303; sys_platform != 'linux'"
    ],
)
