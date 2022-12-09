#!/usr/bin/env bash

DIST=dist
PACKAGE=cheap_pie

rm -rf $DIST # remove old package
python3 setup.py sdist # create package
twine upload ${DIST}/* # upload to testpypi
python3 -m pip install ${PACKAGE} # install