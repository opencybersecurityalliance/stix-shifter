# IBM Security Verify Privilege Vault

REST Web Service APIs: https://www.ibm.com/support/pages/node/1136272

### Format for making STIX translation calls via the CLI

`python3 main.py <translator_module> <query or result> <STIX identity object> <data>`

This example input pattern:

'python3 main.py translate "secretserver" query '{}' "[x-ibm-finding:name LIKE '%'] START t'2019-01-28T12:24:01.009Z' STOP t'2021-07-14T12:54:01.009Z'"'

will return
```
{
    "queries": [
        "SELECT * FROM SecretEventDetail WHERE EventSubject LIKE '%%%' START t'2019-01-28T12:24:01.009Z' STOP t'2021-07-14T12:54:01.009Z'"
    ]
}
```
## Converting from IBM Security Verify Privilege Vault events STIX

IBM Security Verify Privilege Vault data to STIX mapping is defined in `to_stix_map.json`

This example IBM Security Verify Privilege Vault data:

python3 main.py transmit secretserver '{"host":"<hostname>"}' '{"auth":{"username":"<username>","password":"<password>"}}' results "eyJxdWVyeSI6ICJTRUxFQ1QgKiBGUk9NIFNlY3JldEV2ZW50RGV0YWlsIFdIRVJFIEV2ZW50U3ViamVjdCBMSUtFICclJSUnIFNUQVJUIHQnMjAxOS0wMS0yOFQxMjoyNDowMS4wMDlaJyBTVE9QIHQnMjAyMS0wNy0xNFQxMjo1NDowMS4wMDlaJyIsICJ0YXJnZXQiIDogImh0dHA6Ly85LjQ2Ljg2LjEyMC9TZWNyZXRTZXJ2ZXIvb2F1dGgyL3Rva2VuIn0=" 1 2

Will return the following STIX observable:
   {
    "success": true,
    "data": [
        {
            "ItemId": 3,
            "SecretName": "MySql_130",
            "EventTime": "2021-07-06T02:56:58.413",
            "UserId": 5,
            "EventSubject": "[[SecretServer]] [Secret] MySql_130 [Check Out] by New",
            "EventNote": "[[SecretServer]]\r\nEvent: [Secret]\r\nAction: [Check Out]\r\nBy User: New\r\nItem Name: MySql_130 
            (Item Id: 3)\r\n",
            "EventDetails": "",
            "IpAddress": "127.0.0.1",
            "username": "New",
            "Server": "9.202.181.130"
        }
        ]
        }

python3 main.py execute secretserver secretserver '{"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "secretserver", "identity_class": "system"}' '{"host":"<hostname>"}' '{"auth":{"username":"<username>","password":"<password>"}}' "[x-ibm-finding:name LIKE '%'] START t'2019-01-28T12:24:01.009Z' STOP t'2021-07-14T12:54:01.009Z'"



```json
{
    "type": "bundle",
    "id": "bundle--a1bdc9c3-95e4-4224-853c-34c754306b48",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "secretserver",
            "identity_class": "system"
        },
        {
            "id": "observed-data--fec7b914-ead6-4fa4-a3a0-2a56e4ea1471",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2021-07-26T11:13:25.494Z",
            "modified": "2021-07-26T11:13:25.494Z",
            "objects": {
                "0": {
                    "type": "x-secretserver",
                    "ItemId": 3,
                    "UserId": 5
                },
                "1": {
                    "type": "x-ibm-finding",
                    "secret_name": "MySql_130",
                    "event_occurrence": "2021-07-06T02:56:58.413",
                    "name": "[[SecretServer]] [Secret] MySql_130 [Check Out] by New",
                    "description": "[[SecretServer]]\r\nEvent: [Secret]\r\nAction: [Check Out]\r\nBy User: New\r\nItem Name: MySql_130 (Item Id: 3)\r\n",
                    "user_name": "New"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "127.0.0.1"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "9.202.181.130"
                }
            },
            "first_observed": "2021-07-26T11:13:25.494Z",
            "last_observed": "2021-07-26T11:13:25.494Z",
            "number_observed": 1
        }
        ]
}

```
