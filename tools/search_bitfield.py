#!/usr/bin/python3

## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )
from parsers.svd_parse_repo import svd_parse

def search_bitfield(hal,bitfield):
    retval = []    
    for reg in hal: # loop over all registers
        # print reg.regname        
        for field in reg.bitfields:
            if bitfield in field.fieldname:
                print( reg.regname + " @ " + field.fieldname )
                retval.append(field)
    return retval    
    
if __name__ == '__main__':
    hal = svd_parse(fname="./devices/QN908XC.svd", hif=None)
    ret = search_bitfield(hal,'ADC_BM')
    pass


