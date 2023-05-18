#!/usr/bin/python3
"""
This file is part of cheap_pie, a python tool for chip validation
 author: Marco Merlin
 email: marcomerli@gmail.com
"""

import os
import sys
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from parsers.cp_parsers_wrapper import cp_parsers_wrapper # pylint: disable=C0413,E0401
from cheap_pie_core.cp_banner import cp_banner            # pylint: disable=C0413,E0401
from cheap_pie_core.cp_cli import cp_cli                  # pylint: disable=C0413,E0401
from cheap_pie_core.cp_hal import cp_hal                  # pylint: disable=C0413,E0401

# Ipython autoreload
# %load_ext autoreload
# %autoreload 2
# %reset
# %run cheap_pie

def cp_main(argv=[]): # pylint: disable=W0102
    """
    Main cheap_pie function
    """
    ## banner #######################################################################
    cp_banner()
    #
    ## input parameters ###########################################################
    print('Parsing input arguments...')
    prms = cp_cli(argv)

    ## transport hif interface %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    print('Initialising Host Interface...')

    # init jlink transport: importing under if case allows not installing all transport libraries
    if prms.transport == 'jlink': # disable jlink for testing
        from transport.cp_jlink_transport import cp_jlink # pylint: disable=C0413,C0415,E0401
        hif = cp_jlink(device = prms.device )
    elif prms.transport == 'dummy':
        from transport.cp_dummy_transport import cp_dummy # pylint: disable=C0413,C0415,E0401
        hif = cp_dummy()
    elif prms.transport == 'ocd':
        from transport.cp_pyocd_transport import cp_pyocd # pylint: disable=C0413,C0415,E0401
        hif = cp_pyocd(device = prms.device )
    elif prms.transport == 'esptool':
        from transport.cp_esptool_transport import cp_esptool # pylint: disable=C0413,C0415,E0401
        hif = cp_esptool(port = prms.port )
    elif prms.transport == 'verilator':
        from transport.cp_pyverilator_transport import cp_pyverilator_transport # pylint: disable=C0413,C0415,E0401
        hif = cp_pyverilator_transport( prms.top_verilog )
    else:
        hif=None
        assert False, f'Invalid transport: {prms.transport}'

    ## init chip ##################################################################
    print('Initialising Hardware Abstraction Layer...')
    lhal = cp_hal( cp_parsers_wrapper( prms, hif=hif ) )

    ## welcome ####################################################################
    print('Cheap Pie is ready! Type hal.<TAB> to start browsing...')

    return lhal

if __name__ == '__main__':
    hal = cp_main(sys.argv[1:])
