#!/usr/bin/python3

# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import unittest
import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

class CheapPieRdlMethods(unittest.TestCase):

    def test_tools(self):
        from tools.rdl2verilog import test_rdl2verilog
        test_rdl2verilog()

        from tools.rdl2any import test_rdl2any
        test_rdl2any()
        pass

if __name__ == '__main__':
    unittest.main()
