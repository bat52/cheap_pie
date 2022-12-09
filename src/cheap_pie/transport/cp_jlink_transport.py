#!/usr/bin/python3
#
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import pylink
from ast import literal_eval

class cp_jlink(object):
    """ A wrapper around jlink transport """
    jl = None
    mem = dict()
    
    def __init__(self,device = 'QN9080C'):
        if device is None:
            self.jl = None
        else: 
            self.jl = pylink.JLink()
            self.jl.exec_command('ProjectFile = JLinkSettings.ini')
            self.jl.open()
            self.jl.set_speed(10)
            self.jl.set_tif(pylink.enums.JLinkInterfaces.SWD)
            self.jl.connect(device)
            assert(self.jl.connected()==True)

    def __del__(self):
        if not (self.jl is None):
            self.jl.close()
        
    def hifread(self, addr = "0x40000888"):
        # print self
        # print addr    

        if isinstance(addr,str):
            addr = int(literal_eval(addr))
            
        if not self.jl is None:
            r = self.jl.memory_read32(addr,1)
            ret = r[0]
        else:
            ret = self.mem[hex(addr)]
            
        # print hex(r[0])
        return(ret)

    def hifwrite(self,addr = "0x40000888",val = "0x00000352"):

        if isinstance(addr,str):
            addr = int( literal_eval(addr) )
            
        if isinstance(val, str):
            val = int ( literal_eval(val) )
        
        if not self.jl is None:
            self.jl.memory_write32( addr, [val] )
        else:
            # print hex(addr)
            self.mem[hex(addr)] = val
            
        return int( val )
        
    """ def halt(self):
        self.jl.halt()
        return(0)
        
    def go(self):
        self.jl.go()
        return(0) """

def test_cp_jlink():
    t = cp_jlink(device = None)
    addr = 4
    val = 5
    t.hifwrite(addr=addr,val=val)
    val=t.hifread(addr = addr)
    pass

if __name__ == '__main__':
    test_cp_jlink()
    pass
