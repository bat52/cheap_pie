#!/usr/bin/env python3

from IPython import embed

if __name__ == '__main__':
    # needed if cheap_pie not installed
    import os
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

from cheap_pie.cheap_pie_core.cheap_pie_main import cp_main  # pylint: disable=C0413,E0401

def cp_interactive():
    """ Main function for interactive shell """

    hal, prms = cp_main()
    print("Launching IPython...")
    embed(colors="Linux",user_ns={"hal": hal, "prms": prms})

if __name__ == '__main__':
    cp_interactive()