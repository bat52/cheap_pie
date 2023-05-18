#!/usr/bin/python3

""" JLink Cheap Pie transport module """

# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval
import pylink
from transport.cp_dummy_transport import cp_dummy # pylint: disable=E0401
class cp_jlink(cp_dummy):
    """ A wrapper around jlink transport """
    jl = None

    def __init__(self, device = None ):
        if not device is None:
            self.jl = pylink.JLink() # pylint: disable=C0103
            self.jl.exec_command('ProjectFile = JLinkSettings.ini')
            self.jl.open()
            self.jl.set_speed(10)
            self.jl.set_tif(pylink.enums.JLinkInterfaces.SWD)
            self.jl.connect(device)
            assert self.jl.connected()

    def __del__(self):
        if not self.jl is None:
            self.jl.close()

    def hifread(self, addr = "0x40000888"):
        """ read register through JLink """

        if isinstance(addr,str):
            addr = int(literal_eval(addr))

        if self.jl is None:
            ret = cp_dummy.hifread(self,addr)
        else:
            read = self.jl.memory_read32(addr,1)
            ret = read[0]

        return ret

    def hifwrite(self,addr = "0x40000888",val = "0x00000352"):
        """ write register through JLink """

        if isinstance(addr,str):
            addr = int( literal_eval(addr) )

        if isinstance(val, str):
            val = int ( literal_eval(val) )

        if self.jl is None:
            cp_dummy.hifwrite(self, addr, val)
        else:
            self.jl.memory_write32( addr, [val] )

        return int( val )

def test_cp_jlink():
    """ test JLink transport """
    transport = cp_jlink(device = None)
    addr = 4
    val = 5
    transport.hifwrite(addr=addr,val=val)
    retval=transport.hifread(addr = addr)
    assert retval==val

if __name__ == '__main__':
    test_cp_jlink()
