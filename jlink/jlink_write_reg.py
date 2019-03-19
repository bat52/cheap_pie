# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:12:22 2015

Example (Ipython console):
run jlink_write_reg.py 0x40000888 0x00000352 <CORTEX-M4|QN9080C>

Example (windows command line):
python jlink_write_reg.py 0x40000888 0x00000352 <CORTEX-M4|QN9080C>

@author: Marco Merlin: marcomerli@gmail.com
"""
from jlink import JLink
import sys
from ast import literal_eval

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('Usage: %s <ADDRESS> <VALUE> <DEVICE>' % sys.argv[0])
    
    addr = sys.argv[1]
    val  = sys.argv[2]
    
    # print addr
    # print val
    
    if len(sys.argv) > 3:
        device = sys.argv[3]
    else:
        device = "QN9080C"
        
    jl = JLink(device)
    # r,b = jl.write_U32(addr,int(val,32))
    # r,b = jl.write_U32(literal_eval(addr),int( literal_eval(val),32 ))
    # jl.write_U32(literal_eval(addr),int('352',32))
    # jl.write_U32(literal_eval(addr),int(val,32))
    # jl.write_U32(literal_eval(addr),literal_eval(val))
    
    jl.write_U32(literal_eval(addr), int( literal_eval(val) ) )
    
    #print r
    #print b