#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
doclink = """
Documentation
-------------

The full documentation is at http://labwelfare.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='labwelfare',
    version='0.0.1',
    description='Welfare Phibro',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='Murilo Ijanc\'',
    author_email='mbsd@m0x.ru',
    url='https://github.com/lab804/labwelfare',
    packages=[
        'labwelfare',
    ],
    package_dir={'labwelfare': 'labwelfare'},
    include_package_data=True,
    install_requires=[
    ],
    license='BSD',
    zip_safe=False,
    keywords='labwelfare',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
