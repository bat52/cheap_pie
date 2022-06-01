#!/usr/bin/python3

## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

from ast import literal_eval

def str_in_str(str1,str2,case_sensitive=True):
    if case_sensitive:
        return (str1 in str2)
    else:
        return (str1.upper() in str2.upper())
    pass

def register(hal,regname,case_sensitive=True):
    retval = []    
    for reg in hal: # loop over all registers
        if str_in_str(regname,reg.regname,case_sensitive):
            print( reg.regname )
            retval.append(reg.regname)
    return retval    

def bitfield(hal,bitfield,case_sensitive=True):
    retval = []    
    for reg in hal: # loop over all registers
        # print reg.regname        
        for field in reg.bitfields:
            if str_in_str(bitfield,field.fieldname,case_sensitive):
                print( reg.regname + " @ " + field.fieldname )
                retval.append(field)
    return retval

def address(hal, address, mask='0xFFFFFFFF'):     
    # convert address into integer, if needed    
    if isinstance(mask,str):
        mask    = int( literal_eval(mask) )
    if isinstance(address,str):
        address = int( literal_eval(address) )
    
    retval = []    
    for reg in hal: # loop over all registers
        # print reg.regname
        if (reg.addr & mask) == (address & mask):
            print( reg.regname + " : " + hex(reg.addr) )
            return reg.regname

def test_search():
    print('Testing search...')
    from parsers.svd_parse_repo import svd_parse
    hal = svd_parse(fname="./devices/QN908XC.svd", hif=None)

    print('## ADC registers:')    
    ret = register(hal,'ADC')    
    assert(len(ret) > 0)

    print('##  ADC_BM bitfields:')
    ret = bitfield(hal,'ADC_BM')
    assert(len(ret) > 0)

    print('## 0x4000702c register name:')
    ret = address(hal,'0x4000702c')
    assert(len(ret) > 0)
    
    print('## 0xF000702c register name:')
    ret = address(hal,'0xF000702c',mask='0x0FFFFFFF')
    assert(len(ret) > 0)

    ret = address(hal,'0xF000702c')
    assert( ret is None )


if __name__ == '__main__':
    import sys
    import os.path
    sys.path.append( os.path.join(os.path.dirname(__file__), '..') )
    test_search()
    pass


