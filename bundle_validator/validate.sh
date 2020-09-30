#!/bin/bash

if [ -z "$1" ]; then
    echo "Specify your bundle file name. Usage: ./validate.sh <json file name>"
    exit 1
fi

FILE=$1

if [ -f "$FILE" ]; then
    echo "Validating STIX Bundle file: $FILE "
    echo ""
else
    echo "$FILE does not exists. Place your bundle file inside bundle_validator/ folder"
    exit 1
fi

{
    pip3 install virtualenv
    pip3 install venv-run

    virtualenv -p python3 virtualenv

    venv-run pip install stix2-validator==1.1.2
} &> /dev/null

venv-run bundle_validator.py $FILE