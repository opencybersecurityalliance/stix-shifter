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
python main.py translate trustar query '{}' "[x-trustar:x_searchTerm = '9.30.116.81']"


will return
# NOTE - if from/to is not provided, defaults to past 5 minutes
```
{
    "queries": [
        "{\"searchTerm\": \"9.30.116.81\", \"from\": 1631680282000, \"to\": 1631680582000}"
    ]
}
```
## Converting from Secret Server events STIX

### Transmission Call:

```

python main.py transmit trustar '{"host": "api.trustar.co", "port": 443}' '{"auth": {"username":"", "password": ""}}' results '["{\"searchTerm\": \"9.30.116.81\", \"from\": 1631680282000, \"to\": 1631680582000}"]' 0 1


```
Returns:

```
{
    "success": true,
    "data": [
        {
            "indicatorType": "IP",
            "value": "9.30.116.81",
            "priorityLevel": "NOT_FOUND",
            "firstSeen": 1630071439159,
            "lastSeen": 1630588132716,
            "guid": "IP|9.30.116.81",
            "IP": "9.30.116.81",
            "reports": [
                {
                    "id": "9ca88e1d-bd3c-412d-9e34-8db32dcc5540",
                    "created": 1630588132711,
                    "updated": 1630588132711,
                    "title": "QRadar Vulnerability Report",
                    "distributionType": "ENCLAVE",
                    "enclaveIds": [
                        "46d916e1-4e40-469d-b3df-d3b1d706a28d"
                    ]
                },
                {
                    "id": "a5e5895f-c1e9-4a80-9b1f-dabc4581e051",
                    "created": 1630577472499,
                    "updated": 1630577472499,
                    "title": "QRadar Authention Report",
                    "distributionType": "ENCLAVE",
                    "enclaveIds": [
                        "df82c00f-ec71-4910-8c1e-747292981571"
                    ]
                },
                {
                    "id": "3e17c2cd-bf6c-4808-8b08-573a9f1c8ddd",
                    "created": 1630071602240,
                    "updated": 1630321684919,
                    "title": "Asset Details-Qradar",
                    "distributionType": "ENCLAVE",
                    "enclaveIds": [
                        "7c42062e-060d-430d-9dcb-9a28031f71c4"
                    ]
                }
            ],
            "indicatorSummary": [],
            "meta": {
                "indicatorType": "IP",
                "value": "9.30.116.81",
                "correlationCount": 0,
                "priorityLevel": "NOT_FOUND",
                "noteCount": 0,
                "sightings": 5,
                "firstSeen": 1630071439159,
                "lastSeen": 1630588132716,
                "enclaveIds": [
                    "46d916e1-4e40-469d-b3df-d3b1d706a28d",
                    "7c42062e-060d-430d-9dcb-9a28031f71c4",
                    "df82c00f-ec71-4910-8c1e-747292981571"
                ],
                "tags": [
                    {
                        "guid": "119431b6-e75b-49fc-af8f-a87bdca93f8c",
                        "name": "offensetag2",
                        "enclaveId": "df82c00f-ec71-4910-8c1e-747292981571"
                    },
                    {
                        "guid": "ec53d371-3ff9-4cbd-87b8-907070a8bafd",
                        "name": "vatag1",
                        "enclaveId": "46d916e1-4e40-469d-b3df-d3b1d706a28d"
                    }
                ],
                "source": "",
                "notes": [],
                "guid": "IP|9.30.116.81"
            }
        }
    ]
}

```

Translation Call:

