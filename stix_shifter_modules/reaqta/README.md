#  ReaQta

Reaqta is an AI-powered, automated endpoint security platform. ReaQta Connector can be used to search security events and alerts generated in ReaQta platform.

## Supported STIX Mappings

See the [table of mappings](reaqta_supported_stix.md) for the STIX objects and operators supported by this connector.

## API and Query Language

Connector uses Reaqta Hunt API. Endpoint Path: `/1/events/hunt`

For search, the connector uses HunQ: The ReaQta-Hive Hunt Query Language. The query is similar to the WHERE clause of a SQL query.


### Format for making STIX translation calls via the CLI

`python main.py <translator_module> <query or result> <STIX identity object> <data>`

Note the identity object is only used when converting from HunQ response JSON to STIX, but due to positional arguments, an empty hash will need to be passed in when converting from STIX patterns to HunQ query.


## Converting from STIX patterns to HunQ queries

This example input pattern:

`python main.py translate reaqta query {} "[ipv4-addr:value = '192.168.1.2' OR network-traffic:src_port = 443] START t'2022-04-06T00:00:00.000Z' STOP t'2022-04-06T00:05:00.000Z'"`

Returns the following HunQ query:

`(eventdata.localPort = "443" OR (login.ip = "192.168.1.2" OR $ip = "192.168.1.2")) AND happenedAfter = "2022-04-06T00:00:00.000Z" AND happenedBefore = "2022-04-06T00:05:00.000Z"`


## Sending Query to Hunt API

This is a synchronous connector. Therefore, the connector can only uses results transmission call to send query to the API. Example results call:

```
python main.py transmit reaqta '{"host":"<reaqta_host>"}' '{ "auth": { "app_id": "<reaqta_app_id>", "secret_key": "<reaqta_secret_key>" } }' results '(eventdata.localPort = "443" OR (login.ip = "192.168.1.2" OR $ip = "192.168.138.128")) AND happenedAfter = "2022-04-06T00:00:00.000Z" AND happenedBefore = "2022-04-06T00:05:00.000Z"' 0 1
```

### Transmit Results Output

```
        {
            "eventId": "847102109500309505",
            "endpointId": "842028663686823936",
            "payload": {
                "localId": "847101972854081537",
                "process": {
                    "id": "842028663686823936:2222:1648564483636",
                    "parentId": "842028663686823936:1111:1648485432579",
                    "endpointId": "842028663686823936",
                    "program": {
                        "path": "c:\\users\\reaqta\\downloads\\test.exe",
                        "filename": "abcd.exe",
                        "md5": "d05807b758e56634abfdb7cd62798765",
                        "sha1": "adb328949df38cece2fc7ad818788d12ej311a9a90",
                        "sha256": "a4693a722a69bb5b58e02bd1b28369a123459047bd37bda4836b97a6a6c65432",
                        "size": 73802,
                        "arch": "x32",
                        "fsName": "test.exe"
                    },
                    "user": "DESKTOP-TEST\\ReaQta-test",
                    "pid": 2222,
                    "startTime": "2022-03-29T14:34:43.636Z",
                    "ppid": 1111,
                    "pstartTime": "2022-03-28T16:37:12.579Z",
                    "userSID": "S-1-1-11-00000000-1111111-222222222-9999",
                    "privilegeLevel": "MEDIUM",
                    "noGui": false,
                    "logonId": "0xxx1s1"
                },
                "incidents": [],
                "triggeredIncidents": [],
                "data": {
                    "addressFamily": 0,
                    "protocol": 0,
                    "localAddr": "192.168.1.2",
                    "localPort": 443,
                    "remoteAddr": "192.168.2.3",
                    "remotePort": 8443,
                    "outbound": true
                },
                "eventType": 8
            },
            "happenedAt": "2022-03-29T14:40:48.722Z",
            "receivedAt": "2022-03-29T14:41:21.301Z"
        }
```

##  ReaQta response results to STIX objects

