#!/usr/bin/env python3

""" JLink Cheap Pie transport module """

# -*- coding: utf-8 -*-
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

import pylink
from cheap_pie.transport.cp_dummy_transport import CpDummyTransport, test_cp_dummy, \
    hifread_preproc, hifwrite_preproc  # pylint: disable=E0401


class CpJlinkTransport(CpDummyTransport):
    """ A wrapper around jlink transport """
    jl = None

    def __init__(self, device=None):
        if not device is None:
            self.jl = pylink.JLink()  # pylint: disable=C0103
            self.jl.exec_command('ProjectFile = JLinkSettings.ini')
            self.jl.open()
            self.jl.set_speed(10)
            self.jl.set_tif(pylink.enums.JLinkInterfaces.SWD)
            self.jl.connect(device)
            assert self.jl.connected()

    def __del__(self):
        if not self.jl is None:
            self.jl.close()

    def hifread(self, addr="0x40000888"):
        """ read register through JLink """

        addr = hifread_preproc(addr)

        if self.jl is None:
            ret = CpDummyTransport.hifread(self, addr)
        else:
            read = self.jl.memory_read32(addr, 1)
            ret = read[0]

        return ret

    def hifwrite(self, addr="0x40000888", val="0x00000352", verify=True):
        """ write register through JLink """

        waddr, wval, _ = hifwrite_preproc(addr, val)

        if self.jl is None:
            CpDummyTransport.hifwrite(self, waddr, wval)
        else:
            self.jl.memory_write32(waddr, [wval])

        if verify:
            assert int(self.hifread(addr))==int(wval)

        return int(wval)


def test_cp_jlink():
    """ test JLink transport """
    test_cp_dummy(
        CpJlinkTransport(device=None)
    )


if __name__ == '__main__':
    test_cp_jlink()
