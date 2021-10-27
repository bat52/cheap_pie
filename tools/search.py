#!/usr/bin/python3

## this file is part of cheap_pie, a python tool for chip validation
## author: Marco Merlin
## email: marcomerli@gmail.com

def register(hal,regname):
    retval = []    
    for reg in hal: # loop over all registers
        if regname in reg.regname:
            print( reg.regname )
            retval.append(reg.regname)
    return retval    

def bitfield(hal,bitfield):
    retval = []    
    for reg in hal: # loop over all registers
        # print reg.regname        
        for field in reg.bitfields:
            if bitfield in field.fieldname:
                print( reg.regname + " @ " + field.fieldname )
                retval.append(field)
    return retval

def test_search():
    print('Testing search...')
    from parsers.svd_parse_repo import svd_parse
    hal = svd_parse(fname="./devices/QN908XC.svd", hif=None)
    print('## ADC registers:')
    ret = register(hal,'ADC')
    print('##  ADC_BM bitfields:')
    ret = bitfield(hal,'ADC_BM')
    
if __name__ == '__main__':
    import sys
    import os.path
    sys.path.append( os.path.join(os.path.dirname(__file__), '..') )
    test_search()
    pass


