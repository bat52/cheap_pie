#!/usr/bin/python3

""" Esptool Cheap Pie transport module """

# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import os
from ast import literal_eval
import esptool

from transport.cp_dummy_transport import cp_dummy # pylint: disable=E0401

class cp_esptool(cp_dummy):
    """ A wrapper around esptool transport """
    port = None

    def __init__(self, port='/dev/ttyUSB0' ):
        self.port = port

    def hifread(self, addr = '0x3ff00014'):
        """ read register through esptool """

        if isinstance(addr,int):
            # convert to string
            addr = hex(addr)

        if self.port is None:
            # fallback to dummy transport
            ret = cp_dummy.hifread(self,addr)
        else:
            #  ret = esptool.main( ['--port' , self.port , '--after no_reset', 'read_mem', addr]  )
            # dump value on file... horrible hack because no output available
            tmpfile = 'tmpdump'
            ret = esptool.main( # pylint: disable=E1101
                ['--port' , self.port , '--after',
                'no_reset', 'dump_mem', addr, '4', tmpfile]
                               )

            if os.path.isfile(tmpfile):
                with open(tmpfile, "rb") as tmpfh:
                    ret = '0x' + tmpfh.read().hex()
                os.remove(tmpfile)
            else:
                ret = 0

        return ret

    def hifwrite(self, addr = '0x3ff00014', val = "0x00000352"):
        """ write register through esptool """

        if isinstance(addr,int):
            addr = hex(addr)

        if isinstance(val, int):
            val = hex(val)

        if self.port is None:
            # fallback to dummy transport
            cp_dummy.hifwrite(self,addr,val)
        else:
            esptool.main( # pylint: disable=E1101
                ['--port' , self.port , '--after', 'no_reset' ,'write_mem', addr, val ,'0x0']
                )

        return literal_eval( val )

def test_cp_esptool():
    """ Test esptool transport """
    transport = cp_esptool(port=None)
    addr = '0x3ff00014'
    val = 2
    transport.hifwrite(addr=addr,val=val)
    readback=transport.hifread(addr = addr)
    assert readback==val, 'Wrong readback value! val: %x, readback: %x' % (val,readback) # pylint: disable=C0209

if __name__ == '__main__':
    test_cp_esptool()