```
python main.py translate trustar results '{"type": "identity", "id": "identity--afwezcd-sfds-ssdfs-asdfsd3-asdf313", "name": "Trustar", "identity_class": "finding"}'  '[{
    "indicatorType": "IP",
            "value": "9.30.116.81",
            "priorityLevel": "NOT_FOUND",
            "firstSeen": 1630071439159,
            "lastSeen": 1630588132716,
            "guid": "IP|9.30.116.81",
            "IP": "9.30.116.81",
            "reports": [
                {
                    "id": "9ca88e1d-bd3c-412d-9e34-8db32dcc5540",
                    "created": 1630588132711,
                    "updated": 1630588132711,
                    "title": "QRadar Vulnerability Report",
                    "distributionType": "ENCLAVE",
                    "enclaveIds": [
                        "46d916e1-4e40-469d-b3df-d3b1d706a28d"
                    ]
                },
                {
                    "id": "a5e5895f-c1e9-4a80-9b1f-dabc4581e051",
                    "created": 1630577472499,
                    "updated": 1630577472499,
                    "title": "QRadar Authention Report",
                    "distributionType": "ENCLAVE",
                    "enclaveIds": [
                        "df82c00f-ec71-4910-8c1e-747292981571"
                    ]
                },
                {
                    "id": "3e17c2cd-bf6c-4808-8b08-573a9f1c8ddd",
                    "created": 1630071602240,
                    "updated": 1630321684919,
                    "title": "Asset Details-Qradar",
                    "distributionType": "ENCLAVE",
                    "enclaveIds": [
                        "7c42062e-060d-430d-9dcb-9a28031f71c4"
                    ]
                }
            ],
            "indicatorSummary": [],
            "meta": {
                "indicatorType": "IP",
                "value": "9.30.116.81",
                "correlationCount": 0,
                "priorityLevel": "NOT_FOUND",
                "noteCount": 0,
                "sightings": 5,
                "firstSeen": 1630071439159,
                "lastSeen": 1630588132716,
                "enclaveIds": [
                    "46d916e1-4e40-469d-b3df-d3b1d706a28d",
                    "7c42062e-060d-430d-9dcb-9a28031f71c4",
                    "df82c00f-ec71-4910-8c1e-747292981571"
                ],
                "tags": [
                    {
                        "guid": "119431b6-e75b-49fc-af8f-a87bdca93f8c",
                        "name": "offensetag2",
                        "enclaveId": "df82c00f-ec71-4910-8c1e-747292981571"
                    },
                    {
                        "guid": "ec53d371-3ff9-4cbd-87b8-907070a8bafd",
                        "name": "vatag1",
                        "enclaveId": "46d916e1-4e40-469d-b3df-d3b1d706a28d"
                    }
                ],
                "source": "",
                "notes": [],
                "guid": "IP|9.30.116.81"
            }

}]' '{"stix_validator":true}'

```

Return: 

```
{
    "type": "bundle",
    "id": "bundle--55589fbe-c2b6-4ca2-88f0-ecb7cab3444a",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--afwezcd-sfds-ssdfs-asdfsd3-asdf313",
            "name": "Trustar",
            "identity_class": "finding"
        },
        {
            "id": "observed-data--daca32c2-afd0-41e9-89b9-58fa26166803",
            "type": "observed-data",
            "created_by_ref": "identity--afwezcd-sfds-ssdfs-asdfsd3-asdf313",
            "created": "2021-09-15T00:38:27.379Z",
            "modified": "2021-09-15T00:38:27.379Z",
            "objects": {
                "0": {
                    "type": "x-trustar",
                    "x_prioritylevel": "NOT_FOUND",
                    "x_firstseen": "2021-08-27T13:37:19.159Z",
                    "x_lastseen": "2021-09-02T13:08:52.716Z",
                    "x_guid": "IP|9.30.116.81",
                    "x_report_details": [
                        {
                            "id": "9ca88e1d-bd3c-412d-9e34-8db32dcc5540",
                            "created": 1630588132711,
                            "updated": 1630588132711,
                            "title": "QRadar Vulnerability Report",
                            "distributionType": "ENCLAVE",
                            "enclaveIds": [
                                "46d916e1-4e40-469d-b3df-d3b1d706a28d"
                            ]
                        },
                        {
                            "id": "a5e5895f-c1e9-4a80-9b1f-dabc4581e051",
                            "created": 1630577472499,
                            "updated": 1630577472499,
                            "title": "QRadar Authention Report",
                            "distributionType": "ENCLAVE",
                            "enclaveIds": [
                                "df82c00f-ec71-4910-8c1e-747292981571"
                            ]
                        },
                        {
                            "id": "3e17c2cd-bf6c-4808-8b08-573a9f1c8ddd",
                            "created": 1630071602240,
                            "updated": 1630321684919,
                            "title": "Asset Details-Qradar",
                            "distributionType": "ENCLAVE",
                            "enclaveIds": [
                                "7c42062e-060d-430d-9dcb-9a28031f71c4"
                            ]
                        }
                    ],
                    "x_meta": {
                        "x_correlationCount": 0,
                        "x_noteCount": 0,
                        "x_sightings": 5,
                        "x_enclaveIds": [
                            "46d916e1-4e40-469d-b3df-d3b1d706a28d",
                            "7c42062e-060d-430d-9dcb-9a28031f71c4",
                            "df82c00f-ec71-4910-8c1e-747292981571"
                        ],
                        "x_tags": [
                            {
                                "guid": "119431b6-e75b-49fc-af8f-a87bdca93f8c",
                                "name": "offensetag2",
                                "enclaveId": "df82c00f-ec71-4910-8c1e-747292981571"
                            },
                            {
                                "guid": "ec53d371-3ff9-4cbd-87b8-907070a8bafd",
                                "name": "vatag1",
                                "enclaveId": "46d916e1-4e40-469d-b3df-d3b1d706a28d"
                            }
                        ]
                    }
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "9.30.116.81"
                }
            },
            "first_observed": "2021-09-15T00:38:27.379Z",
            "last_observed": "2021-09-15T00:38:27.379Z",
            "number_observed": 1
        }
    ]
}
```