#!/usr/bin/python3
""" Cheap Pie module wrapper around all parsers """
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from parsers.svd_parse_repo import svd_parse_repo # pylint: disable=C0415,E0401,C0413
from parsers.svd_parse import svd_parse           # pylint: disable=C0415,E0401,C0413
from parsers.ipxact_parse import ipxact_parse     # pylint: disable=C0415,E0401,C0413
from parsers.ipyxact_parse import ipyxact_parse   # pylint: disable=C0415,E0401,C0413
from parsers.rdl_parse import rdl_parse           # pylint: disable=C0415,E0401,C0413

def cp_parsers_wrapper(prms,hif=None, base_address_offset = "0x00000000"):
    """ Cheap Pie function wrapper around all parsers """
    if prms.vendor is None:
        fname = os.path.join(prms.devicedir,prms.regfname)
        print(fname)
    else:
        # if vendor is indicated, use file from repository
        fname = prms.regfname
    if prms.format == 'cmsis-svd':
        # parser build for CMSIS-SVD xml file format
        hal = svd_parse_repo(fname=fname,hif=hif,vendor=prms.vendor,
                        base_address_offset=base_address_offset)
    elif prms.format == 'svd':
        # parser build for CMSIS-SVD xml file format
        hal = svd_parse(fname=fname,hif=hif,vendor=prms.vendor,
                        base_address_offset=base_address_offset)
    elif prms.format == 'ipxact':
        hal = ipxact_parse(fname=fname,hif=hif,
                           base_address_offset=base_address_offset)
    elif prms.format == 'ipyxact':
        hal = ipyxact_parse(fname=fname,hif=hif,
                           base_address_offset=base_address_offset)
    elif prms.format == 'rdl':
        hal = rdl_parse(fname=fname,hif=hif,
                        base_address_offset=base_address_offset)
    else:
        assert False, 'Unsupported input format!'

    return hal

def test_cp_parsers_wrapper():
    """ Test function for parsers wrapper """
    from cheap_pie_core.cp_cli import cp_cli
    prms = cp_cli()
    cp_parsers_wrapper(prms)

if __name__ == '__main__':
    test_cp_parsers_wrapper()
