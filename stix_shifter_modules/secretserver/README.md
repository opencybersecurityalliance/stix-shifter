# IBM Security Verify Privilege Vault

## Supported STIX Mappings

See the [table of mappings](secretserver_supported_stix.md) for the STIX objects and operators supported by this connector.

### API Endpoints

REST Web Service APIs: https://www.ibm.com/support/pages/node/1136272

### Prerequisite

Create custom report on IBM Privilege Vault Secret Server/ Delinea Secret Server by using following steps:
- Login to  IBM Privilege Vault Secret Server/ Delinea Secret Server.
- Click on Report tab. 
- Fill the details as below and click the save button. 


|        |        |
|-------------|-------------|
| Report Name         | Secret Server Events Logs |       
| Report Description  | Secret Server Events Logs |
| Report Category     | Activity                  |
| Chart Type          | None                      |
| Page Size           | 15                        |
| Report SQL          | SELECT a.EventDetails AS [EventDetails],a.EventNote,a.EventTime,a.ItemId,a.UserId,u.UserName as Name, u.EmailAddress as Unique_Identtification,a.EventSubject, s.secretname As [SecretName], a.ipaddress AS [IpAddress] FROM tbEventAudit a WITH (NOLOCK) INNER JOIN tbuser u WITH (NOLOCK) ON u.userid = a.userid INNER JOIN tbsecret s WITH (NOLOCK) ON s.secretid = a.ItemId  WHERE a.EventTime >= #StartDate AND a.EventTime <= #EndDate ORDER BY a.EventTime DESC
     
-	New custom report will get listed in General section of Reports tab.
 

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

Note: For on Prem IBM Privilege Vault Secret Server Instace "host":"<hostname/SecretServer>" 
      example: "host":"X.XX.XX.XXX/SecretServer"

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
 These are examples of supported queries for secret server conncetor:

1. "[x-ibm-finding:event_name LIKE '%'] START t'2022-09-14T11:27:00.000Z' STOP t'2022-09-16T11:32:00.000Z'"
2. "[x-ibm-finding:time_observed LIKE '%'] START t'2022-09-14T11:27:00.000Z' STOP t'2022-09-16T11:32:00.000Z'"
3. “[x-secret:secret_name LIKE '%'] START t'2022-09-14T11:27:00.000Z' STOP t'2022-09-16T11:32:00.000Z'"
4. “[ipv4-addr:value LIKE '%'] START t'2022-09-14T11:27:00.000Z' STOP t'2022-09-16T11:32:00.000Z'"
