#!/bin/bash
IPNAME=counter
./tools/rdl2verilog.py -f ./devices/rdl/$IPNAME.rdl
./cheap_pie.sh -dd ./devices/rdl -rf $IPNAME.rdl -fmt rdl -t verilator -topv ./devices/rdl/$IPNAME/${IPNAME}_rf.sv