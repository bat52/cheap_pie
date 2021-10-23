#!/usr/bin/python3
#
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

"""
Created on Wed Jan 17 18:03:31 2018

@author: Marco Merlin
"""

# Ipython autoreload
# %load_ext autoreload
# %autoreload 2
# %reset
# %run cheap_pie

# init transport
import sys
# clear all references
sys.modules[__name__].__dict__.clear()

## logo #######################################################################

logo = (
"  ____ _                        ____  _      _ ",
" / ___| |__   ___  __ _ _ __   |  _ \(_) ___| |",
"| |   | '_ \ / _ \/ _` | '_ \  | |_) | |/ _ \ |",
"| |___| | | |  __/ (_| | |_) | |  __/| |  __/_|",
" \____|_| |_|\___|\__,_| .__/  |_|   |_|\___(_)",
"                       |_|                     ",
"A python tool for chip validation by Marco Merlin\n"
)
for line in logo:
    print(line)

## input parameters ###########################################################
print('Parsing input arguments...')

if 'p' not in locals():
    from cp_cli import cp_cli
    import sys
    p = cp_cli(sys.argv[1:])

## configure paths %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
print('Configuring paths...')

import os
import sys
global system_root
system_root = os.getcwd()

## transport hif interface %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
print('Initialising Host Interface...')

# init jlink transport
if p.transport == 'jlink': # disable jlink for testing
    from cp_jlink_transport import cp_jlink
    # hif = cp_jlink(device = 'QN9080C' )
    hif = cp_jlink(device = p.jdevice )
elif p.transport == 'dummy':
    from cp_dummy_transport import cp_dummy
    hif = cp_dummy()
else:
    hif=None
    # assert(False,'Invalid transport: %s' % p.transport)
    assert(False)

## init chip ##################################################################
print('Initialising Hardware Abstraction Layer...')

from xmlreg2struct import xmlreg2struct
fname = os.path.join(p.devicedir,p.regfname)
print(fname)
# parser build for CMSIS-SVD xml file format
hal = xmlreg2struct(fname=fname,hif=hif)

## welcome ####################################################################
print('Cheap Pie is ready! Type hal.<TAB> to start browsing...')