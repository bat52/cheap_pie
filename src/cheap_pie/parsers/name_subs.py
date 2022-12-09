def name_subs(regname=None):

    # print(regname)
    # regname=strrep(regname,'"','')
    regname=regname.replace('"','')
    regname=regname.replace('[','')
    regname=regname.replace(']','')
    regname=regname.replace('%','')
    if regname[0].isdigit():
        regname= 'M' + regname
    
    return regname