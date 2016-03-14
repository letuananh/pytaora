#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
{{desc}}
Latest version can be found at {% if project.url %}{{project.url}}{% elif author.github %}{{author.github}}{{project.codename}}{% endif %}

References:
    Python documentation:
        https://docs.python.org/
    argparse module:
        https://docs.python.org/3/howto/argparse.html
    PEP 0008 - Style Guide for Python Code
        https://www.python.org/dev/peps/pep-0008/
    PEP 0257 - Python Docstring Conventions:
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

import sys
import os
import logging
import argparse
from collections import defaultdict as dd
from collections import namedtuple

#-------------------------------------------------------------------------------
# CONFIGURATION
#-------------------------------------------------------------------------------

DATA_FOLDER = os.path.abspath(os.path.expanduser('./data'))

#-------------------------------------------------------------------------------
# DATA STRUCTURES
#-------------------------------------------------------------------------------

Person = namedtuple('Person', ['name', 'age'])

#-------------------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------

def dev_mode():
    logging.info("I'm working on this ...")
    logging.debug("A debug message")
    logging.error("When I see an error ...")

#-------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------

def main():
    '''Main entry of {{project.codename}}
    '''

    # It's easier to create a user-friendly console application by using argparse
    # See reference at the top of this script
    parser = argparse.ArgumentParser(description="{{desc}}")
    
    # Positional argument(s)
    parser.add_argument('-d', '--dev', help='Quick method for developer.', action='store_true')

    # Optional argument(s)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")

    # Main script
    if len(sys.argv) == 1:
        # User didn't pass any value in, show help
        parser.print_help()
    else:
        # Parse input arguments
        args = parser.parse_args()
        # Now do something ...
        if args.quiet:
            logging.basicConfig(level=logging.CRITICAL)
            logging.disabled = True
        elif args.verbose:
            logging.basicConfig(level=logging.DEBUG)
        else:
            logging.basicConfig(level=logging.INFO)
        if args.dev:
            dev_mode()
        else:
            parser.print_help()
    pass

if __name__ == "__main__":
    main()
