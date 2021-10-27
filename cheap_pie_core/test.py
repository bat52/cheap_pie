#!/usr/bin/python3

# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval
import unittest

import sys
import os.path
sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

class CheapPieMethods(unittest.TestCase):

    def _test_transport(self):
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

        # subscriptable interface
        hal[0];
        hal[0][0];

        print('Test QN9080 Done')
   
    def test_hal(self):
        hifs = self._test_transport()        
        for hif in hifs:
            print(hif)
            self._test_qn9080( hif )            

    def test_parsers(self):
        from parsers.svd_parse import test_svd_parse
        test_svd_parse()

        from parsers.svd_parse_repo import test_svd_parse_repo
        test_svd_parse_repo()

        from parsers.ipxact_parse import test_ipxact_parse
        test_ipxact_parse()

    def test_tools(self):
        from tools.hal2doc import test_hal2doc
        test_hal2doc()

        from tools.search import test_search
        test_search()
        pass

    def test_cheap_pie_main(self):
        import cheap_pie_core.cheap_pie 

if __name__ == '__main__':
    unittest.main()
