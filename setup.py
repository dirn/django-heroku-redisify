#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

settings = dict()

# Publish
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

settings.update(
    name='django-heroku-redisify',
    version='0.2.0',
    description='Friendly Redis for Django on Heroku',
    long_description=open('README.rst').read(),
    author='Andy Dirnberger',
    author_email='dirn@dirnonline.com',
    url='https://github.com/dirn/django-heroku-redisify',
    py_modules=['redisify'],
    package_data={'': ['LICENSE']},
    include_package_data=True,
    tests_require=['coverage', 'nose'],
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

setup(**settings)
