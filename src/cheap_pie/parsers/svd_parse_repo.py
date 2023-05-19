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
from cmsis_svd.parser import SVDParser

import sys     # pylint: disable=C0411
import os.path # pylint: disable=C0411
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie_core.cp_builder import CpBuilder # pylint: disable=C0413,E0401

def svd_parse_repo(fname,vendor=None,hif=None, base_address_offset = "0x00000000"):
    """ Cheap Pie parser function for .svd files using SVDParser module """
    ## read input file ########################################################
    if vendor is None:
        svd = SVDParser.for_xml_file(fname)
    else:
        svd = SVDParser.for_packaged_svd(vendor,fname)

    ## loop over lines ########################################################
    cpb = CpBuilder(hif)

    for periph in svd.get_device().peripherals:
        # print(periph.name.cdata)

        if hasattr(periph,'registers'):
            for reg in periph.registers:
                if hasattr( reg, 'name'):
                    # new register
                    regaddr=reg.address_offset + periph.base_address + literal_eval(base_address_offset)

                    cpb.reg_open(
                        regname = f'{periph.name}_{reg.name}',
                        regaddr = regaddr,
                        comments = reg.description
                        )

                    if hasattr(reg,'fields'):
                        for field in reg.fields:
                            if not field is None:
                                # Create new field class
                                cpb.newfield(
                                    regfield = field.name,
                                    width = field.bit_width,
                                    offset = field.bit_offset,
                                    comments = field.description,
                                )

            # create last register, if existing
            cpb.reg_close()

    # convert output dictionary into structure
    return cpb.out()

def test_svd_parse_repo():
    """ Test Function for .svd parser based of SVDParser module """
    print('Testing QN9080 with repo parser...')
    hal = svd_parse_repo(fname="./devices/QN908XC.svd")
    assert len(hal) > 0

    print('Testing K20 with repo parser...')
    hal = svd_parse_repo(fname='MK20D7.svd',vendor='Freescale')
    assert len(hal) > 0

if __name__ == '__main__':
    test_svd_parse_repo()
