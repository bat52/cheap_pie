#!/usr/bin/env bash

DIST=dist
PACKAGE=cheap_pie
PIP=pip3

ARGV=$1
if [ -z "$ARGV" ]
then
    echo "Creating new package... "
    rm -rf $DIST # remove old package folder
    python3 setup.py sdist # create package
    twine upload --repository testpypi ${DIST}/* # upload to testpypi
else
    echo "Installing new package... "
    $PIP uninstall ${PACKAGE}
    $PIP install --index-url https://test.pypi.org/simple/ ${PACKAGE} # install
    # $PIP uninstall ${PACKAGE}
fi