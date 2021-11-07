#!/usr/bin/python3
#
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import argparse
import sys

def cp_cli(args=[]):
    parser = argparse.ArgumentParser(description='Cheap Pie Configuration')
    # register format options
    parser.add_argument("-rf", "--regfname", help="register description file name", action='store', type = str, default="QN908XC.svd")
    parser.add_argument("-dd", "--devicedir", help="register description files folder", action='store', type = str, default="./devices")    
    parser.add_argument("-fmt","--format", help="device description format", action='store', type = str, default="cmsis-svd", choices=["svd","cmsis-svd","ipxact","ipyxact","rdl"])
    parser.add_argument("-ve", "--vendor", help="device vendor. if specified parses svd file from github repository.", action='store', type = str, default=None)
    # transport options
    parser.add_argument("-d", "--device", help="jlink/ocd device name", action='store', type = str, default="CORTEX-M4")
    parser.add_argument("-t" , "--transport", help="transport", action='store', type = str, default="dummy", choices=["jlink","dummy","ocd","esptool","verilator"])
    parser.add_argument("-p", "--port", help="esptool serial port", action='store', type = str, default="/dev/ttyUSB0")
    parser.add_argument("-topv", "--top_verilog", help="top verilog file (when simulating with verilator)", action='store', type = str, default="./devices/rdl/basic/basic_rf.sv")

    return parser.parse_args(args)

def test_cli(argv):
    return cp_cli(argv)
    pass

if __name__ == '__main__':    
    print(test_cli(sys.argv[1:]))
    pass    