#!/usr/bin/python3
import pyverilator
import argparse
import sys
from ast import literal_eval
from shutil import copyfile
import os

def cli(args=[]):
    parser = argparse.ArgumentParser(description='rdl2verilog pyverilator ')
    # register format options
    parser.add_argument("-f", "--fname", help="register file description .v", action='store', type = str, default="./devices/verilog/basic_rf.v")
    return parser.parse_args(args)

class cp_pyverilator_transport():
    sim = None

    def __init__(self,fname):

        # rename to .v, if .sv
        if not os.path.isfile(fname):
            print('File %s does not exist!' % fname)
            assert(False)

        base,ext = os.path.splitext(fname)
        # print(ext)

        if ext == '.sv':
            print('renaming input file to .v')
            ofname = base + '.v'
            copyfile(fname, ofname)
        else:
            ofname = fname

        print(ofname)
        self.sim = pyverilator.PyVerilator.build(ofname)

        # start gtkwave to view the waveforms as they are made
        self.sim.start_gtkwave()

        # add all the io and internal signals to gtkwave
        # sim.send_signal_to_gtkwave(sim.io)
        # sim.send_signal_to_gtkwave(sim.internals)

        # add all the io and internal signals to gtkwave
        self.sim.send_to_gtkwave(self.sim.io)
        self.sim.send_to_gtkwave(self.sim.internals)

        self.reset_release()

    def reset_release(self):
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

    def hifwrite(self, addr='0x00', val='0xB16B00B5', mask='0xFFFFFFFF'):

        if isinstance(addr,str):
            addr = literal_eval(addr)

        if isinstance(val,str):
            val = literal_eval(val)

        if isinstance(mask,str):
            mask = literal_eval(mask)

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

    def hifread(self,addr = '0x00'):

        if isinstance(addr,str):
            addr = literal_eval(addr)

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
    import subprocess
    result = subprocess.run(['verilator', '--version'], stdout=subprocess.PIPE)
    ver = result.stdout.split()[1]
    return ver.decode("utf-8") 

def verilator_version_ok():
    # check Verilated::flushCall() exist
    # https://github.com/chipsalliance/chisel3/issues/1565
    from packaging import version
    ver = verilator_version()
    # print(ver)
    if ( version.parse(ver) < version.parse("4.036") or
         version.parse(ver) > version.parse("4.102")):
        return True
    else:
        return False

def test_cp_pyverilator(args = []):

    if verilator_version_ok():
        p = cli(args)
        hif = cp_pyverilator_transport(p.fname)
        
        val = literal_eval('0x5A5A5A5A')
        hif.hifwrite(val = val)
        print( hex(hif.hifread()) )
        assert( hif.hifread() == val )

    else:
        print('Warning: pyverilator not working anymore with verilator versions between 4.036 and 4.102.')
        print('https://github.com/chipsalliance/chisel3/issues/1565')

if __name__ == '__main__':
    test_cp_pyverilator(sys.argv[1:])