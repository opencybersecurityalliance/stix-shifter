import unittest

from stix_shifter_utils.utils.async_utils import run_in_thread
from stix_shifter_modules.elastic_ecs.entry_point import EntryPoint
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "elastic_ecs"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "ElasticEcs",
    "identity_class": "events"
}
options = {}

data = {
          "@timestamp": "2019-04-21T11:05:07.000Z",
          "event": {
            "action": "get",
            "dataset": "apache.access",
            "original": "10.42.42.42 - - [07/Dec/2018:11:05:07 +0100] \"GET /blog HTTP/1.1\" 200 2571 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36\""
          },
          "process": {
            "args": [
              "/System/Library/CoreServices/SubmitDiagInfo",
              "server-init"
            ],
            "pid": 609,
            "ppid": 1,
            "working_directory": "/",
            "executable": "/System/Library/CoreServices/SubmitDiagInfo",
            "start": "2019-04-10T11:33:57.571Z",
            "entity_id": "I2bdm9mEE1xzKvc0",
            "name": "SubmitDiagInfo"
          },
          "message": "\"GET /blog HTTP/1.1\" 200 2571",
          "service": {
            "name": "Company blog",
            "type": "apache"
          },
          "source": {
            "mac": "00:01:a7:a5:b2:b1",
            "ip": "107.0.0.48",
            "port": 49745,
            "bytes": 217,
            "packets": 3
          },
          "destination": {
            "mac": "00:9a:4c:83:dc:f1",
            "ip": "100.101.0.69",
            "port": 443,
            "packets": 11,
            "bytes": 943
          },
          "network": {
            "type": "ipv4",
            "transport": "tcp",
            "community_id": "1:kL4GhKYBNaX4O45xnu+pPYEmq70=",
            "bytes": 4488,
            "packets": 14
          },
          "url": {
            "original": "/blog"
          },
          "user": {
            "name": "-"
          },
          "file": {
              "name": "example.png",
              "directory": "/home/alice"
          },
          "dns": {
            "question": {
                "name": "officehomeblobs.blob.core.windows.net",
            },
            "resolved_ip": [
                "40.116.120.16", "1.2.3.4"
            ]
          }
}

