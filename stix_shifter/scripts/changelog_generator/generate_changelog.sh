#!/bin/bash

if [ -z "$2" ]; then
    echo "Specify the tag of the last release and the tag for the new release. Example: ./git_logs.sh 4.1.0 4.1.2"
    exit 1
fi

OLDTAG=$1
NEWTAG=$2

# OUTPUT=$(git log $(git describe --tags --abbrev=0)..HEAD --oneline)
OUTPUT=$(git log $OLDTAG..HEAD --oneline)

{
    pip3 install virtualenv
    pip3 install venv-run
    virtualenv -p python3 virtualenv
} &> /dev/null

venv-run generate_changelog.py "$OUTPUT" "$NEWTAG"