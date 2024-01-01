#!/usr/bin/env python3
"""
This file is part of cheap_pie, a python tool for chip validation
 author: Marco Merlin
 email: marcomerli@gmail.com
"""

if __name__ == '__main__':
    # needed if cheap_pie not installed
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from cheap_pie.parsers.cp_parsers_wrapper import cp_parsers_wrapper  # pylint: disable=C0413,E0401
from cheap_pie.parsers.svd_parse_repo import svd_repo_print_vendors, svd_repo_print_vendor_devices # pylint: disable=C0413,E0401
from cheap_pie.cheap_pie_core.cp_banner import cp_banner            # pylint: disable=C0413,E0401
from cheap_pie.cheap_pie_core.cp_cli import cp_cli                  # pylint: disable=C0413,E0401
from cheap_pie.transport.cp_dummy_transport import CpDummyTransport  # pylint: disable=C0413,E0401

# Ipython autoreload
# %load_ext autoreload
# %autoreload 2
# %reset
# %run cheap_pie


def cp_main(argv=[]):  # pylint: disable=W0102
    """
    Main cheap_pie function
    """
    ## banner #######################################################################
    cp_banner()
    #
    ## input parameters ###########################################################
    print('Parsing input arguments...')
    prms = cp_cli(argv)

    ## helper functions ###########################################################

    if prms.vendors:
        return svd_repo_print_vendors()
    if prms.devices:
        return svd_repo_print_vendor_devices(vendor=prms.vendor)

    # transport hif interface %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    print('Initialising Host Interface...')

    # init jlink transport: importing under if case allows not installing all transport libraries
    if prms.transport == 'dummy':
        hif = CpDummyTransport()
    elif prms.transport == 'jlink':  # disable jlink for testing
        from cheap_pie.transport.cp_jlink_transport import CpJlinkTransport  # pylint: disable=C0413,C0415,E0401
        hif = CpJlinkTransport(device=prms.device)
    elif prms.transport == 'ocd':
        from cheap_pie.transport.cp_pyocd_transport import CpPyocdTransport  # pylint: disable=C0413,C0415,E0401
        hif = CpPyocdTransport(device=prms.device)
    elif prms.transport == 'esptool':
        from cheap_pie.transport.cp_esptool_transport import CpEsptoolTransport  # pylint: disable=C0413,C0415,E0401
        hif = CpEsptoolTransport(port=prms.port)
    elif prms.transport == 'verilator':
        from cheap_pie.transport.cp_pyverilator_transport import CpPyverilatorTransport  # pylint: disable=C0413,C0415,E0401
        hif = CpPyverilatorTransport(prms.top_verilog)
    else:
        hif = None
        assert False, f'Invalid transport: {prms.transport}'

    ## init chip ##################################################################
    print('Initialising Hardware Abstraction Layer...')
    lhal = cp_parsers_wrapper(prms, hif=hif)

    ## welcome ####################################################################
    print('Cheap Pie is ready! Type hal.<TAB> to start browsing...')

    return lhal


if __name__ == '__main__':
    hal = cp_main(sys.argv[1:])
