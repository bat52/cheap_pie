#!/usr/bin/env python3

""" Cheap Pie Module to export register descriptio into .docx file """

import os
import sys
from pathlib import Path

if __name__ == '__main__':
    # needed if cheap_pie not installed
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from cheap_pie.cheap_pie_core.cheap_pie_main import cp_main  # pylint: disable=C0413,E0401

def cp_hal2doc():
    """ Main function for hal2doc tool """

    hal, prms = cp_main()

    assert not hal is None, f'ERROR: no HAL generated! hal={hal}'

    infilename = Path(prms.regfname)
    outfilename = infilename.with_suffix(".docx")

    print(f"Exporting HAL to file {outfilename}...")
    hal.to_docx(fname=outfilename)
    print("Done!")

    return 0

if __name__ == '__main__':
    cp_hal2doc()
