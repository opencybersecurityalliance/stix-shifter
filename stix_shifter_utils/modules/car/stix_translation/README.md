# CAR

### Format for calling stix-shifter from the command line

python stix_shifter.py `<translator_module>` `<query or result>` `<stix identity object>` `<data>`

(Note the identity object is only used when converting from AQL to STIX, but due to positional arguments, an empty hash will need to be passed in when converting from STIX patterns to AQL. Keyword arguments should be implemented to overcome this).

## Converting from CAR events to STIX

CAR data to STIX mapping is defined in `to_stix_map.json`

### Example of translating a CAR flow object:

`python main.py translate "car" "results" '{"id": "identity--56c5a276-a192-4c46-a61f-b81724c61096"}' '[{"first_observed": "2018-04-20T12:36:17.191Z", "last_observed": "2018-04-20T12:36:17.191Z", "number_observed": 1, "created": "2018-08-05T22:13:02.000Z", "modified": "2018-08-05T22:13:02.000Z", "object": "flow", "fields": {"start_time": "2018-04-20T12:36:17.191Z", "end_time": "2018-04-20T12:36:17.191Z", "src_ip": "192.168.0.2", "dest_ip": "192.168.0.3", "src_port": 12345, "dest_port": 80, "protocol": "HTTP", "content": "GET https://www.example.com/ HTTP/1.1"}}]'`

Will return the following STIX observable:

```json
{
    "type": "bundle",
    "id": "bundle--38c16678-9879-4c73-ac53-9ab49dbea236",
    "objects": [
        {
            "id": "identity--56c5a276-a192-4c46-a61f-b81724c61096"
        },
        {
            "id": "observed-data--0bd617ba-5c9e-47aa-9917-bb71c47ac818",
            "type": "observed-data",
            "created_by_ref": "identity--56c5a276-a192-4c46-a61f-b81724c61096",
            "objects": {
                "0": {
                    "type": "network-traffic",
                    "start": "2018-04-20T12:36:17.191Z",
                    "end": "2018-04-20T12:36:17.191Z",
                    "src_ref": "1",
                    "dst_ref": "2",
                    "src_port": 12345,
                    "dst_port": 80,
                    "protocols": [
                        "http"
                    ],
                    "src_payload_ref": "3"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "192.168.0.2"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "192.168.0.3"
                },
                "3": {
                    "type": "artifact",
                    "payload_bin": "R0VUIGh0dHBzOi8vd3d3LmV4YW1wbGUuY29tLyBIVFRQLzEuMQ=="
                }
            },
            "first_observed": "2018-04-20T12:36:17.191Z",
            "last_observed": "2018-04-20T12:36:17.191Z",
            "number_observed": 1
        }
    ]
}
```

### Example of translating a CAR process object:

`python main.py translate "car" "results" '{"id": "identity--56c5a276-a192-4c46-a61f-b81724c61096"}' '[{"object": "process", "fields": {"pid": 4000, "exe": "blah.exe", "current_directory": "C:\\", "command_line": "blah.exe rofl copter", "user": "myuser", "md5_hash": "00000000000000000000000000000000", "sha1_hash": "1111111111111111111111111111111111111111", "sha256_hash": "2222222222222222222222222222222222222222222222222222222222222222", "parent_exe": "cmd.exe", "ppid": 1024, "sid": "S-1-1-0"}}]'`

Will return the following STIX observable:

```json
{
    "type": "bundle",
    "id": "bundle--1bfd66e6-42d6-4fba-bac8-47e2374c1f5b",
    "objects": [
        {
            "id": "identity--56c5a276-a192-4c46-a61f-b81724c61096"
        },
        {
            "id": "observed-data--f44b84e0-6bc5-4e00-8a98-d6fec52ab9ce",
            "type": "observed-data",
            "created_by_ref": "identity--56c5a276-a192-4c46-a61f-b81724c61096",
            "objects": {
                "0": {
                    "type": "process",
                    "pid": 4000,
                    "binary_ref": "1",
                    "cwd": "C:\\",
                    "command_line": "blah.exe rofl copter",
                    "creator_user_ref": "2",
                    "parent_ref": "4",
                    "extensions": {
                        "windows-process-ext": {
                            "owner_sid": "S-1-1-0"
                        }
                    }
                },
                "1": {
                    "type": "file",
                    "name": "blah.exe",
                    "hashes": {
                        "MD5": "00000000000000000000000000000000",
                        "SHA1": "1111111111111111111111111111111111111111",
                        "SHA-256": "2222222222222222222222222222222222222222222222222222222222222222"
                    }
                },
                "2": {
                    "type": "user-account",
                    "account_login": "myuser"
                },
                "3": {
                    "type": "file",
                    "name": "cmd.exe"
                },
                "4": {
                    "type": "process",
                    "binary_ref": "3",
                    "pid": 1024
                }
            }
        }
    ]
}
```

### Example of translating another CAR process object:

`python main.py translate "car" "results" '{"id": "identity--56c5a276-a192-4c46-a61f-b81724c61096"}' '[{"object": "process", "fields": {"image_path": "C:\\mydir\\blah.exe", "parent_image_path": "C:\\Windows\\System32\\cmd.exe"}}]'`

Will return the following STIX observable:

```json
{
    "type": "bundle",
    "id": "bundle--ff337df6-6c4f-415d-8a34-2d2595def557",
    "objects": [
        {
            "id": "identity--56c5a276-a192-4c46-a61f-b81724c61096"
        },
        {
            "id": "observed-data--03344356-067c-47b8-8090-d24c4da03267",
            "type": "observed-data",
            "created_by_ref": "identity--56c5a276-a192-4c46-a61f-b81724c61096",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "blah.exe",
                    "parent_directory_ref": "2"
                },
                "1": {
                    "type": "process",
                    "binary_ref": "0",
                    "parent_ref": "4"
                },
                "2": {
                    "type": "directory",
                    "path": "C:\\mydir\\"
                },
                "3": {
                    "type": "file",
                    "name": "cmd.exe",
                    "parent_directory_ref": "5"
                },
                "4": {
                    "type": "process",
                    "binary_ref": "3"
                },
                "5": {
                    "type": "directory",
                    "path": "C:\\Windows\\System32\\"
                }
            }
        }
    ]
}
```

