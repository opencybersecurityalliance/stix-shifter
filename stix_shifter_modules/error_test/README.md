# Error Test

### How to use

To create an error test connector it just requires the same values as you would a stix_bundle connector, with a couple small changes. For example if you wanted to create a stix_bundle connector, the following connections and configurations would be valid:

Connection:
```
{
    "description": "teststix bundle",
    "url": "https://raw.github.com/IBM/stix-shifter/master/data/cybox/1.json",
    "name": "test stix bundle",
    "type": "stix_bundle",
    "class": "udi"
}
```

Configuration:
```
{
    "connectionId": "<connection-id>",
    "name": "test name",
    "description": "test description",
    "type": "stix_bundle",
    "class": "udi",
    "acl": {
        "users": [
            {"id": "test.user", "role": "owner"}
        ]
    }
}
```

If you wanted to create an error_test connector you could instead use the following Connection/Configurations:
Connection:
```
{
    "description": "test connector",
    "url": "https://raw.github.com/IBM/stix-shifter/master/data/cybox/1.json",
    "name": "test error connector",
    "type": "error_test",
    "class": "udi",
    "options": {
        "error_type": "transform_exception"
    }
}
```

Configuration:
```
{
    "connectionId": "<connection-id>",
    "name": "test name",
    "description": "test description",
    "type": "error_test",
    "class": "udi",
    "acl": {
        "users": [
            {"id": "test.user", "role": "owner"}
        ]
    }
}
```

As long as `error_test` is the type and you pass in one of the folloing `error_types` in the connection options:

- `transform_exception` If you want to test an exception occuring during the query transformation of stix-shifter
- `translate_exception` If you want to test an exception occuring during the translation of results in stix-shifter
- `timeout` If you want to test a timeout error connecting to a datasource
- `bad_connection` If you want to test an error during the connection of a datasource (bad url, credentials, etc)


Example of error_test transmission:
```
python main.py transmit error_test '{"host":"https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/data/cybox/1.json", "options" : {"error_type" : "bad_connection"}}' '{}' results "[ipv4-addr:value = '127.0.0.1']" 0 9
```

Example of error_test translate:
```
python main.py translate error_test query '{}' "[ipv4-addr:value = '127.0.0.1']" '{"options": {"error_type": "translate_exception"}}'
```