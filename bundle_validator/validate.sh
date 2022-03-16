#!/bin/bash

if [ -z "$1" ]; then
    echo "Specify your bundle file name. Usage: ./validate.sh <json file name>"
    exit 1
fi

if [ -z "$2" ]; then
    echo "Specify the STIX version to validate against. Usage: ./validate.sh <json file name> <2.0 or 2.1>"
    exit 1
fi

FILE=$1
SPEC=$2

if ! [ -f "$FILE" ]; then
    echo "$FILE does not exists. Place your bundle file inside bundle_validator/ folder"
    exit 1
elif [ $SPEC != '2.0' ] && [ $SPEC != '2.1' ]; then
    echo "$SPEC does not match 2.0 or 2.1."
    exit 1
else
    echo "Validating bundle file $FILE against STIX $SPEC "
    echo ""  
fi

if [ $SPEC == '2.0' ]; then
    VALIDATOR_VERSION=1.1.2
else
    VALIDATOR_VERSION=3.0.2
fi

{
    pip3 install virtualenv
    pip3 install venv-run

    virtualenv -p python3 virtualenv

    venv-run pip install stix2-validator==$VALIDATOR_VERSION
} &> /dev/null

venv-run bundle_validator.py $FILE