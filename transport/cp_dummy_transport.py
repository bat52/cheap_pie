#!/usr/bin/python3
#
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval

def hex_bw(val,hex_digits_width = 8 ):
    """ converts integer value into an hex string of fixed width """  
    
    assert( isinstance(val,int) )

    retstr = "{0:#0{1}x}".format(val,hex_digits_width+2)

    #  Explanation:
    # {   # Format identifier
    # 0:  # first parameter
    # #   # use "0x" prefix
    # 0   # fill with zeroes
    # {1} # to a length of n characters (including 0x), defined by the second parameter
    # x   # hexadecimal number, using lowercase letters for a-f
    # }   # End of format identifier

    # print(retstr)

    return(retstr)

class cp_dummy(object):
    """ A transport mockup """
    mem = dict()
           
    def hifread(self, addr = "0x40000888"):

        # make sure string format is always the same
        if isinstance(addr,str):
            addr = int(literal_eval(addr))

        addrstr = hex_bw(addr)
        
        # check address exists, or create it
        if addrstr not in self.mem.keys():
            self.mem[addrstr] = 0

        ret = self.mem[addrstr]
        return(ret)

    def hifwrite(self,addr = "0x40000888",val = "0x00000352"):

        if isinstance(addr,str):
            addr = int( literal_eval(addr) )
            
        if isinstance(val, str):
            val  = int ( literal_eval(val) )
        
        self.mem[hex_bw(addr)] = val
            
        return int( val )

def test_cp_dummy():
    t = cp_dummy()
    addr = 4
    val = 5
    t.hifwrite(addr=addr,val=val)
    assert( val==t.hifread(addr = addr) )
    pass

if __name__ == '__main__':
    test_cp_dummy()
    pass
