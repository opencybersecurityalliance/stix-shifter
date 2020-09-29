# CarbonBlack

## CarbonBlack Process API Supported STIX Pattern values (Querying):

The supported query values are defined in the mapping file [process_api_from_stix_map.json](json/process_api_from_stix_map.json). An example output object can be found [here](#Example-STIX-Output-Format) and is defined in [process_api_to_stix_map.json](json/process_api_to_stix_map.json).


- `network-traffic:src_port`
- `network-traffic:dst_port`
- `ipv4-addr:value`
- `file:name`
- `file:hashes.MD5`
- `user-account:user_id`
- `process:name`
- `process:command_line`
- `process:created`
- `process:pid`
- `process:parent_ref.pid`
- `domain-name:value`

## CarbonBlack Binary API Supported STIX Pattern values (Querying):


Similarly the mapping files for the carbonblack binary api are [binary_api_from_stix_map.json](json/binary_api_from_stix_map.json) and [process_api_to_stix_map.json](json/binary_api_to_stix_map.json).
The following query values are supported for the binary api:

- `file:name`
- `file:hashes.MD5`

## CarbonBlack Multiple API Endpoints

The STIX Patterns are mapped seamlessly to the desired API depending on the query. If any of the STIX observable expressions (query inside of [ ]'s) reference the process object then that query will be mapped to the CarbonBlack Process API. If multiple observable expressions are used that result in separate calls to the Process and Binary API endpoints then multiple queries will be created, one for each endpoint. There is an [example](#Multiple-API-Endpoint-Example) of the translator mapping to both APIs below.

### Execute a STIX pattern on a CarbonBlack instance

```
$ python3 main.py execute carbonblack carbonblack "<data_source>" "<connection>" "<configuration>" "<query>"
```

This example command executes the full STIX translation and transmission pipeline. The commands that make up this pipeline will be include below.
```
$ python3 main.py execute carbonblack carbonblack '{"id": "asdf"}' '{"host":"example.carbonblack.io", "port": 443}' '{"auth":{"token":"0000000000000000000000000000000000000000"}}' "[process:name = 'cmd.exe']"
```

Note in this example some logging is omitted.

Translated CarbonBlack query and parsed STIX expression:
```
$ python3 main.py translate carbonblack query '{}' "[process:name = 'cmd.exe']"
['process_name:cmd.exe']
{'queries': ['process_name:cmd.exe'], 'parsed_stix': [{'attribute': 'process:name', 'comparison_operator': '=', 'value': 'cmd.exe'}]}
```

Note that because the carbonblack api is synchronous the search id is the same as the translated query.
```
$ python3 main.py transmit carbonblack '{"host": "example.carbonblack.io", "port":443}' '{"auth": {"token":"000000000000000000000000000"}}' query '{"query":"process_name:cmd.exe", "dialect":"process"}'
{'success': True, 'search_id': 'process_name:cmd.exe'}
```

Note unlike other modules this module accepts a json string with the keys 'query' and 'dialect' set as it's search_id.
```
$ python3 main.py transmit carbonblack '{"host": "example.carbonblack.io", "port":443}' '{"auth": {"token":"0000000000000000000000000000000000000000"}}' results '{"query":"process_name:cmd.exe", "dialect":"process"}' 0 1
{
  "terms": [
    "process_name:cmd.exe"
  ],
  "results": [
    {
      "process_md5": "5746bd7e255dd6a8afa06f7c42c1ba41",
      "sensor_id": 49,
      "filtering_known_dlls": true,
      "modload_count": 3,
      "parent_unique_id": "00000031-0000-09cc-01d4-b1e61979dd7c-000000000001",
      "emet_count": 0,
      "alliance_score_srstrust": -100,
      "cmdline": "C:\\Windows\\system32\\cmd.exe /c tasklist",
      "alliance_updated_srstrust": "2018-04-05T16:04:34Z",
      "filemod_count": 0,
      "id": "00000031-0000-0768-01d4-b1e6197c3edd",
      "parent_name": "cmd.exe",
      "parent_md5": "000000000000000000000000000000",
      "group": "lab1",
      "parent_id": "00000031-0000-09cc-01d4-b1e61979dd7c",
      "hostname": "lab1-host1",
      "last_update": "2019-01-22T00:04:52.937Z",
      "start": "2019-01-22T00:04:52.875Z",
      "alliance_link_srstrust": "https://example.com",
      "comms_ip": 212262914,
      "regmod_count": 0,
      "interface_ip": 183439304,
      "process_pid": 1896,
      "username": "SYSTEM",
      "terminated": true,
      "alliance_data_srstrust": [
        "5746bd7e255dd6a8afa06f7c42c1ba41"
      ],
      "process_name": "cmd.exe",
      "emet_config": "",
      "last_server_update": "2019-01-22T00:07:07.064Z",
      "path": "c:\\windows\\system32\\cmd.exe",
      "netconn_count": 0,
      "parent_pid": 2508,
      "crossproc_count": 2,
      "segment_id": 1548115627056,
      "host_type": "workstation",
      "processblock_count": 0,
      "os_type": "windows",
      "childproc_count": 4,
      "unique_id": "00080031-0000-0748-01d4-b1e61c7c3edd-016872e1cb30"
    }
  ],

  "elapsed": 0.05147600173950195,
  "comprehensive_search": true,
  "all_segments": true,
  "total_results": 1,
  "highlights": [],
  "facets": {},
  "tagged_pids": {},
  "start": 0,
  "incomplete_results": false,
  "filtered": {}
}
```

Then the results can be translated with the following command: (Note just the json array associated with the results key should be copied into this command)

## Example STIX Output Format

Note that the datasource argument passed on the command line `'{"id": "..."}'` will be used as the first object in the observable bundle.

```
$ python3 main.py translate carbonblack results '{"id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3"}' '<copied results from previous query>'
{
    'type': 'bundle',
        'id': 'bundle--c885b371-fe48-4e64-af10-c69e9ca1593c',
        'objects': [
        {
            'type': 'identity',
            'id': 'identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3',
            'name': 'CarbonBlack',
            'identity_class': 'events'
        },
        {
            'id': 'observed-data--41ef31bc-6f77-4628-b9e4-3e761aed631d',
            'type': 'observed-data',
            'created_by_ref': 'identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3',
            'objects': {
                '0': {'type': 'file',
                    'hashes': {
                        'MD5': '5746bd7e255dd6a8afa06f7c42c1ba41'
                    },
                    'name': 'cmd.exe'
                },
                '1': {
                    'type': 'process',
                    'command_line': 'C:\\Windows\\system32\\cmd.exe /c tasklist',
                    'created': '2019-01-22T00:04:52.875Z',
                    'opened_connection_refs': ['6'],
                    'pid': 1896,
                    'creator_user_ref': '8',
                    'name': 'cmd.exe',
                    'binary_ref': '0',
                    'parent_ref': '3'
                },
                '2': {
                    'type': 'file',
                    'name': 'cmd.exe',
                    'hashes': {
                        'MD5': '000000000000000000000000000000'
                    }
                },
                '3': {
                    'type': 'process',
                    'name': 'cmd.exe',
                    'binary_ref': '2',
                    'pid': 2508
                },
                '4': {
                    'type': 'domain-name',
                    'value': 'lab1-host1'
                },
                '5': {
                    'type': 'ipv4-addr',
                    'value': '193.86.73.118'
                },
                '6': {
                    'type': 'network-traffic',
                    'dst_ref': '5',
                    'src_ref': '7'
                },
                '7': {
                    'type': 'ipv4-addr',
                    'value': '10.239.15.200'
                },
                '8': {
                    'type': 'user-account',
                    'user_id': 'SYSTEM'
                }
            }
        }
    ]
}
```

## Multiple API Endpoint Example

```
$ python3 main.py execute carbonblack carbonblack '{"id": "asdf"}' '{"host":"example.my.carbonblack.io", "port": 443}' '{"auth":{"token":"0000000000000000000000000000000000000000"}}" "[process:name = 'cmd.exe'] OR [file:name = 'notepad.exe']"
```

The translation portion of this command will return:
```
[{'query': 'process_name:cmd.exe', 'dialect': 'process'}, {'query': 'observed_filename:notepad.exe', 'dialect': 'binary'}]
```

The final results will be translated as follows:
```
{
    "type": "bundle",
    "id": "bundle--0cfca80c-e630-45a3-9d50-1d98b1fe2570",
    "objects": [
        {
            "id": "asdf"
        },
        {
            "id": "observed-data--7168e8cb-2daa-4566-8546-418f459e7d4a",
            "type": "observed-data",
            "created_by_ref": "asdf",
            "objects": {
                "0": {
                    "type": "file",
                    "hashes": {
                        "MD5": "5746bd7e255dd6a8afa06f7c42c1ba41"
                    },
                    "name": "cmd.exe"
                },
                "1": {
                    "type": "process",
                    "command_line": "cmd /c \"\"C:\\ProgramData\\VMware\\VMware CAF\\pme\\\\config\\..\\scripts\\is-listener-running.bat\" \"",
                    "created": "2018-12-17T08:37:13.318Z",
                    "opened_connection_refs": [
                        "6"
                    ],
                    "pid": 2184,
                    "creator_user_ref": "8",
                    "name": "cmd.exe",
                    "binary_ref": "0",
                    "parent_ref": "3"
                },
                "2": {
                    "type": "file",
                    "name": "managementagenthost.exe",
                    "hashes": {
                        "MD5": "000000000000000000000000000000"
                    }
                },
                "3": {
                    "type": "process",
                    "name": "managementagenthost.exe",
                    "binary_ref": "2",
                    "pid": 2564
                },
                "4": {
                    "type": "domain-name",
                    "value": "redlab-vuln2"
                },
                "5": {
                    "type": "ipv4-addr",
                    "value": "12.166.224.2"
                },
                "6": {
                    "type": "network-traffic",
                    "dst_ref": "5",
                    "src_ref": "7"
                },
                "7": {
                    "type": "ipv4-addr",
                    "value": "10.239.15.201"
                },
                "8": {
                    "type": "user-account",
                    "user_id": "SYSTEM"
                }
            }
        },
        {
            "id": "observed-data--2fea7e59-4940-4409-95d2-7fe62dd5af45",
            "type": "observed-data",
            "created_by_ref": "asdf",
            "objects": {
                "0": {
                    "type": "file",
                    "hashes": {
                        "MD5": "5746bd7e255dd6a8afa06f7c42c1ba41"
                    },
                    "name": "cmd.exe"
                },
                "1": {
                    "type": "process",
                    "command_line": "cmd /c \"\"C:\\ProgramData\\VMware\\VMware CAF\\pme\\\\config\\..\\scripts\\is-listener-running.bat\" \"",
                    "created": "2018-12-17T08:37:13.318Z",
                    "opened_connection_refs": [
                        "6"
                    ],
                    "pid": 2184,
                    "creator_user_ref": "8",
                    "name": "cmd.exe",
                    "binary_ref": "0",
                    "parent_ref": "3"
                },
                "2": {
                    "type": "file",
                    "name": "managementagenthost.exe",
                    "hashes": {
                        "MD5": "000000000000000000000000000000"
                    }
                },
                "3": {
                    "type": "process",
                    "name": "managementagenthost.exe",
                    "binary_ref": "2",
                    "pid": 2564
                },
                "4": {
                    "type": "domain-name",
                    "value": "redlab-vuln2"
                },
                "5": {
                    "type": "ipv4-addr",
                    "value": "12.166.224.2"
                },
                "6": {
                    "type": "network-traffic",
                    "dst_ref": "5",
                    "src_ref": "7"
                },
                "7": {
                    "type": "ipv4-addr",
                    "value": "10.239.15.201"
                },
                "8": {
                    "type": "user-account",
                    "user_id": "SYSTEM"
                }
            }
        },
        {
            "id": "observed-data--69aa8cd8-94d3-4bea-b479-066eaded8d2f",
            "type": "observed-data",
            "created_by_ref": "asdf",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "NOTEPAD.EXE",
                    "created": "2017-03-14T10:04:35.779Z",
                    "hashes": {
                        "MD5": "FC2EA5BD5307D2CFA5AAA38E0C0DDCE9"
                    }
                }
            }
        },
        {
            "id": "observed-data--a3b32d7b-c641-4f65-87c5-7e00292412a9",
            "type": "observed-data",
            "created_by_ref": "asdf",
            "objects": {
                "0": {
                    "type": "file",
                    "name": "NOTEPAD.EXE",
                    "created": "2017-04-12T21:06:15.216Z",
                    "hashes": {
                        "MD5": "959A31D0CD013CEA0C66DB7C03BCBDDF"
                    }
                }
            }
        }
    ]
}
```
