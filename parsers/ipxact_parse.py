#!/usr/bin/python3

## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import untangle # for parsing xml
from ast import literal_eval
import string as str
from collections import namedtuple

import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie_core.cbitfield   import cp_bitfield
from cheap_pie_core.cp_register import cp_register
from parsers.name_subs import name_subs
    
def ipxact_parse(fname,hif=None):
       
    ## read input file ########################################################
    csv = untangle.parse(fname)
    
    ## loop over lines ########################################################
    outdict = dict()

    periph = csv.ipxact_component.ipxact_memoryMaps.ipxact_memoryMap.ipxact_addressBlock
    # print(periph)
    
    base_addr_str=periph.ipxact_baseAddress.cdata.replace("'h",'0x')
    # print(base_addr_str)
    base_address=literal_eval(base_addr_str)

    if hasattr(periph,'ipxact_register'):
        for reg in periph.ipxact_register:                
            if hasattr( reg.ipxact_name, 'cdata'):
                # close old register, before opening a new one
                if 'regname' in locals():
                    struct_register.dictfield2struct()
                    outdict[regname]=struct_register

                # new register
                periph_name=periph.ipxact_name.cdata
                rname=reg.ipxact_name.cdata
                regname = "%s_%s" % ( periph_name,rname )
                regname=name_subs(regname)

                addr_str=reg.ipxact_addressOffset.cdata.replace("'h",'0x')
                regaddr=literal_eval(addr_str) + base_address
                comments=""
                # print(comments)
                struct_register=cp_register(regname,regaddr,comments,hif)

                # for field_idx in range(nfields):
                if hasattr(reg,'ipxact_field'):
                    for field in reg.ipxact_field :
                        regfield=field.ipxact_name.cdata

                        if not(field is None):
                            # print regfield
                            regfield=name_subs(regfield)

                            csvWidth=field.ipxact_bitWidth.cdata
                            bitoffset=field.ipxact_bitOffset.cdata
                            comments="" # field.description.cdata
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

def test_ipxact_parse(argv=[]):
    if len(argv) > 1: 
        fname=argv[1]
    else:
        fname="./devices/my_subblock.xml"
    return ipxact_parse(fname)
    pass
    
if __name__ == '__main__':    
    print(ipxact_parse(sys.argv))
    pass
    
