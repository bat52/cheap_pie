#!/usr/bin/python3
#
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import argparse
import sys

def cp_cli(args=[]):
    parser = argparse.ArgumentParser(description='Cheap Pie Configuration')
    parser.add_argument("-rf", "--regfname", help="register description file name", action='store', type = str, default="QN908XC.svd")
    parser.add_argument("-dd", "--devicedir", help="register description files folder", action='store', type = str, default="./devices")
    parser.add_argument("-jd", "--jdevice", help="jlink device name", action='store', type = str, default="CORTEX-M4")
    parser.add_argument("-t" , "--transport", help="transport", action='store', type = str, default="jlink", choices=["jlink","dummy"])

    return parser.parse_args(args)

if __name__ == '__main__':    
    p = cp_cli(sys.argv[1:])
    print(p)
    pass    