#!/usr/bin/python3

import sys
import os
from systemrdl import RDLCompiler, RDLCompileError
from peakrdl.verilog import VerilogExporter
import argparse

def cli(args):
    parser = argparse.ArgumentParser(description='rdl2verilog')
    # register format options
    parser.add_argument("-f", "--fname", help="register file description .rdl", action='store', type = str, default="./devices/rdl/basic.rdl")
    return parser.parse_args(args)

def main(args=[]):
    p = cli(args)
    rdlc = RDLCompiler()

    try:
        rdlc.compile_file(p.fname)
        root = rdlc.elaborate()
    except RDLCompileError:
        sys.exit(1)

    exporter = VerilogExporter()
 
    base = os.path.splitext(p.fname)[0]
    print('output directory: ' + base)
    exporter.export(root, base, signal_overrides = dict() )

def test_rdl2verilog():
    main()

if __name__ == '__main__':
    main(sys.argv[1:])
