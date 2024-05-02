#!/usr/bin/env python3
"""
Namedtuple HAL builder for Cheap Pie
"""
#
# -*- coding: utf-8 -*-
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

# import sys     # pylint: disable=C0411
# import os.path # pylint: disable=C0411
# sys.path.append( os.path.join(os.path.dirname(__file__), '..') )

from cheap_pie.cheap_pie_core.cp_register import dict2namedtuple, isnamedtupleinstance, CpRegBuilder  # pylint: disable=C0413,E0401
from cheap_pie.cheap_pie_core.cp_hal import CpHal  # pylint: disable=C0413,E0401


def name_subs(regname=None):
    """ Names Substitution function for Cheap Pie parsers """

    # print(regname)
    # regname=strrep(regname,'"','')
    regname = regname.strip()
    regname = regname.replace('"', '')
    regname = regname.replace('[', '')
    regname = regname.replace(']', '')
    regname = regname.replace('%', '')
    regname = regname.replace('/', '')
    regname = regname.replace('\\', '')
    regname = regname.replace(' ', '_')
    if regname[0].isdigit():
        regname = 'M' + regname
    return regname


class CpHalBuilder():
    """ Namedtuple HAL builder for Cheap Pie """

    hif = None
    outdict = {}
    struct_register = None

    def __init__(self, hif=None):
        self.hif = hif
        # for some reason need to reset this
        self.outdict = {}

    def reg_close(self):
        """ close a register instance declaration """
        if not self.struct_register is None:
            # check
            assert isinstance(self.struct_register, CpRegBuilder)
            self.outdict[self.struct_register.regname] = self.struct_register.dictfield2struct(
            )
            self.struct_register = None

    def reg_open(self, regname, regaddr, comments=''):
        """ start a register instance declaration """
        self.reg_close()
        self.struct_register = CpRegBuilder(
            regname=name_subs(regname),
            regaddr=regaddr,
            comments=comments,
            hif=self.hif)

    def nregs(self):
        """ Return the number of registers already created """
        retval=len(self.outdict)
        if not self.struct_register is None:
            retval += 1
        return retval

    def reg_exists(self,regname):
        """ Returns true if a register with the specified name already exists """
        if not self.struct_register is None:
            if self.struct_register.regname == regname:
                return True

        for key,_ in self.outdict.items():
            if key==regname:
                return True

        return False

    def newfield(self, regfield, width, offset, comments):
        """ add a new field to current register """
        assert isinstance(self.struct_register, CpRegBuilder)
        self.struct_register.addfield(
            regfield=name_subs(regfield),
            width=width,
            offset=offset,
            comments=comments,
        )

    def out(self):
        """ returns a namedtuple that represent the register list """
        self.reg_close()
        return CpHal(dict2namedtuple(outdict=self.outdict))


def test_cp_builder():
    """ test cp_builder """
    cpb = CpHalBuilder()

    assert cpb.nregs()==0
    assert cpb.reg_exists('reg1') is False
    cpb.reg_open('reg1', 1, 'comment1')
    cpb.newfield('reg1_field1', offset=0, width=1, comments='reg1_field1')
    cpb.newfield('reg1_field2', offset=1, width=2, comments='reg1_field2')
    assert cpb.nregs()==1
    assert cpb.reg_exists('reg1') is True

    cpb.reg_open('reg2', 2, 'comment2')
    assert cpb.nregs()==2
    cpb.newfield('reg2_field1', offset=0, width=4, comments='reg2_field1')
    cpb.newfield('reg2_field2', offset=5, width=2, comments='reg2_field2')
    cpb.newfield('reg2_field3', offset=8, width=2, comments='reg2_field3')

    regfile = cpb.out()

    print('# REG1')
    print(regfile.regs.reg1)
    print('# REG2')
    print(regfile.regs.reg2)

    assert isinstance(regfile, CpHal)
    assert len(regfile) == 2

    assert isnamedtupleinstance(regfile.regs)
    assert isnamedtupleinstance(regfile.regs.reg2.bitfields)

    assert len(regfile.regs) == 2
    assert len(regfile.regs.reg1.bitfields) == 2
    assert len(regfile.regs.reg2.bitfields) == 3


if __name__ == '__main__':
    test_cp_builder()
