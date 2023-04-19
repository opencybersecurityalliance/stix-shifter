[![example workflow](https://github.com/opencybersecurityalliance/stix-shifter/actions/workflows/main.yml/badge.svg)](https://github.com/opencybersecurityalliance/stix-shifter/actions)
[![codecov](https://codecov.io/gh/opencybersecurityalliance/stix-shifter/branch/develop/graph/badge.svg?token=gQvl14peRj)](https://codecov.io/gh/opencybersecurityalliance/stix-shifter)

# Introduction to STIX-Shifter

STIX-shifter is an open source python library allowing software to connect to products that house data repositories by using STIX Patterning, and return results as STIX Observations.

This library takes in STIX 2 Patterns as input, and "finds" data that matches the patterns inside various products that house repositories of cybersecurity data. Examples of such products include SIEM systems, endpoint management systems, threat intelligence platforms, orchestration platforms, network control points, data lakes, and more.

In addition to "finding" the data by using these patterns, STIX-Shifter also _transforms the output_ into STIX 2 Observations. Why would we do that you ask? To put it simply - so that all of the security data, regardless of the source, mostly looks and behaves the same.

[## Project Overview and CLI Commands](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/OVERVIEW.md)

For general information about STIX, this project, and the command line utilities, see the [STIX-shifter Overview](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/OVERVIEW.md)


# Installation

The recommended method for installing the STIX-shifter is via pip. Two prerequisite packages needs to be installed inlcuding the package of stix-shifter connector module to complete a stix-shifter connector installation. Run below commands to install all the packages-

1. Main stix-shifter package:  `pip install stix-shifter`

2. Stix-shifter Utility package:  `pip install stix-shifter-utils`

3. Desired stix-shifter connector module package:  `pip install stix-shifter-modules-<module name> `
   Example:  `pip install stix-shifter-modules-qradar`

## Dependencies

STIX-shifter has the following dependencies:

- [stix2-patterns==1.3.0](https://pypi.org/project/stix2-patterns/)
- [stix2-validator==1.1.2](https://pypi.org/project/stix2-validator/)
- [stix2-matcher==1.0.0](https://pypi.org/project/stix2-matcher/)
- [antlr4-python3-runtime==4.8](https://pypi.org/project/antlr4-python3-runtime/)
- [python-dateutil==2.8.1](https://pypi.org/project/python-dateutil/)

Your development environment must use Python version: 3.8 or greater

# Usage

STIX-Shifter can use used the following ways:

## 1. As A Command Line Utility

The STIX-Shifter comes with a bundled script which you can use to translate STIX Pattern to a native datasource query. It can also be used to translate a JSON data source query result to a STIX bundle of observable objects. You can also send query to a datasource by using a transmission option. 

More details of the command line option can be found [here](https://github.com/opencybersecurityalliance/stix-shifter/blob/master/OVERVIEW.md#how-to-use)

```
$ stix-shifter translate <MODULE NAME> query "<STIX IDENTITY OBJECT>" "<STIX PATTERN>" "<OPTIONS>"
```
Example:
```
$ stix-shifter translate qradar query {} "[ipv4-addr:value = '127.0.0.1']" {}
```

In order to build `stix-shifter` packages from source follow the below prerequisite steps:
   1. Go to the stix-shifter parent directory
   2. Optionally, you can create a Python 3 virtual environemnt:
       `virtualenv -p python3 virtualenv && source virtualenv/bin/activate`
   3. Run setup: `python3 setup.py install`


## 2. Running From the Source

You may also use `python3 main.py` script. All the options are the same as "As a command line utility" usage above.

Example:

```
python3 main.py translate qradar query {} "[ipv4-addr:value = '127.0.0.1']" {}
```

In order to run `python3 main.py` from the source follow the below prerequisite steps:
   1. Go to the stix-shifter parent directory
   2. Optionally, you can create a Python 3 virtual environemnt:
       `virtualenv -p python3 virtualenv && source virtualenv/bin/activate`
   3. Run setup to install dependancies: `INSTALL_REQUIREMENTS_ONLY=1 python3 setup.py install`. 

**Note:** setup.py only installs dependencies when INSTALL_REQUIREMENTS_ONLY=1 directive is used. This option is similar to `python3 generate_requirements.py && pip install -r requirements.txt`

## 3. As A Library

You can also use this library to integrate STIX Shifter into your own tools. You can translate a STIX Pattern:

```
from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()
response = translation.translate('<MODULE NAME>', 'query', '{}', '<STIX PATTERN>', '<OPTIONS>')

print(response)
```
### Use of custom mappings

If a connector has been installed using pip, the process for editing the STIX mappings is different than if you have pulled-down the project. When working locally, you can edit the mapping files directly. See the [mapping files for the MySQL connector](stix_shifter_modules/mysql/stix_translation/json) as an example. Editing the mapping files won't work if the connector has been installed with pip; the setup script of the stix-shifter package includes the mapppings inside `config.json`. This allows stix-shifter to injest custom mappings as part of the connector's configuration.

Refer to [Use of custom mappings](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/custom_mappings.md) for more details on how to edit the mappings in the configuration.

# Contributing

We are thrilled you are considering contributing! We welcome all contributors.
Please read our [guidelines for contributing](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/CONTRIBUTING.md).

[## Connector Developer Guide](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-stix-adapter.md)

<!-- If you want to create a new connector for STIX-shifter, see the [developer guide](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/adapter-guide/develop-stix-adapter.md) -->

[## Jupyter Notebook Development Labs](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/lab)

<!-- There are also a few [Jupyter Notebook labs](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/lab) that cover the CLI commands and dev process. -->

# Licensing

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

# More Resources

## Join us on Slack!

[Click here](https://docs.google.com/forms/d/1vEAqg9SKBF3UMtmbJJ9qqLarrXN5zeVG3_obedA3DKs) and fill out the form to receive an invite to the Open Cybersecurity Alliance slack instance, then join the #stix-shifter channel, to meet and discuss usage with the team.

## Introduction Webinar!

[Click here](https://ibm.biz/BdzTyA) to view an introduction webinar on STIX Shifter and the use cases it solves for.

## Changelog

- [Changelog](https://github.com/opencybersecurityalliance/stix-shifter/blob/develop/CHANGELOG.md)