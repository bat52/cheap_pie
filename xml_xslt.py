#!/usr/bin/python3
# import os
import sys
import lxml.etree as ET
import argparse
import os

def xml_xslt_parse(args=[]):
    parser = argparse.ArgumentParser(description='Apply XSLT to .xml file')
    parser.add_argument("-in", "--input", help=".xml input", action='store', type = str, default="./devices/my_subblock.xml")
    parser.add_argument("-xslt", "--xslt", help=".xslt file", action='store', type = str, default="ipxact2svd.xslt")
    parser.add_argument("-out", "--output", help=".xml output", action='store', type = str, default="output.xml")
    return parser.parse_args(args)

def xml_xslt(xmlin, xslt, xmlout):
    dom = ET.parse(xmlin)
    xslt = ET.parse(xslt)
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    infile = ET.tostring(newdom, pretty_print=True).decode('utf-8')
    # print(infile)
    if os.path.isfile(xmlout):
        os.remove(xmlout)
    outfile = open(xmlout, 'a')
    outfile.write(infile)

if __name__ == '__main__':
    p = xml_xslt_parse(sys.argv[1:])
    xml_xslt(xmlin = p.input, xslt = p.xslt, xmlout = p.output)
    pass