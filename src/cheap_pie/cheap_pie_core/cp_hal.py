#!/usr/bin/python3
"""
Cheap Pie Hardware Abstraction Layer
"""
#
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import sys
import os.path
import hickle as hkl

sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from transport.cp_dummy_transport import cp_dummy
import tools.search
from tools.hal2doc import hal2doc

class cp_hal:
    """
    Cheap Pie Hardware Abstraction Layer
    """
    regs = []
    hif = None

    def __init__(self,regs):
        self.regs = regs
        if len(regs) > 0:
            self.hif = regs[0].hif
        else:
            print('# WARNING: no register defined!')

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
        assert False,'Unsupported indexing!'

    def __setitem__(self, idx, value):
        if isinstance(idx,int):
            return self.regs[idx].setreg(value)
        elif isinstance(idx,str):
            return self.regs._asdict()[idx].setreg(value)
        assert False, 'Unsupported indexing!'

## search methods ###########################################################

    def search_bitfield(self,field,case_sensitive=False):
        """
        Search bitfields which name contains a specified string
        """
        return tools.search.bitfield(self.regs,field,case_sensitive=case_sensitive)

    def search_register(self,reg,case_sensitive=False):
        """
        Search registers which name contains a specified string
        """
        return tools.search.register(self.regs,reg,case_sensitive=case_sensitive)

    def search_address(self,address,mask='0xFFFFFFFF'):
        """
        Search register matching a specified address
        """
        return tools.search.address(self.regs,address,mask=mask)

    def to_docx(self,*args):
        """
        Generate a .docx document describing an Hardware Abstraction Layer
        """
        hal2doc(self.regs,*args)

## dump methods #############################################################
    def regs2dict(self):
        """
        Converts an hal structure into a dictionary in the form:
        dictval = {
            'reg1': val1,
            'reg2': val2,
        }
        """
        outdict = {}
        for reg,val in self.regs._asdict().items():
            outdict[reg] = val.getreg()
        return outdict

    def dump(self,fname='dump.hkl'):
        """
        Dump the value of all registers in a .hkl file.
        """
        regs_dict = self.regs2dict()
        hkl.dump(regs_dict, fname, compression='gzip')

    def dump_diff(self,f1name='dump.hkl',f2name='dump2.hkl',width = 60):
        """
        Perform a diff on two dumped .hkl files.
        """
        fmtstr = '%%%ds |%%%ds' % (width,width)

        field1 = hkl.load(f1name)
        field2 = hkl.load(f2name)

        # create a header with filenames
        outstrlist = []
        for reg,val in field1.items():
            if not field2[reg] == val:
                f1regstr = self[reg].__repr__(val).split('\n')
                f2regstr = self[reg].__repr__(field2[reg]).split('\n')

                for idx in range(len(f1regstr)):
                    if not f1regstr[idx]==f2regstr[idx]:
                        linestr = fmtstr % (f1regstr[idx],f2regstr[idx])
                        outstrlist.append(linestr)

        # print output
        if len(outstrlist) > 0:
            headerstr = fmtstr % (f1name,f2name)
            outstrlist.insert(0,headerstr)
            for line in outstrlist:
                print(line)
        else:
            print('No differences found!!!')

def test_to_docx():
    """
    Test Function for Cheap Pie HAL to .docx
    """
    from parsers.cp_parsers_wrapper import cp_parsers_wrapper
    from cheap_pie_core.cp_cli import cp_cli

    prms = cp_cli(['-t','dummy','-rf','my_subblock.xml','-fmt','ipxact'])
    hal = cp_hal(cp_parsers_wrapper(prms))

    hal.to_docx()

def test_cp_hal():
    """
    Test Function for Cheap Pie Hardware Abstraction Layer
    """
    from parsers.cp_parsers_wrapper import cp_parsers_wrapper
    from cheap_pie_core.cp_cli import cp_cli
    from ast import literal_eval

    prms = cp_cli(['-t','dummy'])
    hal = cp_hal(cp_parsers_wrapper(prms,cp_dummy()))

    print('Test register methods...')
    # hex assignement
    inval = "0xFFFFFFFF"
    hal.regs.ADC_ANA_CTRL.setreg(inval)
    retval = hex(hal.regs.ADC_ANA_CTRL.getreg())
    # print('%s' % retval.encode('hex'))
    print(retval)
    assert literal_eval(inval) == literal_eval(retval)

    # decimal assignement
    inval = 2
    hal.regs.ADC_ANA_CTRL.setreg(inval)
    retval = hal.regs.ADC_ANA_CTRL.getreg()
    assert inval == retval

    hal.regs.ADC_ANA_CTRL.display()
    print('Test bitfield methods...')

    hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.display()
    hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.display(2)
    hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.setbit(inval)
    retval = hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.getbit()
    assert inval == retval

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
    reg = hal.search_register('ADC_ANA_CTRL')
    assert len(reg)>0
    field = hal.search_bitfield('ADC_BM')
    assert len(field)>0
    reg = hal.search_address('0x4000702c')
    assert len(reg)>0
    reg = hal.search_address('0xF000702c',mask='0x0FFFFFFF')
    assert len(reg)>0
    reg = hal.search_address('0xF000702c')
    assert reg is None

    # test conversion to doc
    test_to_docx()

    # test dump
    dump1 = 'dump1.hkl'
    dump2 = 'dump2.hkl'
    hal.dump(dump1)
    hal['ADC_ANA_CTRL']['ADC_BM'] = 3
    hal.dump(dump2)
    hal.dump_diff(dump1,dump2)

if __name__ == '__main__':
    test_cp_hal()
