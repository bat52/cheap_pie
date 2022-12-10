#!/usr/bin/env bash

DIST=dist
PACKAGE=cheap_pie
PIP=pip3

ARGV=$1
if [ -z "$ARGV" ]
then
    rm -rf $DIST # remove old package
    python3 setup.py sdist # create package
    twine upload ${DIST}/* # upload to testpypi
else
    echo "Installing new package... "
    $PIP uninstall ${PACKAGE}
    $PIP install ${PACKAGE} # install
    # $PIP uninstall ${PACKAGE}
fi