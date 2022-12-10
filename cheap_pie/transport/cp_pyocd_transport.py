#!/usr/bin/python3
#
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval
from pyocd.core.helpers import ConnectHelper

class cp_pyocd(object):
    """ A wrapper around pyocd transport """
    ocd = None
    mem = dict()
    
    def __init__(self,device = None ):
        if device is None:
            self.ocd = None
        else:
            print('Connecting to pyocd probe... ') 
            self.ocd = ConnectHelper.session_with_chosen_probe(target_override=device)
            self.ocd.open()
            # print(self.ocd.board)
            # print(self.ocd.target)
            # print(self.ocd.target.memory_map)
        
    def hifread(self, addr = "0x40000888"):
        # print self
        # print addr    

        if isinstance(addr,str):
            addr = int(literal_eval(addr))
            
        if not self.ocd is None:
            # ret = self.ocd.board.target.dp.read_reg(addr)
            ret = self.ocd.board.target.read32(addr)
            pass
        else:
            ret = self.mem[hex(addr)]
            
        # print hex(r[0])
        return(ret)

    def hifwrite(self,addr = "0x40000888",val = "0x00000352"):

        if isinstance(addr,str):
            addr = int( literal_eval(addr) )
            
        if isinstance(val, str):
            val = int ( literal_eval(val) )
        
        if not self.ocd is None:
            # ret = self.ocd.board.target.dp.write_reg(addr,val)
            ret = self.ocd.board.target.write32(addr,val)
            pass
        else:
            # print hex(addr)
            self.mem[hex(addr)] = val
            
        return int( val )
       

def test_cp_pyocd():
    # t = cp_pyocd(device = None)
    t = cp_pyocd()
    addr = 4
    val = 5
    t.hifwrite(addr=addr,val=val)
    val=t.hifread(addr = addr)
    pass

if __name__ == '__main__':
    test_cp_pyocd()
    pass
