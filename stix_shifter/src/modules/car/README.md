# QRadar

### Format for calling stix-shifter from the command line

python stix_shifter.py `<translator_module>` `<query or result>` `<data>`

## Converting from STIX patterns to AQL queries

This example input pattern:

`python main.py translate "qradar" "query" "[domain-name:value = 'example.com' and mac-addr:value = '00-00-5E-00-53-00']"`

Returns the following AQL query:

`SELECT <defined QRadar fields> FROM events WHERE (sourcemac='00-00-5E-00-53-00' OR destinationmac='00-00-5E-00-53-00') AND domainname='example.com'`

### AQL query construction: SELECT statement

The QRadar event columns that make up the SELECT portion of the AQL query are defined in `aql_event_fields.json`. A default selection is provided, but custom selections can be added to this file.

### AQL query construction: WHERE clause

STIX to AQL field mapping is defined in `from_stix_map.json` <br/>
STIX attributes that map to multiple AQL fields will have those fields joined by ORs in the returned query. <br/>
Translated STIX attributes are inserted into the AQL query in the order they are defined in the mapping file. <br/>
When translating from STIX patterns to AQL queries, the following objects and attributes can be used:

- ipv4-addr:value
- ipv6-addr:value
- url:value
- mac-addr:value
- domain-name:value
- file:name
- network-traffic:src_port, network=traffic:dst_port

## Converting from QRadar events to STIX

QRadar data to STIX mapping is defined in `to_stix_map.json`

This example QRadar data:

`python main.py translate "qradar" "results" '[{"starttime": 1524227777191, "protocolid": 255, "sourceip": "9.21.123.112", "logsourceid":126, "qid": 55500004, "sourceport": 0, "eventcount": 1, "magnitude": 4, "identityip": "0.0.0.0", "destinationip": "9.21.123.112", "destinationport": 0, "category": 10009, "username": null}]'`

Will return the following STIX observable:

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
