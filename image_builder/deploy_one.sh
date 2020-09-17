#!/bin/bash

cd "$(dirname "$0")"

MYDIR=`pwd`
SS_HOME='..'
SS_MODULES_HOME="${SS_HOME}/stix_shifter_modules"
MODULE=$1

if [ -z "$MODULE" ]
then
      printf 'Usage: %s module_name\n' "$(basename "$0")"
      exit 1
fi

if [ ! -d "$SS_MODULES_HOME/$MODULE" ]; then
  echo "module is not found: ${MODULE}..."
  exit 1
fi

cd $SS_HOME
if [ ! -f "requirements.txt" ]; then
  python3 generate_requirements.py
fi

pip3 install virtualenv
pip3 install venv-run

virtualenv -p python3 virtualenv

venv-run pip install -r requirements.txt
venv-run pip install setuptools wheel twine jsonmerge

rm -rf dist
venv-run setup.py bdist_wheel
cd $MYDIR
rm -rf bundle
mkdir bundle
cp $SS_HOME/dist/stix_shifter_modules_$MODULE-* bundle/
./build.sh
