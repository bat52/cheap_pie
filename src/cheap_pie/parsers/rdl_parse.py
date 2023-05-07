#!/usr/bin/python3
""" Cheap Pie module to parse .rdl files """
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from parsers.ipyxact_parse import ipxact_parse
from tools.rdl2any import rdl2any

def rdl_parse(fname,hif=None,base_address_offset = "0x00000000" ):
    """ Cheap Pie function to parse .rdl files """

    # convert rdl to ipxact
    ipxact_fname = rdl2any(['-f',fname,'-ofmt','ipxact'])
    # parse ipxact
    return ipxact_parse(ipxact_fname,hif=hif, base_address_offset=base_address_offset)

def test_rdl_parse():
    """ Cheap Pie function to test .rdl file parser """
    rdl_parse("./devices/rdl/basic.rdl")
    rdl_parse("./devices/rdl/counter.rdl")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fname=sys.argv[1]
    else:
        fname="./devices/rdl/basic.rdl"
    print(fname)
    hal = rdl_parse(fname)
    print(hal)
