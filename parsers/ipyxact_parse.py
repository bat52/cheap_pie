#!/usr/bin/python3

## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval
import string as str
from collections import namedtuple

from ipyxact.ipyxact import Component

import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie_core.cbitfield   import cp_bitfield
from cheap_pie_core.cp_register import cp_register
from parsers.name_subs import name_subs

def ipxact_parse(fname,hif=None):
       
    ## read input file ########################################################
    xml = Component()
    xml.load(fname)
    
    ## loop over lines ########################################################
    outdict = dict()

    for m in xml.memoryMaps.memoryMap:
        for periph in m.addressBlock:
            # print(periph)
        
            # base_addr_str=periph.baseAddress # .cdata.replace("'h",'0x')
            # print(base_addr_str)
            base_address=periph.baseAddress # literal_eval(base_addr_str)

            if hasattr(periph,'register'):
                for reg in periph.register:                
                    # close old register, before opening a new one
                    if 'regname' in locals():
                        struct_register.dictfield2struct()
                        outdict[regname]=struct_register

                    # new register
                    periph_name=periph.name
                    rname=reg.name
                    regname = "%s_%s" % ( periph_name,rname )
                    regname=name_subs(regname)

                    # addr_str=reg.addressOffset.cdata.replace("'h",'0x')
                    # regaddr=literal_eval(addr_str) + base_address
                    regaddr=reg.addressOffset + base_address
                    comments=reg.description
                    # print(comments)
                    struct_register=cp_register(regname,regaddr,comments,hif)

                    # for field_idx in range(nfields):
                    if hasattr(reg,'field'):
                        for field in reg.field :
                            regfield=field.name

                            if not(field is None):
                                # print regfield
                                regfield=name_subs(regfield)

                                csvWidth=field.bitWidth
                                bitoffset=field.bitOffset
                                comments=field.description
                                # print(comments)
                                
                                # Create new field class
                                class_regfield=cp_bitfield(regfield,regaddr,regname,csvWidth,bitoffset,comments,hif)
                                struct_register.addfield(class_regfield)

            # create last register, if existing
            if 'regname' in locals():
                # outstruct=addreg2struct(outstruct,regname,struct_register)
                struct_register.dictfield2struct()
                outdict[regname]=struct_register
    
    # convert output dictionary into structure
    # return outdict
    return namedtuple("HAL", outdict.keys())(*outdict.values()) 

def test_ipyxact_parse():
    ipxact_parse("./devices/my_subblock.xml")
    # ipxact_parse("./devices/leon2_creg.xml") # ValueError: invalid literal for int() with base 10: '4 * (2 ** 10)'
    ipxact_parse("./devices/generic_example.xml")
    pass
    
if __name__ == '__main__':
    if len(sys.argv) > 1: 
        fname=sys.argv[1]
    else:
        fname="./devices/my_subblock.xml"
    print(fname)    
    hal = ipxact_parse(fname)
    print(hal)
    pass
    
