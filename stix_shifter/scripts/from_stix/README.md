# FROM_STIX mapping file generate

This script will generate:
    1. from_stix_map_sorted.json file from existing from_stix_map.json (sorted and linted) and 
    2. from_stix_map_generated.json file from to_stix_map.json
and put them in ./var/from_stix folder (git ignored), in the root of the project
 
You can use from_stix_map_sorted.json and from_stix_map_generated.json to compare the differences or/and use from_stix_map_generated.json as actual from_stix mapping file. 


Not all connectors have to_stix_map.json file, because they have more than one dialect. The current implementation of the script does not cover that use case.

If the request and result property names are different for an API, another mapping file can be used to translate "to" to "from" stix, example is reaqta's to_to_from_map.json


### USAGE

Comment/uncomment the modules you want to generate in MODULES variable

```
python3 stix_shifter/scripts/create_from_stix.py
```

### PREREQUEST for inline diff (optional)
Uncomment "print('COMPARE CMD .... " line

Install python lib
```
pip3 install ydiff
```

The script will output diff command to be used to compare the files

For UI diif you can use this guide for Visual Studio Code Compare 
https://www.mytecbits.com/microsoft/dot-net/compare-contents-of-two-files-in-vs-code

