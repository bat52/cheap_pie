#!/bin/bash
IPNAME=counter
./tools/rdl2verilog.py -f ./devices/rdl/$IPNAME.rdl
./tools/rdl2any.py -f ./devices/rdl/$IPNAME.rdl -ofmt ipxact
./cheap_pie.sh -dd ./devices/rdl -rf $IPNAME.xml -fmt ipyxact -t verilator -topv ./devices/rdl/$IPNAME/${IPNAME}_rf.sv