#!/bin/bash

# Run this from the root of the repo

for to_stix_map in $(find stix_shifter_modules/ -name "*to_stix_map.json")
do
    echo -e "${to_stix_map}:"
    python3 map_validator/validate_mapping.py $to_stix_map || break
    echo
done
