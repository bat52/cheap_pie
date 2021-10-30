#!/usr/bin/python3
#
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval
import esptool
import os

class cp_esptool(object):
    """ A wrapper around pyocd transport """
    port = None
    mem = dict()
    
    def __init__(self, port='/dev/ttyUSB0' ):
        if port is None:
            self.port = None
        else:
            print('Connecting to pyocd probe... ') 
            self.port = port
        
    def hifread(self, addr = '0x3ff00014'):
        # print self
        # print addr    

        if isinstance(addr,int):
            # convert to string
            addr = hex(addr)
            
        if not self.port is None:
            #  ret = esptool.main( ['--port' , self.port , '--after no_reset', 'read_mem', addr]  )
            # dump value on file... horrible hack because no output available
            tmpfile = 'tmpdump'
            ret = esptool.main( ['--port' , self.port , '--after', 'no_reset', 'dump_mem', addr, '4', tmpfile]  )

            if os.path.isfile(tmpfile):
                f = open(tmpfile, "rb")
                ret = '0x' + f.read().hex()
                os.remove(tmpfile)                
            else:
                ret = 0

            pass
        else:
            ret = self.mem[addr]
            
        return(ret)

    def hifwrite(self,addr = '0x3ff00014',val = "0x00000352"):

        if isinstance(addr,int):
            addr = hex(addr)
            
        if isinstance(val, int):
            val = hex(val)
        
        if not self.port is None:            
            # ret = esptool.main( ['--port' , self.port , 'write_mem', addr, val ,'0xFFFFFFFF'] )
            ret = esptool.main( ['--port' , self.port , '--after', 'no_reset' ,'write_mem', addr, val ,'0x0'] )
            pass
        else:
            # print hex(addr)
            self.mem[addr] = val
            
        return literal_eval( val )
       

def test_cp_esptool():
    t = cp_esptool(port= None)
    # t = cp_esptool()
    addr = '0x3ff00014'
    val = '2'
    t.hifwrite(addr=addr,val=val)
    val=t.hifread(addr = addr)
    print(val)
    pass

if __name__ == '__main__':
    test_cp_esptool()
    pass
