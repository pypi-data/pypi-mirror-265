#!/usr/bin/env python

from setuptools import setup

"""
:authors: ZHRXXgroup
:license: MIT License, see LICENSE file
:copyright: (c) 2024 ZHRXXgroup
"""

version = '1.0'

long_description  = "Python Module from ZHRXXgroup to install ZXpackages"



setup(
    name="zxpm",
    version=version,
    
    author='ZHRXXgroup',
    author_email="info@zhrxxgroup.com",

    description='''Python Module for installing Packages''',
    long_description=long_description,

    url="https://zhrxxgroup.com",
    download_url="https://zhrxxgroup.com/",

    license="MIT License, see LICENSE file",

    packages=['zxpm'],
    install_requires=["requests"],

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3'
    ]
)
