#!/usr/bin/env python3
""" Cheap Pie module to parse .rdl files """
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

from cheap_pie.parsers.ipyxact_parse import ipyxact_parse    # pylint: disable=C0413,E0401
from cheap_pie.tools.rdl2any import rdl2any                  # pylint: disable=C0413,E0401
from cheap_pie.cheap_pie_core.cp_cli import cp_devices_fname  # pylint: disable=C0413,E0401


def rdl_parse(fname, hif=None, base_address_offset="0x00000000"):
    """ Cheap Pie function to parse .rdl files """

    # convert rdl to ipxact
    ipxact_fname = rdl2any(['-f', fname, '-ofmt', 'ipxact'])
    # parse ipxact
    return ipyxact_parse(ipxact_fname, hif=hif, base_address_offset=base_address_offset)


def test_rdl_parse():
    """ Cheap Pie function to test .rdl file parser """
    rdl_parse(cp_devices_fname("rdl/basic.rdl"))
    rdl_parse(cp_devices_fname("rdl/counter.rdl"))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        FNAME = sys.argv[1]
    else:
        FNAME = cp_devices_fname("rdl/basic.rdl")
    print(FNAME)
    hal = rdl_parse(FNAME)
    print(hal)
