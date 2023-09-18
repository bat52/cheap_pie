#!/usr/bin/env python3
""" Cheap Pie Test Module """

# -*- coding: utf-8 -*-
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

import unittest

if __name__ == '__main__':
    # needed if cheap_pie not installed, and running locally
    import sys
    import os.path
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# Cheap Pie Core
from cheap_pie.cheap_pie_core.cbitfield import test_cp_bitfield               # pylint: disable=C0413,E0401
from cheap_pie.cheap_pie_core.cp_register import test_cp_register             # pylint: disable=C0413,E0401
from cheap_pie.cheap_pie_core.cp_builder import test_cp_builder               # pylint: disable=C0413,E0401
from cheap_pie.cheap_pie_core.cp_hal import test_cp_hal, test_cp_hal_to_docx  # pylint: disable=C0413,E0401
from cheap_pie.cheap_pie_core.cheap_pie_main import cp_main                                  # pylint: disable=C0413,E0401

# parsers
from cheap_pie.parsers.svd_parse import test_svd_parse                        # pylint: disable=C0413,E0401
from cheap_pie.parsers.svd_parse_repo import test_svd_parse_repo              # pylint: disable=C0413,E0401
from cheap_pie.parsers.ipxact_parse import test_ipxact_parse                  # pylint: disable=C0413,E0401
from cheap_pie.parsers.ipyxact_parse import test_ipyxact_parse                # pylint: disable=C0413,E0401
from cheap_pie.parsers.rdl_parse import test_rdl_parse                        # pylint: disable=C0413,E0401
from cheap_pie.parsers.cp_parsers_wrapper import test_cp_parsers_wrapper      # pylint: disable=C0413,E0401
from cheap_pie.parsers.xml_xslt import test_xml_xslt                          # pylint: disable=C0413,E0401

# tools
from cheap_pie.tools.hal2doc import test_hal2doc                              # pylint: disable=C0413,E0401
from cheap_pie.tools.search import test_search                                # pylint: disable=C0413,E0401
from cheap_pie.tools.rdl2any import test_rdl2any                              # pylint: disable=C0413,E0401

# Transport
from cheap_pie.transport.cp_dummy_transport import test_cp_dummy              # pylint: disable=C0413,E0401
from cheap_pie.transport.cp_jlink_transport import test_cp_jlink              # pylint: disable=C0413,E0401
from cheap_pie.transport.cp_pyocd_transport import test_cp_pyocd              # pylint: disable=C0413,E0401
from cheap_pie.transport.cp_esptool_transport import test_cp_esptool          # pylint: disable=C0413,E0401
from cheap_pie.transport.cp_pyverilator_transport import test_cp_pyverilator  # pylint: disable=C0413,E0401


class CheapPieMethods(unittest.TestCase):
    """ Cheap Pie Test Class """

    def test_transport(self):
        """ Cheap Pie Test Transport Method """

        # dummy for mockup
        test_cp_dummy()
        # NB: requirements_extra.txt are needed!
        test_cp_jlink()
        test_cp_pyocd()
        test_cp_esptool()
        test_cp_pyverilator()

    def test_cheap_pie_core(self):
        """ Test cheap pie core classes """
        test_cp_bitfield()
        test_cp_register()
        test_cp_builder()
        test_cp_hal()
        test_cp_hal_to_docx()
        cp_main()

    def test_parsers(self):
        """ Test cheap pie parsers """
        test_svd_parse()
        test_svd_parse_repo()
        test_ipxact_parse()
        test_ipyxact_parse()
        test_rdl_parse()
        test_xml_xslt()
        test_cp_parsers_wrapper()

    def test_tools(self):
        """ Test cheap_pie tools """
        test_hal2doc()
        test_search()
        test_rdl2any()


if __name__ == '__main__':
    unittest.main()
