# Sumologic

Connector to load events from SumoLogic

## Supported STIX Mappings

See the [table of mappings](sumologic_supported_stix.md) for the STIX objects and operators supported by this connector.

### SumoLogic API endpoints

Ping Endpoint: `https://api.<region>.sumologic.com/api/collectors`

Search Endpoint: `https://api.sumologic.com/api/v1/search/jobs`

Result Endpoint: `https://api.sumologic.com/api/v1/search/jobs/<SEARCH_JOB_ID>/messages?offset=<OFFSET>&limit=<LIMIT>`

##### Reference

[SumoLogic Search Job API](https://help.sumologic.com/APIs/Search-Job-API/About-the-Search-Job-API)

## Dialects

The connector supports two dialects: the default one and [the cloud_siem one](https://help.sumologic.com/docs/cse/get-started-with-cloud-siem/insight-generation-process/#entities-in-messages-are-mapped-to-entity-type-schema-attributes)

### Format for making STIX translation calls via the CLI

`python main.py <translator_module> <query or result> <STIX identity object> <data>`

Note the STIX identity object is only used when translating data source results into STIX, so it can be passed in as an
empty object for query translation calls.

## Translate

This example input pattern:

```
python main.py translate sumologic query {} "[domain-name:value='sumologic.domain.com'] START t'2021-09-01T00:00:00.000Z' STOP t'2021-09-08T19:00:00.000Z'"
```

Returns the following AQL query:

```
"{'query': '(_sourcehost = \"sumologic.domain.com\")','fromTime': '20210901T000000','toTime': '20210908T190000'}"
```

## Transmit

### Transmit functions

Transmit offers several functions: ping, query, results and is_async.

### Ping

Uses the data source API to ping the connection

CLI command example:

```
python main.py transmit sumologic '{"region": <region>}' '{"auth": {"access_id": <access_id>, "access_key": <access_key>}}' ping
```

If connection establish returns the following response:

```
{
    "success": true
}
```

### Query

Queries the data source API with the translated query and returns the search id

CLI command example:

```
python main.py transmit sumologic '{"region": <region>}' '{"auth": {"access_id": <access_id>, "access_key": <access_key>}}' query '{"query": "(_sourcehost = \"sumologic.domain.com\")", "fromTime": "20210901T000000", "toTime": "20210927T190000"}'
```

If successful, will return the following response:

```
{
    "success": true,
    "search_id": <search_id>
}
```

### Results

Returns the result of a search using the search id provided from the response of the previous command.

CLI command example:

```
python main.py transmit sumologic '{"region": <region>}' '{"auth": {"access_id": <access_id>, "access_key": <access_key>}}' results <search_id> 0 5
```

If successful, will return the following response:

```json
{
  "success": true,
  "data": [
    {
      "_blockid": "921277042830107648",
      "_messagetime": "1632768971000",
      "_raw": "Sep 27 18:56:11 sumologic nm-dispatcher: req:1 'dhcp4-change' [eth0]: start running ordered scripts...",
      "_collectorid": "100695732",
      "_sourceid": "103458456",
      "_collector": "sumologic.domain.com",
      "_messagecount": "16",
      "_sourcehost": "sumologic.domain.com",
      "_messageid": "921277042813330448",
      "_sourcename": "/var/log/messages",
      "_size": "102",
      "_view": "",
      "_receipttime": "1632749174377",
      "_sourcecategory": "linux/system",
      "_format": "t:cache:o:0:l:15:p:MMM dd HH:mm:ss",
      "_source": "Linux System_3",
      "firstName": "FirstName",
      "lastName": "LastName",
      "email": "firstname.lastname@domain.com",
      "roleIds": [
        "000000000002E875"
      ],
      "createdAt": "2021-09-23T11:34:07.255Z",
      "createdBy": "FFFFFFFFFFFFFD66",
      "modifiedAt": "2021-10-08T10:14:34.911Z",
      "modifiedBy": "000000000001F46E",
      "id": "000000000001F46E",
      "isActive": true,
      "isLocked": false,
      "isMfaEnabled": false,
      "lastLoginTimestamp": "2021-10-08T10:14:34.902Z",
      "displayName": "FirstName LastName"
    }
  ]
}
```

### Execute

This command executes translation and transmission of the query to the data source and returns STIX Observable mappings
defined in the `to_stix_map.json` file.

```
python main.py execute sumologic sumologic '{"type": "identity","id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name": "sumologic","identity_class": "events"}' '{"region": <region> '{"auth": {"access_id": <access_id>, "access_key": <access_key> "[domain-name:value='sumologic.domain.com'] START t'2021-09-01T00:00:00.000Z' STOP t'2021-09-26T10:16:00.000Z'"
```

If successful, will return the following response

```
{
  "queries": [
    "{'query': '(_sourcehost = \"sumologic.domain.com\")','fromTime': '20210901T000000','toTime': '20210926T101600'}"
  ]
}
 2021-10-19 18:26:31,734 stix_shifter.scripts.stix_shifter INFO     STIX Results: 
{
  "type": "bundle",
  "id": "bundle--beedba86-7d24-49be-b394-27b8b1cbb5fe",
  "objects": [
    {
      "type": "identity",
      "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
      "name": "sumologic",
      "identity_class": "events"
    },
    {
      "id": "observed-data--1d0dc2a5-b3a1-4992-b232-5662b5e8e5cc",
      "type": "observed-data",
      "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
      "created": "2021-10-19T12:56:31.732Z",
      "modified": "2021-10-19T12:56:31.732Z",
      "objects": {
        "0": {
          "type": "x-oca-event",
          "created": "2021-09-26T10:12:40.000Z",
          "original_ref": "2",
          "agent": "sumologic.domain.com",
          "domain_ref": "4",
          "code": "919300499030345744",
          "provider": "linux/system",
          "module": "Linux System_3",
          "user_ref": "5"
        },
        "1": {
          "type": "x-ibm-finding",
          "time_observed": "2021-09-26T10:12:40.000Z",
          "src_device": "sumologic.domain.com",
          "event_count": 16,
          "start": "2021-09-26T04:42:44.565Z"
        },
        "2": {
          "type": "artifact",
          "payload_bin": "U2VwIDI2IDEwOjEyOjQwIHN1bW9sb2dpYyBubS1kaXNwYXRjaGVyOiByZXE6MSAnZGhjcDQtY2hhbmdlJyBbZXRoMF06IHN0YXJ0IHJ1bm5pbmcgb3JkZXJlZCBzY3JpcHRzLi4u"
        },
        "3": {
          "type": "x-sumologic-source",
          "collectorid": "100695732",
          "sourcename": "/var/log/messages"
        },
        "4": {
          "type": "domain-name",
          "value": "sumologic.domain.com"
        },
        "5": {
          "type": "user-account",
          "account_login": "firstname.lastname@domain.com",
          "account_created": "2021-09-23T11:34:07.255Z",
          "user_id": "000000000001F46E",
          "account_last_login": "2021-10-18T17:28:55.324Z",
          "display_name": "FirstName LastName"
        }
      },
      "first_observed": "2021-09-26T10:12:40.000Z",
      "last_observed": "2021-09-26T10:12:40.000Z",
      "number_observed": 16
    }
  ],
  "spec_version": "2.0"
}
```

### Delete

This command deletes the results of a particular search id.

```
python main.py transmit sumologic '{"region": <region>}' '{"auth": {"access_id": <access_id>, "access_key": <access_key>}}' delete <search_id>
```

If successful, will return the following:

```
{
    "success": true
}
```

## Converting from SumoLogic events to STIX

SumoLogic data to STIX mapping is defined in `to_stix_map.json`

This example SumoLogic data:

```
python main.py translate sumologic results '{"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "SumoLogic", "identity_class": "events"}' '[{"_blockid": "921277042830107648", "_messagetime": "1632768971000", "_raw": "Sep 27 18:56:11 sumologic NetworkManager[677]: <info>  [1632749171.2911] dhcp4 (eth0):   nameserver <ip_ad>", "_collectorid": "100695732", "_sourceid": "103458456", "_collector": "sumologic.domain.com", "_messagecount": "7", "_sourcehost": "sumologic.domain.com", "_messageid": "921277042813330439", "_sourcename": "/var/log/messages", "_size": "115", "_view": "", "_receipttime": "1632749174377", "_sourcecategory": "linux/system", "_format": "t:cache:o:0:l:15:p:MMM dd HH:mm:ss", "_source": "Linux System_3", "id": "000000000001F46E", "email": "firstname.lastname@domain.com", "displayName": "FirstName LastName", "createdAt": "2021-09-23T11:34:07.255Z", "lastLoginTimestamp": "2021-09-28T08:34:34.952Z"}]'
```

Will return the following STIX observable:

```json
{
  "type": "bundle",
  "id": "bundle--37626475-ac17-419b-a767-bfb97929f077",
  "objects": [
    {
      "type": "identity",
      "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
      "name": "SumoLogic",
      "identity_class": "events"
    },
    {
      "id": "observed-data--318f2b23-ac9a-43fa-9d5b-2e064f8dfb7b",
      "type": "observed-data",
      "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
      "created": "2021-10-18T13:42:16.029Z",
      "modified": "2021-10-18T13:42:16.029Z",
      "objects": {
        "0": {
          "type": "x-oca-event",
          "created": "2021-09-27T18:56:11.000Z",
          "original_ref": "2",
          "agent": "sumologic.domain.com",
          "domain_ref": "4",
          "code": "921277042813330439",
          "provider": "linux/system",
          "module": "Linux System_3",
          "user_ref": "5"
        },
        "1": {
          "type": "x-ibm-finding",
          "time_observed": "2021-09-27T18:56:11.000Z",
          "src_device": "sumologic.domain.com",
          "event_count": 7,
          "start": "2021-09-27T13:26:14.377Z"
        },
        "2": {
          "type": "artifact",
          "payload_bin": "U2VwIDI3IDE4OjU2OjExIHN1bW9sb2dpYyBOZXR3b3JrTWFuYWdlcls2NzddOiA8aW5mbz4gIFsxNjMyNzQ5MTcxLjI5MTFdIGRoY3A0IChldGgwKTogICBuYW1lc2VydmVyIDxpcF9hZD4="
        },
        "3": {
          "type": "x-sumologic-source",
          "collectorid": "100695732",
          "sourcename": "/var/log/messages"
        },
        "4": {
          "type": "domain-name",
          "value": "sumologic.domain.com"
        },
        "5": {
          "type": "user-account",
          "user_id": "000000000001F46E",
          "account_login": "firstname.lastname@domain.com",
          "display_name": "FirstName LastName",
          "account_created": "2021-09-23T11:34:07.255Z",
          "account_last_login": "2021-09-28T08:34:34.952Z"
        }
      },
      "first_observed": "2021-09-27T18:56:11.000Z",
      "last_observed": "2021-09-27T18:56:11.000Z",
      "number_observed": 7
    }
  ],
  "spec_version": "2.0"
}
```
