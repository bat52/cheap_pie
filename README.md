# cheap_pie
A python tool for chip validation

"Cheap Pie" is a python tool for chip validation.
The name is a translitteration of "chip py" for obvious reasons.

Given an input description file for the chip, it provides a register-level and 
bitfield-level read/write access, through a generic transport layer.

Currently the implemented description input mode is an .xml that is bundled with 
with the NXP QN9080 SDK
 ( https://www.nxp.com/products/wireless/bluetooth-low-energy/qn908x-ultra-low-power-bluetooth-low-energy-system-on-chip-solution:QN9080 ),
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

# Example:

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
	# for XML parsing
	pip3 install untangle
	# for JLINK
        pip3 install pylink-square
	# for exporting XML info into a human-readable document
        pip3 install python-docx

# See Also
regtool from opentitan project seems similar, using JSON to represent chip/IP structure, and I2C transport
( https://docs.opentitan.org/doc/rm/register_tool/ ).
	
# Others	
Banner created with pyfiglet
( https://www.devdungeon.com/content/create-ascii-art-text-banners-python#install_pyfiglet ).

