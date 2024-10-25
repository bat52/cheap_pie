#!/usr/bin/env python3
"""
Cheap Pie module for pyverilator transport
"""
import os
import argparse
import sys
from ast import literal_eval
from shutil import copyfile
import subprocess
from packaging import version

import pyverilator

from cheap_pie.transport.cp_dummy_transport import hifread_preproc, hifwrite_preproc  # pylint: disable=E0401


def cli(args):
    """ Command Line Interface for pyverilator transport class """
    parser = argparse.ArgumentParser(description='rdl2verilog pyverilator ')
    # register format options
    parser.add_argument("-f", "--fname",
                        help="register file description .v", action='store',
                        type=str, default="./devices/verilog/basic_rf.v")
    return parser.parse_args(args)


class CpPyverilatorTransport():
    """
    Cheap Pie class for pyverilator transport
    """
    sim = None

    def __init__(self, fname, gtkwave_en=False):

        # rename to .v, if .sv
        if not os.path.isfile(fname):
            assert False, f'File {fname} does not exist!'

        base, ext = os.path.splitext(fname)
        # print(ext)

        if ext == '.sv':
            print('renaming input file to .v')
            ofname = base + '.v'
            copyfile(fname, ofname)
        else:
            ofname = fname

        print(ofname)
        self.sim = pyverilator.PyVerilator.build(ofname)

        if gtkwave_en:  # still causing trouble in VSC and/or WSL
            # start gtkwave to view the waveforms as they are made
            self.sim.start_gtkwave()

            # add all the io and internal signals to gtkwave
            # sim.send_signal_to_gtkwave(sim.io)
            # sim.send_signal_to_gtkwave(sim.internals)

            # add all the io and internal signals to gtkwave
            # self.sim.send_to_gtkwave(self.sim.io)
            # self.sim.send_to_gtkwave(self.sim.internals)

            self.sim.clock.send_to_gtkwave()
            self.sim.io.resetn.send_to_gtkwave()  # pylint: disable=E1101
            self.sim.io.addr.send_to_gtkwave()
            self.sim.io.wdata.send_to_gtkwave()
            self.sim.io.rdata.send_to_gtkwave()

        self.reset_release()

    def reset_release(self):
        """ Release Reset signal """
        # tick the automatically detected clock
        self.sim.clock.tick()

        # set rst back to 0
        # sim.io.rst = 0
        self.sim.io.resetn = 0
        self.sim.clock.tick()
        self.sim.io.resetn = 1

        # check out when en = 0
        # sim.io.en = 0
        # curr_out = sim.io.out
        # sim.io is a pyverilator.Collection, accessing signals by attribute or
        # dictionary syntax returns a SignalValue object which inherits from int.
        # sim.io.out can be used just like an int in most cases, and it has extra
        # features like being able to add it to gtkwave with
        # sim.io.out.send_to_gtkwave(). To just get the int value, you can call
        # sim.io.out.value
        # print('sim.io.out = ' + str(curr_out))

        # check out when en = 1
        # sim.io.en = 1
        # curr_out = sim.io.out
        # print('sim.io.out = ' + str(curr_out))

    def hifwrite(self, addr='0x00', val='0xB16B00B5', mask='0xFFFFFFFF', verify=True):
        """ Write register """

        addr, val, mask = hifwrite_preproc(addr, val, mask)

        # write value
        self.sim.io.addr = addr
        self.sim.io.wdata = val
        self.sim.io.wmask = mask
        self.sim.io.read = 0
        self.sim.io.valid = 0

        self.sim.clock.tick()

        self.sim.io.valid = 1

        self.sim.clock.tick()

        self.sim.io.valid = 0

        self.sim.clock.tick()

        # HW write
        # sim.io.basicreg_basicfield_wdata = literal_eval('0xB16B00B5')
        # sim.io.basicreg_basicfield_we = 0
        # sim.clock.tick()
        # sim.io.basicreg_basicfield_we = 1
        # sim.clock.tick()

        if verify:
            assert int(self.hifread(addr))==int(val)

    def hifread(self, addr='0x00'):
        """ Read register """
        addr = hifread_preproc(addr)

        # SW read
        self.sim.io.addr = addr
        self.sim.io.read = 1

        self.sim.io.valid = 0
        self.sim.clock.tick()

        self.sim.io.valid = 1
        self.sim.clock.tick()

        outval = self.sim.io.rdata

        self.sim.io.valid = 0
        self.sim.clock.tick()

        # print(hex(outval))
        return outval


def verilator_version():
    """ Return verilator version """
    result = subprocess.run(['verilator', '--version'],
                            stdout=subprocess.PIPE, check=False)
    ver = result.stdout.split()[1]
    return ver.decode("utf-8")


def verilator_version_ok():
    """ True if the installed verilator version works as transport for cheap_pie """
    # check Verilated::flushCall() exist
    # https://github.com/chipsalliance/chisel3/issues/1565
    ver = verilator_version()
    # print(ver)

    return (
        version.parse(ver) < version.parse("4.036") or
        version.parse(ver) > version.parse("4.102")
    )


def test_cp_pyverilator(args=[]):  # pylint: disable=W0102
    """ Test pyverilator transport """
    if True:  # verilator_version_ok(): pylint: disable=W0125
        prms = cli(args)
        hif = CpPyverilatorTransport(prms.fname)
        val = literal_eval('0x5A5A5A5A')
        hif.hifwrite(val=val)
        print(hex(hif.hifread()))
        assert hif.hifread() == val
    else:
        # this was fixed by pyverilator-mm
        print('Warning: pyverilator not working anymore \
              with verilator versions between 4.036 and 4.102.')
        print('https://github.com/chipsalliance/chisel3/issues/1565')


if __name__ == '__main__':
    test_cp_pyverilator(sys.argv[1:])
