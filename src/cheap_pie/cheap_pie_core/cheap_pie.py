#!/usr/bin/python3
"""
This file is part of cheap_pie, a python tool for chip validation
 author: Marco Merlin
 email: marcomerli@gmail.com
"""

# Ipython autoreload
# %load_ext autoreload
# %autoreload 2
# %reset
# %run cheap_pie

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie_core.cp_banner import cp_banner
from cheap_pie_core.cp_cli import cp_cli
from parsers.cp_parsers_wrapper import cp_parsers_wrapper
from cheap_pie_core.cp_hal import cp_hal

def main(argv=[]):
    ## banner #######################################################################
    cp_banner()
    
    ## input parameters ###########################################################
    print('Parsing input arguments...')
    p = cp_cli(argv)

    ## transport hif interface %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    print('Initialising Host Interface...')

    # init jlink transport
    if p.transport == 'jlink': # disable jlink for testing
        from transport.cp_jlink_transport import cp_jlink
        hif = cp_jlink(device = p.device )
    elif p.transport == 'dummy':
        from transport.cp_dummy_transport import cp_dummy
        hif = cp_dummy()
    elif p.transport == 'ocd':
        from transport.cp_pyocd_transport import cp_pyocd
        hif = cp_pyocd(device = p.device )
    elif p.transport == 'esptool':
        from transport.cp_esptool_transport import cp_esptool
        hif = cp_esptool(port = p.port )   
    elif p.transport == 'verilator':
        from transport.cp_pyverilator_transport import cp_pyverilator_transport
        hif = cp_pyverilator_transport( p.top_verilog )
    else:
        hif=None
        # assert(False,'Invalid transport: %s' % p.transport)
        assert(False)

    ## init chip ##################################################################
    print('Initialising Hardware Abstraction Layer...')
    hal = cp_hal( cp_parsers_wrapper( p, hif=hif ) )

    ## welcome ####################################################################
    print('Cheap Pie is ready! Type hal.<TAB> to start browsing...')

    return hal

if __name__ == '__main__':    
    # global system_root
    # system_root = os.getcwd()

    hal = main(sys.argv[1:])
    pass