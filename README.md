# stix-shifter

This project consists of an open source library allowing software to connect to data repositories using STIX Patterning, and return results as STIX Observations.

## Converting from STIX Patterns to data source queries

Call the stix_shifter in the format of

python stix_shifter.py `<data sourc">` `<input format>` `<STIX pattern>`

Example of converting a STIX pattern to an AQL query:

`python3 stix_shifter.py "qradar" "sco" "[ipv4-addr:value = '198.51.100.1' or ipv4-addr:value = '198.51.200.1']"`

Returns:

`SELECT * FROM events WHERE destinationip="198.51.200.1" OR destinationip="198.51.100.1"`

## Contributing

We are thrilled you are considering contributing to <code>kale</code>!
Please read our [guidelines for contributing](CONTRIBUTING.md).

## Licensing

:copyright: Copyright IBM Corp. 2016

All code contained within this project repository or any
subdirectories is licensed according to the terms of the MIT license,
which can be viewed in the file [LICENSE](LICENSE).

## Open Source @ IBM
