#!/bin/bash
./tools/rdl2verilog.py -f ./devices/rdl/basic.rdl
./tools/rdl2any.py -f ./devices/rdl/basic.rdl -ofmt ipxact
./cheap_pie.sh -dd  ./devices/rdl -rf basic.xml -fmt ipyxact -t verilator -topv ./devices/rdl/basic/basic_rf.sv