#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='django-management-api',
    version='0.0.1',
    description='A REST interface for interacting with django management commands',
    author='Tareque Hossain',
    author_email='tareque@codexn.com',
    url='http://github.com/tareque/django-management-api/',
    long_description=open('README.md', 'r').read(),
    packages=[
        'management_api',
    ],
    package_data={
    },
    zip_safe=False,
    requires=[
    ],
    install_requires=[
    ],
    classifiers=[
        'Development Status :: Pre Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: MIT',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
