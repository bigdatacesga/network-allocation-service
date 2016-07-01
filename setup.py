#!/usr/bin/env python

from setuptools import setup

setup(
    name='network-allocation-service',
    version='0.2.1',
    author='Javier Cacheiro',
    author_email='bigdata-dev@cesga.es',
    url='https://github.com/javicacheiro/network-allocation-service',
    license='MIT',
    description='REST service for network address allocation similar to DHCP',
    long_description=open('README.rst').read(),
    #py_modules=['consul'],
    install_requires=['Flask', 'kvstore', 'requests', 'python-keyczar',
        'gunicorn', 'coverage'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
