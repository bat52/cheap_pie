#!/usr/bin/python3

import sys
import lxml.etree as ET
import argparse
import os

def xml_xslt_parse(args=[]):
    parser = argparse.ArgumentParser(description='Apply XSLT to .xml file')
    # parser.add_argument("-in", "--input", help=".xml input", action='store', type = str, default="./devices/my_subblock.xml")
    parser.add_argument("-in", "--input", help=".xml input", action='store', type = str, default="./devices/generic_example.xml")
    # parser.add_argument("-xslt", "--xslt", help=".xslt file", action='store', type = str, default="ipxact2svd.xslt")
    # parser.add_argument("-xslt", "--xslt", help=".xslt file", action='store', type = str, default="./parsers/rules/from1.0_to_1.1.xsl")
    parser.add_argument("-xslt", "--xslt", help=".xslt file", action='store', type = str, default="./parsers/rules/from1685_2009_to_1685_2014.xsl")
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

def compare(fromfile,tofile):
    with open(fromfile) as ff:
        fromlines = ff.readlines()
    with open(tofile) as tf:
        tolines = tf.readlines()

    import difflib
    # diff = difflib.context_diff(fromlines,tolines,fromfile=fromfile,tofile=tofile)
    diff = difflib.unified_diff(fromlines,tolines,fromfile=fromfile,tofile=tofile)
    sys.stdout.writelines(diff)

def test_xml_xslt(args):
    p = xml_xslt_parse(args)
    xml_xslt(xmlin = p.input, xslt = p.xslt, xmlout = p.output)
    # diff input output
    compare(p.input,p.output)

if __name__ == '__main__':
    test_xml_xslt(sys.argv[1:])
    pass