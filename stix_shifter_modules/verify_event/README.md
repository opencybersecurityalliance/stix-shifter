# IBM Security Verify

This is a connector for searching IBM Security Verify events. 

### Prerequisite
install IBMSecurity app mentioned in requirement.txt
pip install -r requirements.txt

### Format for making STIX translation calls via the CLI

`python main.py <translator_module> <query or result> <STIX identity object> <data>`

Note the STIX identity object is only used when translating data source results into STIX, so it can be passed in as an empty object for query translation calls.

### Converting from STIX patterns to verify_event queries

This example input pattern for TRANSLATE:

'
    python main.py translate verify_event query "{}" "[x-oca-event:category='sso']"
'
Returns the following search query:

```
{
   "queries": [
        "event_type=\"sso\"&limit=10000"
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
python main.py transmit verify_event  '{ "host": "<Host Name>" }' '{ "auth": { "clientId": "<client-Id", "clientSecret": "<token"}}' ping

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
'{ "host": "<Host Name>" }' '{ "auth": { "clientId": "<client-Id", "clientSecret": "<token>"}}' results "event_type=\"sso\"&limit=10000" 0 10
```
Returns following result
```
STIX Results: 
{
   "type": "bundle",
   "id": "bundle--51b0b02a-cafa-4109-813b-5822c0f83b69",
   "objects": [
       {
           "type": "identity",
           "id": "32a23267-52fb-4e82-859b-0a15d6a2d334",
           "name": "verify_event",
           "identity_class": "events"
       },
       {
           "id": "observed-data--11f971c9-8781-4ec0-9017-819340f4d7fb",
           "type": "observed-data",
           "created_by_ref": "32a23267-52fb-4e82-859b-0a15d6a2d334",
           "created": "2021-11-22T06:10:42.596Z",
           "modified": "2021-11-22T06:10:42.596Z",
           "objects": {
               "0": {
                   "type": "x-verify",
                   "continent_name": "Europe",
                   "country_iso_code": "PL",
                   "ip": "<ipadd>",
                   "country_name": "Poland",
                   "result": "success",
                   "subtype": "user_password",
                   "subject": "609000ALKP",
                   "origin": "<ipadd>",
                   "cause": "Authentication Successful",
                   "action": "login",
                   "sourcetype": "clouddirectory",
                   "realm": "cloudIdentityRealm",
                   "devicetype": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
                   "target": "https://<Host Name>/oidc/endpoint/default/authorize?qsId=2919eda7-e114-48b3-b18c-3ed58914b157&client_id=usc-client",
                   "username": "<username>",
                   "year": 2021,
                   "event_type": "authentication",
                   "month": 11,
                   "indexed_at": 1637515371578,
                   "@processing_time": 161,
                   "tenantid": <uuid>,
                   "tenantname": <tenantname>,
                   "correlationid": "",
                   "servicename": "authsvc",
                   "id": <uuid>,
                   "time": 1637515371417,
                   "day": 21
               }
           },
           "first_observed": "2021-11-22T06:10:42.596Z",
           "last_observed": "2021-11-22T06:10:42.596Z",
           "number_observed": 1
       }
   "spec_version": "2.0"
}
```

## Mapping
    Example to pass query for event data ** [eventy_type:value='authentication']
    Example to pass query for event data ** [ipv4-addr:value='129.41.59.13']

