# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com
"""
Created on Mon Mar 05 16:22:48 2018

@author: Marco Merlin
"""
from ast import literal_eval
import unittest

class CheapPieMethods(unittest.TestCase):

    def test_paths(self):        
        print('Configuring paths...')

        import os
        import sys
        global system_root
        system_root = os.getcwd()
        sys.path.append(os.path.abspath(system_root + '\\jlink\\'))

    def test_transport(self):
        self.test_paths()
        print('Initialising Host Interface...');

        # init jlink transport
        from jlink.cp_jlink_transport import cp_jlink
        # cannot run transport tests without chip connected to pc
        hif = cp_jlink('NONE')
        return hif

    def test_hal(self):
        hif = self.test_transport()
        print('Initialising Hardware Abstraction Layer...')

        from xmlreg2struct import xmlreg2struct
        hal = xmlreg2struct(fname="./devices/QN908XC.xml", hif = hif)
        
        print('Test register methods...')     
        # hex assignement       
        inval = "0xFFFFFFFF"
        hal.ADC_ANA_CTRL.setreg(inval)
        retval = hex(hal.ADC_ANA_CTRL.getreg())
        assert(literal_eval(inval) == literal_eval(retval))

        # decimal assignement        
        inval = 2
        hal.ADC_ANA_CTRL.setreg(inval)
        retval = hal.ADC_ANA_CTRL.getreg()        
        assert(inval == retval)
        
        hal.ADC_ANA_CTRL.display()
                
        print('Test bitfield methods...')
        
        hal.ADC_ANA_CTRL.bitfields.ADC_BM.display()
        hal.ADC_ANA_CTRL.bitfields.ADC_BM.display(2)
        hal.ADC_ANA_CTRL.bitfields.ADC_BM.setbit(inval)
        retval = hal.ADC_ANA_CTRL.bitfields.ADC_BM.getbit()
        assert(inval == retval)

if __name__ == '__main__':
    unittest.main()