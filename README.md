STIX-shifter is an open source python library allowing software to connect to products that house data repositories by using STIX Patterning, and return results as STIX Observations.

STIX-Shifter is the heart of the Universal Data Service (UDS) that is provided as part of [IBM Security Connect](https://www.ibm.com/security/connect/).

For more information about this project, see the [stix-shifter project](https://github.com/IBM/stix-shifter/blob/master/README.md)

### Dependencies

This stix-shifter has the following dependencies:

- [stix2-patterns>=1.1.0](https://pypi.org/project/stix2-patterns/)
- [stix2-validator>=0.5.0](https://pypi.org/project/stix2-validator/)
- [stix2-matcher](https://github.com/oasis-open/cti-pattern-matcher): There is no python package publish in pypi for stix2-matcher. The bellow command can be used to install this package:
    ```
    pip install git+git://github.com/oasis-open/cti-pattern-matcher.git@v0.1.0#egg=stix2-matcher
    ```
- [antlr4-python3-runtime==4.7](https://pypi.org/project/antlr4-python3-runtime/)
- [python-dateutil>=2.7.3](https://pypi.org/project/python-dateutil/)

Your development environment must use Python 3.6.x

## Installation
The recommended method for installing the STIX-shifter is via pip.
```
pip install stix-shifter
```

## Contributing

We are thrilled you are considering contributing! We welcome all contributors.

Please read our [guidelines for contributing](https://github.com/IBM/stix-shifter/blob/master/CONTRIBUTING.md).

## Guide for creating new adapters

If you want to create a new adapter for STIX-shifter, see the [developer guide](https://github.com/IBM/stix-shifter/blob/bundle_sample/adapter-guide/develop-stix-adapter.md)

## Licensing

:copyright: Copyright IBM Corp. 2018

All code contained within this project repository or any
subdirectories is licensed according to the terms of the Apache v2.0 license,
which can be viewed in the file [LICENSE](https://github.com/IBM/stix-shifter/blob/master/LICENSE).

## Open Source at IBM

[Find more open source projects on the IBM GitHub Page](http://ibm.github.io/)