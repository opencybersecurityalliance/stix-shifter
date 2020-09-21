#!/bin/bash

cd "$(dirname "$0")"

MYDIR=`pwd`
SS_HOME='../..'
SS_MODULES_HOME="${SS_HOME}/stix_shifter_modules"
MODULE=$1
BUILD_LOCATION=$2
REPOSITORY=$3

if [ -z "$MODULE" ]; then
  printf 'Usage: %s module_name\n' "$(basename "$0")"
  exit 1
fi

if ! ([ $BUILD_LOCATION == "local" ] || [ $BUILD_LOCATION == "remote" ]); then
  echo "Image build location must be 'local' or 'remote'"
  exit 1
fi

if [ ! -d "$SS_MODULES_HOME/$MODULE" ]; then
  echo "Module not found: ${MODULE}..."
  exit 1
fi

if [ -f cert.key ] && [ -f cert.pem ]; then
  echo "Install cryptography for cert signing"
  pip3 install cryptography pyopenssl
fi

cd $SS_HOME
if [ ! -f "requirements.txt" ]; then
  python3 generate_requirements.py
fi

pip3 install virtualenv
pip3 install venv-run


virtualenv -p python3 virtualenv

venv-run pip install -r requirements.txt
venv-run pip install setuptools wheel twine

rm -rf dist
venv-run setup.py bdist_wheel
cd $MYDIR
rm -rf bundle
mkdir bundle
cp $SS_HOME/dist/stix_shifter_modules_$MODULE-* bundle/
if [ $BUILD_LOCATION == "local" ]; then
  echo "Building image locally"
  ./_build_local.sh
elif [ $REPOSITORY != "" ]; then
  echo "Deploying image from repository: ${REPOSITORY}"
  ./_build.sh $REPOSITORY
else
  echo "Building and deploying image"
  ./_build.sh
fi
