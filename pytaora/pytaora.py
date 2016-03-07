#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
A tool for generating source code
Latest version can be found at https://github.com/letuananh/pytaora

References:
    Python documentation:
        https://docs.python.org/
    argparse module:
        https://docs.python.org/3/howto/argparse.html
    PEP 0008 - Style Guide for Python Code
        https://www.python.org/dev/peps/pep-0008/
    PEP 0257 - Python Docstring Conventions:
        https://www.python.org/dev/peps/pep-0257/

@author: Le Tuan Anh <tuananh.ke@gmail.com>
'''

# Copyright (c) 2016, Le Tuan Anh <tuananh.ke@gmail.com>
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

__author__ = "Le Tuan Anh <tuananh.ke@gmail.com>"
__copyright__ = "Copyright 2016, pytaora"
__credits__ = [ "Le Tuan Anh" ]
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Le Tuan Anh"
__email__ = "<tuananh.ke@gmail.com>"
__status__ = "Prototype"

########################################################################

import os
import sys
import jinja2
import datetime
from collections import defaultdict, namedtuple
import json
import argparse


#-------------------------------------------------------------------------------
# CONFIGURATION
#-------------------------------------------------------------------------------

TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
TAORA_CFG_FILE  = os.path.abspath(os.path.expanduser('~/.taora'))

#-------------------------------------------------------------------------------
# CLASSES
#-------------------------------------------------------------------------------

Requirement = namedtuple('Requirement', ['field', 'compulsory', 'default'])

class RequirementReader:
    def __init__(self):
        pass

    @staticmethod
    def parse(lines):
        requirements = []
        for line in lines:
            if line.strip().startswith("#") or len(line.strip()) == 0:
                continue
            else:
                parts = line.split("\t")
                if len(parts) == 1:
                    field, compulsory, default = parts[0], '', ''
                elif len(parts) == 2:
                    field, compulsory, default = parts[0], parts[1], ''
                else:
                    field, compulsory, default = line.split('\t')
            compulsory = (compulsory.strip().upper() in ['T', 'Y', 'TRUE', 'YES'])
            requirements.append(Requirement(field.strip(), compulsory, default.strip()))
        return requirements

    @staticmethod
    def parse_file(file_name):
        with open(file_name, 'r') as infile:
            return RequirementReader.parse(infile.readlines())

class GlobalConfig:
    def __init__(self):
        if os.path.isfile(TAORA_CFG_FILE):
            self.load(TAORA_CFG_FILE)
        elif os.path.isfile('./.taora'):
            self.load('./.taora')
        else:
            self.contents = {}

    def load(self, fname):
        with open(fname, 'r') as cfgfile:
            self.contents = json.loads(cfgfile.read())
        return self.contents

    @staticmethod
    def read():
        return GlobalConfig().contents
    
class Template:

    def __init__(self, template_file):
        # Jinja template loader
        self.templateLoader = jinja2.FileSystemLoader( searchpath=TEMPLATE_FOLDER )
        self.templateEnv    = jinja2.Environment( loader=self.templateLoader )
        self.template       = self.templateEnv.get_template(template_file)
        self.ext            = os.path.splitext(template_file)[1]

        # Template requirements
        self.requirements = RequirementReader.parse_file(os.path.join(TEMPLATE_FOLDER, template_file + '.config'))
        self.contents = defaultdict(dict)
        self.contents.update({ 'now' : datetime.datetime.now() })

        # Prefill stuff from Global config
        prefilled = GlobalConfig.read()
        if prefilled:
            self.contents.update(prefilled)
    
    def fillin(self):
        print(self.requirements)
        for req in self.requirements:
            # print(req)
            if not self.ask(req):
                return False
        return True

    def ask(self, requirement):
        answer = self.get(requirement)
        while not answer:
            answer = input("Please fill in %s (Default = %s): " % (requirement.field, requirement.default,))
            if not answer:
                if requirement.compulsory:
                    if not self.confirm("This field is compulsory, do you want to continue? (Y/N) "):
                        return False
                else:
                    if self.confirm("No input detected, do you want to use default value (%s)? (Y/N) " % (requirement.default)):
                        self.update(requirement, answer)
                        return True
            else:
                self.update(requirement, answer)
        return True

    def update(self, requirement, answer):
        path = list(reversed(requirement.field.split('.')))
        level = self.contents
        while len(path) > 1:
            step = path.pop()
            if step in self.contents:
                level = self.contents[step]
        level[path.pop()] = answer

    def get(self, requirement):
        field = requirement if isinstance(requirement,str) else requirement.field
        path = list(reversed(field.split('.')))
        level = self.contents
        while len(path) > 1:
            level = self.contents[path.pop()]
        step = path.pop()
        return level[step] if step in level else None
        
    def confirm(self, msg):
        answer = input(msg)
        return answer.lower() in [ 'y', 'yes' ]

    def render(self):
        return self.template.render(self.contents)
    
    def save(self, filename):
        filename = os.path.abspath(filename)
        if os.path.isfile(filename):
            if not self.confirm("File %s exists, do you want to overwrite (Y/N): " % (filename,)):
                print("Cancelled")
                return False
        with open(filename, 'w') as outfile:
            outfile.write(self.render())
            print("Code has been generated to %s" % (filename,))


#-------------------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------

def dev_mode(outpath=None):
    template = Template('template.py')
    if template.fillin():
        print(template.contents)
        codename = template.get('project.codename')
        if not outpath and codename:
            outpath = codename + template.ext
        
        if outpath:
            template.save(outpath)
        else:
            print("\n\n")
            print(template.render())
    else:
        print("Code generation cancelled")

def generate_code(outpath=None):
    pass
#-------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------

def main():
    '''Main entry of pyTaora
    '''

    parser = argparse.ArgumentParser(description="pyTaora - A code generator")
    
    parser.add_argument('template', help='Name of the code template to use')

    # Positional argument(s)
    parser.add_argument('-d', '--dev', help='Run developing feature', action="store_true")
    # parser.add_argument('-i', '--input', help='Template to be used')
    parser.add_argument('-o', '--output', help='Path to output file')

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
        if args.dev:
            dev_mode(args.output)
    pass

if __name__ == "__main__":
    main()
