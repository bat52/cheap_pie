#!/usr/bin/python3

import sys
import os
import argparse

from systemrdl import RDLCompiler, RDLCompileError
# from peakrdl.verilog import VerilogExporter

try:
    # newer version
    from peakrdl_ipxact import IPXACTExporter
    from peakrdl_uvm import UVMExporter
except:
    # older version
    from peakrdl.ipxact import IPXACTExporter
    from peakrdl.uvm import UVMExporter

def cli(args):
    parser = argparse.ArgumentParser(description='rdl2any')
    # register format options
    parser.add_argument("-f", "--fname", help="register file description .rdl", action='store', type = str, default="./devices/rdl/basic.rdl")
    parser.add_argument("-ofmt", "--out-format", help="output format", action='store', type = str, default="ipxact", choices=["ipxact","uvm"])

    return parser.parse_args(args)

def rdl2any(args=[]):
    p = cli(args)
    rdlc = RDLCompiler()

    try:
        rdlc.compile_file(p.fname)
        root = rdlc.elaborate()
    except RDLCompileError:
        sys.exit(1)

    if p.out_format == 'ipxact': 
        exporter = IPXACTExporter()
        ext = '.xml'
    elif p.out_format == 'uvm': 
        exporter = UVMExporter()
        ext = '.uvm'
    else:
        print('Unsupported output format!')
        assert(False)

    base = os.path.splitext(p.fname)[0]
    outfname = base + ext
    print('output file: ' + outfname)
    exporter.export(root, outfname )
    return outfname

def test_rdl2any():
    rdl2any(['-ofmt','ipxact'])
    rdl2any(['-ofmt','uvm'])

if __name__ == '__main__':
    rdl2any(sys.argv[1:])
