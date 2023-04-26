# OneLogin

This is a connector for searching OneLogin events. 

## Supported STIX Mappings

See the [table of mappings](onelogin_supported_stix.md) for the STIX objects and operators supported by this connector.

### Format for making STIX translation calls via the CLI

`python main.py <translator_module> <query or result> <STIX identity object> <data>`

Note the STIX identity object is only used when translating data source results into STIX, so it can be passed in as an empty object for query translation calls.

### Converting from STIX patterns to OneLogin queries

This example input pattern for TRANSLATE:

`python main.py translate onelogin query '{}' "[user-account:user_id= '123456']"`

Returns the following search query:

```
{
    "queries": [
        "user_id=123456&limit=1000"
    ]
}
```

### Converting from OneLogin events to STIX

OneLogin data to STIX mapping is defined in `to_stix_map.json`

This example OneLogin data:

`python main.py translate onelogin results '{"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "Onelogin", "identity_class": "events"}' '[{
            "id": 81004691744,
            "created_at": "2021-06-22T13:12:06.437Z",
            "account_id": 192204,
            "user_id": 138593517,
            "event_type_id": 149,
            "notes": "Default",
            "ipaddr": "121.0.0.1",
            "actor_user_id": 12345,
            "assuming_acting_user_id": 12345,
            "role_id": 441778,
            "app_id": "Default",
            "group_id": "Default",
            "otp_device_id": "Default",
            "policy_id": 123,
            "actor_system": "Mapping",
            "custom_message": "Default",
            "role_name": "Default",
            "app_name": "Default",
            "group_name": "Default",
            "actor_user_name": "Mapping",
            "user_name": "Firstname Lastname",
            "policy_name": "policy_name",
            "otp_device_name": "Default",
            "operation_name": "Default",
            "directory_sync_run_id": "Default",
            "directory_id": 12345678,
            "resolution": "resolution",
            "client_id": 12345678,
            "resource_type_id": "Default",
            "error_description": "error_description",
            "proxy_ip": "121.0.0.1",
            "risk_score": 2,
            "risk_reasons": "risk_reasons",
            "risk_cookie_id": 123,
            "browser_fingerprint": true
        }]'`

Will return the following STIX observable:

```json
{
    "type": "bundle",
    "id": "bundle--7fd7d3ac-dbdc-4f31-804f-1f8726a86910",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "name": "Onelogin",
            "identity_class": "events"
        },
        {
            "id": "observed-data--83a85c38-b086-499a-b28f-ecaea0938695",
            "type": "observed-data",
            "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
            "created": "2021-08-05T15:09:47.341Z",
            "modified": "2021-08-05T15:09:47.341Z",
            "objects": {
                "0": {
                    "type": "x-onelogin-finding",
                    "unique_id": 81004691744,
                    "event_type_id": 149,
                    "notes": "Default",
                    "role_id": 441778,
                    "app_id": "Default",
                    "custom_message": "Default",
                    "role_name": "Default",
                    "app_name": "Default",
                    "group_name": "Default",
                    "otp_device_name": "Default",
                    "operation_name": "Default",
                    "directory_sync_run_id": "Default",
                    "directory_id": 12345678,
                    "resolution": "resolution",
                    "client_id": 12345678,
                    "resource_type_id": "Default",
                    "proxy_ip": "121.0.0.2",
                    "browser_fingerprint": true
                },
                "1": {
                    "type": "x-ibm-finding",
                    "time_observed": "2021-06-22T13:12:06.437Z",
                    "policy_id": 123,
                    "name": "policy_name"
                },
                "2": {
                    "type": "user-account",
                    "x_account_id": 192204,
                    "user_id": "138593517",
                    "x_actor_user_id": 12345,
                    "x_assuming_acting_user_id": 12345,
                    "x_actor_user_name": "Mapping",
                    "display_name": "Firstname Lastname"
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "121.0.0.1"
                },
                "4": {
                    "type": "x-onelogin-risk",
                    "error_description": "error_description",
                    "risk_score": 2,
                    "risk_reasons": "risk_reasons",
                    "risk_cookie_id": 123
                }
            },
            "first_observed": "2021-08-05T15:09:47.341Z",
            "last_observed": "2021-08-05T15:09:47.341Z",
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
python main.py transmit onelogin '{ "region": <region> }' '{ "auth": { "clientId": <clientId>, "clientSecret": <clientSecret>}}' ping
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
python main.py transmit onelogin '{ "region": <region> }' '{ "auth": { "clientId": <clientId>, "clientSecret": <clientSecret>}}' results "user_id=12345678&limit=50" <OFFSET> <LENGTH> 
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