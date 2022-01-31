# Verify

This is a connector for searching IBM Verify events. 

### Format for making STIX translation calls via the CLI

`python main.py <translator_module> <query or result> <STIX identity object> <data>`

Note the STIX identity object is only used when translating data source results into STIX, so it can be passed in as an empty object for query translation calls.

### Converting from STIX patterns to verify_event queries

This example input pattern for TRANSLATE:

python main.py translate verify query "{}" "[x-oca-event:category='sso']"'
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
python main.py transmit verify  '{ "host": "<Host Name>" }' '{ "auth": { "clientId": "<client-Id", "clientSecret": "<token"}}' ping

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

python main.py transmit verify '{ "host": "<Host Name>" }' '{ "auth": { "clientId": "<client-Id", "clientSecret": "<token>"}}' results "event_type=\"authentication\"&limit=10000" 0 10
```
Returns JSON response data from verify
```
### Execute 
python main.py execute verify verify '{"type": "identity","id": "<identity Id>","name":"verify","identity_class":"events"}' '{ }' '{ "host": "<Host Name>" }' '{ "auth": { "clientId": "<client-Id", "clientSecret": "<token>"}}' "[x-oca-event:category = 'sso' AND x-oca-event:category = 'authentication']"

'''
  Return stix format data 
'''

