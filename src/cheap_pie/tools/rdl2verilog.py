#!/usr/bin/python3

""" Cheap Pie module to convert .rdl register description into verilog """

import sys
import os
import argparse
from systemrdl import RDLCompiler, RDLCompileError
from peakrdl.verilog import VerilogExporter

def cli(args):
    """ Command Line parse to convert .rdl register description into verilog """
    parser = argparse.ArgumentParser(description='rdl2verilog')
    # register format options
    parser.add_argument("-f", "--fname", help="register file description .rdl",
                        action='store', type = str, default="./devices/rdl/basic.rdl")
    return parser.parse_args(args)

def rdl2verilog_main(args):
    """ convert .rdl register description into verilog """
    prms = cli(args)
    rdlc = RDLCompiler()

    try:
        rdlc.compile_file(prms.fname)
        root = rdlc.elaborate()
    except RDLCompileError:
        sys.exit(1)

    exporter = VerilogExporter()
    base = os.path.splitext(prms.fname)[0]
    print('output directory: ' + base)
    exporter.export(root, base, signal_overrides = {} )

def test_rdl2verilog():
    """ test convert .rdl register description into verilog """
    rdl2verilog_main([])

if __name__ == '__main__':
    rdl2verilog_main(sys.argv[1:])
