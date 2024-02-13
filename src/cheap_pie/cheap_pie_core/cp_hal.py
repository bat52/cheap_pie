#!/usr/bin/env python3
"""
Cheap Pie Hardware Abstraction Layer
"""
#
# -*- coding: utf-8 -*-
# this file is part of cheap_pie, a python tool for chip validation
# author: Marco Merlin
# email: marcomerli@gmail.com

import os
import hickle as hkl

import cheap_pie.tools.search  # pylint: disable=W0611
from cheap_pie.tools.hal2doc import hal2doc, int2hexstr, hexstr2int


class CpHal():
    """
    Cheap Pie Hardware Abstraction Layer
    """
    regs = []
    hif = None

    def __init__(self, regs):
        if isinstance(regs, CpHal):
            # this allows generating CpHal super-classes from a CpHal instance
            self.regs = regs.regs
        else:
            self.regs = regs
            if len(regs) > 0:
                self.hif = regs[0].hif
            else:
                print('# WARNING: no register defined!')

    def __len__(self):
        return len(self.regs)

    def __iter__(self):
        return self.regs.__iter__()

    def __next__(self):
        return self.regs.next()

    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.regs[idx]
        if isinstance(idx, str):
            return self.regs._asdict()[idx]
        assert False, 'Unsupported indexing!'

    def __setitem__(self, idx, value):
        if isinstance(idx, int):
            return self.regs[idx].setreg(value)
        if isinstance(idx, str):
            return self.regs._asdict()[idx].setreg(value)
        assert False, 'Unsupported indexing!'

    def __repr__(self):
        return 'CP_HAL: %d registers' % len(self.regs)  # pylint: disable=C0209

## search methods ###########################################################

    def search_bitfield(self, field, case_sensitive=False):
        """
        Search bitfields which name contains a specified string
        """
        return cheap_pie.tools.search.bitfield(self.regs, field, case_sensitive=case_sensitive)  # pylint: disable=E0601

    def search_register(self, reg, case_sensitive=False):
        """
        Search registers which name contains a specified string
        """
        return cheap_pie.tools.search.register(self.regs, reg, case_sensitive=case_sensitive)

    def search_address(self, address, mask='0xFFFFFFFF'):
        """
        Search register matching a specified address
        """
        return cheap_pie.tools.search.address(self.regs, address, mask=mask)

    def to_docx(self, *args):
        """
        Generate a .docx document describing an Hardware Abstraction Layer
        """
        hal2doc(self.regs, *args)

