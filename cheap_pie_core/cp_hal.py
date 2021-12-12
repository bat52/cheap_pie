#!/usr/bin/python3
#
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import sys
import os.path

sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from transport.cp_dummy_transport import cp_dummy
import tools.search
from tools.hal2doc import hal2doc

class cp_hal:
    regs = []
    hif = None
    """ Hardware abstraction layer class """
    def __init__(self,regs):
        self.regs = regs
        self.hif = regs[0].hif
        pass

    def __len__(self):
        return len(self.regs)

    def __iter__(self):
        return self.regs.__iter__()
    
    def __next__(self):
        return self.regs.next()
    
    def __getitem__(self, idx):
        if isinstance(idx,int):
            return self.regs[idx]
        elif isinstance(idx,str):
            return self.regs._asdict()[idx]
        else:
            print('Unsupported indexing!')
            assert(False)
    
    def __setitem__(self, idx, value):
        if isinstance(idx,int):
            return self.regs[idx].setreg(value)
        elif isinstance(idx,str):
            return self.regs._asdict()[idx].setreg(value)
        else:
            print('Unsupported indexing!')
            assert(False)

    def search_bitfield(self,field):
        return tools.search.bitfield(self.regs,field)
        pass

    def search_register(self,reg):
        return tools.search.register(self.regs,reg)

    def to_docx(self,*args):
        hal2doc(self.regs,*args)

    pass


def test_to_docx():
    from parsers.cp_parsers_wrapper import cp_parsers_wrapper
    from cheap_pie_core.cp_cli import cp_cli
    
    p = cp_cli(['-t','dummy','-rf','my_subblock.xml','-fmt','ipxact'])
    hal = cp_hal(cp_parsers_wrapper(p))

    hal.to_docx()
    pass

def test_cp_hal():
    from parsers.cp_parsers_wrapper import cp_parsers_wrapper
    from cheap_pie_core.cp_cli import cp_cli
    from ast import literal_eval

    p = cp_cli(['-t','dummy'])
    hal = cp_hal(cp_parsers_wrapper(p,cp_dummy()))

    print('Test register methods...')     
    # hex assignement       
    inval = "0xFFFFFFFF"
    hal.regs.ADC_ANA_CTRL.setreg(inval)
    retval = hex(hal.regs.ADC_ANA_CTRL.getreg())
    # print('%s' % retval.encode('hex'))
    print(retval)
    assert(literal_eval(inval) == literal_eval(retval))

    # decimal assignement        
    inval = 2
    hal.regs.ADC_ANA_CTRL.setreg(inval)
    retval = hal.regs.ADC_ANA_CTRL.getreg()        
    assert(inval == retval)

    hal.regs.ADC_ANA_CTRL.display()
            
    print('Test bitfield methods...')

    hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.display()
    hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.display(2)
    hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.setbit(inval)
    retval = hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.getbit()
    assert(inval == retval)

    # subscriptable interface
    hal[0]
    hal[0][0]
    hal['ADC_ANA_CTRL']

    # test assignement
    hal['ADC_ANA_CTRL'] = 1
    hal['ADC_ANA_CTRL']['ADC_BM'] = 2
    # dict-based assignement in single register write
    hal['ADC_ANA_CTRL'] = {'DITHER_EN': 1, 'CHOP_EN': 1, 'INV_CLK': 1}

    # test search
    r = hal.search_register('ADC_ANA_CTRL')
    f = hal.search_bitfield('ADC_BM')

    # test conversion to doc
    # hal.to_docx()
    test_to_docx()
    pass
        
if __name__ == '__main__':    
    test_cp_hal()
    pass