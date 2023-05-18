#!/usr/bin/python3

""" Cheap Pie module to convert .rdl register description into IP-XACT or UVM """

import sys
import os
import argparse

from systemrdl import RDLCompiler, RDLCompileError

try:
    # newer version
    from peakrdl_ipxact import IPXACTExporter
    from peakrdl_uvm import UVMExporter
except:
    # older version
    from peakrdl.ipxact import IPXACTExporter
    from peakrdl.uvm import UVMExporter

def cli(args):
    """ Command Line parse to convert .rdl register description into IP-XACT or UVM """
    parser = argparse.ArgumentParser(description='rdl2any')

    # register format options
    parser.add_argument("-f", "--fname", help="register file description .rdl",
                        action='store', type = str, default="./devices/rdl/basic.rdl")
    parser.add_argument("-ofmt", "--out-format", help="output format",
                        action='store', type = str, default="ipxact", choices=["ipxact","uvm"])

    return parser.parse_args(args)

def rdl2any(args):
    """  convert .rdl register description into IP-XACT or UVM """
    prms = cli(args)
    rdlc = RDLCompiler()

    try:
        rdlc.compile_file(prms.fname)
        root = rdlc.elaborate()
    except RDLCompileError:
        sys.exit(1)

    if prms.out_format == 'ipxact':
        exporter = IPXACTExporter()
        ext = '.xml'
    elif prms.out_format == 'uvm':
        exporter = UVMExporter()
        ext = '.uvm'
    else:
        assert False, f'Unsupported output format {prms.out_format} !'

    base = os.path.splitext(prms.fname)[0]
    outfname = base + ext
    print('output file: ' + outfname)
    exporter.export(root, outfname )
    return outfname

def test_rdl2any():
    """ test convert .rdl register description into IP-XACT and UVM """
    rdl2any(['-ofmt','ipxact'])
    rdl2any(['-ofmt','uvm'])

if __name__ == '__main__':
    rdl2any(sys.argv[1:])
