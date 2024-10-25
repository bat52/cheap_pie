#!/usr/bin/env python3
""" A dummy mockup transport module for Cheap Pie """

# -*- coding: utf-8 -*-
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

from ast import literal_eval
from abc import ABCMeta


def hex_bw(val, hex_digits_width=8):
    """ converts integer value into an hex string of fixed width """
    assert isinstance(val, int)

    retstr = "{0:#0{1}x}".format( # pylint: disable=C0209
        val, hex_digits_width+2)

    #  Explanation:
    # {   # Format identifier
    # 0:  # first parameter
    # #   # use "0x" prefix
    # 0   # fill with zeroes
    # {1} # to a length of n characters (including 0x), defined by the second parameter
    # x   # hexadecimal number, using lowercase letters for a-f
    # }   # End of format identifier

    # print(retstr)

    return retstr


def numeric_input(val):
    """ Numeric input that supports string evaluation with literal_eval """
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        return int(literal_eval(val))
    assert False, f'Unsupported input type: {type(val)}'


def hifread_preproc(addr):
    """ convert input of hifread into numeric """
    return numeric_input(addr)


def hifwrite_preproc(addr, val, mask='0xFFFFFFFF'):
    """ convert input of hifwrite into numeric """
    return numeric_input(addr), numeric_input(val), numeric_input(mask)


class CpDummyTransport(metaclass=ABCMeta):
    """ A transport mockup """
    mem = {}

    def hifread(self, addr="0x40000888"):
        """ Mockup for read a register """

        # make sure string format is always the same
        addr = hifread_preproc(addr)

        addrstr = hex_bw(addr)

        # check address exists, or create it
        if addrstr not in self.mem.keys():  # pylint: disable=C0201
            self.mem[addrstr] = 0

        return self.mem[addrstr]

    def hifwrite(self, addr="0x40000888", val="0x00000352", verify=True):
        """ Mockup for write a register """

        waddr, wval, _ = hifwrite_preproc(addr, val)

        self.mem[hex_bw(waddr)] = wval

        if verify:
            assert int(self.hifread(addr))==int(wval)

        return int(wval)


def test_cp_dummy(transport=CpDummyTransport()):
    """ Test transport mockup """
    print("# Test dummy transport")
    addr = 4
    val = 5
    transport.hifwrite(addr=addr, val=val)
    assert val == transport.hifread(addr=addr)


if __name__ == '__main__':
    test_cp_dummy()
