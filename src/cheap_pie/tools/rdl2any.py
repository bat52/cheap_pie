#!/usr/bin/python3

""" Cheap Pie module to convert .rdl register description into IP-XACT, UVM or verilog """

import sys
import os
import argparse
import pathlib

from systemrdl import RDLCompiler, RDLCompileError
from peakrdl.verilog import VerilogExporter

try:
    # newer version
    from peakrdl_ipxact import IPXACTExporter
    from peakrdl_uvm import UVMExporter
except ModuleNotFoundError:  # not sure what should be put here
    # older version
    from peakrdl.ipxact import IPXACTExporter  # pylint: disable=C0412
    from peakrdl.uvm import UVMExporter # pylint: disable=C0412


def cli(args):
    """ Command Line parse to convert .rdl register description into IP-XACT, UVM or verilog """
    parser = argparse.ArgumentParser(description='rdl2any')

    # register format options
    parser.add_argument("-f", "--fname", help="register file description .rdl",
                        action='store', type=str,
                        default=os.path.join(
                            pathlib.Path(__file__).parent.parent.absolute(),
                            "devices",
                            "rdl",
                            "basic.rdl"
                        )
                        )
    parser.add_argument("-ofmt", "--out-format", help="output format",
                        action='store', type=str, default="ipxact",
                        choices=["ipxact", "uvm", "vlog"])

    return parser.parse_args(args)


def rdl2any(args):
    """  convert .rdl register description into IP-XACT, UVM or verilog """
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
    elif prms.out_format == 'vlog':
        exporter = VerilogExporter()
        ext = '.v'
    else:
        assert False, f'Unsupported output format {prms.out_format} !'

    base = os.path.splitext(prms.fname)[0]
    outfname = base + ext
    print('output file: ' + outfname)

    if prms.out_format == 'vlog':
        exporter.export(root, outfname, signal_overrides={})
    else:
        exporter.export(root, outfname)

    return outfname


def test_rdl2any():
    """ test convert .rdl register description into IP-XACT, UVM or verilog """
    print("# Test rdl2ipxact")
    rdl2any(['-ofmt', 'ipxact'])

    print("# Test rdl2uvm")
    rdl2any(['-ofmt', 'uvm'])

    print("# Test rdl2verilog")
    rdl2any(['-ofmt', 'vlog'])


if __name__ == '__main__':
    rdl2any(sys.argv[1:])
