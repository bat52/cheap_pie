# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 19:36:19 2018

@author: Marco Merlin
"""

def reload_module(full_module_name):
    """
        Assuming the folder `full_module_name` is a folder inside some
        folder on the python sys.path, for example, sys.path as `C:/`, and
        you are inside the folder `C:/Path With Spaces` on the file 
        `C:/Path With Spaces/main.py` and want to re-import some files on
        the folder `C:/Path With Spaces/tests`

        @param full_module_name   the relative full path to the module file
                                  you want to reload from a folder on the
                                  python `sys.path`
    """
    import imp
    import sys
    import importlib

    if full_module_name in sys.modules:
        module_object = sys.modules[full_module_name]
        module_object = imp.reload( module_object )

    else:
        importlib.import_module( full_module_name )