# cheap_pie
A python tool for register-based chip verification and validation

"Cheap Pie" is a python tool for register-based chip verification and validation.
The name is a translitteration of "chip py" for obvious reasons.

Given an input description file for the chip, it provides a register-level and 
bitfield-level read/write access, through a generic transport layer.

Currently the implemented description input modes are:
- CMSIS-SVD (https://www.keil.com/pack/doc/CMSIS/SVD/html/svd_Format_pg.html)
- IP-XACT ( https://www.accellera.org/downloads/standards/ip-xact )
- SystemRDL (https://www.accellera.org/activities/working-groups/systemrdl)

but it should be relatively easy to add different chip description formats.

Although tested on few real chips (NXP QN9080, I.MX RT1010, K64F),
cheap_pie parser already supports dozen of devices, listed in the CMSIS-SVD 
repository https://github.com/posborne/cmsis-svd .

Currently the supported transport layers are jlink and pyocd, but it should be really easy
to add support for different transport layers, like for instance openSDA, 
CMSIS-DAP, Total Phase Cheetah, GDB or any other.

Experimental support for pyverilator transport allows to run interactive simulation
of register blocks generated from SystemRDL source.

Author: Marco Merlin
Tested on ipython3 (python 3.8.5) on ubuntu 20.04

# IPython Example:
        %run cheap_pie
        inval = "0xFFFFFFFF"
        hal.regs.ADC_ANA_CTRL.setreg(inval)
        retval = hex(hal.regs.ADC_ANA_CTRL.getreg())
        assert(literal_eval(inval) == literal_eval(retval))

        # decimal assignement        
        inval = 2
        hal.regs.ADC_ANA_CTRL.setreg(inval)
        retval = hal.regs.ADC_ANA_CTRL.getreg()        
        assert(inval == retval)
        
        hal.regs.ADC_ANA_CTRL
        hal.regs.ADC_ANA_CTRL.display()
                
        print('Test bitfield methods...')
        
        hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM
        hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.display()
        hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.display(2)
        hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.setbit(inval)
        retval = hal.regs.ADC_ANA_CTRL.bitfields.ADC_BM.getbit()
        assert(inval == retval)

        # subscriptable register access
        hal[0]
        # subscriptable bitfield access
        hal[0][0]
        # subscriptable as a dictionary
        hal['SYSCON_RST_SW_SET']
        hal['ADC_ANA_CTRL']['ADC_BM']
        
        # assignement
        hal['ADC_ANA_CTRL'] = 1
        hal['ADC_ANA_CTRL']['ADC_BM'] = 2
        # dict-based assignement in single register write
        hal['ADC_ANA_CTRL'] = {'DITHER_EN': 1, 'CHOP_EN': 1, 'INV_CLK': 1}

        # help
        hal.regs.ADC_ANA_CTRL.help()
        ADC core and reference setting regsiter
                   ADC_BM: 
                         : ADC bias current selection.
                ADC_ORDER: 
                         : 1 to enable SD ADC 2 order mode selection
                DITHER_EN: 
                         : 1 to enable SD ADC PN Sequence in chopper mode
                  CHOP_EN: 
                         : 1 to enable SD ADC chopper
                  INV_CLK: 
                         : 1 to invert SD ADC Output Clock
                  VREF_BM: 
                         : SD ADC Reference Driver bias current selection.
               VREF_BM_X3: 
                         : SD ADC Reference Driver bias current triple.
               VINN_IN_BM: 
                         : PGA VlNN Input Driver bias current selection.
              VINN_OUT_BM: 
                         : PGA VlNN Output Driver bias current selection.
           VINN_OUT_BM_X3: 
                         : PGA VlNN Output Driver bias current triple.
              ADC_BM_DIV2: 
                         : SD ADC bias current half.

# CLI Example:
        # load RT1010 from local svd file under ./devices/
        # automatically calls ipython and cheap_pie initialization
        ./cheap_pie.sh -rf MIMXRT1011.svd -t jlink

        # load K64 from CMSIS-SVD
        # need to specify vendor for svd not in ./devices/
        ./cheap_pie.sh -rf MK64F12.svd -ve Freescale -t jlink

        # calls QN9080 with dummy transport layer 
        # useful to explore device registers
        ./cheap_pie.sh -t dummy

# Default configurations Examples:
        # calls QN9080 device with dummy transport layer
        ./cfgs/cp_qn9080_dummy.sh
        # calls RT1010 device with jlink transport layer
        ./cfgs/cp_rt1010_jlink.sh
        # calls K20 device with dummy transport layer
        ./cfgs/cp_k20_dummy.sh

# Verilator interactive simulation Examples:
        ./tools/rdl2verilog.py -f ./devices/rdl/basic.rdl
        ./cheap_pie.sh -dd  ./devices/rdl -rf basic.rdl -fmt rdl -t verilator -topv ./devices/rdl/basic/basic_rf.sv

# Install
## From pypi
        pip3 install cheap_pie
## From github
        pip3 install git+https://github.com/bat52/cheap_pie.git@master

# Dependencies for core (required):        
        # for XML parsing (used by legacy svd parser and IP-XACT parser)
        pip3 install untangle
        # for exporting XML info into a human-readable document
        pip3 install python-docx
        # for dumping registers
        pip3 install hickle
        # CMSIS-SVD python parser including many svd files https://github.com/posborne/cmsis-svd
        pip3 install cmsis-svd
        # SPIRIT IP-XACT parser through ipyxact https://github.com/olofk/ipyxact
        pip3 install ipyxact                
        # SystemRDL to register-file verilog
        https://github.com/hughjackson/PeakRDL-verilog
        # SystemRDL to IP-XACT
        https://github.com/SystemRDL/PeakRDL-ipxact
# Dependencies for validation/transport layers (optional):        
        # for JLINK
        pip3 install pylink-square
        # pyOCD for CMSIS-DAP and JLINK support (only tested in python-venv)
        pip3 install pyocd
        # esptool for Espressif devices (not yet functional)
        pip3 install esptool        
# Dependencies for verification (optional AND experimental):
        # verilator
        https://www.veripool.org/verilator/
        # pyverilator (python verilator wrapper)
        https://github.com/csail-csg/pyverilator        
        # gtkwave
        http://gtkwave.sourceforge.net/

# Register description formats
regtool from opentitan project seems similar, using JSON to represent chip/IP structure, and I2C transport
https://docs.opentitan.org/doc/rm/register_tool/

custom input, output: verilog, VHDL, YAML, JSON, TOML, Spreadsheet (XLSX, XLS, OSD, CSV)
https://github.com/rggen/rggen

convert ipxact register file description into verilog register bank
https://github.com/oddball/ipxact2systemverilog

# Others	
In conjunction with pyVISA (https://pyvisa.readthedocs.io/en/master/), used for 
instument control, it provides a simple and fully python-contained environment
for silicon validation.

Graphical Render of bitfield structures
https://github.com/wavedrom/bitfield

C++ register/bitfields access (including generation from svd)
https://github.com/thanks4opensource/regbits

STM C++ regbits implementation
https://github.com/thanks4opensource/regbits_stm

a barebone embedded library generator
https://modm.io/

hardware descriptions for AVR and STM32 devices
https://github.com/modm-io/modm-devices

STM32 Peripheral Access Crates (from svd)
https://github.com/stm32-rs/stm32-rs

Banner created with pyfiglet
https://www.devdungeon.com/content/create-ascii-art-text-banners-python#install_pyfiglet

Cheap Pie is modeled after an original Octave/Matlab implementation that cannot
be shared due to licensing reasons. The original code was converted to python
using SMOP ( https://github.com/ripple-neuro/smop ).
