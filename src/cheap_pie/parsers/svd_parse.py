#!/usr/bin/python3
""" Cheap Pie module for native .svd files parser """
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
# ADC_BM = cp_bitfield("ADC_BM","0x4000702C","ADC_ANA_CTRL",3,0, "ADC bias current selection." ,hif)

from ast import literal_eval
import untangle # for parsing xml

import sys     # pylint: disable=C0411
import os.path # pylint: disable=C0411
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie_core.cbitfield   import cp_bitfield  # pylint: disable=C0413,E0401
from cheap_pie_core.cp_register import cp_register  # pylint: disable=C0413,E0401
from parsers.common import name_subs, dict2namedtuple             # pylint: disable=C0413,E0401

def svd_parse(fname,vendor=None,hif=None, base_address_offset = "0x00000000"): # pylint: disable=W0613
    """ Cheap Pie native parser for .svd files """
    ## read input file ########################################################
    svd = untangle.parse(fname)

    ## loop over lines ########################################################
    outdict = {}

    for periph in svd.device.peripherals.peripheral:
        # print(periph.name.cdata)

        base_addr_str=periph.baseAddress.cdata
        base_address=literal_eval(base_addr_str)

        if hasattr(periph,'registers'):
            for reg in periph.registers.register:
                if hasattr( reg.name, 'cdata'):
                    # close old register, before opening a new one
                    if 'regname' in locals():
                        struct_register.dictfield2struct()
                        outdict[regname]=struct_register

                    # new register
                    regname = name_subs(f'{periph.name.cdata}_{reg.name.cdata}')

                    addr_str=reg.addressOffset.cdata
                    regaddr=literal_eval(addr_str) + base_address + literal_eval(base_address_offset)
                    comments=reg.description.cdata
                    # print(comments)
                    struct_register=cp_register(regname,regaddr,comments,hif)

                    if hasattr(reg,'fields'):
                        for field in reg.fields.field:
                            regfield=field.name.cdata

                            if not field is None:
                                # print(regfield)
                                regfield=name_subs(regfield)
                                width=field.bitWidth.cdata
                                bitoffset=field.bitOffset.cdata
                                comments=field.description.cdata
                                # print(comments)

                                # Create new field class
                                class_regfield=cp_bitfield(
                                    regfield,regaddr,regname,width,bitoffset,comments,hif)
                                struct_register.addfield(class_regfield)
            # create last register, if existing
            if 'regname' in locals():
                # outstruct=addreg2struct(outstruct,regname,struct_register)
                struct_register.dictfield2struct()
                outdict[regname]=struct_register

    # convert output dictionary into structure
    return dict2namedtuple(outdict=outdict)

def test_svd_parse(argv=[]): # pylint: disable=W0102
    """ test function for .svd parser """
    if len(argv) > 1:
        fname=argv[1]
    else:
        fname="./devices/QN908XC.svd"
        # fname="./devices/MIMXRT1011.svd"
    return svd_parse(fname)

if __name__ == '__main__':
    print(svd_parse(sys.argv))
