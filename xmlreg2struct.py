#!/usr/bin/python3

## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

# simplified manual initialization
# 
# import untangle
# hal = untangle.parse('QN908XC.xml')
# from cbitfield import cp_bitfield
# from cp_register import cp_register
# ADC_ANA_CTRL = cp_register("ADC_ANA_CTRL","0x4000702C", "ADC core and reference setting regsiter" , hif )
# ADC_BM = cp_bitfield("ADC_BM","0x4000702C","ADC_ANA_CTRL",3,0, "ADC bias current selection." ,hif)

import untangle # for parsing xml
from ast import literal_eval
import string as str
from collections import namedtuple

from cbitfield   import cp_bitfield
from cp_register import cp_register
import sys
    
def xmlreg2struct(fname,hif=None):
    
    ## get full file name #####################################################
    #if logical_not(exist(fname,'file')):
    #    fname,fpath=uigetfile('*.xml',nargout=2)
    #    fname=fullfile(fpath,fname)
    
    ## read input file ########################################################
    csv = untangle.parse(fname)

    ## loop over lines ########################################################
    outdict = dict()

    for periph in csv.device.peripherals.peripheral:
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
                    periph_name=periph.name.cdata
                    rname=reg.name.cdata
                    regname = "%s_%s" % ( periph_name,rname )
                    regname=name_subs(regname)

                    addr_str=reg.addressOffset.cdata
                    regaddr=literal_eval(addr_str) + base_address
                    comments=reg.description.cdata
                    # print(comments)
                    struct_register=cp_register(regname,regaddr,comments,hif)

                    # for field_idx in range(nfields):
                    if hasattr(reg,'fields'):
                        for field in reg.fields.field :
                            regfield=field.name.cdata

                            if not(field is None):
                                # print regfield
                                regfield=name_subs(regfield)

                                csvWidth=field.bitWidth.cdata
                                bitoffset=field.bitOffset.cdata
                                comments=field.description.cdata
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
    
def name_subs(regname=None):

    # print(regname)
    # regname=strrep(regname,'"','')
    regname=regname.replace('"','')
    regname=regname.replace('[','')
    regname=regname.replace(']','')
    regname=regname.replace('%','')
    if regname[0].isdigit():
        regname= 'M' + regname
    
    return regname
    
if __name__ == '__main__':
    if len(sys.argv) > 1: 
        fname=sys.argv[1]
    else:
        # fname="./devices/QN908XC.xml"
        fname="./devices/MIMXRT1011.xml"
    xmlreg2struct(fname)
    pass
    
