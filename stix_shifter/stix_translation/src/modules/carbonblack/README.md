# CarbonBlack

## CarbonBlack Process API Supported STIX Pattern values (Querying):

The supported query values are defined in the mapping file [process_api_from_stix_map.json](carbonblack/json/process_api_from_stix_map.json). An example output object can be found [here](#Example-STIX-Output-Format) and is defined in [process_api_to_stix_map.json](carbonblack/json/process_api_to_stix_map.json).


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


Similarly the mapping files for the carbonblack binary api are [binary_api_from_stix_map.json](carbonblack/json/process_api_from_stix_map.json) [process_api_to_stix_map.json](carbonblack/json/process_api_to_stix_map.json).
The following query values are supported for the binary api:

- `file:name`
- `file:hashes.MD5`

In the following examples the module name is `carbonblack`. This will default to the `carbonblack:process` module. Alternatively you can explicitly use the binary or process api by using the module name `carbonblack:binary` or `carbonblack:process`.

### Execute a STIX pattern on a CarbonBlack instance

```
$ python3 main.py execute carbonblack carbonblack "<data_source>" "<connection>" "<configuration>" "<query>"
```


This example command executes the full STIX translation and transmission pipeline. The commands that make up this pipeline will be include below.
```
$ python3 main.py execute carbonblack carbonblack '{"id": "asdf"}' '{"host":"example.carbonblack.io", "port": "443"}' '{"auth":{"token":"0000000000000000000000000000000000000000"}}' "[process:name = 'cmd.exe']"
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
$ python3 main.py transmit carbonblack '{"host": "example.carbonblack.io", "port":443}' '{"auth": {"token":"000000000000000000000000000"}}' query "process_name:cmd.exe"
{'success': True, 'search_id': 'process_name:cmd.exe'}
```

```
$ python3 main.py transmit carbonblack '{"host": "example.carbonblack.io", "port":443}' '{"auth": {"token":"0000000000000000000000000000000000000000"}}' results 'process_name:cmd.exe' '{}' '{}'
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

```
$ python3 main.py translate carbonblack results '{"id": "blah"}' '<copied results from previous query>'
{
    "type": "bundle",
    "id": "bundle--f61b8f2b-30a1-4e00-9c09-2ee812148021",
    "objects": [
        {
            "id": "blah"
        },
        {
            "id": "observed-data--650f0319-817d-4f8a-acc6-26157bc1400e",
            "type": "observed-data",
            "created_by_ref": "blah",
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
                    "command_line": "C:\\Windows\\system32\\cmd.exe /c tasklist",
                    "created": "2019-01-22T00:04:52.875Z",
                    "pid": 1896,
                    "creator_user_ref": "7",
                    "name": "cmd.exe",
                    "binary_ref": "0",
                    "parent_ref": "3"
                },
                "2": {
                    "type": "file",
                    "name": "cmd.exe",
                    "hashes": {
                        "MD5": "000000000000000000000000000000"
                    }
                },
                "3": {
                    "type": "process",
                    "name": "cmd.exe",
                    "binary_ref": "2",
                    "pid": 2508
                },
                "4": {
                    "type": "domain-name",
                    "value": "lab1-host1"
                },
                "5": {
                    "type": "ipv4-addr",
                    "value": "12.166.224.2"
                },
                "6": {
                    "type": "ipv4-addr",
                    "value": "10.239.15.200"
                },
                "7": {
                    "type": "user-account",
                    "user_id": "SYSTEM"
                }
            }
        }
    ]
}
```


