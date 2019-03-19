# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from jlink import JLink
from ast import literal_eval

class cp_jlink(object):
    """ A wrapper around jlink transport """
    jl = None
    mem = dict()
    
    def __init__(self,device = 'QN9080C'):
        if device is 'NONE':
            self.jl = None
        else: 
            self.jl = JLink(device)
        
    def hifread(self, addr = "0x40000888"):
        # print self
        # print addr    

        if isinstance(addr,str):
            addr = int(literal_eval(addr))
            
        if not self.jl is None:
            r,b = self.jl.read_mem_U32(addr,1)
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
            self.jl.write_U32( addr, val )
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
