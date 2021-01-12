# QRadar

### Format for calling stix-shifter from the command line

python stix_shifter.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

(Note the identity object is only used when converting from AQL to STIX, but due to positional arguments, an empty hash will need to be passed in when converting from STIX patterns to AQL. Keyword arguments should be implemented to overcome this).

## Converting from STIX patterns to AQL queries

Returns an object representing the aql query and a parsing of the input stix pattern:

`{'aql_query:' resulting_aql_query_string, 'stix_parsing': [{'attribute': <STIX attribute>, 'comparison_operator': <comparison operator>, 'value': <STIX value>}]}`

This example input pattern:

`python main.py translate "qradar" "query" '{}' "[url:value = 'www.example.com' and mac-addr:value = '00-00-5E-00-53-00']"`

Returns the following AQL query:

`SELECT <defined QRadar fields> FROM events WHERE (sourcemac='00-00-5E-00-53-00' OR destinationmac='00-00-5E-00-53-00') AND url='www.example.com'`

and returns the parsed STIX pattern:

`[{'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}, {'attribute': 'url:value', 'comparison_operator': '=', 'value': 'www.example.com'}]`

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
- file:name
- network-traffic:src_port, network=traffic:dst_port

## Converting from QRadar events to STIX

QRadar data to STIX mapping is defined in `to_stix_map.json`

This example QRadar data:

`python main.py translate "qradar" "results" '{"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "QRadar", "identity_class": "events"}' '[{"starttime": 1524227777191, "protocolid": 255, "sourceip": "9.21.123.112", "logsourceid":126, "qid": 55500004, "sourceport": 0, "eventcount": 1, "magnitude": 4, "identityip": "0.0.0.0", "destinationip": "9.21.123.112", "destinationport": 0, "category": 10009, "username": null}]'`

Will return the following STIX observable:

```json
{
  "type": "bundle",
  "id": "bundle--994b685e-6c42-4e0c-b6c4-f3da97fb4cf4",
  "objects": [
    {
      "type": "identity",
      "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
      "name": "QRadar",
      "identity_class": "events"
    },
    {
      "id": "observed-data--62392b84-66a7-4984-a49d-7872986e0c48",
      "type": "observed-data",
      "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
      "objects": {
        "0": {
          "type": "ipv4-addr",
          "value": "9.21.123.112"
        },
        "1": {
          "type": "ipv6-addr",
          "value": "9.21.123.112"
        },
        "2": {
          "type": "network-traffic",
          "src_ref": "1",
          "src_port": 0,
          "dst_ref": "0",
          "dst_port": 0,
          "protocols": ["tcp"]
        }
      },
      "x_ibm_ariel": {
        "log_source_id": 126,
        "identity_ip": "0.0.0.0",
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
}
```
