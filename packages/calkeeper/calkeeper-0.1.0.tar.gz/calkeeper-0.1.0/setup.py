#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = []

setup_requirements = []

test_requirements = ['pytest>=3', ]

setup(
    author="Maximilian F.S.J. Menger",
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Simple calculation tracking",
    install_requires=requirements,
    license="Apache License v2.0",
    long_description=readme,
    include_package_data=False,
    name='calkeeper',
    packages=find_packages(include=['calkeeper', 'calkeeper.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mfsjmenger/calkeeper',
    version='0.1.0',
    zip_safe=True,
)
