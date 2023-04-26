# Carbon Black CB Response

## Supported STIX Mappings

See the [table of mappings](carbonblack_supported_stix.md) for the STIX objects and operators supported by this connector.


## CarbonBlack Module Search API Endpoints

CarbonBlack Module searches Process API Endpoint.

> Notice: If "Include Process Events?" option is enabled, CarbonBlack module searches events API endpoint. Enabling this option requires Carbon Black Response of version >= 6.1.


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
{'queries': ['((process_name:cmd.exe) and last_update:-5m)']}
```

Note that because the carbonblack api is synchronous the search id is the same as the translated query.
```
$ python3 main.py transmit carbonblack '{"host": "example.carbonblack.io", "port":443}' '{"auth": {"token":"000000000000000000000000000"}}' query '((process_name:cmd.exe) and last_update:-5m)'
{'success': True, 'search_id': '((process_name:cmd.exe) and last_update:-5m)'}
```

As the synchronous connector, module uses the search id which is the same as translated query:
```
$ python3 main.py transmit carbonblack '{"host": "example.carbonblack.io", "port":443}' '{"auth": {"token":"0000000000000000000000000000000000000000"}}' results '((process_name:cmd.exe) and last_update:-5m)' 0 1
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
