#!/usr/bin/env python
from distutils.core import setup

setup(name='py-uploader',
      version='0.2',
      description='Python application for uploading to file hosting services',
      author='d-fens',
      url='http://github.com/d-fens/py-uploader/',
      license = 'MIT',
      py_modules=['rapidshare', 'uploaded'],
      scripts=['uploader'],
      classifiers=[
            'Environment :: Console',
            'Natural Language :: English',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python'
      ])
