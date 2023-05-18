""" Names Substitution module for Cheap Pie parsers """

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
