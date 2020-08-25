### Join us on Slack!

[Click here](https://docs.google.com/forms/d/1vEAqg9SKBF3UMtmbJJ9qqLarrXN5zeVG3_obedA3DKs) and fill out the form to receive an invite to the Open Cybersecurity Alliance slack instance, then join the #stix-shifter channel, to meet and discuss usage with the team.

### Introduction Webinar!

[Click here](https://ibm.biz/BdzTyA) to view an introduction webinar on STIX Shifter and the use cases it solves for.

### Introduction

STIX-shifter is an open source python library allowing software to connect to products that house data repositories by using STIX Patterning, and return results as STIX Observations.

For more information about this project, see the [STIX-shifter Overview](https://github.com/opencybersecurityalliance/stix-shifter/blob/master/OVERVIEW.md)

### Dependencies

This stix-shifter has the following dependencies:

- [stix2-patterns==1.3.0](https://pypi.org/project/stix2-patterns/)
- [stix2-validator==1.1.2](https://pypi.org/project/stix2-validator/)
- [stix2-matcher==1.0.0](https://pypi.org/project/stix2-matcher/)
- [antlr4-python3-runtime==4.8](https://pypi.org/project/antlr4-python3-runtime/)
- [python-dateutil==2.8.1](https://pypi.org/project/python-dateutil/)

Your development environment must use Python 3.6.x

## Installation

The recommended method for installing the STIX-shifter is via pip. Two prerequisite packages needs to be installed inlcuding the package of stix-shifter connector module to complete a stix-shifter connector installation. Run below commands to install all the packages-

1. Main stix-shifter package:  `pip install stix-shifter`

2. stix-shifter-utility package:  `pip install stix-shifter-utils`

3. Desired stix-shifter connector module package:  `pip install stix-shifter-modules-<module name> `
   Example:  `pip install stix-shifter-modules-qradar`

## Usage


### As A Script

The STIX-Shifter comes with a bundled script which you can use to translate STIX Pattern to a native datasource query. It can also be used to translate a JSON data source query result to a STIX bundle of observable objects. You can also send query to a datasource by using a transmission option. 

More details of the command line option can be found [here](https://github.com/opencybersecurityalliance/stix-shifter/blob/master/OVERVIEW.md#how-to-use)

```
$ stix-shifter translate <MODULE NAME> query "<STIX IDENTITY OBJECT>" "<STIX PATTERN>" "<OPTIONS>"
```
Example:
```
$ stix-shifter translate qradar query {} "[ipv4-addr:value = '127.0.0.1']" {}
```

**Note:** In order to create python executable `stix-shifter` from source run the following command from stix-shifter parent directory in your python 3 environment: `python setup.py install`

### As A Library

You can also use this library to integrate STIX Shifter into your own tools. You can translate a STIX Pattern:

```
from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()
response = translation.translate('<MODULE NAME>', 'query', '{}', '<STIX PATTERN>', '<OPTIONS>')

print(response)
```

## Contributing

We are thrilled you are considering contributing! We welcome all contributors.

Please read our [guidelines for contributing](https://github.com/opencybersecurityalliance/stix-shifter/blob/master/CONTRIBUTING.md).

## Guide for creating new connectors

If you want to create a new connector for STIX-shifter, see the [developer guide](https://github.com/opencybersecurityalliance/stix-shifter/blob/master/adapter-guide/develop-stix-adapter.md)

## Licensing

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
