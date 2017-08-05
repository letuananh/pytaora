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
__credits__ = []
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
MY_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FOLDER = os.path.join(MY_DIR, 'templates')
TAORA_CFG_FILE = os.path.abspath(os.path.expanduser('~/.taora'))


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
            self.__cfg = cfg
            self.template = cfg['template']
            self.ext = cfg['ext']
            self.name = cfg['name']
            self.description = cfg['desc'] if 'desc' in cfg else ''
            self.default_name = cfg['default_name'] if 'default_name' in cfg else None

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
        try:
            with open(file_name, 'r') as infile:
                return TemplateConfig.parse(infile.read())
        except Exception as e:
            logger.exception("Cannot load template from file {}".format(file_name))
            raise


class GlobalConfig:
    ''' pyTaoRa Configuration reader. Configuration file will be read from [~/.taora]. If the file cannot be found, the next place will be [./.taora]
    '''
    def __init__(self):
        if os.path.isfile(TAORA_CFG_FILE):
            self.load(TAORA_CFG_FILE)
        elif os.path.isfile('./.taora'):
            self.load('./.taora')
        elif os.path.isfile(os.path.join(MY_DIR, '../.taora')):
            self.load(os.path.join(MY_DIR, '../.taora'))
        else:
            logging.warning("There is no configuration file (either ~/.taora or ./.taora)")
            self.contents = {}

    def load(self, fname):
        logging.info("Loading configuration from {}".format(fname))
        with open(fname, 'r') as cfgfile:
            self.contents = json.loads(cfgfile.read())
        return self.contents

    __singleton = None

    @staticmethod
    def read():
        if GlobalConfig.__singleton is None:
            GlobalConfig.__singleton = GlobalConfig()
        return GlobalConfig.__singleton.contents


class Template:

    def __init__(self, template_config_file, template_folder=TEMPLATE_FOLDER):
        # Read template config
        self.config = TemplateConfig.parse_file(os.path.join(template_folder, template_config_file))
        # Jinja template loader
        self.templateLoader = jinja2.FileSystemLoader(searchpath=template_folder)
        self.templateEnv = jinja2.Environment(loader=self.templateLoader)
        self.template = self.templateEnv.get_template(self.config.template)
        self.ext = self.config.ext
        self.description = self.config.description
        self.default_name = self.config.default_name
        self.contents = defaultdict(dict)
        self.contents.update({'now': datetime.datetime.now()})

        # Prefill stuff from Global config
        prefilled = GlobalConfig.read()
        if prefilled:
            logging.info("Prefilled value(s) from .taora file: %s" % json.dumps(prefilled))
            self.contents.update(prefilled)
            logging.info("My values: %s" % self.contents)

    def get_default_name(self):
        if self.default_name:
            return self.templateEnv.from_string(self.default_name).render(self.contents)
        elif self.contents['project.codename']:
            return self.contents['default_name'] + '.' + self.ext

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
            default_value = self.contents[requirement.field] if requirement.field in self.contents else requirement.default
            answer = input("Please fill in %s (Default = %s): " % (requirement.field, default_value,))
            if not answer:
                if requirement.compulsory and not default_value:
                    if not self.confirm("This field is compulsory, do you want to continue? (Y/N) "):
                        return False
                else:
                    if self.confirm("No input detected, do you want to use default value (%s)? (Y/N) " % (default_value), default_yes=True):
                        self[requirement] = default_value
                        return True
            else:
                self[requirement] = answer
        return True

    def __getitem__(self, requirement):
        field = requirement if isinstance(requirement, str) else requirement.field
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
        return answer.lower() in ['y', 'yes'] or (default_yes and answer == '')

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


class TemplateManager(object):

    __singleton = None

    def __init__(self, template_folder=TEMPLATE_FOLDER):
        self.template_folder = template_folder
        self.templates = {}

    def load(self):
        ''' Load all available templates '''
        for filename in os.listdir(self.template_folder):
            if filename.endswith('.taora'):
                logging.debug('Loading template: %s' % filename)
                template_obj = Template(filename)
                self.templates[template_obj.config.name] = template_obj
        return self

    def search(self, template_name):
        return self.templates[template_name] if template_name in self.templates else None

    @staticmethod
    def all(template_folder=TEMPLATE_FOLDER):
        if TemplateManager.__singleton is None:
            TemplateManager.__singleton = TemplateManager(template_folder)
            TemplateManager.__singleton.load()
        return TemplateManager.__singleton.load()


#-------------------------------------------------------------------------------
# FUNCTIONS
#-------------------------------------------------------------------------------

def mkdir(args):
    if not os.path.exists(args.dirname):
        os.makedirs(args.dirname)


def gen_code(args):
    template_name = args.template
    outpath = args.outpath
    terms = args.terms
    to_stdout = args.stdout

    template = TemplateManager.all().search(template_name)
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
        if to_stdout:
            print("\n\n")
            print(template.render())
        elif outpath:
            if os.path.isdir(outpath):
                # if there is a default name, use that
                if template.get_default_name():
                    outpath = os.path.join(outpath, template.get_default_name())
            # write file
            template.save(outpath)
        elif template.get_default_name():
            template.save(template.get_default_name())
        else:
            print("\n\n")
            print(template.render())
    else:
        print("Code generation cancelled")


def list_templates(args=None):
    print("Available templates:")
    print("-" * 40)
    templates = TemplateManager.all().templates
    for t in templates:
        print("{k}: {d}".format(k=t, d=templates[t].description))


#-------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------

def main():
    '''Main entry of pyTaora
    '''
    parser = argparse.ArgumentParser(description="pyTaora - A code generator")

    # Positional argument(s)
    task_parsers = parser.add_subparsers(help='taora type (file/dir)')

    # dir creation task
    dir_task = task_parsers.add_parser('dir')
    dir_task.add_argument('dirname')
    dir_task.set_defaults(func=mkdir)

    # file creation task
    file_task = task_parsers.add_parser('file')
    file_task.add_argument('template', help='Name of the code template to use')
    file_task.set_defaults(func=gen_code)

    # list templates task
    list_task = task_parsers.add_parser('list')
    list_task.set_defaults(func=list_templates)

    # code gen configuration
    parser.add_argument('-t', '--terms', nargs='*', dest='terms', help='Config')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-o', '--outpath', help='Path to output file or directory (default_name will be used)')
    group.add_argument('--stdout', help='Write generated content to standard output stream', action='store_true')
    # logging/verbose, etc.
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-v", "--verbose", action="store_true")
    group.add_argument("-q", "--quiet", action="store_true")
    group.add_argument('--debug', help='Activate debug mode', action="store_true")

    # Main script
    if len(sys.argv) == 1:
        # User didn't pass any value in, show help
        parser.print_help()
        print("")
        list_templates()
    else:
        args = parser.parse_args()
        # config logging
        if args.debug:
            logging.basicConfig(level=logging.DEBUG)
        elif args.verbose:
            logging.basicConfig(level=logging.INFO)
        elif args.quiet:
            logging.disabled = True
        else:
            logging.basicConfig(level=logging.CRITICAL)
        # perform task
        args.func(args)
    pass


if __name__ == "__main__":
    main()
