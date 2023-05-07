#!/usr/bin/python3
""" Cheap Pie native module parser for IP-XACT """
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval
from collections import namedtuple
import untangle # for parsing xml

import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie_core.cbitfield   import cp_bitfield
from cheap_pie_core.cp_register import cp_register
from parsers.name_subs import name_subs

def ipxact_remove_prefix(ipx):
    """ remove ipxact or spirit prefix"""
    replist = ['ipxact_','spirit_']

    if hasattr(ipx,'children'):
        for elm in ipx.children:
            # remove all suffixes
            for repl in replist:
                elm._name = elm._name.replace(repl,'')
            # remove recursively
            ipxact_remove_prefix(elm)

    return ipx
    pass

def ipxact_parse(fname,hif=None, base_address_offset = "0x00000000"):
    """ Cheap Pie native module parser for IP-XACT """
    ## read input file ########################################################
    csv = untangle.parse(fname)

    ## remove ipxact/spirit prefixes ##########################################
    csv = ipxact_remove_prefix(csv)

    ## loop over lines ########################################################
    outdict = {}

    periph = csv.component.memoryMaps.memoryMap.addressBlock
    base_addr_str=periph.baseAddress.cdata.replace("'h",'0x')
    base_address=literal_eval(base_addr_str)

    if hasattr(periph,'register'):
        for reg in periph.register:
            if hasattr( reg.name, 'cdata'):
                # close old register, before opening a new one
                if 'regname' in locals():
                    struct_register.dictfield2struct()
                    outdict[regname]=struct_register

                # new register
                periph_name=periph.name.cdata
                rname=reg.name.cdata
                regname = f'{periph_name}_{rname}'
                regname=name_subs(regname)

                addr_str=reg.addressOffset.cdata.replace("'h",'0x')
                regaddr=literal_eval(addr_str) + base_address + literal_eval(base_address_offset)
                comments=""
                # print(comments)
                struct_register=cp_register(regname,regaddr,comments,hif)

                # for field_idx in range(nfields):
                if hasattr(reg,'field'):
                    for field in reg.field :
                        regfield=field.name.cdata

                        if not field is None:
                            # print regfield
                            regfield=name_subs(regfield)

                            csv_width=field.bitWidth.cdata
                            bitoffset=field.bitOffset.cdata
                            comments="" # field.description.cdata
                            # print(comments)

                            # Create new field class
                            class_regfield=cp_bitfield(
                                regfield,regaddr,regname,csv_width,bitoffset,comments,hif)
                            struct_register.addfield(class_regfield)

        # create last register, if existing
        if 'regname' in locals():
            # outstruct=addreg2struct(outstruct,regname,struct_register)
            struct_register.dictfield2struct()
            outdict[regname]=struct_register

    # convert output dictionary into structure
    return namedtuple("HAL", outdict.keys())(*outdict.values())

def test_ipxact_parse():
    """ Test function for cheap pie native IP-XACT parser """
    ipxact_parse("./devices/my_subblock.xml")
    ipxact_parse("./devices/leon2_creg.xml")
    ipxact_parse("./devices/generic_example.xml")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        fname=sys.argv[1]
    else:
        fname="./devices/my_subblock.xml"
    print(fname)
    print(ipxact_parse(fname))
