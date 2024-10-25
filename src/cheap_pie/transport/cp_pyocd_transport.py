#!/usr/bin/env python3

""" pyocd Cheap Pie transport module """

# -*- coding: utf-8 -*-
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

from pyocd.core.helpers import ConnectHelper
from cheap_pie.transport.cp_dummy_transport import CpDummyTransport, test_cp_dummy, \
    hifread_preproc, hifwrite_preproc  # pylint: disable=E0401


class CpPyocdTransport(CpDummyTransport):
    """ A wrapper around pyocd transport """
    ocd = None

    def __init__(self, device=None):
        if not device is None:
            print('Connecting to pyocd probe... ')
            self.ocd = ConnectHelper.session_with_chosen_probe(
                target_override=device)
            self.ocd.open()
            # print(self.ocd.board)
            # print(self.ocd.target)
            # print(self.ocd.target.memory_map)

    def hifread(self, addr="0x40000888"):
        """ read register through pyocd """

        addr = hifread_preproc(addr)

        if self.ocd is None:
            ret = CpDummyTransport.hifread(self, addr)
        else:
            # ret = self.ocd.board.target.dp.read_reg(addr)
            ret = self.ocd.board.target.read32(addr)

        return ret

    def hifwrite(self, addr="0x40000888", val="0x00000352", verify=True):
        """ rwrite register through pyocd """
        waddr, wval, _ = hifwrite_preproc(addr, val)

        if self.ocd is None:
            CpDummyTransport.hifwrite(self, waddr, wval)
        else:
            # ret = self.ocd.board.target.dp.write_reg(addr,val)
            self.ocd.board.target.write32(waddr, wval)

        if verify:
            assert int(self.hifread(addr))==int(wval)

        return int(val)


def test_cp_pyocd():
    """ test pyocd transport """
    test_cp_dummy(
        CpPyocdTransport()
    )


if __name__ == '__main__':
    test_cp_pyocd()
