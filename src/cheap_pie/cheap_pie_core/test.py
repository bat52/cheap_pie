#!/usr/bin/python3

# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import unittest
import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

class CheapPieMethods(unittest.TestCase):

    def test_transport(self):
        # dummy for mockup
        from transport.cp_dummy_transport import test_cp_dummy
        test_cp_dummy()

        # jlink
        from transport.cp_jlink_transport import test_cp_jlink
        test_cp_jlink()

        # pyocd
        from transport.cp_pyocd_transport import test_cp_pyocd
        test_cp_pyocd()

        # esptool
        from transport.cp_esptool_transport import test_cp_esptool
        test_cp_esptool()

        # pyverilator 
        from transport.cp_pyverilator_transport import test_cp_pyverilator
        test_cp_pyverilator()

        pass
   
    def test_bitfield(self):
        from cheap_pie_core.cbitfield import test_cp_bitfield
        test_cp_bitfield()
    
    def test_register(self):
        from cheap_pie_core.cp_register import test_cp_register
        test_cp_register()

    def test_cp_hal(self):
        from cheap_pie_core.cp_hal import test_cp_hal
        test_cp_hal()
        pass   

    def test_parsers(self):
        from parsers.svd_parse import test_svd_parse
        test_svd_parse()

        from parsers.svd_parse_repo import test_svd_parse_repo
        test_svd_parse_repo()

        from parsers.ipxact_parse import test_ipxact_parse
        test_ipxact_parse()

        from parsers.ipyxact_parse import test_ipyxact_parse
        test_ipyxact_parse()

        from parsers.rdl_parse import test_rdl_parse
        test_rdl_parse()

    def test_parsers_wrapper(self):
        from parsers.cp_parsers_wrapper import test_cp_parsers_wrapper
        test_cp_parsers_wrapper()
        pass

    def test_tools(self):
        from tools.hal2doc import test_hal2doc
        test_hal2doc()

        from tools.search import test_search
        test_search()
        pass

    def test_cheap_pie_main(self):
        from cheap_pie_core.cheap_pie import main
        main()

if __name__ == '__main__':
    unittest.main()
