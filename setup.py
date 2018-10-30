#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read().replace('.. :changelog:', '')


needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest-runner'] if needs_pytest else []

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    'six',
    'mock',
    'pytest',
    'django<2.0.0',
    'requests',
]

setup(
    name='curlit',
    version='0.1.0',
    description="Generate curl commands from various python libraries request objects",
    long_description=readme + '\n\n' + history,
    author="Adam Hitchcock",
    author_email='adam@northisup.com',
    url='https://github.com/NorthIsUp/curlit',
    packages=[
        'curlit',
    ],
    package_dir={
        'curlit': 'curlit'
    },
    include_package_data=True,
    install_requires=requirements,
    # test_suite='tests',
    tests_require=test_requirements,
    setup_requires=pytest_runner,
)
