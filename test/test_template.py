#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Test template function
Latest version can be found at https://github.com/letuananh/pytaora

References:
    Python unittest documentation:
        https://docs.python.org/3/library/unittest.html
    Python documentation:
        https://docs.python.org/
    PEP 0008 - Style Guide for Python Code
        https://www.python.org/dev/peps/pep-0008/
    PEP 0257 - Python Docstring Conventions:
        https://www.python.org/dev/peps/pep-0257/

@author: Le Tuan Anh <tuananh.ke@gmail.com>
'''

# Copyright (c) 2017, Le Tuan Anh <tuananh.ke@gmail.com>
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

__author__ = "Le Tuan Anh"
__email__ = "<tuananh.ke@gmail.com>"
__copyright__ = "Copyright 2017, pytaora"
__license__ = "MIT"
__maintainer__ = "Le Tuan Anh"
__version__ = "0.1"
__status__ = "Prototype"
__credits__ = ["Le Tuan Anh"]

########################################################################

import os
import unittest
from pytaora import Template

#-------------------------------------------------------------------------------
# CONFIGURATION
#-------------------------------------------------------------------------------

TEST_DIR = os.path.dirname(os.path.realpath(__file__))
TEST_TEMPLATE_DIR = os.path.join(TEST_DIR, 'test_data')
#-------------------------------------------------------------------------------
# DATA STRUCTURES
#-------------------------------------------------------------------------------


class TestTemplate(unittest.TestCase):
    
    def test_load_template(self):
        tmp = Template('report.txt.taora', TEST_TEMPLATE_DIR)
        # the default name should be report.txt
        self.assertEqual('report.txt', tmp.get_default_name())
        # now we add more information to the report
        tmp.contents['author_name'] = 'Le Tuan Anh'
        tmp.contents['author_email'] = 'tuananh.ke@gmail.com'
        tmp.contents['report_title'] = 'Uber report'
        tmp.contents['report_code'] = 'UR-001'
        # now file name should be report_UR-001.txt
        self.assertEqual('report_UR-001.txt', tmp.get_default_name())
        # print("\nReport will be saved to: {filename}\n---------\n{content}\n".format(filename=tmp.get_default_name(), content=tmp.render()))
        expected_report = '''.:: Uber report ::.
--
Report code: UR-001
Prepared by: Le Tuan Anh <tuananh.ke@gmail.com>
Created on : 5 1 2017
------------------------------------------------------------------------
I have nothing to report today'''
        self.assertEqual(tmp.render(), expected_report)

#-------------------------------------------------------------------------------
# MAIN
#-------------------------------------------------------------------------------


if __name__ == "__main__":
    unittest.main()
