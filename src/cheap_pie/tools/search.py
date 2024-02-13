#!/usr/bin/env python3

""" Module including functions to search registers and bitifield in a
Cheap Pie register description
"""

# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

from ast import literal_eval


def str_in_str(str1, str2, case_sensitive=True):
    """ Check if a string is present into another string """
    if case_sensitive:
        return str1 in str2
    return str1.upper() in str2.upper()


def register(hal, regname, case_sensitive=True):
    """ Search a register by name """
    retval = []
    for reg in hal:  # loop over all registers
        if str_in_str(regname, reg.regname, case_sensitive):
            print(reg.regname)
            retval.append(reg.regname)
    return retval


def bitfield(hal, bitfield_name, case_sensitive=True):
    """ Search a bitfield by name """
    retval = []
    for reg in hal:  # loop over all registers
        # print reg.regname
        for field in reg.bitfields:
            if str_in_str(bitfield_name, field.fieldname, case_sensitive):
                fieldstr = str(field)
                print(fieldstr)
                retval.append(fieldstr)
    return retval


def address(hal, addr, mask='0xFFFFFFFF'):
    """ Search a register by address """
    # convert address into integer, if needed
    if isinstance(mask, str):
        mask = int(literal_eval(mask))
    if isinstance(addr, str):
        addr = int(literal_eval(addr))

    for reg in hal:  # loop over all registers
        # print reg.regname
        if (reg.addr & mask) == (addr & mask):
            print(reg.regname + " : " + hex(reg.addr))
            return reg.regname

    return ''


def test_search():
    """ Test Search Module """
    from parsers.svd_parse_repo import svd_parse_repo  # pylint: disable=E0401,C0415
    from cheap_pie_core.cp_cli import cp_devices_fname  # pylint: disable=E0401,C0415
    print('Testing search...')

    fname = cp_devices_fname("QN908XC.svd")
    hal = svd_parse_repo(fname=fname, hif=None)

    print('## ADC registers:')
    ret = register(hal, 'ADC')
    assert len(ret) > 0

    print('##  ADC_BM bitfields:')
    ret = bitfield(hal, 'ADC_BM')
    assert len(ret) > 0

    print('## 0x4000702c register name:')
    ret = address(hal, '0x4000702c')
    assert len(ret) > 0

    print('## 0xF000702c register name:')
    ret = address(hal, '0xF000702c', mask='0x0FFFFFFF')
    assert len(ret) > 0

    ret = address(hal, '0xF000702c')
    assert ret == ''


if __name__ == '__main__':
    import sys
    import os.path
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    test_search()
