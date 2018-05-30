# stix-shifter

This project consists of an open source library allowing software to connect to data repositories using STIX Patterning, and return results as STIX Observations.

## Converting from STIX Patterns to data source queries

Call the stix_shifter in the format of

python stix_shifter.py `<data source>` `<input format>` `<STIX pattern>`

Example of converting a STIX pattern to an AQL query:

`python3 stix_shifter.py "qradar" "sco" "[ipv4-addr:value = '192.168.122.83' or ipv4-addr:value = '192.168.122.84']"`

Returns:

`SELECT * FROM events WHERE destinationip='192.168.122.84' OR sourceip='192.168.122.84' OR destinationip='192.168.122.83' OR sourceip='192.168.122.83'`

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
