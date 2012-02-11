#!/bin/bash

AFS_PATH=/afs/cern.ch/atlas/software/tools/atlasmeta
source setup.sh
cp setup.sh $AFS_PATH
export ATLASMETA_USE_DISTRIBUTE=1
python setup.py install --prefix=$AFS_PATH
