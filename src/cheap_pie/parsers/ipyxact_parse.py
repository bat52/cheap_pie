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

from cheap_pie_core.cp_builder import CpHalBuilder # pylint: disable=C0413,E0401
from cheap_pie_core.cp_hal import CpHal # pylint: disable=C0413,E0401

def ipyxact_parse(fname,hif=None, base_address_offset = "0x00000000"):
    """ Cheap Pie parser for IP-XACT structure with ipyxact """
    ## read input file ########################################################
    xml = Component()
    xml.load(fname)

    ## loop over lines ########################################################
    cpb = CpHalBuilder(hif)

    for mem in xml.memoryMaps.memoryMap:
        for periph in mem.addressBlock:
            if hasattr(periph,'register'):
                for reg in periph.register:
                    # new register
                    regaddr=reg.addressOffset + periph.baseAddress + literal_eval(base_address_offset)

                    cpb.reg_open(
                        regname=f'{periph.name}_{reg.name}',
                        regaddr=regaddr,
                        comments=reg.description,
                        )

                    if hasattr(reg,'field'):
                        for field in reg.field :
                            if not field is None:
                                # Create new field class
                                cpb.newfield(
                                    regfield = field.name,
                                    width = field.bitWidth,
                                    offset=field.bitOffset,
                                    comments=field.description
                                    )

            # create last register, if existing
            # cpb.reg_close()

    # convert output dictionary into structure
    return cpb.out()

def test_ipyxact_parse():
    """ Test function for IP-XACT parser with ipyxact """
    sbhal = ipyxact_parse("./devices/my_subblock.xml")
    assert isinstance(sbhal,CpHal)
    ehal = ipyxact_parse("./devices/generic_example.xml")
    assert isinstance(ehal,CpHal)

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
