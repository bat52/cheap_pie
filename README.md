# cheap_pie
A python tool for chip validation

"Cheap Pie" is a python tool for chip validation.
The name is a translitteration of "chip py" for obvious reasons.

Given an input description file for the chip, it provides a register-level and 
bitfield-level read/write access, through a generic transport layer.

Currently the implemented description input modes are:
- CMSIS-SVD (https://www.keil.com/pack/doc/CMSIS/SVD/html/svd_Format_pg.html)
- IP-XACT ( https://www.accellera.org/downloads/standards/ip-xact )
but it should be relatively easy to add different chip description formats.

Currently the supported transport layer is Jlink, but it should be really easy
to add support for different transport layers, like for instance Total Phase
Cheetah 
( https://www.totalphase.com/catalog/product/view/id/3/s/cheetah-spi/?GA_network=g&GA_device=c&GA_campaign=169793414&GA_adgroup=38297664135&GA_target=&GA_placement=&GA_creative=259919292215&GA_extension=&GA_keyword=cheetah%20spi&GA_loc_physical_ms=9054949&GA_landingpage=https://www.totalphase.com/catalog/product/view/id/3/s/cheetah-spi/&ga_keyword_match=e&ga_ad_position=1t1&gclid=Cj0KCQjwpsLkBRDpARIsAKoYI8y4QJe48cAGH2vPK769Js7LbnM2VjUSXz2slVFTQByO-I23_DKdVqsaAhsBEALw_wcB ), or any other.

In conjunction with pyVISA (https://pyvisa.readthedocs.io/en/master/), used for 
instument control, it provides a simple and fully python-contained environment
for silicon validation.

Cheap Pie is modeled after an original Octave/Matlab implementation that cannot
be shared due to licensing reasons. The original code was converted to python
using SMOP ( https://github.com/ripple-neuro/smop ).

Author: Marco Merlin
Email: marcomerli@gmail.com

Tested on ipython3 (python 3.8.5) on ubuntu 20.04

# Default configurations Examples:
        # calls QN9080 device with dummy transport layer
        ./cfgs/cp_qn9080_dummy.sh
        # calls RT1010 device with jlink transport layer
        ./cfgs/cp_rt1010_jlink.sh
        # calls K20 device with dummy transport layer
        ./cfgs/cp_k20_dummy.sh

# CLI Example:
        # calls with dummy transport layer 
        # useful to explore device registers
        # automatically calls ipython and cheap_pie initialization
        ./cheap_pie.sh -t dummy

# IPython Example:
        %run cheap_pie
        inval = "0xFFFFFFFF"
        hal.ADC_ANA_CTRL.setreg(inval)
        retval = hex(hal.ADC_ANA_CTRL.getreg())
        assert(literal_eval(inval) == literal_eval(retval))

        # decimal assignement        
        inval = 2
        hal.ADC_ANA_CTRL.setreg(inval)
        retval = hal.ADC_ANA_CTRL.getreg()        
        assert(inval == retval)
        
        hal.ADC_ANA_CTRL.display()
                
        print('Test bitfield methods...')
        
        hal.ADC_ANA_CTRL.bitfields.ADC_BM.display()
        hal.ADC_ANA_CTRL.bitfields.ADC_BM.display(2)
        hal.ADC_ANA_CTRL.bitfields.ADC_BM.setbit(inval)
        retval = hal.ADC_ANA_CTRL.bitfields.ADC_BM.getbit()
        assert(inval == retval)

# Dependencies:
        # CMSIS-SVD python parser including many svd files
        pip3 install cmsis-svd
	# for XML parsing (used by legacy svd parser and IP-XACT parser)
	pip3 install untangle
	# for JLINK
        pip3 install pylink-square
	# for exporting XML info into a human-readable document
        pip3 install python-docx

# See Also
regtool from opentitan project seems similar, using JSON to represent chip/IP structure, and I2C transport
https://docs.opentitan.org/doc/rm/register_tool/

RDL to IP-XACT
https://github.com/SystemRDL/PeakRDL-ipxact

RDL to verilog
https://github.com/hughjackson/PeakRDL-verilog

IP-XACT to C header, markdown
https://github.com/olofk/ipyxact

custom input, output: verilog, VHDL, YAML, JSON, TOML, Spreadsheet (XLSX, XLS, OSD, CSV)
https://github.com/rggen/rggen
	
# Others	
Banner created with pyfiglet
( https://www.devdungeon.com/content/create-ascii-art-text-banners-python#install_pyfiglet ).