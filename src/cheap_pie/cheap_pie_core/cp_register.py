#!/usr/bin/python3
#
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

import textwrap
from collections import namedtuple
from ast import literal_eval

try:
    from cheap_pie_core.cbitfield import cp_bitfield
except:
    from cbitfield import cp_bitfield    

class cp_register:
    """ A chip register class """
    addr = 0    
    regname = ''
    bitfields = []
    dictfields = dict()
    comments = ''
    # host interface handler
    hif = None
    addr_offset = 0
    addr_base   = 0
    
    def __init__(self, regname, regaddr, comments, hif, addr_offset=0, addr_base=0):
        # address
        self.addr = regaddr        
        
        # name
        self.regname = regname
        
        # fields
        self.dictfields = dict()
        
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
        
        # if isinstance(self.hif,cp_jlink):
        if not (self.hif is None ):
            regval = self.hif.hifread(self.addr)
        else :
            regval = 0

        if asdict:
            # dictionary
            retval = dict()
            for field in self.bitfields:
                retval[field.fieldname] = field.getbit(regval)
        elif as_signed:
            # signed integer
            retval = -(regval & literal_eval('0x80000000')) + (regval & literal_eval('0x7FFFFFFF'))
        else: 
            # unsigned integer (default)
            retval = regval
        
        return retval    
        
    def setreg(self,regval = 0, echo =False, *args,**kwargs):
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
            for f,fval in regval.items():
                rval = self[f].setbit(fval, regval=rval, writeback=False)
            regval = rval

        ## handle negative values ########################################################
        elif regval < 0:
            regval = (abs(regval) ^ literal_eval('0xFFFFFFFF')) + 1
            # print('regval write: 0x%x' % regval)

        #% write %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        # if isinstance(self.hif,cp_jlink):   
        if not (self.hif is None ):                    
            ret = self.hif.hifwrite(self.addr, regval, *args,**kwargs)
        else :
            ret = regval
        
        #% only display output if no nargout %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        if echo:
            self.display(regval)          
        
        return ret

    def getbit(self, bit_offset=0, width=1):                
        b = cp_bitfield(regaddr=self.addr, width=width, bit_offset=bit_offset, hif=self.hif)        
        return b.getbit()

    def setbit(self, bitval=0, bit_offset=0, width=1):                
        b = cp_bitfield(regaddr=self.addr, width=width, bit_offset=bit_offset, hif=self.hif)        
        return b.setbit(bitval)

    def getbyte(self, byte_offset=0):
        b = cp_bitfield(regaddr=self.addr, width=8, bit_offset=byte_offset*8, hif=self.hif)        
        return b.getbit()

    def setbyte(self, byteval=0, byte_offset=0):
        b = cp_bitfield(regaddr=self.addr, width=8, bit_offset=byte_offset*8, hif=self.hif)        
        return b.setbit(byteval)

    def help(self,width=25):
        """ function ret = help(self)        
        # displays register comments """    
        print(self.comments)
        
        fmtstr = '%%%ds: %%s' % width
        for field in self.bitfields:
            print( fmtstr % (field.fieldname,''))

            for line in textwrap.wrap(field.comments):
                print( fmtstr % ('',line))
        
    def __repr__(self,regval = None ):
        if regval is None:
            # read register value
            regval = self.getreg()

        if len(self.bitfields) > 0:
            r = []        
            for field in self.bitfields :
                # field.display(regval)
                r.append(field.__repr__(regval))        
            outstr = "\n".join(r)
        else: 
            outstr = self.regname + ' = ' + hex(regval)
        return outstr

    def display(self, regval = None ):
        r = self.__repr__(regval=regval)
        print(r)
        return r    
        
    def addfield(self, field):
        # assert isinstance(field,cp_bitfield)
        # self.bitfields.append(field)
        self.dictfields[field.fieldname] = field
        # cmdstr = "self." + field.fieldname + " = field "
        # eval(cmdstr)
        
    def dictfield2struct(self):
        if len(self.dictfields) > 0:
            self.bitfields = namedtuple(self.regname, self.dictfields.keys())(*self.dictfields.values())
        
    def get_bitfields(self, name=None):
        """
        Find a child element by name
        """
        if name:
            return [e for e in self.bitfields if e._name == name]
        else:
            return self.bitfields

    def __contains__(self, key):
        if self.bitfields is None:
            raise TypeError('not indexable')
        return any(item.fieldname == key for item in self.bitfields)

    def __len__(self):
        return len(self.bitfields)

    def __iter__(self):
        return self.bitfields.__iter__()
        # for field in self.bitfields:
        #    yield (field.fieldname, field.getbit())
    
    def __next__(self):
        return self.bitfields.next()
    
    def __getitem__(self, idx):
        if isinstance(idx,int):
            return self.bitfields[idx]
        elif isinstance(idx,str):
            return self.bitfields._asdict()[idx]
        else:
            print('Unsupported indexing!')
            assert(False)
        pass    
    
    def __setitem__(self, idx, value):
        if isinstance(idx,int):
            return self.bitfields[idx].setbit(value)
        elif isinstance(idx,str):
            return self.bitfields._asdict()[idx].setbit(value)
        else:
            print('Unsupported indexing!')
            assert(False)
        pass

    def __index__(self):
        return int(self.getreg())

def test_cp_register():
    import sys
    import os.path
    sys.path.append( os.path.join(os.path.dirname(__file__), '..') )
    from transport.cp_dummy_transport import cp_dummy
    from cheap_pie_core.cbitfield import cp_bitfield
    from random import randint

    r = cp_register( 
        regname='regname',
        regaddr=10,
        comments='comments',
        hif = cp_dummy(),
        addr_offset=10,
        addr_base=10
    )

    # test value
    val = 15
    r.setreg(val)
    assert(val==r.getreg())
    r.display()
    r.help()

    # negative assignement
    negval = -1
    r.setreg(negval)
    retval = r.getreg(as_signed=True)
    print(retval)
    assert(retval==negval)

    # test bitfield
    f1 = cp_bitfield(
        regfield = 'fname',
        regaddr = 10,
        regname = 'rname',
        width = '2',
        bit_offset = '2',
        comments = 'comment',
        hif = cp_dummy()
    )
    f2 = cp_bitfield(
        regfield = 'fname2',
        regaddr = 10,
        regname = 'rname',
        width = '2',
        bit_offset = '4',
        comments = 'comment2',
        hif = cp_dummy()
    )

    r.addfield(f1)
    r.addfield(f2)
    r.dictfield2struct()
    r.get_bitfields()
    # display with bitfields
    r.display()
    r.help()

    # item access
    r[0]
    r['fname']

    # item assignement
    r[0] = 1
    r['fname'] = 2

    # bit access
    for offset in range(32):
        for bitval in range(2):
            r.setbit(bitval, bit_offset=offset)    
            assert( r.getbit(bit_offset=offset) == bitval ) 
    
    # byte access
    for offset in range(4):
        byteval = randint(0,255)
        r.setbyte(byteval, byte_offset=offset)    
        assert( r.getbyte(byte_offset=offset) == byteval ) 

    # integer representation
    print(hex(r))

    # dict-based assignement
    d = {'fname': 1, 'fname2': 2}
    r.setreg(d)

    # dict-based readback
    dr = r.getreg(asdict=True)
    assert(d == dr)

if __name__ == '__main__':
    test_cp_register()
    pass