## dump methods #############################################################
    def regs2dict(self):
        """
        Converts an hal structure into a dictionary in the form:
        dictval = {
            'reg1': val1,
            'reg2': val2,
        }
        """
        outdict = {}
        for reg, val in self.regs._asdict().items():
            outdict[reg] = val.getreg()
        return outdict

    def dump(self, fname='dump.hkl', regs_dict=None):
        """
        Dump the value of all registers in a .hkl file.
        Inputs:
            - fname: .hkl or .txt output file
            - regs_dict: specify a dictionary of register values.
                registers will be read from chip, if not provided.
        """

        if regs_dict is None:
            # read all registers
            regs_dict = self.regs2dict()

        # detect input file type from extension
        _, file_extension = os.path.splitext(fname)
        assert file_extension in ['.txt', '.hkl']

        if file_extension == '.txt':
            self.dump2text(f1name=fname, field1=regs_dict)
        else:
            hkl.dump(regs_dict, fname, compression='gzip')

    def dump_load(self, fname='dump.hkl'):
        """
        Load a dumped file and returns a dictionary of registers
        """
        _, file_extension = os.path.splitext(fname)
        assert file_extension in ['.txt', '.hkl']

        if file_extension == '.txt':
            _, fields = self.text2dump(fname)
        else:
            fields = hkl.load(fname)

        return fields

    def dump_diff(self, f1name='dump.hkl', f2name='dump2.hkl', width=60):
        """
        Perform a diff on two dumped .hkl files.
        """
        fmtstr = '%%%ds |%%%ds' % (width, width)  # pylint: disable=C0209

        field1 = self.dump_load(f1name)
        field2 = self.dump_load(f2name)

        # create a header with filenames
        outstrlist = []
        for reg, val in field1.items():
            # print(f'reg:{reg}, val: {val}')
            if len(reg) > 0: # just check reg that have a name
                if not field2[reg] == val:
                    f1regstr = self[reg].__repr__(val).split(  # pylint: disable=C2801
                        '\n')
                    f2regstr = self[reg].__repr__(field2[reg]).split(  # pylint: disable=C2801
                        '\n')

                    for idx in range(len(f1regstr)):  # pylint: disable=C0200
                        if not f1regstr[idx] == f2regstr[idx]:
                            outstrlist.append(fmtstr %
                                            (f1regstr[idx], f2regstr[idx]))

        # print output
        if len(outstrlist) > 0:
            headerstr = fmtstr % (f1name, f2name)
            outstrlist.insert(0, headerstr)
            for line in outstrlist:
                print(line)
        else:
            print('No differences found!!!')

        return outstrlist

    def dump2text(self, f1name='dump.hkl', field1=None,
                  width=60, save_en=True, print_en=False, header_en=False,
                  byval=True, nbits_addr=32, nbits_val=32
                  ):  # pylint: disable=R0913,R0914
        """
        Convert a dumped .hkl file, or a dumped dictionary into a text file representation.
        Inputs:
            f1name: .hkl file containing dump dictionary, also defines .txt file output name
            field1: input dictionary of dumped values to save.
                    .hkl file specified by f1name must exist, if this is not specified
            width: number of columns reserved for register and bitfield name
            save_en: save output to text file (default: True)
            print_en: print output to shell (default: False)
            byval: dump in hex ascii format. ie ADD43550 C0D3C057 (default: True)
            nbits_addr: number of address bits for byval dump (default: 32)
            nbits_val: number of value bits for byval dump (default: 32)
        """

        if not isinstance(field1, dict):
            assert os.path.isfile(f1name)
            field1 = hkl.load(f1name)

        fmtstr = '%%%ds' % width  # pylint: disable=C0209

        # generate register description list
        outstrlist = []
        for reg, val in field1.items():
            if byval:
                f1regstr = '%s %s\n' % (  # pylint: disable=C0209
                    int2hexstr(self[reg].addr, nbits_addr/4),
                    int2hexstr(val, nbits_val / 4)
                )
                outstrlist.append(f1regstr)
            else:
                f1regstr = self[reg].__repr__(val).split(  # pylint: disable=C2801
                    '\n')
                for idx in range(len(f1regstr)):  # pylint: disable=C0200
                    outstrlist.append(fmtstr % f1regstr[idx])

        fname_wo_ext, _ = os.path.splitext(f1name)

        if header_en:
            # create a header with filenames
            headerstr = f'{f1name}\n'
            outstrlist.insert(0, headerstr)

        if save_en:
            outfname = fname_wo_ext + '.txt'
            file_handler = open(outfname, "w", encoding='utf8') # pylint: disable=R1732
            print(f'Output file: {outfname}')

        # print output
        if len(outstrlist) > 0:
            for line in outstrlist:
                if print_en:
                    print(line)
                if save_en:
                    file_handler.write(line)

        # close file
        if save_en:
            file_handler.close()

        # return outstrlist

    def text2dump(self, fname='dump.txt', save_en=True):
        """
        Convert a dumped .txt file, in a .hkl file or a dictionary.
        Inputs:
            f1name: .txt file containing dump address and value in the form:
                ADD43550 C0D3C057
        """

        assert os.path.isfile(fname)

        regs_dict = {}
        with open(fname, 'r', encoding='utf8') as file_handler:
            for line in file_handler:
                try:
                    line = line.strip()
                    if len(line) > 0:
                        addrstr, valstr = line.split()
                        # print(f'addr: {addrstr}, val: {valstr}')

                        addr = hexstr2int(addrstr)
                        val = hexstr2int(valstr)

                        regname = self.search_address(addr)
                        # print(regname)

                        regs_dict[regname] = val
                except Exception as err: # pylint: disable=W0718
                    print(f"Unable to process line: <{line}>",repr(err))

        if save_en:
            fname_wo_ext, _ = os.path.splitext(fname)
            outfname = fname_wo_ext + '.hkl'
            self.dump(fname=outfname, regs_dict=regs_dict)
        else:
            outfname = ''

        return outfname, regs_dict


class CpHalSuper(CpHal):
    """ Just a dummy class for test """

    def super_method(self):
        """ Just a dummy method of super-class CpHalSuper """
        print('Super Method!!!')


def test_cp_hal_to_docx():
    """
    Test Function for Cheap Pie HAL to .docx
    """
    from parsers.cp_parsers_wrapper import cp_parsers_wrapper  # pylint: disable=C0415,C0413,E0401
    from cheap_pie_core.cp_cli import cp_cli                   # pylint: disable=C0415,C0413,E0401

    prms = cp_cli(['-t', 'dummy', '-rf', 'my_subblock.xml', '-fmt', 'ipxact'])
    hal = cp_parsers_wrapper(prms)
    hal.to_docx()


