#!/bin/bash

PYAMI_AFS_PATH=/afs/cern.ch/atlas/software/tools/atlasmeta
cp setup.sh $PYAMI_AFS_PATH
source $PYAMI_AFS_PATH/setup.sh
export PYAMI_AFS_INSTALL=1
python setup.py install --prefix=$PYAMI_AFS_PATH
