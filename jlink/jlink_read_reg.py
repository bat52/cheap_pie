# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 11:12:22 2015

Example (Ipython console):
run jlink_read_reg.py 0x40000888 <CORTEX-M4|QN9080C>

Example (windows command line):
python jlink_read_reg.py 0x40000888 <CORTEX-M4|QN9080C>

@author: Marco Merlin: marcomerli@gmail.com
"""
from jlink import JLink
import sys
from ast import literal_eval

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: %s <ADDRESS> <DEVICE>' % sys.argv[0])
    
    addr = sys.argv[1]
    
    if len(sys.argv) > 2:
        device = sys.argv[2]
    else:
        device = "QN9080C"
        
    jl = JLink(device)
    # print addr    
    r,b = jl.read_mem_U32(literal_eval(addr),1);
    
    print hex(r[0])