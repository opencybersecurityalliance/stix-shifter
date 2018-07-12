# stix-shifter

This project consists of an open source library allowing software to connect to data repositories using STIX Patterning, and return results as STIX Observations.

Requires Python 3.6

## Converting from STIX Patterns to data source queries

### Call the stix_shifter in the format of

```
usage: stix_shifter.py translate [-h]
                                 {qradar,dummy,aql_passthrough}
                                 {results,query} data

positional arguments:
  {qradar,dummy,aql_passthrough}         What translation module to use
  {results,query}                        What translation action to perform
  data source                            A STIX identity object
  data                                   The data to be translated

optional arguments:
  -h, --help            show this help message and exit
  -x                    run STIX validation on each observable as it's written to the output JSON
```

### Example of converting a STIX pattern to an AQL query:

[See the QRadar module documentation](stix_shifter/src/modules/qradar/README.md)

### Example of converting QRadar events to STIX:

[See the QRadar module documentation](stix_shifter/src/modules/qradar/README.md)

## Creating new translator modules

To create a new module that can be used when importing stix-shifter, follow these steps:

- Create a directory with the name of your module in the `stix-shifter/src/modules/` directory
- In `stix-shifter.py`, add `<module-name>` to the `MODULES` array at the top of the file
- In your module directory, create a new python code file named `<module-name>_translator.py`. This is where you'll be defining your concrete translator class
  - In `<module-name>_translator.py`, define a class named `Translator` and have it extend `BaseTranslator` from `stix-shifter/src/modules/base/base_translator.py`. (You can use `stix-shifter/src/modules/dummy/dummy_translator.py` as an example)
  - In `__init__` you need to assign `self.result_translator` and `self.query_translator` to the appropriate query and result translator you want your module to use. For example the QRadar translator uses `JSONToStix` as its result translator and `StixToAQL` as its query translator
  - You can write your own query and result translators as well, they must be based off of `BaseQueryTranslator` and `BaseResultTranslator` found in `stix-shifter/src/modules/base/`. Again, you can use the dummy module as a decent example on how to setup the concrete classes found in `stix-shifter/src/modules/dummy/`
- Once you have this all set up you can invoke your module by running `stix_shifter.py` and passing in your translator module name as the first parameter. The second parameter `query or result` determines if your module runs the query or result translator. The third parameter `data` is passed into your translator as the data that will be translated. If you've imported `stix_shifter.py` into other python code, you can invoke it by running the `translate(module, translation_type, data)` method
- IMPORTANT: If you're including any json data files in your module, be sure to include the path in `MANIFEST.in` so that it's included in the packaging

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
