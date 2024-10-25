#!/usr/bin/env python3
"""
Register Class Module for Cheap Pie
"""
#
# -*- coding: utf-8 -*-
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

import textwrap
from collections import namedtuple
from ast import literal_eval
from operator import attrgetter
import json

import wavedrom
from wavedrom_ascii import BitfieldASCII
from cheap_pie.cheap_pie_core.cbitfield import CpBitfield


def dict2namedtuple(outdict, tuplename="HAL"):
    """ Convert a dictionary into a namedtuple """
    assert isinstance(outdict, dict)
    return namedtuple(tuplename, outdict.keys())(*outdict.values())


def isnamedtupleinstance(xtuple):
    """ check if a given instance is a namedtuple (can return false positives) """
    # https://stackoverflow.com/questions/2166818/how-to-check-if-an-object-is-an-instance-of-a-namedtuple
    ttt = type(xtuple)
    bbb = ttt.__bases__
    if len(bbb) != 1 or bbb[0] != tuple:
        return False
    fff = getattr(ttt, '_fields', None)
    if not isinstance(fff, tuple):
        return False
    return all(isinstance(n, str) for n in fff)


def reg_add_reserved_bitfields(fields, regwidth=32, fieldname="Reserved", read_write="r"):
    """ Add inferred reserved bits to register description """
    next_lsb = 0
    outfields = []

    if isinstance(fields, list):
        if len(fields) > 0:
            for idx in reversed(range(len(fields))):
                field = fields[idx]
                outfields.insert(0, field)
                # outfields.append(field)

                if next_lsb < field.lsb:
                    # print("Add Reserved field!")
                    newfield = CpBitfield(fieldname, 0, field.regname,
                                          field.lsb-next_lsb, next_lsb,
                                          comments="Reserved",
                                          read_write=read_write)
                    outfields.insert(1, newfield)
                    # outfields.append(newfield)

                # print("LSB: %d, WIDTH: %d" % ( field.lsb, field.width ) )
                next_lsb = field.lsb + field.width

            # check if register is filled up to full width
            if next_lsb < regwidth:
                newfield = CpBitfield(fieldname, 0, fields[0].regname,
                                      regwidth-next_lsb, next_lsb,
                                      comments="Reserved",
                                      read_write=read_write
                                      )
                outfields.insert(0, newfield)

    return outfields