def test_cp_hal():  # pylint: disable=R0914,R0915
    """
    Test Function for Cheap Pie Hardware Abstraction Layer
    """
    from ast import literal_eval                                        # pylint: disable=C0415
    from parsers.cp_parsers_wrapper import cp_parsers_wrapper  # pylint: disable=C0415,E0401
    from transport.cp_dummy_transport import CpDummyTransport  # pylint: disable=C0415,E0401
    from cheap_pie_core.cp_cli import cp_cli                  # pylint: disable=C0415,E0401

    print('# hal initialize')
    prms = cp_cli(['-t', 'dummy'])
    hal = cp_parsers_wrapper(prms, hif=CpDummyTransport())

    print('# hal test register methods...')
    print('# hal hex assignement')
    inval = "0xFFFFFFFF"
    hal.regs.ADC_ANA_CTRL.setreg(inval)
    retval = hex(hal.regs.ADC_ANA_CTRL.getreg())
    print(retval)
    assert literal_eval(inval) == literal_eval(retval)

    print('# hal decimal assignement')
    inval = 2
    hal.regs.ADC_ANA_CTRL.setreg(inval)
    retval = hal.regs.ADC_ANA_CTRL.getreg()
    assert inval == retval

    print('# hal reg representation')
    hal.regs.ADC_ANA_CTRL  # pylint: disable=W0104

    print('# hal reg display')
    hal.regs.ADC_ANA_CTRL.display()

    print('# hal reg print')
    print(hal.regs.ADC_ANA_CTRL)

    print('# hal reg str')
    print(str(hal.regs.ADC_ANA_CTRL))

    print('# hal test bitfield methods...')
    print('# hal bitfield display')
    hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.display()
    print('# hal bitfield display with value')
    hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.display(2)
    print('# hal bitfield setbit')
    hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.setbit(inval)
    retval = hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.getbit()
    assert inval == retval

    print('# hal subscriptable interface...')
    print('# hal[0]')
    print(hal[0])

    print('# hal[0][0]')
    print(hal[0][0])

    print("# hal['ADC_ANA_CTRL']")
    print(hal['ADC_ANA_CTRL'])

    print('# hal dict-based reg assignement')
    regval = 1
    hal['ADC_ANA_CTRL'] = regval
    assert hal.regs.ADC_ANA_CTRL.getreg() == regval

    print('# hal dict-based bitfield assignement')
    fieldval = 2
    hal['ADC_ANA_CTRL']['ADC_BM'] = fieldval
    assert hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.getbit() == fieldval

    print('# hal dict-based assignement in single register write')
    dither = 1
    chop = 1
    inv = 1
    hal['ADC_ANA_CTRL'] = {'DITHER_EN': dither,
                           'CHOP_EN': chop, 'INV_CLK': inv}
    assert hal.regs.ADC_ANA_CTRL.bitfields.DITHER_EN.getbit() == dither
    assert hal.regs.ADC_ANA_CTRL.bitfields.CHOP_EN.getbit() == chop
    assert hal.regs.ADC_ANA_CTRL.bitfields.INV_CLK.getbit() == inv

    print('# hal search_register')
    searchreg = 'ADC_ANA_CTRL'
    reglist = hal.search_register(searchreg)
    reg = reglist[0]
    print(reg)
    assert str(reg) == searchreg

    print('# hal search_bitfield')
    searchfield = 'ADC_BM'
    fieldlist = hal.search_bitfield(searchfield)
    print(fieldlist)
    field = fieldlist[0]
    print(field)
    assert searchfield in field

    print('# hal search_address')
    searchaddr = '0x4000702c'
    reg = hal.search_address(searchaddr)
    print(f'# Register {reg}')
    addr = hex(hal[reg].addr)
    print(f'# Address: {addr}')
    assert addr == searchaddr

    print('# hal search_address with mask')
    searchaddr = '0xF000702c'
    searchmask = '0x0FFFFFFF'
    reg = hal.search_address(searchaddr, mask=searchmask)
    print(f'# Register {reg}')
    addr = hex(hal[reg].addr)
    print(f'# Address: {addr}')
    assert (literal_eval(addr) & literal_eval(searchmask) ==
            literal_eval(searchaddr) & literal_eval(searchmask))
    reg = hal.search_address(searchaddr)
    assert reg == ''

    print('# hal dump')
    dump1 = 'dump1.hkl'
    dump2 = 'dump2.hkl'
    hal.dump(dump1)
    hal['ADC_ANA_CTRL']['ADC_BM'] = 3
    hal.dump(dump2)
    diff = hal.dump_diff(dump1, dump2)
    print(diff)
    assert len(diff) == 2

    print('# hal regs2dict')
    mydict = hal.regs2dict()
    assert isinstance(mydict, dict)

    print('# hal dump text')
    txt_dump = 'tdump.txt'
    hal.dump(txt_dump)
    hkl_dump, _ = hal.text2dump(txt_dump)
    assert len(hal.dump_diff(hkl_dump, dump2)) == 0

    print('# CpHalSuper inheritance')
    hal_super = CpHalSuper(hal)
    hal_super.super_method()


if __name__ == '__main__':
    test_cp_hal()
