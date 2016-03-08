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
import logging
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

class TemplateConfig:
    ''' Code Template Configuration Reader
    Do not create instances by using the constructor. Instead TemplateConfig.parse('{ "key" : "value" }') or TemplateConfig.parse_file('~/path/to/file.config') should be used.
    '''

    def __init__(self, cfg):
        # Read requirements
        self.requirements = []
        if 'fields' in cfg:
            for field in cfg['fields']:
                name = field['name']
                compulsory = 'required' in field and (field['required'].strip().upper() in ['T', 'Y', 'TRUE', 'YES'])
                default = "" if "default" not in field else field['default']
                self.requirements.append(Requirement(name, compulsory, default))

        # Template file
        if 'template' not in cfg or 'ext' not in cfg:
            raise Exception('Invalid template config file (Template file or extension not found)')
        else:
            self.template = cfg['template']
            self.ext      = cfg['ext']
            self.name     = cfg['name']

    def __len__(self):
        return len(self.requirements)

    def __getitem__(self, idx):
        return self.requirements[idx]

    def __iter__(self):
        for req in self.requirements:
            yield req

    @staticmethod
    def parse(raw_text):
        cfg = json.loads(raw_text)
        return TemplateConfig(cfg)

    @staticmethod
    def parse_file(file_name):
        with open(file_name, 'r') as infile:
            return TemplateConfig.parse(infile.read())

class GlobalConfig:
    ''' pyTaoRa Configuration reader. Configuration file will be read from [~/taora]. If the file cannot be found, the next place will be [./taora]
    '''
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

    def __init__(self, template_config_file):
        # Read template config
        self.config = TemplateConfig.parse_file(os.path.join(TEMPLATE_FOLDER, template_config_file))
        # Jinja template loader
        self.templateLoader = jinja2.FileSystemLoader( searchpath=TEMPLATE_FOLDER )
        self.templateEnv    = jinja2.Environment( loader=self.templateLoader )
        self.template       = self.templateEnv.get_template(self.config.template)
        self.ext            = self.config.ext
        self.contents = defaultdict(dict)
        self.contents.update({ 'now' : datetime.datetime.now() })

        # Prefill stuff from Global config
        prefilled = GlobalConfig.read()
        logging.info("----------")
        if prefilled:
            logging.info("Prefilled value(s) from .taora file: %s" % json.dumps(prefilled))
            self.contents.update(prefilled)
        logging.info("----------")
    
    def fillin(self):
        for req in self.config.requirements:
            current_value = self[req]
            if current_value is not None and current_value.strip() != '':
                logging.debug(req)
                continue
            if not self.ask(req):
                return False
        return True

    def ask(self, requirement):
        answer = None
        while not answer:
            answer = input("Please fill in %s (Default = %s): " % (requirement.field, requirement.default,))
            if not answer:
                if requirement.compulsory:
                    if not self.confirm("This field is compulsory, do you want to continue? (Y/N) "):
                        return False
                else:
                    if self.confirm("No input detected, do you want to use default value (%s)? (Y/N) " % (requirement.default), default_yes=True):
                        self[requirement] = answer
                        return True
            else:
                self[requirement] = answer
        return True

    def __getitem__(self, requirement):
        field = requirement if isinstance(requirement,str) else requirement.field
        path = list(reversed(field.split('.')))
        logging.debug("path: %s" % (path,))
        level = self.contents
        while len(path) > 1:
            step = path.pop()
            logging.debug("current step: %s from %s " % (step, level))
            level = self.contents[step]
            logging.debug("current level: %s" % (level,))
        step = path.pop()
        # logging.debug(step)
        value = level[step] if step in level else None
        logging.debug("Get value: %s => %s" % (requirement, value))
        return value

    def __setitem__(self, key, value):
        logging.debug("setting [%s] = %s" % (key, value))
        field = key if isinstance(key, str) else key.field
        path = list(reversed(field.split('.')))
        level = self.contents
        while len(path) > 1:
            step = path.pop()
            level = self.contents[step]
        level[path.pop()] = value
        
    def confirm(self, msg, default_yes=False):
        answer = input(msg)
        return answer.lower() in [ 'y', 'yes' ] or (default_yes and answer == '')

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

def dev_mode(outpath=None,terms=None):
    print("Working ...")
    pass

template_cache = None

def search_template(template_name):
    global template_cache
    if not template_cache:
        template_cache = {}
        # load all templates
        for filename in os.listdir(TEMPLATE_FOLDER):
            if filename.endswith('.taora'):
                template_obj = Template(filename)
                template_cache[template_obj.config.name] = template_obj
    if template_name in template_cache:
        return template_cache[template_name]
    else:
        return None
        
def gen_code(template_name, outpath=None, terms=None):
    template = search_template(template_name)
    if not template:
        print("Template `%s` not found" % (template_name,))
        return None
    if terms:
        for term in terms:
            parts = term.partition('=')
            if parts[1] != '=':
                print("Invalid term (%s)" % (term,))
                exit()
            else:
                template[parts[0].strip()] = parts[2].strip()
                logging.debug("Template values before template.fillin(): %s" % (template.contents,))
    if template.fillin():
        # print(template.contents)
        codename = template['project.codename']
        if not outpath and codename:
            outpath = codename + '.' + template.ext
        
        if outpath:
            template.save(outpath)
        else:
            print("\n\n")
            print(template.render())
    else:
        print("Code generation cancelled")

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
    parser.add_argument('-t', '--terms', nargs = '*', dest = 'terms', help = 'Config')
    # Optional argument(s)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    group.add_argument('--debug', help='Activate debug mode', action="store_true")
    # Main script
    if len(sys.argv) == 1:
        # User didn't pass any value in, show help
        parser.print_help()
    else:
        # Parse input arguments
        args = parser.parse_args()
        if args.debug:
            logging.basicConfig(level=logging.DEBUG)
        elif args.verbose:
            logging.basicConfig(level=logging.INFO)
        elif args.quiet:
            logging.disabled = True
        else:
            logging.basicConfig(level=logging.CRITICAL)


        # Now do something ...
        if args.dev:
            dev_mode(args.output, terms=args.terms)
        else:
            gen_code(args.template, args.output, terms=args.terms)
    pass

if __name__ == "__main__":
    main()
