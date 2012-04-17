#!/bin/bash
# deterine path to this script
# http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
SOURCE_PYAMI_SETUP="${BASH_SOURCE[0]}"
while [ -h "$SOURCE_PYAMI_SETUP" ] ; do SOURCE_PYAMI_SETUP="$(readlink "$SOURCE_PYAMI_SETUP")"; done
DIR_PYAMI_SETUP="$( cd -P "$( dirname "$SOURCE_PYAMI_SETUP" )" && pwd )"
echo "sourcing ${SOURCE_PYAMI_SETUP}..."

export PATH=${DIR_PYAMI_SETUP}/bin${PATH:+:$PATH}
export PYTHONPATH=${DIR_PYAMI_SETUP}/lib/python2.4/site-packages${PYTHONPATH:+:$PYTHONPATH}
export PYAMI_VERSION=`cat ${DIR_PYAMI_SETUP}/version.txt`
echo "Setting up pyAMI ${PYAMI_VERSION}"
