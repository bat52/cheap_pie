#!/usr/bin/env python3
""" Cheap Pie module for native .svd files parser """
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

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
import untangle  # for parsing xml

from cheap_pie.cheap_pie_core.cp_builder import CpHalBuilder  # pylint: disable=C0413,E0401
from cheap_pie.cheap_pie_core.cp_cli import cp_devices_fname


def svd_parse(fname, vendor=None, hif=None, base_address_offset="0x00000000"):  # pylint: disable=W0613
    """ Cheap Pie native parser for .svd files """
    ## read input file ########################################################
    svd = untangle.parse(fname)

    ## loop over lines ########################################################
    cpb = CpHalBuilder(hif)

    for periph in svd.device.peripherals.peripheral:  # pylint: disable=R1702
        # print(periph.name.cdata)

        base_addr_str = periph.baseAddress.cdata
        base_address = literal_eval(base_addr_str)

        if hasattr(periph, 'registers'):
            for reg in periph.registers.register:
                if hasattr(reg.name, 'cdata'):
                    # new register
                    addr_str = reg.addressOffset.cdata
                    regaddr = (
                        literal_eval(addr_str) +
                        base_address +
                        literal_eval(base_address_offset)
                    )

                    cpb.reg_open(
                        regname=f'{periph.name.cdata}_{reg.name.cdata}',
                        regaddr=regaddr,
                        comments=reg.description.cdata,
                    )

                    if hasattr(reg, 'fields'):
                        for field in reg.fields.field:
                            if not field is None:
                                # Create new field class
                                cpb.newfield( # pylint: disable=R0801
                                    regfield=field.name.cdata,
                                    width=field.bitWidth.cdata,
                                    offset=field.bitOffset.cdata,
                                    comments=field.description.cdata,
                                )

    # convert output dictionary into structure
    return cpb.out()


def test_svd_parse(argv=[]):  # pylint: disable=W0102
    """ test function for .svd parser """

    if len(argv) > 1:
        fname = argv[1]
    else:
        fname = cp_devices_fname("QN908XC.svd")

    hal = svd_parse(fname)
    assert len(hal) > 0

    return hal


if __name__ == '__main__':
    import sys
    print(svd_parse(sys.argv))
