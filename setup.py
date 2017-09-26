#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name='pyzenodo',
    version='1.0.0-alpha',
    description='Python wrapper for the Zenodo REST API',
    author='Tom Klaver',
    author_email='t.klaver@esciencecenter.nl',
    license='Apache 2.0',
    url='https://github.com/Tommos0/pyzenodo',
    include_package_data=True,
    keywords=['zenodo', 'pyzenodo'],
    classifiers=[
        'Programming Language :: Python',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(),
    install_requires=['requests'],
    # install_requires=['feedparser >= 5.1.0', 'pytz', 'requests', 'pathlib'],
    long_description="""\
A Python wrapper for the Zenodo REST API
---------------------------------------------

Provides methods for accessing Zenodo REST API.

This version requires Python 2.7.x / 3.4.x / 3.5.x / 3.6.x"""
)
