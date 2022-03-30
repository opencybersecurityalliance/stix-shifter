# Trustar 
​
REST Web Service APIs: https://docs.trustar.co/api/v13/
​
### Format for making STIX translation calls via the CLI
​
`python3 main.py <translator_module> <query or result> <STIX identity object> <data>`
​
This example input pattern:
​
python main.py translate trustar query '{}' "[x-trustar-report:searchTerm LIKE '%'] START t'2022-01-04T07:34:00.000Z' STOP t'2022-01-04T08:34:00.000Z'"

will return
# NOTE - if from/to is not provided, defaults to past 5 minutes
```
{
    "queries": [
        "{\"searchTerm\": \" \", \"from\": 1641281640000, \"to\": 1641285240000}"
    ]
}
```
## Converting from Secret Server events STIX

### Transmission Call:

```

 python main.py execute trustar trustar '{"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name": "mysql","identity_class": "events"}' '{"host": "", "port": }' '{"auth": {"clientId":"", "clientSecret": ""}}' "[x-trustar-report:searchTerm LIKE '%'] START t'2022-01-04T07:34:00.000Z' STOP t'2022-01-04T08:34:00.000Z'"

```
Returns:

```

{
    "type": "bundle",
    "id": "bundle--8e1027b6-9ed0-48f7-b367-8c9d5ff4b9d4",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "mysql",
            "identity_class": "events"
        },
        {
            "id": "observed-data--8113c3f4-d21f-459e-ab3c-8ac42a5dcf37",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-03-30T11:50:37.239Z",
            "modified": "2022-03-30T11:50:37.239Z",
            "objects": {
                "0": {
                    "type": "x-trustar-indicator",
                    "prioritylevel": "NOT_FOUND",
                    "firstseen": "2022-01-04T08:14:25.066Z",
                    "lastseen": "2022-01-04T08:14:25.066Z",
                    "guid": "IP|212.192.216.55",
                    "meta": {
                        "correlationcount": 0,
                        "notecount": 0,
                        "sightings": 1,
                        "enclaveids": [
                            "cabbfa67-afd7-4a0c-a20f-e51e25923629"
                        ]
                    }
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "212.192.216.55"
                }
            },
            "first_observed": "2022-03-30T11:50:37.239Z",
            "last_observed": "2022-03-30T11:50:37.239Z",
            "number_observed": 1
        },
        {
            "id": "observed-data--f4d93b9a-4612-4f11-8cde-270d67400cd5",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-03-30T11:50:37.240Z",
            "modified": "2022-03-30T11:50:37.240Z",
            "objects": {
                "0": {
                    "type": "x-trustar-report",
                    "id": "6ad230c7-75b4-49ef-b68e-ab6d57d46234",
                    "created": "2022-01-04T08:14:25.065Z",
                    "updated": "2022-01-04T08:14:25.065Z",
                    "title": "MalwareDownload_Generic",
                    "enclaveids": [
                        "cabbfa67-afd7-4a0c-a20f-e51e25923629"
                    ],
                    "indicators": [
                        {
                            "indicatorType": "IP",
                            "value": "212.192.216.55",
                            "whitelisted": false,
                            "guid": "IP|212.192.216.55"
                        }
                    ]
                }
            },
            "first_observed": "2022-03-30T11:50:37.240Z",
            "last_observed": "2022-03-30T11:50:37.240Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}


```

