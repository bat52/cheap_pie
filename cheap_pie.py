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
    print line

## configure paths %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
print('Configuring paths...')

import os
import sys
global system_root
system_root = os.getcwd()
sys.path.append(os.path.abspath(system_root + '\\jlink\\'))

## transport hif interface %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
print('Initialising Host Interface...')

# init jlink transport
if (True): # disable jlink for testing
    from jlink.cp_jlink_transport import cp_jlink
    hif = cp_jlink(device = 'QN9080C' )
else:
    hif = None

## init chip ##################################################################
print('Initialising Hardware Abstraction Layer...')

from xmlreg2struct import xmlreg2struct
hal = xmlreg2struct(fname="./devices/QN908XC.xml",hif=hif)
