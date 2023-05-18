""" Names Substitution module for Cheap Pie parsers """

from collections import namedtuple

def name_subs(regname=None):
    """ Names Substitution function for Cheap Pie parsers """

    # print(regname)
    # regname=strrep(regname,'"','')
    regname=regname.replace('"','')
    regname=regname.replace('[','')
    regname=regname.replace(']','')
    regname=regname.replace('%','')
    if regname[0].isdigit():
        regname= 'M' + regname
    return regname

def dict2namedtuple(outdict,tuplename="HAL"):
    """ Convert a dictionary into a namedtuple """
    return namedtuple(tuplename, outdict.keys())(*outdict.values())
