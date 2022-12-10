#!/usr/bin/env bash

DIST=dist
PACKAGE=cheap_pie
PIP="python3 -m pip"

rm -rf $DIST # remove old package
python3 setup.py sdist # create package
twine upload --repository testpypi ${DIST}/* # upload to testpypi
$PIP uninstall ${PACKAGE} # uninstal, just in case
$PIP install --index-url https://test.pypi.org/simple/ ${PACKAGE} # install
# $PIP uninstall ${PACKAGE}