class CpRegister():  # pylint: disable=R0902
    """
    Register Class for Cheap Pie
    """
    addr = 0
    regname = ''
    bitfields = []
    comments = ''
    # host interface handler
    hif = None
    addr_offset = 0
    addr_base = 0
    #

    def __init__(self, regname, regaddr, comments, hif, addr_offset=0, addr_base=0, bitfields=None):  # pylint: disable=R0913
        # address
        self.addr = regaddr

        # name
        self.regname = regname

        # fields
        if not bitfields is None:
            self.bitfields = dict2namedtuple(bitfields)

        # Comments
        self.comments = comments

        # host interface handler
        self.hif = hif

        # address offset
        self.addr_offset = addr_offset

        # address base
        self.addr_base = addr_base

    def getreg(self, asdict=False, as_signed=False):
        """ function getreg(self,regval)
        %
        % Displays value of a register from a register value
        %
        % input : regval value of the full register either in decimal or
        % hexadecimal """

        if not self.hif is None:
            regval = self.hif.hifread(self.addr)
        else:
            regval = 0

        if asdict:
            # dictionary
            retval = {}
            for field in self.bitfields:
                retval[field.fieldname] = field.getbit(regval)
        elif as_signed:
            # signed integer
            retval = -(regval & literal_eval('0x80000000')) + \
                (regval & literal_eval('0x7FFFFFFF'))
        else:
            # unsigned integer (default)
            retval = regval

        return retval

    def setreg(self, regval=0, echo=False, verify=True):  # pylint: disable=W1113
        """ function setreg(self,regval)
        %
        % Displays value of a register from a register value
        %
        % input : regval value of the full register either in decimal or
        % hexadecimal """

        ## handle string input as binary #################################################
        if isinstance(regval, str):
            regval = literal_eval(regval)

        ## handle dict values ############################################################
        elif isinstance(regval, dict):
            rval = self.getreg()
            for field, fval in regval.items():
                rval = self[field].setbit(fval, regval=rval, writeback=False)
            regval = rval

        ## handle negative values ########################################################
        elif regval < 0:
            regval = (abs(regval) ^ literal_eval('0xFFFFFFFF')) + 1
            # print('regval write: 0x%x' % regval)

        # % write %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        if not self.hif is None:
            ret = self.hif.hifwrite(self.addr, regval, verify=verify)
        else:
            ret = regval

        # % only display output if no nargout %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if echo:
            self.display(regval)

        return ret

    def getbit(self, bit_offset=0, width=1):
        """ Get a custom bitfield within a register """
        bitfield = CpBitfield(regaddr=self.addr, width=width,
                              bit_offset=bit_offset, hif=self.hif)
        return bitfield.getbit()

    def setbit(self, bitval=0, bit_offset=0, width=1, verify=True):
        """ Set a custom bitfield within a register """
        bitfield = CpBitfield(regaddr=self.addr, width=width,
                              bit_offset=bit_offset, hif=self.hif)
        return bitfield.setbit(bitval, verify=verify)

    def getbyte(self, byte_offset=0):
        """ Get a custom byte within a register """
        byte = CpBitfield(regaddr=self.addr, width=8,
                          bit_offset=byte_offset*8, hif=self.hif)
        return byte.getbit()

    def setbyte(self, byteval=0, byte_offset=0, verify=True):
        """ Set a custom byte within a register """
        byte = CpBitfield(regaddr=self.addr, width=8,
                          bit_offset=byte_offset*8, hif=self.hif)
        return byte.setbit(byteval, verify=verify)

    def get_addr(self, mode='hex'):
        """ Returns the address of the register
          input:
            mode: 'hex' return hex string, 'dec' returns decimal number
        """
        assert mode in ['hex','dec'], f"Wrong mode {mode}"
        if mode=='dec':
            return self.addr
        if mode=='hex':
            return hex(self.addr) # return hex string
        return 0

    def help(self, width=25):
        """ function ret = help(self)
        # displays register comments """
        self.print_wavedrom()
        print(f"Address: {self.get_addr()}")
        print(self.comments)

        fmtstr = '%%%ds: %%s' % width  # pylint: disable=C0209
        for field in self.bitfields:
            print(fmtstr % (field.fieldname, ''))

            for line in textwrap.wrap(field.comments):
                print(fmtstr % ('', line))

    def __repr__(self, regval=None):
        if len(self.bitfields) > 0:
            reg = []
            for field in self.bitfields:
                # field.display(regval)
                reg.append(field.__repr__(regval=regval))
            outstr = "\n".join(reg)
        else:
            outstr = self.regname + ' = '
            if not regval is None:
                outstr += hex(regval)
        return outstr

    def display(self, regval=None):
        """ Show a register """
        if regval is None:
            # read register value
            regval = self.getreg()
        outstr = self.__repr__(regval)  # pylint: disable=C2801
        print(outstr)
        # return outstr

    def get_bitfields(self, name=None):
        """
        Find a child element by name
        """
        if name:
            return [e for e in self.bitfields if e._name == name]  # pylint: disable=W0212

        return self.bitfields

    def get_ordered_bitfields(self, fieldname="Reserved"):
        """ Return ordered list of bitfields sorted by position and including Reserved fields """
        # convert bitfields namedtuple into list
        bitfields = list(self.bitfields)

        # sort by lsb
        bitfields = sorted(bitfields, key=attrgetter('lsb'))
        bitfields.reverse()

        # add reserved bitfields
        return reg_add_reserved_bitfields(bitfields, fieldname=fieldname)

    def gen_wavedrom(self, vspace=200):
        """ generate wavedrom representation of register """
        wdfields = []

        for field in reversed(self.get_ordered_bitfields(fieldname="")):
            wdfields.append(
                {'name': field.fieldname,
                 'bits': field.width,
                 'attr': field.read_write,
                 'rotate': -90}
            )

        wdconfig = {'vspace': vspace}

        wdreg = {
            'reg': wdfields,
            'config': wdconfig
        }

        return wdreg

    def save_wavedrom_json(self):
        """ Export wavedrom .svg representation of register """
        jfname = f'{self.regname}.json'

        wdlines = json.dumps(self.gen_wavedrom(), indent=2)

        with open(jfname, 'w', encoding='utf-8') as fileh:
            for line in wdlines:
                fileh.write(line)

        return jfname

    def save_wavedrom_svg(self):
        """ Export wavedrom .svg representation of register """
        svgfname = f'{self.regname}.svg'
        jfname = self.save_wavedrom_json()
        wavedrom.render_file(jfname, svgfname)
        return svgfname

    def print_wavedrom(self):
        """ Display wavedrom representation of register in the terminal """
        field = BitfieldASCII.from_dict(self.gen_wavedrom())
        print('')
        print(field)
        return field

    def __contains__(self, key):
        if self.bitfields is None:
            raise TypeError('not indexable')
        return any(item.fieldname == key for item in self.bitfields)

    def __len__(self):
        return len(self.bitfields)

    def __iter__(self):
        return self.bitfields.__iter__()

    def __next__(self):
        return self.bitfields.next()

    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.bitfields[idx]
        if isinstance(idx, str):
            bfdict = self.bitfields._asdict()
            return bfdict[idx]
        assert False, 'Unsupported indexing!'

    def __setitem__(self, idx, value):
        if isinstance(idx, int):
            return self.bitfields[idx].setbit(value)
        if isinstance(idx, str):
            bfdict = self.bitfields._asdict()
            return bfdict[idx].setbit(value)
        assert False, 'Unsupported indexing!'

    def __index__(self):
        return int(self.getreg())


