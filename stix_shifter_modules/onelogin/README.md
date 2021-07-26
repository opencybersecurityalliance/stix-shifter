# OneLogin

This is a connector for searching Onelogin events. 

### Format for making STIX translation calls via the CLI

`python main.py <translator_module> <query or result> <STIX identity object> <data>`

Note the identity object is only used when converting from AQL to STIX, but due to positional arguments, an empty hash will need to be passed in when converting from STIX patterns to AQL.

This example input pattern for TRANSLATE:

`python main.py translate "onelogin" "query" '{}' "[user-account:user_id= '123456']"`

Returns the following search query:

```
{
    "queries": [
        "user_id=123456&limit=50"
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
python3 main.py transmit onelogin '{ "host": <Onelogin_host>, "port": 443, "selfSignedCert": false}' '{ "auth": { "clientId": <clientId>, "clientSecret": <clientSecret>}}' ping
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
python3 main.py transmit onelogin '{ "host": <Onelogin_host>, "port": 443, "selfSignedCert": false}' '{ "auth": { "clientId": <clientId>, "clientSecret": <clientSecret>}}' results "user_id=12345678&limit=50" <OFFSET> <LENGTH> 
```
Returns following result
```
{
    "success": true,
    "data": [
        {
            "id": <id>,
            "created_at": "2021-06-22T13:12:06.437Z",
            "account_id": <account_id>,
            "user_id": 12345678,
            "event_type_id": <event_type_id>,
            "notes": <notes>,
            "ipaddr": "<ipaddr>",
            "actor_user_id": <actor_user_id>,
            "assuming_acting_user_id": <assuming_acting_user_id>,
            "role_id": <role_id>,
            "app_id": <app_id>,
            "group_id": <group_id>,
            "otp_device_id": <otp_device_id>,
            "policy_id": <policy_id>,
            "actor_system": "Mapping",
            "custom_message": null,
            "role_name": "Default",
            "app_name": null,
            "group_name": null,
            "actor_user_name": "Mapping",
            "user_name": "<user_name>",
            "policy_name": null,
            "otp_device_name": null,
            "operation_name": null,
            "directory_sync_run_id": null,
            "directory_id": null,
            "resolution": null,
            "client_id": null,
            "resource_type_id": null,
            "error_description": null,
            "proxy_ip": <proxy_ip>,
            "risk_score": <risk_score>,
            "risk_reasons": null,
            "risk_cookie_id": <risk_cookie_id>,
            "browser_fingerprint": null
        }
    ]
}
```