#!/usr/bin/env python3

""" Convert between different .xml formats using .xslt rules
Examples of conversion between different IP-XACT versions
"""

import sys
import argparse
import os
import difflib

import lxml.etree as ET
from cheap_pie.cheap_pie_core.cp_cli import cp_devices_fname, cp_root_dir


def xml_xslt_parse(args=[]):  # pylint: disable=W0102
    """ Parsing function for xml converter """
    parser = argparse.ArgumentParser(description='Apply XSLT to .xml file')
    parser.add_argument("-in", "--input", help=".xml input",
                        action='store', type=str, default=cp_devices_fname("generic_example.xml"))
    parser.add_argument("-xslt", "--xslt", help=".xslt file",
                        action='store', type=str,
                        default=os.path.join(
                            cp_root_dir(),
                            "parsers/ipxact_rules/from1685_2009_to_1685_2014.xsl"
                        )
                        )
    parser.add_argument("-out", "--output", help=".xml output",
                        action='store', type=str, default="output.xml")
    return parser.parse_args(args)


def xml_xslt(xmlin, xslt, xmlout):
    """ Convert between different .xml formats using .xslt rules """
    dom = ET.parse(xmlin)  # pylint: disable=I1101
    xslt = ET.parse(xslt)  # pylint: disable=I1101
    transform = ET.XSLT(xslt)   # pylint: disable=I1101
    newdom = transform(dom)
    infile = ET.tostring(newdom, pretty_print=True).decode( # pylint: disable=I1101
        'utf-8')
    # print(infile)
    if os.path.isfile(xmlout):
        os.remove(xmlout)
    with open(xmlout, 'a', encoding='utf-8') as outfile:
        outfile.write(infile)


def compare(fromfile, tofile):
    """ Compare two text files """
    with open(fromfile, encoding='utf-8') as ffh:
        fromlines = ffh.readlines()
    with open(tofile, encoding='utf-8') as tfh:
        tolines = tfh.readlines()
    diff = difflib.unified_diff(
        fromlines, tolines, fromfile=fromfile, tofile=tofile)

    difflines = []
    for line in diff:
        difflines.append(line)
        # print(line)

    assert len(difflines) > 0


def test_xml_xslt(args=[]):  # pylint: disable=W0102
    """ Test convert between different .xml formats using .xslt rules """
    prms = xml_xslt_parse(args)
    xml_xslt(xmlin=prms.input, xslt=prms.xslt, xmlout=prms.output)
    # diff input output
    compare(prms.input, prms.output)


if __name__ == '__main__':
    test_xml_xslt(sys.argv[1:])