### Translate command
``` 
python main.py translate reaqta results '{"type":"identity","id":"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff","name":"reaqta","identity_class":"events", "created": "2022-04-07T20:35:41.042Z", "modified": "2022-04-07T20:35:41.042Z"}' '[<Reaqta JSON response>]'
```
### STIX 2.0 Output

```
{
    "type": "bundle",
    "id": "bundle--bb93d310-7f24-4c02-8830-b1a34413cf67",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "reaqta",
            "identity_class": "events",
            "created": "2022-04-07T20:35:41.042Z",
            "modified": "2022-04-07T20:35:41.042Z"
        },
        {
            "id": "observed-data--85159562-3104-41ea-b032-757fdcb7b88b",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2022-07-28T16:31:51.951Z",
            "modified": "2022-07-28T16:31:51.951Z",
            "objects": {
                "0": {
                    "type": "x-oca-event",
                    "code": 847102109500309505,
                    "file_ref": "6",
                    "user_ref": "7",
                    "process_ref": "3",
                    "parent_process_ref": "4",
                    "network_ref": "9",
                    "category": "8",
                    "action": "Network Connection Established",
                    "created": "2022-03-29T14:41:21.301Z"
                },
                "1": {
                    "type": "x-oca-asset",
                    "host_id": "842028663686823936",
                    "ip_refs": [
                        "10"
                    ]
                },
                "2": {
                    "type": "x-reaqta-event",
                    "local_id": "847101972854081537"
                },
                "3": {
                    "type": "process",
                    "x_unique_id": "842028663686823936:2222:1648564483636",
                    "binary_ref": "6",
                    "creator_user_ref": "7",
                    "pid": 2222,
                    "created": "2022-03-29T14:34:43.636Z",
                    "parent_ref": "4",
                    "extensions": {
                        "windows-process-ext": {
                            "owner_sid": "S-1-1-11-00000000-1111111-222222222-9999"
                        },
                        "x-reaqta-process": {
                            "privilege_level": "MEDIUM",
                            "no_gui": false,
                            "logon_id": "0xxx1s1"
                        }
                    }
                },
                "4": {
                    "type": "process",
                    "x_unique_id": "842028663686823936:1111:1648485432579",
                    "pid": 1111
                },
                "5": {
                    "type": "directory",
                    "path": "c:\\users\\reaqta\\downloads"
                },
                "6": {
                    "type": "file",
                    "parent_directory_ref": "5",
                    "name": "abcd.exe",
                    "hashes": {
                        "MD5": "d05807b758e56634abfdb7cd62798765",
                        "SHA-1": "adb328949df38cece2fc7ad818788d12ej311a9a90",
                        "SHA-256": "a4693a722a69bb5b58e02bd1b28369a123459047bd37bda4836b97a6a6c65432"
                    },
                    "size": 73802,
                    "extensions": {
                        "x-reaqta-program": {
                            "arch": "x32",
                            "fsname": "test.exe"
                        }
                    }
                },
                "7": {
                    "type": "user-account",
                    "user_id": "DESKTOP-TEST\\ReaQta-test"
                },
                "8": {
                    "type": "x-ibm-finding",
                    "extensions": {
                        "x-reaqta-alert": {
                            "incidents": [],
                            "triggered_incidents": []
                        }
                    },
                    "src_ip_ref": "10",
                    "dst_ip_ref": "11"
                },
                "9": {
                    "type": "network-traffic",
                    "extensions": {
                        "x-reaqta-network": {
                            "address_family": "IPv4",
                            "outbound": true
                        }
                    },
                    "protocols": [
                        "tcp"
                    ],
                    "src_port": 443,
                    "dst_port": 8443,
                    "src_ref": "10",
                    "dst_ref": "11"
                },
                "10": {
                    "type": "ipv4-addr",
                    "value": "192.168.1.2"
                },
                "11": {
                    "type": "ipv4-addr",
                    "value": "192.168.2.3"
                }
            },
            "first_observed": "2022-03-29T14:40:48.722Z",
            "last_observed": "2022-03-29T14:40:48.722Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```

## Limitations

- Only 500 events can be retrieved in a single API call.