class CpRegBuilder():
    """
    Register Class builder for Cheap Pie
    """
    addr = 0
    regname = ''
    dictfields = {}
    comments = ''
    # host interface handler
    hif = None
    addr_offset = 0
    addr_base = 0

    def __init__(self, regname, regaddr, comments, hif, addr_offset=0, addr_base=0):  # pylint: disable=R0913
        # address
        self.addr = regaddr

        # name
        self.regname = regname

        # Comments
        self.comments = comments

        # host interface handler
        self.hif = hif

        # address offset
        self.addr_offset = addr_offset

        # address base
        self.addr_base = addr_base

        # for some reason need to reset this
        self.dictfields = {}

    def addfield(self, regfield, width, offset, comments=''):
        """ Add a field to a register dictionary of fields """
        self.dictfields[regfield] = CpBitfield(
            regfield=regfield,
            width=width,
            bit_offset=offset,
            comments=comments,
            regaddr=self.addr,
            regname=self.regname,
            hif=self.hif)

    def dictfield2struct(self):
        """ Convert the list of bitfields into a namedtuple """
        return CpRegister(regname=self.regname,
                          regaddr=self.addr,
                          comments=self.comments,
                          hif=self.hif,
                          addr_offset=self.addr_offset,
                          addr_base=self.addr_base,
                          bitfields=self.dictfields)


def test_cp_register():  # pylint: disable=R0914,R0915
    """ Cheap Pie test for cp_register class """
    import sys  # pylint: disable=C0415
    import os.path  # pylint: disable=C0415
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from random import randint  # pylint: disable=C0415
    from transport.cp_dummy_transport import CpDummyTransport  # pylint: disable=C0415,E0401

    reg = CpRegister(
        regname='regname',
        regaddr=10,
        comments='comments',
        hif=CpDummyTransport(),
        addr_offset=10,
        addr_base=10
    )

    print('# setreg, getreg')
    val = 15
    reg.setreg(val)
    assert val == reg.getreg()

    print('# display')
    reg.display()

    print('# help')
    reg.help()

    print('# negative assignement')
    negval = -1
    reg.setreg(negval)
    retval = reg.getreg(as_signed=True)
    print(retval)
    assert retval == negval

    print('# test CpRegBuilder with bitfields')
    reg_build = CpRegBuilder(
        regname='regname',
        regaddr=10,
        comments='comments',
        hif=CpDummyTransport(),
        addr_offset=10,
        addr_base=10
    )

    reg_build.addfield(
        regfield='fname1',
        width='2',
        offset='2',
        comments='comment1',
    )

    reg_build.addfield(
        regfield='fname2',
        width='3',
        offset='4',
        comments='comment2',
    )

    reg = reg_build.dictfield2struct()
    assert isnamedtupleinstance(reg.bitfields)
    assert len(reg.get_bitfields()) == 2

    print('# reg display with bitfields')
    reg.display()
    print('# reg help with bitfields')
    reg.help()

    print('# reg item access')
    reg[0]        # pylint: disable=W0104
    reg['fname1']  # pylint: disable=W0104

    print('# numeric item assignement')
    val = 1
    reg[0] = val
    assert reg[0].getbit() == val

    print('# dict item assignement')
    val = 2
    reg['fname2'] = val
    assert reg['fname2'].getbit() == val

    print('# reg bit access')
    for offset in range(32):
        for bitval in range(2):
            reg.setbit(bitval, bit_offset=offset)
            assert reg.getbit(bit_offset=offset) == bitval

    print('# reg byte access')
    for offset in range(4):
        byteval = randint(0, 255)
        reg.setbyte(byteval, byte_offset=offset)
        assert reg.getbyte(byte_offset=offset) == byteval

    print('# reg integer representation')
    print(hex(reg))

    print('# reg dict-based assignement')
    val1 = 1
    val2 = 2
    dreg = {'fname1': val1, 'fname2': val2}
    reg.setreg(dreg)
    assert reg['fname1'].getbit() == val1
    assert reg['fname2'].getbit() == val2

    print('# reg dict-based readback')
    dregb = reg.getreg(asdict=True)
    assert dreg == dregb

    print('# reg get_ordered_bitfields')
    bitfields = reg.get_ordered_bitfields()
    for field in bitfields:
        print(field)
    assert len(bitfields) == 4

    print('# reg gen wavedrom')
    wd_dict = reg.gen_wavedrom()
    assert isinstance(wd_dict, dict)
    print('# reg save wavedrom json')
    wdfile = reg.save_wavedrom_json()
    assert os.path.isfile(wdfile)
    print('# reg save wavedrom svg')
    wdfile = reg.save_wavedrom_svg()
    assert os.path.isfile(wdfile)

    print('# get_addr default')
    assert reg.get_addr()==hex(reg.addr)
    print('# get_addr hex')
    assert reg.get_addr(mode='hex')==hex(reg.addr)
    print('# get_addr dec')
    assert reg.get_addr(mode='dec')==reg.addr

if __name__ == '__main__':
    test_cp_register()
