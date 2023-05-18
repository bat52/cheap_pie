#!/usr/bin/python3
""" Cheap Pie parser module for IP-XACT structure with ipyxact """

## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval
from ipyxact.ipyxact import Component              # pylint: disable=E0611

import sys                                         # pylint: disable=C0411
import os.path                                     # pylint: disable=C0411
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie_core.cbitfield   import cp_bitfield # pylint: disable=C0413,E0401
from cheap_pie_core.cp_register import cp_register # pylint: disable=C0413,E0401
from parsers.common import name_subs,dict2namedtuple # pylint: disable=C0413,E0401

def ipyxact_parse(fname,hif=None, base_address_offset = "0x00000000"):
    """ Cheap Pie parser for IP-XACT structure with ipyxact """
    ## read input file ########################################################
    xml = Component()
    xml.load(fname)

    ## loop over lines ########################################################
    outdict = {}

    for mem in xml.memoryMaps.memoryMap:
        for periph in mem.addressBlock:
            # print(periph)

            if hasattr(periph,'register'):
                for reg in periph.register:
                    # close old register, before opening a new one
                    if 'regname' in locals():
                        struct_register.dictfield2struct()
                        outdict[regname]=struct_register

                    # new register
                    regname = name_subs(f'{periph.name}_{reg.name}')
                    regaddr=reg.addressOffset + periph.baseAddress + literal_eval(base_address_offset)
                    comments=reg.description
                    struct_register=cp_register(regname,regaddr,comments,hif)

                    if hasattr(reg,'field'):
                        for field in reg.field :
                            if not field is None:
                                regfield=name_subs(field.name)

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
    return dict2namedtuple(outdict=outdict)

def test_ipyxact_parse():
    """ Test function for IP-XACT parser with ipyxact """
    ipyxact_parse("./devices/my_subblock.xml")
    ipyxact_parse("./devices/generic_example.xml")

    # ipyxact_parse("./devices/leon2_creg.xml")
    # ValueError: invalid literal for int() with base 10: '4 * (2 ** 10)'

if __name__ == '__main__':
    if len(sys.argv) > 1:
        FNAME=sys.argv[1]
    else:
        FNAME="./devices/my_subblock.xml"
    print(FNAME)
    hal = ipyxact_parse(FNAME)
    print(hal)
