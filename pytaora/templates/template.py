#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
{{desc}}
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
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

__author__ = "{{author_name}}"
__email__ = "<{{author_email}}>"
__copyright__ = "Copyright {{now.year}}, {{project_codename}}"
__license__ = "MIT"
__maintainer__ = "{{author_name}}"
__version__ = "0.1"
__status__ = "Prototype"
__credits__ = []

########################################################################

import os
import logging
import argparse
from collections import defaultdict as dd
from collections import namedtuple


# -------------------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------------------

logger = logging.getLogger(__name__)
DATA_FOLDER = os.path.abspath(os.path.expanduser('./data'))

# -------------------------------------------------------------------------------
# Data structures
# -------------------------------------------------------------------------------

Person = namedtuple('Person', ['name', 'age'])
people = dd(list)


# -------------------------------------------------------------------------------
# Application logic
# -------------------------------------------------------------------------------

def uber_action(args):
    logging.info("I'm working on this ...")
    logging.debug("A debug message")
    logging.error("When I see an error ...")


def config_logging(args):
    ''' Override root logger's level '''
    if args.quiet:
        logging.getLogger().setLevel(logging.CRITICAL)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)


# -------------------------------------------------------------------------------
# Main method
# -------------------------------------------------------------------------------

def main():
    '''Main entry of {{project_codename}}
    '''

    # It's easier to create a user-friendly console application by using argparse
    # See reference at the top of this script
    parser = argparse.ArgumentParser(description="{{desc}}", add_help=False)
    parser.set_defaults(func=None)

    # Optional argument(s)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")

    tasks = parser.add_subparsers(help="Task to be done")

    uber_task = tasks.add_parser('uber', parents=[parser], help='To perform an uber action')
    uber_task.set_defaults(func=uber_action)

    # Main script
    args = parser.parse_args()
    config_logging(args)
    if args.func is not None:
        args.func(args)
    else:
        parser.print_help()
    pass


if __name__ == "__main__":
    main()
