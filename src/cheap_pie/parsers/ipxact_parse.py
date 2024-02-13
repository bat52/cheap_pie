#!/usr/bin/env python3
""" Cheap Pie native module parser for IP-XACT """
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

from ast import literal_eval
import untangle  # for parsing xml

# import sys     # pylint: disable=C0411
# import os.path # pylint: disable=C0411
# sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie.cheap_pie_core.cp_builder import CpHalBuilder  # pylint: disable=C0413,E0401
from cheap_pie.cheap_pie_core.cp_cli import cp_devices_fname


def ipxact_remove_prefix(ipx):
    """ remove ipxact or spirit prefix"""
    replist = ['ipxact_', 'spirit_']

    if hasattr(ipx, 'children'):
        for elm in ipx.children:
            # remove all suffixes
            for repl in replist:
                elm._name = elm._name.replace( # pylint: disable=W0212
                    repl, '')
            # remove recursively
            ipxact_remove_prefix(elm)

    return ipx


def ipxact_parse(fname, hif=None, base_address_offset="0x00000000"):
    """ Cheap Pie native module parser for IP-XACT """
    ## read input file ########################################################
    csv = untangle.parse(fname)

    ## remove ipxact/spirit prefixes ##########################################
    csv = ipxact_remove_prefix(csv)

    ## loop over lines ########################################################
    cpb = CpHalBuilder(hif)

    periph = csv.component.memoryMaps.memoryMap.addressBlock
    base_addr_str = periph.baseAddress.cdata.replace("'h", '0x')
    base_address = literal_eval(base_addr_str)

    if hasattr(periph, 'register'):  # pylint: disable=R1702
        for reg in periph.register:
            if hasattr(reg.name, 'cdata'):
                # new register
                addr_str = reg.addressOffset.cdata.replace("'h", '0x')
                regaddr = literal_eval(
                    addr_str) + base_address + literal_eval(base_address_offset)

                cpb.reg_open(regname=f'{periph.name.cdata}_{reg.name.cdata}',
                             regaddr=regaddr)

                # for field_idx in range(nfields):
                if hasattr(reg, 'field'):
                    for field in reg.field:
                        if not field is None:
                            # Create new field
                            cpb.newfield(
                                regfield=field.name.cdata,
                                width=field.bitWidth.cdata,
                                offset=field.bitOffset.cdata,
                                comments=""  # field.description.cdata
                            )

    # convert output dictionary into structure
    return cpb.out()


def test_ipxact_parse():
    """ Test function for cheap pie native IP-XACT parser """

    ipxact_parse(cp_devices_fname("my_subblock.xml"))
    ipxact_parse(cp_devices_fname("leon2_creg.xml"))
    ipxact_parse(cp_devices_fname("generic_example.xml"))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        LFNAME = sys.argv[1]
    else:
        LFNAME = cp_devices_fname("my_subblock.xml")
    print(LFNAME)
    print(ipxact_parse(LFNAME))