event_data = {
    "@timestamp": "2020-11-15T16:29:12.130Z",
    "message": "Process Create:\nRuleName: -\nUtcTime: 2020-11-15 16:29:12.130\nProcessGuid: {253acf67-5758-5fb1-3d3c-000000000800}\nProcessId: 26424\nImage: C:\\Windows\\System32\\wbem\\unsecapp.exe\nFileVersion: 10.0.19041.546 (WinBuild.160101.0800)\nDescription: Sink to receive asynchronous callbacks for WMI client application\nProduct: Microsoft® Windows® Operating System\nCompany: Microsoft Corporation\nOriginalFileName: unsecapp.dll\nCommandLine: C:\\WINDOWS\\system32\\wbem\\unsecapp.exe -Embedding\nCurrentDirectory: C:\\WINDOWS\\system32\\\nUser: AzureAD\\USERNAME\nLogonGuid: {253acf67-bb01-5fac-d398-0a0200000000}\nLogonId: 0x20A98D3\nTerminalSessionId: 2\nIntegrityLevel: Medium\nHashes: MD5=EB249AE927EB20812BDEB5484CEC67B0,SHA256=F1BE6DDD38CEE4959B58C5DD593A8A4BFF32E05638426C30A4D4ADD43E387590,IMPHASH=87E54E3D04D772F26002D8B564B2426C\nParentProcessGuid: {253acf67-5e7e-5fac-1200-000000000800}\nParentProcessId: 1248\nParentImage: C:\\Windows\\System32\\svchost.exe\nParentCommandLine: C:\\WINDOWS\\system32\\svchost.exe -k DcomLaunch -p",
    "user": {
      "name": "USERNAME",
      "domain": "AzureAD"
    },
    "agent": {
      "name": "HOST-NAME",
      "type": "winlogbeat",
      "version": "7.9.1",
      "hostname": "HOST-NAME"
    },
    "file": {
        "name": "example.png",
        "directory": "/home/alice"
    },
    "event": {
      "kind": "event",
      "code": 1,
      "provider": "Microsoft-Windows-Sysmon",
      "action": "Process Create (rule: ProcessCreate)",
      "created": "2020-11-15T16:29:13.269Z",
      "module": "sysmon",
      "category": [
        "process"
      ],
      "type": [
        "start",
        "process_start"
      ]
    },
    "host": {
      "name": "HOST-NAME",
      "hostname": "HOST-NAME",
      "architecture": "x86_64",
      "os": {
        "name": "Windows 10 Enterprise",
      },
      "id": "253acf67-a779-42fc-8e15-e55230de7e64",
      "ip": [
        "aaaa::bbbb:1111:2222:3333",
        "9.9.9.9"
      ],
      "mac": [
        "00:01:02:0a:0b:0c"
      ]
    },
    "process": {
      "command_line": "C:\\WINDOWS\\system32\\wbem\\unsecapp.exe -Embedding",
      "parent": {
        "pid": 1248,
        "executable": "C:\\Windows\\System32\\svchost.exe",
        "command_line": "C:\\WINDOWS\\system32\\svchost.exe -k DcomLaunch -p",
        "name": "svchost.exe"
      },
      "hash": {
        "md5": "eb249ae927eb20812bdeb5484cec67b0",
        "sha256": "f1be6ddd38cee4959b58c5dd593a8a4bff32e05638426c30a4d4add43e387590"
      },
      "pid": 26424,
      "executable": "C:\\Windows\\System32\\wbem\\unsecapp.exe",
      "working_directory": "C:\\WINDOWS\\system32\\",
      "name": "unsecapp.exe"
    },
    "url": {
        "original": "http://domain.com/path?query=abc",
        "domain": "domain.com"
    },
    "registry": {
      "path": "HKLM\\a\\b\\c\\val",
      "hive": "HKLM",
      "key": "a\\b\\c\\val",
      "value": "val",
      "data": {
        "strings": [
          "ddd"
        ],
        "type": "SZ_DWORD"
      }
    },
    "dns": {
        "question": {
            "name": "officehomeblobs.blob.core.windows.net",
        },
        "resolved_ip": [
            "40.116.120.16", "1.2.3.4"
        ]
    }
  }

