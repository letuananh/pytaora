#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Setup script for {{project_codename}}
Latest version can be found at {% if project_url %}{{project_url}}{% elif author_github %}{{author_github}}{{project_codename}}{% endif %}

References:
    Python documentation:
        https://docs.python.org/
    PEP 0008 - Style Guide for Python Code
        https://www.python.org/dev/peps/pep-0008/
    PEP 257 - Python Docstring Conventions:
        https://www.python.org/dev/peps/pep-0257/

@author: {{author_name}} <{{author_email}}>
'''

# Copyright (c) {{now.year}}, {{author_name}} <{{author_email}}>
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

__author__ = "{{author_name}}"
__email__ = "<{{author_email}}>"
__copyright__ = "Copyright {{now.year}}, {{project_codename}}"
__license__ = "MIT"
__maintainer__ = "{{author_name}}"
__version__ = "0.1"
__status__ = "Prototype"
__credits__ = []

########################################################################

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

from {{project_codename}} import {{project_codename}}

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
    name='{{project_codename}}',
    version={{project_codename}}.__version__,
    url='{% if project_url %}{{project_url}}{% elif author_github %}{{author_github}}{{project_codename}}{% endif %}',
    license='MIT License',
    author='{{author_name}}',
    tests_require=[],
    install_requires=[],
    author_email='{{author_email}}',
    description='{{desc}}',
    long_description=long_description,
    packages=['{{project_codename}}'],
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
