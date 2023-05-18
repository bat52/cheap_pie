#!/usr/bin/python3
""" Cheap Pie parser module for .svd files using SVDParser module """
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

# parser build for CMSIS-SVD xml file format
# https://www.keil.com/pack/doc/CMSIS/SVD/html/index.html
#
# simplified manual initialization
#
# import untangle
# hal = untangle.parse('QN908XC.xml')
# from cbitfield import cp_bitfield
# from cp_register import cp_register
# ADC_ANA_CTRL = cp_register("ADC_ANA_CTRL","0x4000702C",
#                            "ADC core and reference setting regsiter" , hif )
# ADC_BM = cp_bitfield("ADC_BM","0x4000702C",
#                      "ADC_ANA_CTRL",3,0, "ADC bias current selection." ,hif)

from ast import literal_eval
from collections import namedtuple
from cmsis_svd.parser import SVDParser

import sys     # pylint: disable=C0411
import os.path # pylint: disable=C0411
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie_core.cbitfield   import cp_bitfield # pylint: disable=C0413,E0401
from cheap_pie_core.cp_register import cp_register # pylint: disable=C0413,E0401
from parsers.name_subs import name_subs            # pylint: disable=C0413,E0401

def svd_parse_repo(fname,vendor=None,hif=None, base_address_offset = "0x00000000"):
    """ Cheap Pie parser function for .svd files using SVDParser module """
    ## read input file ########################################################
    if vendor is None:
        svd = SVDParser.for_xml_file(fname)
    else:
        svd = SVDParser.for_packaged_svd(vendor,fname)

    ## loop over lines ########################################################
    outdict = {}

    for periph in svd.get_device().peripherals:
        # print(periph.name.cdata)

        base_address=periph.base_address

        if hasattr(periph,'registers'):
            for reg in periph.registers:
                if hasattr( reg, 'name'):
                    # close old register, before opening a new one
                    if 'regname' in locals():
                        struct_register.dictfield2struct()
                        outdict[regname]=struct_register

                    # new register
                    periph_name=periph.name
                    rname=reg.name
                    regname = name_subs(f'{periph_name}_{rname}')

                    regaddr=reg.address_offset + base_address + literal_eval(base_address_offset)
                    comments=reg.description
                    # print(comments)
                    struct_register=cp_register(regname,regaddr,comments,hif)

                    # for field_idx in range(nfields):
                    if hasattr(reg,'fields'):
                        for field in reg.fields :
                            regfield=field.name

                            if not field is None:
                                # print regfield
                                regfield=name_subs(regfield)

                                width=field.bit_width
                                bitoffset=field.bit_offset
                                comments=field.description
                                # print(comments)

                                # Create new field class
                                class_regfield=cp_bitfield(regfield,regaddr,regname,
                                                           width,bitoffset,comments,hif)
                                struct_register.addfield(class_regfield)

            # create last register, if existing
            if 'regname' in locals():
                # outstruct=addreg2struct(outstruct,regname,struct_register)
                struct_register.dictfield2struct()
                outdict[regname]=struct_register

    # convert output dictionary into structure
    return namedtuple("HAL", outdict.keys())(*outdict.values())

def test_svd_parse_repo():
    """ Test Function for .svd parser based of SVDParser module """
    print('Testing QN9080 with repo parser...')
    svd_parse_repo(fname="./devices/QN908XC.svd")

    print('Testing K20 with repo parser...')
    svd_parse_repo(fname='MK20D7.svd',vendor='Freescale')

if __name__ == '__main__':
    test_svd_parse_repo()
