#!/usr/bin/env python
# encoding: UTF-8

from distutils.core import setup


setup(
    name = 'continuum_ci',
    version = '0.0.0',
    author = 'Michel Casabianca',
    author_email = 'casa@sweetohm.net',
    packages = ['continuum'],
    url = 'https://pypi.org/project/continuum_ci/',
    license = 'Apache Software License',
    description = 'Continuum is a minimalist continuous integration tool',
    long_description=open('README.rst', encoding='UTF-8').read(),
    install_requires=[
        'PyYAML',
        'mail1',
    ],
    entry_points = {
        'console_scripts': [
            'continuum = continuum:run',
        ],
    },
)
