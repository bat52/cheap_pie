#!/usr/bin/python3

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
# ADC_ANA_CTRL = cp_register("ADC_ANA_CTRL","0x4000702C", "ADC core and reference setting regsiter" , hif )
# ADC_BM = cp_bitfield("ADC_BM","0x4000702C","ADC_ANA_CTRL",3,0, "ADC bias current selection." ,hif)

from cmsis_svd.parser import SVDParser
from ast import literal_eval
import string as str
from collections import namedtuple

import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie_core.cbitfield   import cp_bitfield
from cheap_pie_core.cp_register import cp_register
from parsers.name_subs import name_subs
    
def svd_parse(fname,vendor=None,hif=None, base_address_offset = "0x00000000"):
        
    ## read input file ########################################################
    if vendor is None:
        svd = SVDParser.for_xml_file(fname)
    else:
        svd = SVDParser.for_packaged_svd(vendor,fname)

    ## loop over lines ########################################################
    outdict = dict()

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
                    regname = "%s_%s" % ( periph_name,rname )
                    regname=name_subs(regname)

                    regaddr=reg.address_offset + base_address + literal_eval(base_address_offset)
                    comments=reg.description
                    # print(comments)
                    struct_register=cp_register(regname,regaddr,comments,hif)

                    # for field_idx in range(nfields):
                    if hasattr(reg,'fields'):
                        for field in reg.fields :
                            regfield=field.name

                            if not(field is None):
                                # print regfield
                                regfield=name_subs(regfield)

                                csvWidth=field.bit_width
                                bitoffset=field.bit_offset
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

def test_svd_parse_repo():
    print('Testing QN9080 with repo parser...')

    from parsers.svd_parse_repo import svd_parse
    # hal = svd_parse(fname="./devices/MIMXRT1011.svd")
    hal = svd_parse(fname="./devices/QN908XC.svd")
        
    print('Testing K20 with repo parser...')
    hal = svd_parse(fname='MK20D7.svd',vendor='Freescale')
    
if __name__ == '__main__':
    test_svd_parse_repo()
    pass
    