ecs_event_data = {
    "event" : {
      "category" : [
        "process"
      ],
      "type" : [
        "start",
        "process_start"
      ],
      "provider" : "Microsoft-Windows-Sysmon",
      "code" : 1,
      "action" : "Process Create (rule: ProcessCreate)",
      "created" : "2021-10-24T23:58:21.586Z",
      "kind" : "event",
      "module" : "sysmon"
    },
    "winlog" : {
      "task" : "Process Create (rule: ProcessCreate)",
      "provider_name" : "Microsoft-Windows-Sysmon",
      "event_id" : 1,
      "channel" : "Microsoft-Windows-Sysmon/Operational",
      "event_data" : {
        "FileVersion" : "10.0.17763.2145 (WinBuild.160101.0800)",
        "Company" : "Microsoft Corporation",
        "Product" : "Microsoft® Windows® Operating System",
        "Description" : "DSREG commandline tool",
        "RuleName" : "-",
        "TerminalSessionId" : "0",
        "LogonId" : "0x3e7",
        "LogonGuid" : "{8dfc401c-1ef5-6175-e703-000000000000}",
        "IntegrityLevel" : "System"
      },
      "api" : "wineventlog",
      "user" : {
        "domain" : "NT AUTHORITY",
        "name" : "SYSTEM",
        "type" : "User",
        "identifier" : "S-1-5-18"
      },
      "provider_guid" : "{5770385f-c22a-43e0-bf4c-06f5698ffbd9}",
      "opcode" : "Info",
      "computer_name" : "win-server1.example.com",
      "process" : {
        "pid" : 3684,
        "thread" : {
          "id" : 4616
        }
      },
      "record_id" : 1778428,
      "version" : 5
    },
    "message" : "Process Create:\nRuleName: -\nUtcTime: 2021-10-24 23:58:20.569\nProcessGuid: {8dfc401c-f31c-6175-5715-000000001b00}\nProcessId: 5244\nImage: C:\\Windows\\System32\\dsregcmd.exe\nFileVersion: 10.0.17763.2145 (WinBuild.160101.0800)\nDescription: DSREG commandline tool\nProduct: Microsoft® Windows® Operating System\nCompany: Microsoft Corporation\nOriginalFileName: dsregcmd.exe\nCommandLine: C:\\Windows\\System32\\dsregcmd.exe $(Arg0) $(Arg1) $(Arg2)\nCurrentDirectory: C:\\Windows\\system32\\\nUser: NT AUTHORITY\\SYSTEM\nLogonGuid: {8dfc401c-1ef5-6175-e703-000000000000}\nLogonId: 0x3E7\nTerminalSessionId: 0\nIntegrityLevel: System\nHashes: MD5=D6957ACEDA86DE523AF0157800AA3C73,SHA256=BA79462455B6E216D0E7CD6FE36BF0EFF8A0D9DD06358D1C97B1014016256618,IMPHASH=382C77BFA0EEE2BA2BA8671D108AD9A3\nParentProcessGuid: {8dfc401c-1ef7-6175-2900-000000001b00}\nParentProcessId: 2244\nParentImage: C:\\Windows\\System32\\svchost.exe\nParentCommandLine: C:\\Windows\\system32\\svchost.exe -k netsvcs -p -s Schedule",
    "tags" : [
      "beats_input_codec_plain_applied"
    ],
    "hash" : {
      "imphash" : "382c77bfa0eee2ba2ba8671d108ad9a3",
      "sha256" : "ba79462455b6e216d0e7cd6fe36bf0eff8a0d9dd06358d1c97b1014016256618",
      "md5" : "d6957aceda86de523af0157800aa3c73"
    },
    "host" : {
      "architecture" : "x86_64",
      "hostname" : "win-server1",
      "os" : {
        "kernel" : "10.0.17763.2237 (WinBuild.160101.0800)",
        "build" : "17763.2237",
        "family" : "windows",
        "name" : "Windows Server 2019 Standard",
        "version" : "10.0",
        "platform" : "windows"
      },
      "id" : "8dfc401c-b042-4f41-b427-91a9dc0b61ac",
      "name" : "win-server1.example.com",
      "mac" : [
        "06:07:08:09:0a:0b"
      ],
      "ip" : [
        "fedc::ba98:7654:3210:1234",
        "9.10.11.12",
        "10.11.12.13"
      ]
    },
    "log" : {
      "level" : "information"
    },
    "user" : {
      "domain" : "NT AUTHORITY",
      "name" : "SYSTEM"
    },
    "@timestamp" : "2021-10-24T23:58:20.569Z",
    "ecs" : {
      "version" : "1.7.0"
    },
    "agent" : {
      "type" : "winlogbeat",
      "ephemeral_id" : "c5c31d91-f913-4f23-9609-3f92e83e4cb7",
      "hostname" : "win-server1",
      "id" : "50a12d7e-a002-4a69-a5e8-f3b07afbfeb7",
      "name" : "win-server1",
      "version" : "7.11.2"
    },
    "process" : {
      "pid" : 5244,
      "parent" : {
        "pid" : 2244,
        "entity_id" : "{8dfc401c-1ef7-6175-2900-000000001b00}",
        "executable" : "C:\\Windows\\System32\\svchost.exe",
        "command_line" : "C:\\Windows\\system32\\svchost.exe -k netsvcs -p -s Schedule",
        "name" : "svchost.exe",
        "args" : [
          "C:\\Windows\\system32\\svchost.exe",
          "-k",
          "netsvcs",
          "-p",
          "-s",
          "Schedule"
        ],
        "exit_code": 0,
        "title": "Just for testing",
        "thread": {
          "id": 3333
        },
        "uptime": 100
      },
      "pe" : {
        "company" : "Microsoft Corporation",
        "file_version" : "10.0.17763.2145 (WinBuild.160101.0800)",
        "description" : "DSREG commandline tool",
        "imphash" : "382c77bfa0eee2ba2ba8671d108ad9a3",
        "original_file_name" : "dsregcmd.exe",
        "product" : "Microsoft® Windows® Operating System"
      },
      "entity_id" : "{8dfc401c-f31c-6175-5715-000000001b00}",
      "executable" : "C:\\Windows\\System32\\dsregcmd.exe",
      "working_directory" : "C:\\Windows\\system32\\",
      "command_line" : "C:\\Windows\\System32\\dsregcmd.exe $(Arg0) $(Arg1) $(Arg2)",
      "args" : [
        "C:\\Windows\\System32\\dsregcmd.exe",
        "$(Arg0)",
        "$(Arg1)",
        "$(Arg2)"
      ],
      "hash" : {
        "md5" : "d6957aceda86de523af0157800aa3c73",
        "sha256" : "ba79462455b6e216d0e7cd6fe36bf0eff8a0d9dd06358d1c97b1014016256618"
      },
      "name" : "dsregcmd.exe"
    },
    "@version" : "1",
    "related" : {
      "hash" : [
        "d6957aceda86de523af0157800aa3c73",
        "ba79462455b6e216d0e7cd6fe36bf0eff8a0d9dd06358d1c97b1014016256618",
        "382c77bfa0eee2ba2ba8671d108ad9a3"
      ],
      "user" : "SYSTEM"
    }
}

