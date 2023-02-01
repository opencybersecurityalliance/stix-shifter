# Use of custom mappings

Follow the below steps, if a user or threat hunter wants to use custom mapping after installing stix-shifter libraries:


1. Go to the standard python library installation location. The installation path usually looks like this ***lib/pythonX.Y/site-packages*** or go to https://docs.python.org/3/install/ for more details on the python library installation based on your system.

2. Go to the ***stix_shifter_modules*** folder and find the connector name that is installed.

3. Inside the connector folder, go to the ***config.json*** file found under the ***stix_shifter_modules/\<CONNECTOR\>/configuration/*** directory.

4. There is a `mapping` object nested inside the `options` JSON object. This includes all the mappings from the `from_stix` and `to_stix` mapping files. Here's an example of the `config.json` file:

```
{
    "connection": {
        "type": {
            "displayName": "MySQL",
            "group": "mysql",
            "type": "connectorType"
        },
        "options": {
            "mapping": {
                "type": "json",
                "optional": true,
                "previous": "connection.mapping",
                "default": {
                    "from_stix_map": {
                        "ipv4-addr": {
                            "fields": {
                                "value": [
                                    "source_ipaddr",
                                    "dest_ipaddr"
                                ]
                            }
                        },
                        "file": {
                            "fields": {
                                "name": [
                                    "filename"
                                ]
                            }
                        }
                    },
                    "operators": {
                        "ComparisonExpressionOperators.And": "AND",
                        "ComparisonExpressionOperators.Or": "OR"
                    },
                    "to_stix_map": {
                        "source_ipaddr": [
                            {
                                "key": "ipv4-addr.value",
                                "object": "src_ip"
                            },
                            {
                                "key": "network-traffic.src_ref",
                                "object": "nt",
                                "references": "src_ip"
                            }
                        ],
                        "dest_ipaddr": [
                            {
                                "key": "ipv4-addr.value",
                                "object": "dst_ip"
                            },
                            {
                                "key": "network-traffic.dst_ref",
                                "object": "nt",
                                "references": "dst_ip"
                            }
                        ]
                    }
                }
            }
        }
    },
    "configuration": {
        "auth": {
            "type": "fields",
            "username": {
                "type": "password"
            },
            "password": {
                "type": "password"
            }
        }
    }
}
```


5. You can change, update or use the existing custom mappings fields and save the file.

6. The stix-shifter CLI commands should automatically pick up your custom mappings in the next command execution.