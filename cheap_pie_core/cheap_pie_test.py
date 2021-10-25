#!/usr/bin/python3

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

import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

class CheapPieMethods(unittest.TestCase):
    def test_paths(self):        
        print('Configuring paths...')

        import os
        import sys
        global system_root
        system_root = os.getcwd()
        # sys.path.append(os.path.abspath(system_root + '\\jlink\\'))

    def test_transport(self):
        self.test_paths()
        print('Initialising Host Interface...')

        hifs = []

        # dummy for mockup
        from transport.cp_dummy_transport import cp_dummy
        # cannot run transport tests without chip connected to pc
        hifs.append( cp_dummy() )

        # jlink
        from transport.cp_jlink_transport import cp_jlink
        # cannot run transport tests without chip connected to pc
        hifs.append( cp_jlink(None) )

        # print('Testing hifs:')
        # print(hifs)
        print('Initialising Host Interface Done')

        return hifs

    def _test_qn9080(self, hif, hal=None):
        print('Initialising QN9080 Hardware Abstraction Layer...')
        if hal is None:
            from parsers.svd_parse import svd_parse
            hal = svd_parse(fname="./devices/QN908XC.svd", hif = hif)

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

        print('Test QN9080 Done')

    def _test_rt1010(self, hif):
        print('Initialising RT1010 Hardware Abstraction Layer...')
        from parsers.svd_parse import svd_parse
        hal = svd_parse(fname="./devices/MIMXRT1011.svd", hif = hif)

        print('Test register methods...')     
        # hex assignement       
        inval = "0xFFFFFFFF"
        hal.ADC1_CAL.setreg(inval)
        retval = hex(hal.ADC1_CAL.getreg())
        assert(literal_eval(inval) == literal_eval(retval))
        hal.ADC1_CAL.bitfields.CAL_CODE.display()
        
        print('Test RT1010 Done')
    
    def test_hal(self):
        hifs = self.test_transport()        
        for hif in hifs:
            print(hif)
            self._test_qn9080( hif )            
            self._test_rt1010( hif )

    def test_parse_repo(self):
        print('Testing QN9080 with repo parser...')

        hif = self.test_transport()[0]  
        from parsers.svd_parse_repo import svd_parse
        hal = svd_parse(fname="./devices/QN908XC.svd",hif = hif)
        self._test_qn9080( hif , hal = hal )
        
        print('Testing K20 with repo parser...')
        hal = svd_parse(fname='MK20D7.svd',vendor='Freescale',hif = hif)

    def test_hal2doc(self):
        from parsers.svd_parse import svd_parse
        from tools.hal2doc import hal2doc
        hal = svd_parse(fname="./devices/QN908XC.svd")
        
        # convert to .docx
        hal2doc(hal)
        pass

    def test_ipxact(self):
        from parsers.ipxact_parse import ipxact_parse
        hal = ipxact_parse(fname="./devices/my_subblock.xml")
        hal.my_subblock_reg1.bitfields.f1.display() 

if __name__ == '__main__':
    unittest.main()
