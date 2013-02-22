#!/bin/bash

# install version for use with python 2.6
rm -rf /afs/cern.ch/atlas/software/tools/pyAMI/python2.6
make install \
PYTHON=/afs/cern.ch/sw/lcg/external/Python/2.6.5/x86_64-slc5-gcc43-opt/bin/python \
PREFIX=/afs/cern.ch/atlas/software/tools/pyAMI/python2.6
