# -*- coding: utf-8 -*-
"""
Created on Fri May 03 11:27:39 2019

## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com
"""

from xmlreg2struct import xmlreg2struct

def search_bitfield(hal,bitfield):

    retval = []    
    for reg in hal: # loop over all registers
        # print reg.regname        
        for field in reg.bitfields:
            if bitfield in field.fieldname:
                print reg.regname + " @ " + field.fieldname
                retval.append(field)
    return retval    
    
if __name__ == '__main__':
    hal = xmlreg2struct(fname="./devices/QN908XC.xml", hif=None)
    ret = search_bitfield(hal,'ADC_BM')
    pass


