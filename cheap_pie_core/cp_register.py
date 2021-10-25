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
    bitfields = None
    dictfields = None
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
        # self.bitfields = []
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
        
    def setreg(self,regval = 0,*args,**kwargs):
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
            ret = self.hif.hifwrite(self.addr,regval)
        else :
            ret = regval
        
        #% only display output if no nargout %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # if setreg.nargout == 0:
        self.display(regval)
        # fields = fieldnames(self.fields);
        #structfun(@(x) x.display(regval),self.fields,'UniformOutput',false);                
        
        return ret
        
    def display(self,regval = "0" ):
        # read register value
        regval = self.getreg()

        # 
        for field in self.bitfields :
            field.display(regval)
        
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
        return any(item.name == key for item in self.bitfields)

    def __len__(self):
        return len(self.bitfields.keys())
