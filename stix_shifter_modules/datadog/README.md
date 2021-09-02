# Datadog

This is a connector for searching Datadog events. 

### Format for making STIX translation calls via the CLI

`python main.py <translator_module> <query or result> <STIX identity object> <data>`

Note the STIX identity object is only used when translating data source results into STIX, so it can be passed in as an empty object for query translation calls.

### Converting from STIX patterns to Datadog queries

This example input pattern for TRANSLATE:

`python main.py translate datadog query '{}' "[domain-name:value = 'abc.com']"`

Returns the following search query:

```
{
    "queries": [
        "{\"host\": \"abc.com\", \"start\": 9580878, \"end\": 12345678}"
    ]
}
```

### Converting from Datadog events to STIX

Datadog data to STIX mapping is defined in `to_stix_map.json`

This example Datadog data:

`python3 main.py translate datadog results '{"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "datadog", "identity_class": "events"}' '[{
                "date_happened": 1628017283,
                "alert_type": "info",
                "title": "An API key has been created.",
                "url": "/event/event?id=6102786433786642502",
                "text": "API key getevents created by qradar10.34.38.141@gmail.com in org qradar",
                "tags": [
                    "account",
                    "audit"
                ],
                "device_name": "windows-GS-2190",
                "priority": "normal",
                "host": "121.0.0.1",
				"resource": "/api/event/6102786433786642502",
                "id": 6102786433786642502
            }]'`

Will return the following STIX observable:

```json
{
    "type": "bundle",
    "id": "bundle--261ea1e6-20b2-4191-b56d-04333e059964",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "datadog",
            "identity_class": "events"
        },
        {
            "id": "observed-data--e3cf92ee-f838-4a32-a292-6f2d280c38fd",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2021-09-02T05:30:23.823Z",
            "modified": "2021-09-02T05:30:23.823Z",
            "objects": {
                "0": {
                    "type": "x-ibm-finding",
                    "time_observed": "1970-01-19T20:13:37.283Z"
                },
                "1": {
                    "type": "x-datadog-event",
                    "alert_type": "info",
                    "title": "An API key has been created.",
                    "text": "API key getevents created by qradar10.34.38.141@gmail.com in org qradar",
                    "tags": [
                        "account",
                        "audit"
                    ],
                    "device_name": "windows-GS-2190",
                    "priority": "normal",
                    "event_id": 6102786433786642502
                },
                "2": {
                    "type": "url",
                    "value": "/event/event?id=6102786433786642502"
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "121.0.0.1"
                },
                "4": {
                    "type": "domain-name",
                    "host": "121.0.0.1"
                },
                "5": {
                    "type": "url",
                    "value": "/api/event/6102786433786642502"
                }
            },
            "first_observed": "2021-09-02T05:30:23.823Z",
            "last_observed": "2021-09-02T05:30:23.823Z",
            "number_observed": 1
        }
    ]
}
```
## Transmit

### Transmit functions

Transmit offers several functions: ping, query, results and is_async.

### Ping

Uses the data source API to ping the connection

CLI command example:
```
python3 main.py transmit datadog '{"site_url": <site_url>}' '{ "auth": { "api_key": <api_key>, "application_key": <application_key>}}' ping
```
If connection establish returns the following response:
```
{
    "success": true
}
```
### Results

Uses the data source API to fetch the query results based on the search ID, offset, and length.

CLI Command example:
```
python3 main.py transmit datadog '{"site_url": <site_url>}' '{ "auth": { "api_key": <api_key>, "application_key": <application_key>}}' results "{\"tags\": \"account\", \"start\": 1627207221, \"end\": 1629972021}" <OFFSET> <LENGTH>
```
Returns following result
```json
{
    "success": true,
    "data": [
        {
            "date_happened": 1628017898,
            "alert_type": "info",
            "title": "A new application key has been created.",
            "url": "/event/event?id=6102796743464967547",
            "text": "Application key test created by qradar10.34.38.141@gmail.com in org qradar",
            "tags": [
                "account",
                "audit"
            ],
            "device_name": null,
            "priority": "normal",
            "host": null,
            "id": 6102796743464967547
        }
    ]
}
```