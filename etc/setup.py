#!/usr/bin/env python
# encoding: UTF-8

from distutils.core import setup

setup(
    name = 'continuum_ci',
    version = '#VERSION#',
    author = 'Michel Casabianca',
    author_email = 'casa@sweetohm.net',
    packages = ['continuum'],
    url = 'http://pypi.python.org/pypi/python-continuum/',
    license = 'Apache Software License',
    description = 'Continuum is a minimalist continuous integration tool',
    long_description=open('README.rst').read(),
    entry_points = {
        'console_scripts': [
            'continuum = continuum:run',
        ],
    },
)
