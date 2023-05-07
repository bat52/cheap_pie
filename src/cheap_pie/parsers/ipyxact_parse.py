#!/usr/bin/python3
""" Cheap Pie parser module for IP-XACT structure with ipyxact """   

## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval
from collections import namedtuple
from ipyxact.ipyxact import Component

import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie_core.cbitfield   import cp_bitfield
from cheap_pie_core.cp_register import cp_register
from parsers.name_subs import name_subs

def ipxact_parse(fname,hif=None, base_address_offset = "0x00000000"):
    """ Cheap Pie parser for IP-XACT structure with ipyxact """   
    ## read input file ########################################################
    xml = Component()
    xml.load(fname)

    ## loop over lines ########################################################
    outdict = {}

    for mem in xml.memoryMaps.memoryMap:
        for periph in mem.addressBlock:
            # print(periph)

            base_address=periph.baseAddress

            if hasattr(periph,'register'):
                for reg in periph.register:
                    # close old register, before opening a new one
                    if 'regname' in locals():
                        struct_register.dictfield2struct()
                        outdict[regname]=struct_register

                    # new register
                    periph_name=periph.name
                    rname=reg.name
                    regname = name_subs(f'{periph_name}_{rname}')
                    regaddr=reg.addressOffset + base_address + literal_eval(base_address_offset)
                    comments=reg.description

                    struct_register=cp_register(regname,regaddr,comments,hif)

                    if hasattr(reg,'field'):
                        for field in reg.field :
                            regfield=field.name

                            if not field is None:
                                regfield=name_subs(regfield)

                                csv_width=field.bitWidth
                                bitoffset=field.bitOffset
                                comments=field.description

                                # Create new field class
                                class_regfield=cp_bitfield(
                                    regfield,regaddr,regname,csv_width,bitoffset,comments,hif)
                                struct_register.addfield(class_regfield)

            # create last register, if existing
            if 'regname' in locals():
                struct_register.dictfield2struct()
                outdict[regname]=struct_register

    # convert output dictionary into structure
    return namedtuple("HAL", outdict.keys())(*outdict.values())

def test_ipyxact_parse():
    """ Test function for IP-XACT parser with ipyxact """   
    ipxact_parse("./devices/my_subblock.xml")
    # ipxact_parse("./devices/leon2_creg.xml") # ValueError: invalid literal for int() with base 10: '4 * (2 ** 10)'
    ipxact_parse("./devices/generic_example.xml")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fname=sys.argv[1]
    else:
        fname="./devices/my_subblock.xml"
    print(fname)
    hal = ipxact_parse(fname)
    print(hal)
