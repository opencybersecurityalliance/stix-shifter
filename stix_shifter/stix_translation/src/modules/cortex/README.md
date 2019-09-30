# Cortex Analyzers

### Format for calling stix-shifter from the command line

python stix_shifter.py cortex `<query or result>` `<stix identity object>` `<data>`

## Converting from STIX2 to a _custom_ Cortex format - used by the transmission module

STIX2 to a _custom_ [Cortex](https://github.com/TheHive-Project/Cortex) format mapping is defined in `from_stix_map.json` which is located in Cortex module.
As Cortex currently does not support an actual query language but rather a mapping of common ioc types to multiple enrichment sources it is easy to translate the STIX2 data to a list of __cortex-datatype: data__ dictonaries.

## Converting from _custom_ Cortex format to STIX2

The hereby defined _custom_ Cortex format returned by the transmission module to STIX2 is defined in `to_stix_map.json`. 
__REMINDER: The transmission module is only returning results for a Cortex analyzer who's option `Extract Observables` is enabled.__ 

This example Cortex data (__ATTENTION: the domain is listed as malicious! Do not follow the link!__):

`python3 main.py translate cortex results '{"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name": "cortex","identity_class": "enrichment"}' '[{"cortex_analyzer": "CyberCrime-Tracker_1_0", "domain": "testingservice1337.ru"}]'`

will return:

```
{
    "type": "bundle",
    "id": "bundle--79f404b7-5179-4220-a88b-271d7b1dc1e3",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "cortex",
            "identity_class": "enrichment"
        },
        {
            "id": "observed-data--d82539bb-f5be-4a37-a2e0-c2b53e611fc1",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-09-30T13:51:02.932Z",
            "modified": "2019-09-30T13:51:02.932Z",
            "objects": {
                "0": {
                    "type": "domain-name",
                    "value": "testingservice1337.ru"
                }
            },
            "x_cortex_analyzer": {
                "name": "CyberCrime-Tracker_1_0"
            }
        }
    ]
}
```
