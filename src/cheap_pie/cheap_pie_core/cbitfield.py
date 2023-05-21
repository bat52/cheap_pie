#!/usr/bin/python3
"""
bitfield register class for cheap-pie.
"""
#
# Autogenerated with SMOP
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval

class CpBitfield():  # pylint: disable=R0902
    """A bitfield register class """
    # field width
    width = 1

    # LSB
    lsb = 1

    # mask
    mask = 1

    # comments
    comments = ""

    # Address (Duplicate information)
    addr = 0

    # reg name
    regname = ""

    # field name
    fieldname = ""

    # host interface handler
    hif = None

    # read/write
    read_write = "rw"

    # reset value
    reset = 0

    def __init__(self, regfield="",regaddr=0, regname="", width="1", # pylint: disable=R0913
                 bit_offset="0", comments="", hif=None, read_write = "rw", reset=0):

        if isinstance(width,str):
            width= literal_eval(width)
        # field width
        self.width = int( width )

        if isinstance(bit_offset,str):
            lsb=literal_eval(bit_offset)
        else:
            lsb = bit_offset
        self.lsb = int( lsb )

        if lsb is None:
            print(f'Bad definition for register field {regname} @ {regfield}!')
            lsb=0

        if isinstance(regaddr,str):
            regaddr=literal_eval(regaddr)

        # mask
        bstr = "0b" + ("1" * self.width) + ("0" * self.lsb)
        self.mask=literal_eval( bstr )
        self.comments = comments
        self.addr = int( regaddr )
        self.regname = regname
        self.fieldname = regfield
        self.hif = hif

        assert isinstance(read_write,str)
        assert read_write.lower() in ['r','w','rw']
        self.read_write = read_write

        self.reset = reset

    def __str__(self,fieldval=None,width=25):
        """ returns value string of a bitfield from a register value
        input : regval value of the full register either in decimal or
        hexadecimal """
        #
        bitstr = self.fieldname  + ' [' + str(self.width) + ']'
        if not fieldval is None:
            bitstr += ' = ' + hex(fieldval)

        if self.width > 1:
            msb = str( self.lsb + self.width - 1)
            regstr = self.regname + '[' + msb + ':' + str(self.lsb) + ']'
        else:
            regstr = self.regname + '[' + str(self.lsb) + ']'

        fmtstr = '%%%ds @ %%%ds' % (width,width) # pylint: disable=C0209
        return fmtstr % (regstr,bitstr)

    def __repr__(self, regval = None):
        """
        displays position of a bitfield in a register
        """
        #
        if regval is None:
            fieldval = None
        else:
            fieldval = self.getbit(regval=regval)
        return self.__str__(fieldval=fieldval)

    def display(self,regval=None):
        """
        Display the bitfield
        """
        fieldval = self.getbit(regval=regval)
        fieldstr = self.__str__(fieldval=fieldval) # pylint: disable=C2801
        print(fieldstr)

    def getbit(self,regval=None,echo=False,as_signed=False,*args,**kwargs):
        """ function display(self,regval=None,echo=False,as_signed=False)
        # displays value of a bitfield from a register value
        # input : regval value of the full register either in decimal or
        # hexadecimal"""
        #
        if regval is None:
            if self.hif is None:
                regval=0
            else:
                regval=self.hif.hifread(self.addr,*args,**kwargs)

        # compute field value from register value
        if isinstance(regval, str):
            regval=literal_eval(regval)
        fieldval = (regval & self.mask ) >> (self.lsb)

        # get bitfield as signed value
        if as_signed:
            fieldsign = -(fieldval & (1 << (self.width - 1)))
            fieldmod = (fieldval & (self.mask>>(self.lsb+1)))
            fieldval = fieldsign + fieldmod

        if echo:
            self.display(regval)
        #
        return fieldval

    def setbit(self,fieldval=0,echo=False, writeback=True, regval=None,*args,**kwargs): # pylint: disable=W1113
        """ function display(self,regval)
        # displays value of a bitfield from a register value
        # input : regval value of the full register either in decimal or
        # hexadecimal """

        ## read input register value ###################################################
        if not (self.hif is None) and regval is None:
            hexval=self.hif.hifread(self.addr)
            if isinstance(hexval, str):
                regval=literal_eval(hexval)
            else:
                regval = hexval
        #
        ## handle char input as binary #################################################
        if isinstance(fieldval, str):
            fieldval = literal_eval(fieldval)

        ## handle negative values ######################################################
        if fieldval < 0:
            fieldval = (abs(fieldval) ^ (self.mask >> self.lsb)) + 1

        ## compute new register value ##################################################
        #
        shiftval= fieldval << self.lsb
        maskinv= self.mask ^ literal_eval('0xFFFFFFFF')
        regmasked = regval & maskinv
        outregval = regmasked + (shiftval & self.mask)

        # check new value in range
        if (shiftval & self.mask) < shiftval:
            raise ValueError(f'Bitifield value f{fieldval} out of range!')
        #
        ## write back new register value ###############################################
        if writeback:
            self.hif.hifwrite(self.addr,outregval,*args,**kwargs)
        #
        if echo:
            self.display(regval=regval)
        #
        return outregval

    #@function
    def help(self):
        """ function ret = help(self)
        # displays register comments """
        print(self.comments)

    def __index__(self):
        return int(self.getbit())

def test_cp_bitfield():
    """
    Test function for cp_bitfield class
    """
    import sys # pylint: disable=C0415
    import os.path # pylint: disable=C0415
    sys.path.append( os.path.join(os.path.dirname(__file__), '..') )
    from transport.cp_dummy_transport import CpDummyTransport # pylint: disable=C0415, disable=E0401

    field = CpBitfield(
        regfield = 'fname',
        regaddr = 10,
        regname = 'rname',
        width = '2',
        bit_offset = '2',
        comments = 'comment',
        hif = CpDummyTransport()
    )

    print('# setbit, getbit')
    val = 3
    field.setbit(val)
    assert field.getbit() == val

    print('# display')
    field.display(4)

    print('# str')
    print(str(field))

    print('# print')
    print(field)

    print('# help')
    field.help()

    print('# signed assignement')
    negval = -1
    field.setbit(negval)
    retval = field.getbit(as_signed=True)
    assert negval==retval

    print('# decimal representation')
    print(hex(field))

    print('# setbit with echo')
    field.setbit(val,echo=True)

    print('# setbit without writeback')
    val=1
    field.setbit(val)
    assert field.getbit() == val
    newval = 3
    field.setbit(newval,writeback=False)
    assert field.getbit() == val

    print('# setbit with regval')
    val=3
    regretval = field.setbit(val)
    assert field.setbit(val,regval=regretval) == regretval

    print('# test assertion')
    try:
        field.setbit(7)
        assert False, 'Assertion was not raised!!!'
    except ValueError as error:
        print(f'Assertion raised correctly: <{error}>')

if __name__ == '__main__':
    test_cp_bitfield()
