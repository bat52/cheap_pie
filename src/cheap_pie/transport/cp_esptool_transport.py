#!/usr/bin/env python3

""" Esptool Cheap Pie transport module """

# -*- coding: utf-8 -*-
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

import os
from ast import literal_eval
import esptool

from cheap_pie.transport.cp_dummy_transport import CpDummyTransport, test_cp_dummy  # pylint: disable=E0401


class CpEsptoolTransport(CpDummyTransport):
    """ A wrapper around esptool transport """
    port = None

    def __init__(self, port='/dev/ttyUSB0'):
        self.port = port

    def hifread(self, addr='0x3ff00014'):
        """ read register through esptool """

        if isinstance(addr, int):
            # convert to string
            addr = hex(addr)

        if self.port is None:
            # fallback to dummy transport
            ret = CpDummyTransport.hifread(self, addr)
        else:
            #  ret = esptool.main( ['--port' , self.port , '--after no_reset', 'read_mem', addr]  )
            # dump value on file... horrible hack because no output available
            tmpfile = 'tmpdump'
            esptool.main(  # pylint: disable=E1101
                ['--port', self.port, '--after',
                 'no_reset', 'dump_mem', addr, '4', tmpfile]
            )

            ret = 0
            if os.path.isfile(tmpfile):
                with open(tmpfile, "rb") as tmpfh:
                    ret = '0x' + tmpfh.read().hex()
                os.remove(tmpfile)

        return ret

    def hifwrite(self, addr='0x3ff00014', val="0x00000352", verify=True):
        """ write register through esptool """

        if isinstance(addr, int):
            addr = hex(addr)

        if isinstance(val, int):
            val = hex(val)

        if self.port is None:
            # fallback to dummy transport
            CpDummyTransport.hifwrite(self, addr, val)
        else:
            esptool.main(  # pylint: disable=E1101
                ['--port', self.port, '--after', 'no_reset',
                    'write_mem', addr, val, '0x0']
            )

        if verify:
            assert self.hifread(addr)==literal_eval(val)

        return literal_eval(val)


def test_cp_esptool():
    """ Test esptool transport """
    test_cp_dummy(
        transport=CpEsptoolTransport(port=None)
    )


if __name__ == '__main__':
    test_cp_esptool()
