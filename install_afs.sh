#!/bin/bash

PYAMI_AFS_PATH=/afs/cern.ch/atlas/software/tools/atlasmeta
source setup.sh
cp setup.sh $PYAMI_AFS_PATH
export PYAMI_USE_DISTRIBUTE=1
export PYAMI_AFS_INSTALL=1
python setup.py install --prefix=$PYAMI_AFS_PATH
