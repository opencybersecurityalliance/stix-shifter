# stix-shifter

This project consists of an open source library allowing software to connect to data repositories using STIX Patterning, and return results as STIX Observations.

Requires Python 3.6

## Converting from STIX Patterns to data source queries

Call the stix_shifter in the format of

```
usage: stix_shifter.py translate [-h]
                                 {qradar,dummy,aql_passthrough}
                                 {results,query} data

positional arguments:
  {qradar,dummy,aql_passthrough}         What translation module to use
  {results,query}                        What translation action to perform
  data                                   The data to be translated

optional arguments:
  -h, --help            show this help message and exit
```

Example of converting a STIX pattern to an AQL query:

`python stix_shifter.py translate "qradar" "query" "[ipv4-addr:value = '198.51.100.1' or ipv4-addr:value = '198.51.200.1']"`

Returns:

`SELECT * FROM events WHERE destinationip='192.168.122.84' OR sourceip='192.168.122.84' OR destinationip='192.168.122.83' OR sourceip='192.168.122.83'`

Example of converting AQL events to STIX:

`python stix_shifter.py translate "qradar" "results" '[{"starttime": 1524227777191, "protocolid": 255, "sourceip": "9.21.123.112", "logsourceid":126, "qid": 55500004, "sourceport": 0, "eventcount": 1, "magnitude": 4, "identityip": "0.0.0.0", "destinationip": "9.21.123.112", "destinationport": 0, "category": 10009, "username": null}]'`

Returns:

```json
[
  {
    "x_com_ibm_uds_datasource": {
      "id": "7c0de425-33bf-46be-9e38-e42319e36d95",
      "name": "events"
    },
    "id": "observed-data--62392b84-66a7-4984-a49d-7872986e0c48",
    "type": "observed-data",
    "objects": {
      "0": { "type": "ipv4-addr", "value": "9.21.123.112" },
      "1": { "type": "ipv4-addr", "value": "9.21.123.112" },
      "2": { "type": "network-traffic", "src_ref": "1", "dst_ref": "0" }
    },
    "x_com_ibm_ariel": {
      "log_source_id": 126,
      "identity_ip": "0.0.0.0",
      "protocol_id": 255,
      "magnitude": 4,
      "qid": 55500004
    },
    "number_observed": 1,
    "created": "2018-04-20T12:36:17.191Z",
    "modified": "2018-04-20T12:36:17.191Z",
    "first_observed": "2018-04-20T12:36:17.191Z",
    "last_observed": "2018-04-20T12:36:17.191Z"
  }
]
```

## Creating new translator modules

To create a new module that can be used when importing stix-shifter, follow these steps:

* Create a directory with the name of your module in the `src/modules/` directory
* In `stix-shifter.py`, add `<module-name>` to the `MODULES` array at the top of the file
* In your module directory, create a new python code file named `<module-name>_translator.py`. This is where you'll be defining your concrete translator class
  * In `<module-name>_translator.py`, define a class named `Translator` and have it extend `BaseTranslator` from `src/modules/base/base_translator.py`. (You can use `src/modules/dummy/dummy_translator.py` as an example)
  * In `__init__` you need to assign `self.result_translator` and `self.query_translator` to the appropriate query and result translator you want your module to use. For example the QRadar translator uses `JSONToStix` as its result translator and `StixToAQL` as its query translator
  * You can write your own query and result translators as well, they must be based off of `BaseQueryTranslator` and `BaseResultTranslator` found in `src/modules/base/`. Again, you can use the dummy module as a decent example on how to setup the concrete classes found in `src/modules/dummy/`
* Once you have this all set up you can invoke your module by running `stix_shifter.py` and passing in your translator module name as the first parameter. The second parameter `query or result` determines if your module runs the query or result translator. The third parameter `data` is passed into your translator as the data that will be translated. If you've imported `stix_shifter.py` into other python code, you can invoke it by running the `translate(module, translation_type, data)` method

## Contributing

We are thrilled you are considering contributing!
Please read our [guidelines for contributing](CONTRIBUTING.md).

## Licensing

:copyright: Copyright IBM Corp. 2018

All code contained within this project repository or any
subdirectories is licensed according to the terms of the Apache v2.0 license,
which can be viewed in the file [LICENSE](LICENSE).

## Open Source @ IBM

[Find more open source projects on the IBM Github Page](http://ibm.github.io/)
