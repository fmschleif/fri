#!/usr/bin/env bash

set -ex # fail on first error, print commands

command -v conda >/dev/null 2>&1 || {
  echo "Requires conda but it is not installed.  Run install_miniconda.sh." >&2;
  exit 1;
}

ENVNAME="testenv"
PYTHON_VERSION=${PYTHON_VERSION:-3.6} # if no python specified, use 3.6

if [ -z ${GLOBAL} ]
then
    if conda env list | grep -q ${ENVNAME}
    then
      echo "Environment ${ENVNAME} already exists, keeping up to date"
    else
      conda create -n ${ENVNAME} --yes -q pip python=${PYTHON_VERSION}
      source activate ${ENVNAME}
    fi
fi


conda install --yes numpy scipy pytest pytest-cov coverage scikit-learn pandas seaborn matplotlib
python setup.py install