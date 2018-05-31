# stix-shifter

This project consists of an open source library allowing software to connect to data repositories using STIX Patterning, and return results as STIX Observations.

Requires Python 3.6

## Converting from STIX Patterns to data source queries

Call the stix_shifter in the format of

python stix_shifter.py `<data source>` `<input format>` `<STIX pattern>`

Example of converting a STIX pattern to an AQL query:

`python3 stix_shifter.py "qradar" "sco" "[ipv4-addr:value = '192.168.122.83' or ipv4-addr:value = '192.168.122.84']"`

Returns:

`SELECT * FROM events WHERE destinationip='192.168.122.84' OR sourceip='192.168.122.84' OR destinationip='192.168.122.83' OR sourceip='192.168.122.83'`

Example of converting AQL events to STIX:

`python3 stix_shifter.py "qradar" "qradar_events" '[{"starttime": 1524227777191, "protocolid": 255, "sourceip": "9.21.123.112", "logsourceid":126, "qid": 55500004, "sourceport": 0, "eventcount": 1, "magnitude": 4, "identityip": "0.0.0.0", "destinationip": "9.21.123.112", "destinationport": 0, "category": 10009, "username": null}]'`

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