observer_data = {
    "process": {
      "args": [
        "C:\\Users\\Administrator\\Desktop\\abc\\abc.exe"
      ],
      "parent": {
        "name": "explorer.exe",
        "entity_id": "485466882194"
      },
      "start": "2023-04-01T21:21:53.540Z",
      "pid": 9989,
      "args_count": 1,
      "entity_id": "485541455428",
      "command_line": "\"C:\\Users\\Administrator\\Desktop\\abc\\abc.exe\" ",
      "executable": "\\Device\\HarddiskVolume3\\Users\\Administrator\\Desktop\\abc\\abc.exe",
      "hash": {
        "sha256": "d438e472cd374d76776c2f23f654e28c6eba57081f322be7777a0d2356732fea",
        "md5": "642e934263d1316ed0d30c7336414a89"
      }
    },
    "os": {
      "type": "windows"
    },
    "url": {
      "scheme": "http"
    },
    "observer": {
      "geo": {
        "continent_name": "North America",
        "region_iso_code": "US-TX",
        "city_name": "Austin",
        "country_iso_code": "US",
        "country_name": "United States",
        "region_name": "Texas",
        "location": {
          "lon": -97.7419,
          "lat": 30.2732
        }
      },
      "address": "10.0.0.101",
      "vendor": "crowdstrike",
      "ip": "10.0.0.101",
      "serial_number": "6484b65c806520073f0337894bc0cd24",
      "type": "agent",
      "version": "1007.3.0016411.1",
    }
}

