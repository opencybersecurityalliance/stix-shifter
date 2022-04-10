# IBM Security Verify

This is a connector for searching IBM Security Verify events. Connector uses stix-patterns and IBM event verify REST API to make a convert and execute the qurey.

* To know more about IBM Security Verify API refer to the [API Reference](https://docs.verify.ibm.com/verify/reference/getallevents)
* Connector uses the stix schema defined as per [stix-extension/stix2.0/x-oca-event](https://github.ibm.com/IBM-Security-STIX/stix-extensions/blob/verify/STIX%202.0/x-oca-event.md)
* Connector supports ` Equal, AND, IN ` stix operations
* Possible event types are ` sso,authentication,management,risk,adaptive_risk `

### Some of Stix pattern examples
 
 * Event type   `[x-oca-event:category='authentication']`
 * IPv4-Addr    `[ ipv4-addr:value IN ('192.168.1.1', '192.168.1.2', '192.168.1.3') ]"`
 * oca-event    `[x-oca-event:extensions.'x-iam-ext'.application_name='Bane']`
`
`

### Format for making STIX translation calls via the CLI

`python main.py <translator_module> <query or result> <STIX identity object> <data>
`

### Converting from STIX patterns to verify_event queries

CLI example of stix input pattern for TRANSLATE


`
 python main.py translate ibm_security_verify query "{}" "[x-oca-event:category='sso']" 
`

Returns the following search query:

`
 {
    "queries": [
        "event_type=\"sso\"&limit=10000"
    ]
 }
`

### Transmit functions

Transmit offers several functions: ping, query, results and execute.
### Ping
Uses the data source API to ping the connection.


`
python main.py transmit ibm_security_verify  '{ "host": "<Host Name>","port" :<port>}' '{ "auth": { "clientId": "<client-Id>, "clientSecret": "<token>"}}' ping
`

If connection is established, Connector will return the following response: 

`
{
    "success": true
}
`
### Results

Uses the data source API to fetch the query results based on the search ID, offset, and length.

CLI Command 

`
python main.py transmit ibm_security_verify '{ "host": "<Host Name>" ,"port" :<port>}' '{ "auth": { "clientId": "<client-Id>, "clientSecret": "<token>"}}' 
`

Response

`
{
    "success": true,
    "search_id": "event_type=\"sso\"&limit=10000"
}
`

### Execute 

```
python main.py execute ibm_security_verify ibm_security_verify '{"type": "identity","id": "<identity Id>","name":"verify","identity_class":"events"}' '{ }' '{ "host": "<Host Name>" ,"port" :<port>}' '{ "auth": { "clientId": "<client-Id>, "clientSecret": "<token>"}}' "[x-oca-event:category = 'sso']"
```

Response object

```json
{
    "type": "bundle",
    "id": "bundle--65fc22ff-0063-4afc-a61e-b9b50c0b1e18",
    "objects": [
        {
            "type": "identity",
            "id": "32a23267-52fb-4e82-859b-0a15d6a2d334",
            "name": "verify",
            "identity_class": "events"
        },
        {
            "id": "observed-data--63964544-6b66-4673-ad37-bbeab66d328d",
            "type": "observed-data",
            "created_by_ref": "32a23267-52fb-4e82-859b-0a15d6a2d334",
            "created": "2022-02-17T07:33:21.969Z",
            "modified": "2022-02-17T07:33:21.969Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "extensions": {
                        "x-iam-ext": {
                            "continent_name": "Asia",
                            "city_name": "mumbai",
                            "country_iso_code": "IN",
                            "country_name": "India",
                            "subcategory": "saml",
                            "provider_id": "http://ibm.com",
                            "realm": "www.google.com",
                            "application_id": "6773634223410562472",
                            "application_type": "Custom Application",
                            "browser_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36",
                            "applicationname": "Bane"
                        }
                    },
                    "ip_refs": [
                        "1"
                    ],
                    "outcome": "success",
                    "user_ref": "2",
                    "category": "sso",
                    "provider": "IBM Security Verify IAM",
                    "domain_ref": "3",
                    "module": "saml_runtime",
                    "created": "2022-02-17T07:31:38.824Z"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "192.168.1.1"
                },
                "2": {
                    "type": "user-account",
                    "user_id": "123456"
                },
                "3": {
                    "type": "domain-name",
                    "value": "ibmcloud.com"
                }
            },
            "first_observed": "2022-02-17T07:33:21.969Z",
            "last_observed": "2022-02-17T07:33:21.969Z",
            "number_observed": 1
        }
}
```

