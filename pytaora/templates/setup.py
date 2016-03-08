#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Setup script for {{project.codename}}
Latest version can be found at {% if project.url %}{{project.url}}{% elif author.github %}{{author.github}}{{project.codename}}{% endif %}

References:
    Python documentation:
        https://docs.python.org/
    PEP 0008 - Style Guide for Python Code
        https://www.python.org/dev/peps/pep-0008/
    PEP 257 - Python Docstring Conventions:
        https://www.python.org/dev/peps/pep-0257/

@author: {{author.name}} <{{author.email}}>
'''

# Copyright (c) {{now.year}}, {{author.name}} <{{author.email}}>
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

__author__ = "{{author.name}} <{{author.email}}>"
__copyright__ = "Copyright {{now.year}}, {{project.codename}}"
__credits__ = [ "{{author.name}}" ]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "{{author.name}}"
__email__ = "<{{author.email}}>"
__status__ = "Prototype"

########################################################################

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

from {{project.codename}} import {{project.codename}}

########################################################################


here = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read('README.md', 'CHANGES.md')

setup(
    name='{{project.codename}}',
    version={{project.codename}}.__version__,
    url='{% if project.url %}{{project.url}}{% elif author.github %}{{author.github}}{{project.codename}}{% endif %}',
    license='MIT License',
    author='{{author.name}}',
    tests_require=[],
    install_requires=[],
    author_email='{{author.email}}',
    description='{{desc}}',
    long_description=long_description,
    packages=['{{project.codename}}'],
    include_package_data=True,
    platforms='any',
    test_suite='test',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 0.1 - Alpha',
        'Natural Language :: English',
        'Environment :: Console Application',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]#,
    #extras_require={
        # 'testing': ['pytest'],
    #}
)