class TestElasticEcsTransform(unittest.TestCase, object):
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestElasticEcsTransform.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    def test_common_prop(self):
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [data])
        assert (result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert (result_bundle_identity['type'] == data_source['type'])
        assert (result_bundle_identity['id'] == data_source['id'])
        assert (result_bundle_identity['name'] == data_source['name'])
        assert (result_bundle_identity['identity_class']
                == data_source['identity_class'])

        observed_data = result_bundle_objects[1]

        assert (observed_data['id'] is not None)
        assert (observed_data['type'] == "observed-data")
        assert (observed_data['created_by_ref'] == result_bundle_identity['id'])
        assert (observed_data['created'] is not None)
        assert (observed_data['modified'] is not None)
        assert (observed_data['number_observed'] == 1)

    def test_stix_2_1(self):
        test_options = {
            "stix_2.1": True
        }
        entry_point = EntryPoint(options=test_options)
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [data])
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert (observed_data['id'] is not None)
        assert (observed_data['type'] == "observed-data")
        assert (observed_data['created_by_ref'] == data_source['id'])
        assert (observed_data['created'] is not None)
        assert (observed_data['modified'] is not None)
        assert (observed_data['number_observed'] == 1)
        assert('object_refs' in observed_data)
        assert('objects' not in observed_data)
        #TODO: check other objects

    def test_custom_mapping(self):
        data_source_string = data_source
        data = [{
            "custompayload": "SomeBase64Payload",
            "url": "www.example.com",
            "filename": "somefile.exe",
            "username": "someuserid2018"
        }]
        data_string = data

        options = {
            "mapping": {
                "default": {
                    "to_stix": {
                        "username": {"key": "user-account.user_id"},
                        "url": {"key": "url.value"},
                        "custompayload": {"key": "artifact.payload_bin"}
                    }
                }
            }
        }

        translation = stix_translation.StixTranslation()
        result_bundle = translation.translate('elastic_ecs', 'results', data_source_string, data_string, options)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        file_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'file')
        assert(file_object is None), 'default file object type was returned even though it was not included in the custom mapping'

        curr_obj = TestElasticEcsTransform.get_first_of_type(objects.values(), 'artifact')
        #TODO fix test translation.translate: qradar-> elastic_ecs in line 132
        # >> results: {
        #     "type": "bundle",
        #     "id": "bundle--c7650e4e-b6f7-430a-b9d1-1a501f394b5a",
        #     "spec_version": "2.0",
        #     "objects": [
        #         {
        #             "type": "identity",
        #             "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
        #             "name": "ElasticEcs",
        #             "identity_class": "events"
        #         },
        #         {
        #             "id": "observed-data--92592394-f272-469f-b8c9-45b9795dd71e",
        #             "type": "observed-data",
        #             "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
        #             "created": "2020-04-19T20:06:41.756Z",
        #             "modified": "2020-04-19T20:06:41.756Z",
        #             "objects": {},
        #             "number_observed": 1
        #         }
        #     ]
        # }
        # assert(curr_obj is not None), 'artifact object type not found'
        # assert(curr_obj.keys() == {'type', 'payload_bin'})
        # assert(curr_obj['payload_bin'] == "SomeBase64Payload")


    def test_network_traffic_prop(self):
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [data])
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        nt_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'network-traffic')
        assert (nt_object is not None), 'network-traffic object type not found'
        assert (nt_object.keys() ==
                {'type', 'src_port', 'src_byte_count', 'src_packets', 'dst_port', 'dst_byte_count', 'dst_packets', 'src_ref', 'dst_ref', 'protocols', 'extensions', 'x_community_id'})
        assert (nt_object['type'] == 'network-traffic')
        assert (nt_object['src_port'] == 49745)
        assert (nt_object['dst_port'] == 443)
        assert (nt_object['protocols'] == ['ipv4', 'tcp'])

        ip_ref = nt_object['dst_ref']
        assert (ip_ref in objects), f"dst_ref with key {nt_object['dst_ref']} not found"
        ip_obj = objects[ip_ref]
        assert (ip_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert (ip_obj['type'] == 'ipv4-addr')
        assert (ip_obj['value'] == '100.101.0.69')
        assert (isinstance(ip_obj['resolves_to_refs'], list) and isinstance(ip_obj['resolves_to_refs'][0], str))

        ip_ref = nt_object['src_ref']
        assert (ip_ref in objects), f"src_ref with key {nt_object['src_ref']} not found"
        ip_obj = objects[ip_ref]
        assert (ip_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert (ip_obj['type'] == 'ipv4-addr')
        assert (ip_obj['value'] == '107.0.0.48')
        assert (isinstance(ip_obj['resolves_to_refs'], list) and isinstance(ip_obj['resolves_to_refs'][0], str))

        dns_ext = nt_object['extensions']['dns-ext']
        assert(dns_ext is not None)
        assert(dns_ext["question"] is not None)
        name_ref = dns_ext["question"]["domain_ref"]
        assert(name_ref in objects), f"name_ref with key {dns_ext['question']['name_ref']} not found"
        domain_obj = objects[name_ref]
        assert(domain_obj["type"] == "domain-name")
        assert(domain_obj["value"] == "officehomeblobs.blob.core.windows.net")
        assert(dns_ext["resolved_ip_refs"] is not None)
        for ip_ref in dns_ext["resolved_ip_refs"]:
            assert(ip_ref in objects), f"resolved_ip_ref with key {ip_ref} not found"
            ip_obj = objects[ip_ref]
            assert(ip_obj["type"] == "ipv4-addr")
            assert(ip_obj["value"] in ["40.116.120.16", "1.2.3.4"])


    def test_process_prop(self):
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [data])
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        proc_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'process')
        assert (proc_object is not None), 'process object type not found'
        assert (proc_object.keys() ==
                {'type', 'pid', 'name', 'created', 'opened_connection_refs', 'creator_user_ref', 'binary_ref', 'parent_ref', 'x_unique_id', 'cwd'})
        assert (proc_object['type'] == 'process')
        assert (proc_object['pid'] == 609)
        assert (proc_object['created'] == '2019-04-10T11:33:57.571Z')

        creator_user_ref = proc_object['creator_user_ref']
        assert (creator_user_ref in objects), f"creator_user_ref with key {proc_object['creator_user_ref']} not found"
        creator_user_ref_obj = objects[creator_user_ref]
        assert (creator_user_ref_obj.keys() == {'type', 'user_id', 'account_login'})
        assert (creator_user_ref_obj['type'] == 'user-account')
        assert (creator_user_ref_obj['user_id'] == '-')

        parent_ref = proc_object['parent_ref']
        assert (parent_ref in objects), f"parent_ref with key {proc_object['creator_user_ref']} not found"
        process_parent = objects[parent_ref]
        assert (process_parent.keys() == {'type', 'pid'})
        assert (process_parent['type'] == 'process')
        assert (process_parent['pid'] == 1)

    def test_x_ibm_event(self):
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [event_data])
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        event_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'x-oca-event')
        assert (event_object is not None), 'x-oca-event object type not found'

        host_ref = event_object['host_ref']
        assert (host_ref in objects), f"host_ref with key {event_object['host_ref']} not found"
        host_obj = objects[host_ref]
        assert(host_obj['type'] == 'x-oca-asset')
        assert(host_obj['hostname'] == 'HOST-NAME')

        mac_refs = host_obj['mac_refs']
        assert(mac_refs is not None), "host mac_refs not found"
        assert(len(mac_refs) == 1)
        mac_obj = objects[mac_refs[0]]
        assert(mac_obj.keys() == {'type', 'value'})
        assert(mac_obj['type'] == 'mac-addr')
        assert(mac_obj['value'] == "00:01:02:0a:0b:0c")

        process_ref = event_object['process_ref']
        assert(process_ref in objects), f"process_ref with key {event_object['process_ref']} not found"
        process_obj = objects[process_ref]
        assert(process_obj['type'] == 'process')
        assert(process_obj['command_line'] == "C:\\WINDOWS\\system32\\wbem\\unsecapp.exe -Embedding")
        binary_obj = objects[process_obj['binary_ref']]
        assert(binary_obj is not None), "process binary ref not found"
        assert(binary_obj.keys() == {'type', 'name', 'parent_directory_ref', 'hashes', 'x_owner_ref'})
        assert(binary_obj['type'] == "file")
        assert(binary_obj['name'] == "unsecapp.exe")
        binary_parent_dir_obj = objects[binary_obj['parent_directory_ref']]
        assert(binary_parent_dir_obj is not None), "process binary parent directory ref not found"
        assert(binary_parent_dir_obj['type'] == "directory")
        assert(binary_parent_dir_obj['path'] == "C:\\Windows\\System32\\wbem")

        process_parent_ref = process_obj['parent_ref']
        assert(process_parent_ref in objects), f"parent_ref with key {process_obj['parent_ref']} not found"
        parent_obj = objects[process_parent_ref]
        assert(parent_obj.keys() == {'type', 'pid', 'binary_ref', 'command_line', 'name'})
        assert(parent_obj['type'] == "process")
        assert(parent_obj['command_line'] == "C:\\WINDOWS\\system32\\svchost.exe -k DcomLaunch -p")
        assert(parent_obj['pid'] == 1248)
        assert(parent_obj['name'] == "svchost.exe")
        binary_obj = objects[parent_obj['binary_ref']]
        assert(binary_obj is not None), "process parent binary ref not found"
        assert(binary_obj.keys() == {'type', 'name', 'parent_directory_ref'})
        assert(binary_obj['type'] == "file")
        assert(binary_obj['name'] == "svchost.exe")
        binary_parent_dir_obj = objects[binary_obj['parent_directory_ref']]
        assert(binary_parent_dir_obj is not None), "process parent binary parent directory ref not found"
        assert(binary_parent_dir_obj['type'] == "directory")
        assert(binary_parent_dir_obj['path'] == "C:\\Windows\\System32")

        file_ref = event_object['file_ref']
        assert(file_ref in objects), f"file_ref with key {event_object['file_ref']} not found"
        file_obj = objects[file_ref]
        assert(file_obj.keys() == {'type', 'name', 'parent_directory_ref'})
        assert(file_obj['type'] == 'file')
        assert(file_obj['name'] == "example.png")
        parent_obj = objects[file_obj['parent_directory_ref']]
        assert(parent_obj is not None), "file parent ref not found"
        assert(parent_obj.keys() == {'type', 'path'})
        assert(parent_obj['type'] == "directory")
        assert(parent_obj['path'] == "/home/alice")

        domain_ref = event_object['domain_ref']
        assert(domain_ref in objects), f"domain_ref with key {event_object['domain_ref']} not found"
        domain_obj = objects[domain_ref]
        assert(domain_obj.keys() == {'type', 'value'})
        assert(domain_obj['type'] == 'domain-name')
        assert(domain_obj['value'] == "domain.com")

        registry_ref = event_object['registry_ref']
        assert(registry_ref in objects), f"registry_ref with key {event_object['registry_ref']} not found"
        reg_obj = objects[registry_ref]
        assert(reg_obj['type'] == 'windows-registry-key')
        assert(reg_obj['key'] == 'HKEY_LOCAL_MACHINE\\a\\b\\c')

        network_ref = event_object['network_ref']
        assert(network_ref in objects), f"network_ref with key {event_object['network_ref']} not found"
        nt_obj = objects[network_ref]
        assert(nt_obj['type'] == 'network-traffic')

        user_ref = event_object['user_ref']
        assert(user_ref in objects), f"user_ref with key {event_object['user_ref']} not found"
        user_obj = objects[user_ref]
        assert(user_obj['type'] == 'user-account')
        assert(user_obj['user_id'] == 'USERNAME')


    def test_artifact_prop(self):
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [data])
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        artifact_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'artifact')
        assert (artifact_object is not None), 'artifact object type not found'
        assert (artifact_object.keys() ==
                {'type', 'payload_bin', 'mime_type'})
        assert (artifact_object['type'] == 'artifact')
        assert (artifact_object['payload_bin'] == 'MTAuNDIuNDIuNDIgLSAtIFswNy9EZWMvMjAxODoxMTowNTowNyArMDEwMF0gIkdFVCAvYmxvZyBIVFRQLzEuMSIgMjAwIDI1NzEgIi0iICJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xNF8wKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNzAuMC4zNTM4LjEwMiBTYWZhcmkvNTM3LjM2Ig==')
        assert (artifact_object['mime_type'] == 'text/plain')

    def test_url_prop(self):
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [data])
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        url_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'url')
        assert (url_object is not None), 'url object type not found'
        assert (url_object.keys() ==
                {'type', 'value'})
        assert (url_object['type'] == 'url')
        assert (url_object['value'] == '/blog')

    def test_file_prop(self):
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [data])
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        file_object = TestElasticEcsTransform.get_first(objects.values(), lambda o: type(o) == dict and o.get('type') == 'file' and o.get('name') == 'example.png')
        assert (file_object is not None), 'file object type not found'
        assert (file_object.keys() == {'type', 'name', 'parent_directory_ref'})
        assert (file_object['type'] == 'file')
        assert (file_object['name'] == 'example.png')
        parent_directory_ref = file_object['parent_directory_ref']
        assert(parent_directory_ref in objects), f"parent_directory_ref with key {objects['parent_directory_ref']} not found"
        parent_obj = objects[parent_directory_ref]
        assert(parent_obj['type'] == "directory")
        assert(parent_obj['path'] == "/home/alice")


    def test_unmapped_attribute_with_mapped_attribute(self):
        message = "\"GET /blog HTTP/1.1\" 200 2571"
        data = {"message": message, "unmapped": "nothing to see here"}
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [data])
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert('objects' in observed_data)
        objects = observed_data['objects']
        assert(objects == {})
        curr_obj = TestElasticEcsTransform.get_first_of_type(objects.values(), 'message')
        assert(curr_obj is None), 'url object type not found'


    def test_unmapped_attribute_alone(self):
        data = {"unmapped": "nothing to see here"}
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [data])
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert('objects' in observed_data)
        objects = observed_data['objects']
        assert(objects == {})


    def test_x_ecs_event(self):
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [ecs_event_data])
        assert (result_bundle['type'] == 'bundle')
        translation_objects = result_bundle.get('objects')
        assert (translation_objects and len(translation_objects) == 2)
        observed_data = translation_objects[1]
        stix_objects = observed_data.get("objects")
        assert (stix_objects and (stix_objects.__class__ is dict) and (len(stix_objects) > 10))
        x_oca_event = stix_objects.get("0")
        assert (x_oca_event and x_oca_event.get("type") == "x-oca-event")
        main_process = stix_objects.get("1")
        assert (
          main_process and
          main_process.get("type") == "process"
          and main_process.get("x_unique_id") == "{8dfc401c-f31c-6175-5715-000000001b00}"
        )
        parent_process_key = main_process.get("parent_ref")
        executable_file_key = main_process.get("binary_ref")
        parent_process = stix_objects.get(parent_process_key)
        assert (
          parent_process and
          parent_process.get("type") == "process" and
          parent_process.get("pid") == 2244 and
          parent_process.get("x_unique_id") == "{8dfc401c-1ef7-6175-2900-000000001b00}" and
          parent_process.get("command_line") == "C:\\Windows\\system32\\svchost.exe -k netsvcs -p -s Schedule" and
          parent_process.get("name") == "svchost.exe" and
          parent_process.get("x_exit_code") == 0 and
          parent_process.get("x_window_title") == "Just for testing" and
          parent_process.get("x_thread_id") == 3333 and
          parent_process.get("x_uptime") == 100
        )
        executable_file = stix_objects.get(executable_file_key)
        assert (
          executable_file and
          executable_file.get("type") == "file" and
          executable_file.get("name") == "dsregcmd.exe"
        )
        exec_file_hashes = executable_file.get("hashes")
        assert (
          exec_file_hashes and
          exec_file_hashes.get("MD5") == "d6957aceda86de523af0157800aa3c73" and
          exec_file_hashes.get("SHA-256") == "ba79462455b6e216d0e7cd6fe36bf0eff8a0d9dd06358d1c97b1014016256618"
        )
        exec_file_software_key = executable_file.get("x_software_ref")
        exec_file_software = stix_objects.get(exec_file_software_key)
        assert (
          exec_file_software and
          exec_file_software.get("type") == "software" and
          exec_file_software.get("name") == "dsregcmd.exe" and 
          exec_file_software.get("vendor") == "Microsoft Corporation" and
          exec_file_software.get("version") == "10.0.17763.2145 (WinBuild.160101.0800)" and
          exec_file_software.get("x_product") == "Microsoft® Windows® Operating System" and
          exec_file_software.get("x_description") == "DSREG commandline tool" 
        )

    def test_observer(self):
        result_bundle = run_in_thread(entry_point.translate_results, data_source, [observer_data])
        assert (result_bundle['type'] == 'bundle')
        translation_objects = result_bundle.get('objects')
        assert (translation_objects and len(translation_objects) == 2)
        observed_data = translation_objects[1]
        stix_objects = observed_data.get("objects")
        assert (stix_objects and (stix_objects.__class__ is dict) and (len(stix_objects) > 5))
        observer_asset = stix_objects.get("6")
        assert (
            observer_asset and observer_asset.get("type") == "x-oca-asset" and
            observer_asset.get("device_id") == "6484b65c806520073f0337894bc0cd24" and
            observer_asset.get("host_type") == "agent"
        )
        observer_geo_key = observer_asset.get("geo_ref")
        observer_geolocation = stix_objects.get(observer_geo_key)
        assert (
          observer_geolocation and
          observer_geolocation.get("type") == "x-oca-geo" and
          observer_geolocation.get("continent_name") == "North America" and
          observer_geolocation.get("region_iso_code") == "US-TX" and
          observer_geolocation.get("city_name") == "Austin" and
          observer_geolocation.get("country_iso_code") == "US" and
          observer_geolocation.get("country_name") == "United States" and
          observer_geolocation.get("region_name") == "Texas" 
        )
        observer_location = observer_geolocation.get("location")
        assert ( 
            observer_location and
            observer_location.get("lon") == -97.7419 and
            observer_location.get("lat") == 30.2732
        )
        observer_ip_key = observer_asset.get("ip_refs")[0]
        observer_ip = stix_objects.get(observer_ip_key)
        assert (
          observer_ip and 
          observer_ip.get("type") == "ipv4-addr" and
          observer_ip.get("value") == "10.0.0.101" 
        )