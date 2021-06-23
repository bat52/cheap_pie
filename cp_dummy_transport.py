# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval

class cp_dummy(object):
    """ A transport mockup """
    mem = dict()
           
    def hifread(self, addr = "0x40000888"):
        # print self
        # print addr    

        if isinstance(addr,str):
            addr = int(literal_eval(addr))
            
        ret = self.mem[hex(addr)]
            
        # print hex(r[0])
        return(ret)

    def hifwrite(self,addr = "0x40000888",val = "0x00000352"):

        if isinstance(addr,str):
            addr = int( literal_eval(addr) )
            
        if isinstance(val, str):
            val = int ( literal_eval(val) )
        
        # print hex(addr)
        self.mem[hex(addr)] = val
            
        return int( val )
