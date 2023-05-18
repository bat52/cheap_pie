#!/usr/bin/python3
"""
Register Class Module for Cheap Pie
"""
#
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import textwrap
from collections import namedtuple
from ast import literal_eval

try:
    # cheap_pie installed with pip
    from cheap_pie.cheap_pie_core.cbitfield import cp_bitfield
except:
    try:
        from cheap_pie_core.cbitfield import cp_bitfield
    except:
        from cbitfield import cp_bitfield

class cp_register(): # pylint: disable=R0902
    """
    Register Class for Cheap Pie
    """
    addr = 0
    regname = ''
    bitfields = []
    dictfields = {}
    comments = ''
    # host interface handler
    hif = None
    addr_offset = 0
    addr_base   = 0
    #
    def __init__(self, regname, regaddr, comments, hif, addr_offset=0, addr_base=0): # pylint: disable=R0913
        # address
        self.addr = regaddr

        # name
        self.regname = regname

        # fields
        self.dictfields = {}

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
        else :
            regval = 0

        if asdict:
            # dictionary
            retval = {}
            for field in self.bitfields:
                retval[field.fieldname] = field.getbit(regval)
        elif as_signed:
            # signed integer
            retval = -(regval & literal_eval('0x80000000')) + (regval & literal_eval('0x7FFFFFFF'))
        else:
            # unsigned integer (default)
            retval = regval

        return retval

    def setreg(self,regval = 0, echo =False, *args,**kwargs): # pylint: disable=W1113
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
        elif isinstance(regval,dict):
            rval = self.getreg()
            for field,fval in regval.items():
                rval = self[field].setbit(fval, regval=rval, writeback=False)
            regval = rval

        ## handle negative values ########################################################
        elif regval < 0:
            regval = (abs(regval) ^ literal_eval('0xFFFFFFFF')) + 1
            # print('regval write: 0x%x' % regval)

        #% write %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        if not self.hif is None:
            ret = self.hif.hifwrite(self.addr, regval, *args,**kwargs)
        else :
            ret = regval

        #% only display output if no nargout %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if echo:
            self.display(regval)

        return ret

    def getbit(self, bit_offset=0, width=1):
        """ Get a custom bitfield within a register """
        bitfield = cp_bitfield(regaddr=self.addr, width=width, bit_offset=bit_offset, hif=self.hif)
        return bitfield.getbit()

    def setbit(self, bitval=0, bit_offset=0, width=1):
        """ Set a custom bitfield within a register """
        bitfield = cp_bitfield(regaddr=self.addr, width=width, bit_offset=bit_offset, hif=self.hif)
        return bitfield.setbit(bitval)

    def getbyte(self, byte_offset=0):
        """ Get a custom byte within a register """
        byte = cp_bitfield(regaddr=self.addr, width=8, bit_offset=byte_offset*8, hif=self.hif)
        return byte.getbit()

    def setbyte(self, byteval=0, byte_offset=0):
        """ Set a custom byte within a register """
        byte = cp_bitfield(regaddr=self.addr, width=8, bit_offset=byte_offset*8, hif=self.hif)
        return byte.setbit(byteval)

    def help(self,width=25):
        """ function ret = help(self)
        # displays register comments """
        print(self.comments)

        fmtstr = '%%%ds: %%s' % width # pylint: disable=C0209
        for field in self.bitfields:
            print( fmtstr % (field.fieldname,''))

            for line in textwrap.wrap(field.comments):
                print( fmtstr % ('',line))

    def __repr__(self,regval = None ):
        if len(self.bitfields) > 0:
            reg = []
            for field in self.bitfields :
                # field.display(regval)
                reg.append(field.__repr__(regval=regval))
            outstr = "\n".join(reg)
        else:
            outstr = self.regname + ' = '
            if not regval is None:
                outstr += hex(regval)
        return outstr

    def display(self, regval = None ):
        """ Show a register """
        if regval is None:
            # read register value
            regval = self.getreg()
        outstr = self.__repr__(regval) # pylint: disable=C2801
        print(outstr)
        # return outstr

    def addfield(self, field):
        """ Add a field to a register """
        self.dictfields[field.fieldname] = field

    def dictfield2struct(self):
        """ Convert the list of bitfields into a namedtuple """
        if len(self.dictfields) > 0:
            self.bitfields = namedtuple(self.regname,
                                        self.dictfields.keys())(*self.dictfields.values())

    def get_bitfields(self, name=None):
        """
        Find a child element by name
        """
        if name:
            return [e for e in self.bitfields if e._name == name] # pylint: disable=W0212

        return self.bitfields

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
        if isinstance(idx,int):
            return self.bitfields[idx]
        if isinstance(idx,str):
            return self.bitfields._asdict()[idx]
        assert False, 'Unsupported indexing!'

    def __setitem__(self, idx, value):
        if isinstance(idx,int):
            return self.bitfields[idx].setbit(value)
        if isinstance(idx,str):
            return self.bitfields._asdict()[idx].setbit(value)
        assert False, 'Unsupported indexing!'

    def __index__(self):
        return int(self.getreg())

def test_cp_register(): # pylint: disable=R0914,R0915
    """ Cheap Pie test for cp_register class """
    import sys # pylint: disable=C0415
    import os.path # pylint: disable=C0415
    sys.path.append( os.path.join(os.path.dirname(__file__), '..') )
    from random import randint # pylint: disable=C0415
    from transport.cp_dummy_transport import CpDummyTransport # pylint: disable=C0415,E0401

    reg = cp_register(
        regname='regname',
        regaddr=10,
        comments='comments',
        hif = CpDummyTransport(),
        addr_offset=10,
        addr_base=10
    )

    print('# setreg, getreg')
    val = 15
    reg.setreg(val)
    assert val==reg.getreg()

    print('# display')
    reg.display()

    print('# help')
    reg.help()

    print('# negative assignement')
    negval = -1
    reg.setreg(negval)
    retval = reg.getreg(as_signed=True)
    print(retval)
    assert retval==negval

    print('# test bitfield')
    field1 = cp_bitfield(
        regfield = 'fname',
        regaddr = 10,
        regname = 'rname',
        width = '2',
        bit_offset = '2',
        comments = 'comment',
        hif = CpDummyTransport()
    )
    field2 = cp_bitfield(
        regfield = 'fname2',
        regaddr = 10,
        regname = 'rname',
        width = '2',
        bit_offset = '4',
        comments = 'comment2',
        hif = CpDummyTransport()
    )

    reg.addfield(field1)
    reg.addfield(field2)
    reg.dictfield2struct()
    reg.get_bitfields()

    print('# reg display with bitfields')
    reg.display()
    print('# reg help with bitfields')
    reg.help()

    print('# reg item access')
    reg[0]       # pylint: disable=W0104
    reg['fname'] # pylint: disable=W0104

    print('# item assignement')
    reg[0] = 1
    reg['fname'] = 2

    print('# reg bit access')
    for offset in range(32):
        for bitval in range(2):
            reg.setbit(bitval, bit_offset=offset)
            assert reg.getbit(bit_offset=offset) == bitval

    print('# reg byte access')
    for offset in range(4):
        byteval = randint(0,255)
        reg.setbyte(byteval, byte_offset=offset)
        assert reg.getbyte(byte_offset=offset) == byteval

    print('# reg integer representation')
    print(hex(reg))

    print('# reg dict-based assignement')
    dreg = {'fname': 1, 'fname2': 2}
    reg.setreg(dreg)

    print('# reg dict-based readback')
    dregb = reg.getreg(asdict=True)
    assert dreg == dregb

if __name__ == '__main__':
    test_cp_register()
