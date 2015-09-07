#!/bin/bash

#--------------------------------------------------------------------------
# Get path to this script to use as base path
#

#Note: Handles many use cases (e.g. '.' vs 'source', sym links, etc) 
#Stolen from: http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
SCRIPT_PATH="${BASH_SOURCE[0]}";
if ([ -h "${SCRIPT_PATH}" ]) then
  while([ -h "${SCRIPT_PATH}" ]) do SCRIPT_PATH=`readlink "${SCRIPT_PATH}"`; done
fi
pushd . > /dev/null
cd `dirname ${SCRIPT_PATH}` > /dev/null
SCRIPT_PATH=`pwd`;
popd  > /dev/null
export GM2PLOTS_DIR=$SCRIPT_PATH
echo "Project top-level: $GM2PLOTS_DIR"


#--------------------------------------------------------------------------
# Set python path
#

export PYTHONPATH=$PYTHONPATH:$GM2PLOTS_DIR/util
