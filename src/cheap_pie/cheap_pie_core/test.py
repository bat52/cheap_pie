#!/usr/bin/python3
""" Cheap Pie Test Module """
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import unittest
import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

class CheapPieMethods(unittest.TestCase):
    """ Cheap Pie Test Class """

    def test_transport(self):
        """ Cheap Pie Test Transport Method """

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

    def test_bitfield(self):
        """ Test bitfield class """
        from cheap_pie_core.cbitfield import test_cp_bitfield
        test_cp_bitfield()

    def test_register(self):
        """ Test register class """
        from cheap_pie_core.cp_register import test_cp_register
        test_cp_register()

    def test_cp_hal(self):
        """ Test hal class """
        from cheap_pie_core.cp_hal import test_cp_hal
        test_cp_hal()

    def test_parsers(self):
        """ Test cheap pie parsers """
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
        """ Test parsers wrapper """
        from parsers.cp_parsers_wrapper import test_cp_parsers_wrapper
        test_cp_parsers_wrapper()

    def test_tools(self):
        """ Test cheap_pie tools """
        from tools.hal2doc import test_hal2doc
        test_hal2doc()

        from tools.search import test_search
        test_search()

    def test_cheap_pie_main(self):
        """ Test cheap pie main """
        from cheap_pie_core.cheap_pie import main
        main()

if __name__ == '__main__':
    unittest.main()
