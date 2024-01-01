#!/usr/bin/env python3
"""
Cheap Pie Command Line Interface
"""
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

import os
import sys
import pathlib
import argparse


def cp_root_dir():
    """ Returns the full path of Cheap Pie root directory """
    return pathlib.Path(__file__).parent.parent.absolute()


def cp_devices_dir():
    """ Returns the full path of ad filename in Cheap Pie devices directory """
    return os.path.join(
        cp_root_dir(),
        'devices')


def cp_devices_fname(fname):
    """ Returns the full path of ad filename in Cheap Pie devices directory """
    return os.path.join(
        cp_devices_dir(), fname
    )


def cp_cli(args=[]):  # pylint: disable=W0102
    """
    Cheap Pie Command Line Interface
    """
    parser = argparse.ArgumentParser(description='Cheap Pie Configuration')
    # register format options
    parser.add_argument("-rf", "--regfname", help="register description file name",
                        action='store', type=str, default="QN908XC.svd")
    parser.add_argument("-dd", "--devicedir", help="register description files folder",
                        action='store', type=str,
                        default=cp_devices_dir()
                        )
    parser.add_argument("-fmt", "--format", help="device description format",
                        action='store', type=str, default="cmsis-svd",
                        choices=["svd", "cmsis-svd", "ipxact", "ipyxact", "rdl"])
    parser.add_argument("-ve", "--vendor",
                        help="device vendor. if specified parses svd file from github repository.",
                        action='store', type=str, default=None)
    parser.add_argument("-vendors", "--vendors",
                        help="Available device vendors from cmsis-svd package.",
                        action='store_true')
    parser.add_argument("-devices", "--devices",
                        help="Available devices for specified vendor from cmsis-svd package.",
                        action='store_true')
    # transport options
    parser.add_argument("-d", "--device", help="jlink/ocd device name", action='store',
                        type=str, default="CORTEX-M4")
    parser.add_argument("-t", "--transport", help="transport", action='store', type=str,
                        default="dummy", choices=["jlink", "dummy", "ocd", "esptool", "verilator"])
    parser.add_argument("-p", "--port", help="esptool serial port", action='store', type=str,
                        default="/dev/ttyUSB0")
    parser.add_argument("-topv", "--top_verilog",
                        help="top verilog file (when simulating with verilator)",
                        action='store', type=str, default="./devices/rdl/basic/basic_rf.sv")

    return parser.parse_args(args)


def test_cli(argv):
    """
    Test function for Cheap Pie Command Line Interface
    """
    return cp_cli(argv)


if __name__ == '__main__':
    print(test_cli(sys.argv[1:]))
