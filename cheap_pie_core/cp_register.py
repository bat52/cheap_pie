#!/usr/bin/python3
#
# -*- coding: utf-8 -*-
## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

# from cbitfield import cp_bitfield
from collections import namedtuple

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

    def getreg(self):
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
        
        return regval
        
    def setreg(self,regval = 0, *args,**kwargs):
        """ function setreg(self,regval)
        %
        % Displays value of a register from a register value
        %
        % input : regval value of the full register either in decimal or
        % hexadecimal """        
        
        # convert to number if in hexa format
        #if ischar(regval)
        #    regval = hex2dec(regval);        
        
        #% write %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        
        # if isinstance(self.hif,cp_jlink):   
        if not (self.hif is None ):                    
            ret = self.hif.hifwrite(self.addr,regval, *args,**kwargs)
        else :
            ret = regval
        
        #% only display output if no nargout %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # if setreg.nargout == 0:
        self.display(regval)
        # fields = fieldnames(self.fields);
        #structfun(@(x) x.display(regval),self.fields,'UniformOutput',false);                
        
        return ret

    def help(self):
        """ function ret = help(self)        
        # displays register comments """    
        print(self.comments)
        
    def __repr__(self,regval = "0" ):
        # read register value
        regval = self.getreg()

        r = []
        # 
        for field in self.bitfields :
            # field.display(regval)
            r.append(field.__repr__(regval))
        
        jr = "\n".join(r)
        return jr

    def display(self,regval = "0" ):
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

    # test bitfield
    f = cp_bitfield(
        regfield = 'fname',
        regaddr = 10,
        regname = 'rname',
        width = '2',
        bit_offset = '2',
        comments = 'comment',
        hif = cp_dummy()
    )

    r.addfield(f)
    r.dictfield2struct()
    r.get_bitfields()

    # item access
    r[0]
    r['fname']

    # item assignement
    r[0] = 1
    r['fname'] = 2

    # integer representation
    print(hex(r))

if __name__ == '__main__':
    test_cp_register()
    pass