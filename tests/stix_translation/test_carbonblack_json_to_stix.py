from stix_shifter.stix_translation.src.modules.carbonblack import carbonblack_translator
import json
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

interface = carbonblack_translator.Translator()
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "CarbonBlack",
    "identity_class": "events"
}
options = {}


process_data_1 = json.loads("""
{
  "terms": [
    "process_name:cmd.exe",
    "start:[2019-01-22T00:00:00 TO *]"
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
      "cmdline": "C:\\\\Windows\\\\system32\\\\cmd.exe /c tasklist",
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
      "comms_ip": -1051309706,
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
      "path": "c:\\\\windows\\\\system32\\\\cmd.exe",
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
}""")


binary_data_1 = json.loads("""
{
  "terms": [
    "md5:F5AE03DE0AD60F5B17B82F2CD68402FE"
  ],
  "total_results": 1,
  "highlights": [
    {
      "name": "PREPREPREF5AE03DE0AD60F5B17B82F2CD68402FEPOSTPOSTPOST",
      "ids": [
        "F5AE03DE0AD60F5B17B82F2CD68402FE"
      ]
    }
  ],
  "facets": {},
  "results": [
    {
      "host_count": 13,
      "alliance_updated_srstrust": "2016-09-04T04:59:53Z",
      "original_filename": "Cmd.Exe.MUI",
      "legal_copyright": "\u00a9 Microsoft Corporation. All rights reserved.",
      "digsig_result": "Signed",
      "observed_filename": [
        "c:\\\\windows\\\\system32\\\\cmd.exe"
      ],
      "product_version": "6.3.9600.16384",
      "alliance_score_srstrust": -100,
      "watchlists": [
        {
          "wid": "5",
          "value": "2016-10-19T10:20:05.424Z"
        }
      ],
      "facet_id": 431419,
      "copied_mod_len": 357376,
      "server_added_timestamp": "2016-10-19T10:00:25.734Z",
      "digsig_sign_time": "2014-11-07T08:02:00Z",
      "orig_mod_len": 357376,
      "alliance_data_srstrust": [
        "f5ae03de0ad60f5b17b82f2cd68402fe"
      ],
      "is_executable_image": true,
      "is_64bit": true,
      "md5": "F5AE03DE0AD60F5B17B82F2CD68402FE",
      "digsig_publisher": "Microsoft Corporation",
      "endpoint": [
        "ADTWO|24",
        "ADONE|26",
        "CERT|27",
        "REPO|29",
        "adone|26",
        "cert|27",
        "adtwo|24",
        "iestestmachine3|53",
        "iestestmachine0|52",
        "iestestmachine1|54"
      ],
      "group": [ "CTF Lab", "Default Group", "ctf lab", "default group" ],
      "event_partition_id": [ 97777295491072, 97794283536384, 97811271778304, 97828260020224, 97845247737856, 97862235979776, 97879224221696, 97896211152896, 97913199394816 ],
      "digsig_result_code": "0",
      "file_version": "6.3.9600.16384 (winblue_rtm.130821-1623)",
      "signed": "Signed",
      "alliance_link_srstrust": "https://services.bit9.com/Services/extinfo.aspx?ak=b8b4e631d4884ad1c56f50e4a5ee9279&sg=0313e1735f6cec221b1d686bd4de23ee&md5=f5ae03de0ad60f5b17b82f2cd68402fe",
      "company_name": "Microsoft Corporation",
      "internal_name": "cmd",
      "timestamp": "2016-10-19T10:00:25.734Z",
      "cb_version": 624,
      "os_type": "Windows",
      "file_desc": "Windows Command Processor",
      "product_name": "Microsoft\u00ae Windows\u00ae Operating System",
      "last_seen": "2019-01-14T03:19:05.687Z"
    }
  ],
  "elapsed": 0.02470088005065918,
  "start": 0
}""")

process_data_2 = json.loads("""
{
  "terms": [
    "process_name:cmd.exe"
  ],
  "results": [
    {
      "process_md5": "5746bd7e255dd6a8afa06f7c42c1ba41",
      "sensor_id": 50,
      "filtering_known_dlls": false,
      "modload_count": 16,
      "parent_unique_id": "00000032-0000-0a04-01d4-8bc245c6c9e6-000000000001",
      "emet_count": 0,
      "cmdline": "cmd /c \\"\\"C:\\\\ProgramData\\\\VMware\\\\VMware CAF\\\\pme\\\\\\\\config\\\\..\\\\scripts\\\\is-listener-running.bat\\" \\"",
      "filemod_count": 0,
      "id": "00000032-0000-0888-01d4-95e3b558aacb",
      "parent_name": "managementagenthost.exe",
      "parent_md5": "000000000000000000000000000000",
      "group": "mdr redlab",
      "parent_id": "00000032-0000-0a04-01d4-8bc245c6c9e6",
      "hostname": "redlab-vuln2",
      "last_update": "2018-12-17T08:37:13.396Z",
      "start": "2018-12-17T08:37:13.318Z",
      "comms_ip": 212262914,
      "regmod_count": 0,
      "interface_ip": 183439305,
      "process_pid": 2184,
      "username": "SYSTEM",
      "terminated": false,
      "process_name": "cmd.exe",
      "emet_config": "",
      "last_server_update": "2019-02-01T18:44:10.53Z",
      "path": "c:\\\\windows\\\\system32\\\\cmd.exe",
      "netconn_count": 0,
      "parent_pid": 2564,
      "crossproc_count": 2,
      "segment_id": 1549046650410,
      "host_type": "workstation",
      "processblock_count": 0,
      "os_type": "windows",
      "childproc_count": 8,
      "unique_id": "00000032-0000-0888-01d4-95e3b558aacb-0168aa60162a"
    },
    {
      "process_md5": "5746bd7e255dd6a8afa06f7c42c1ba41",
      "sensor_id": 50,
      "filtering_known_dlls": false,
      "modload_count": 16,
      "parent_unique_id": "00000032-0000-0a04-01d4-8bc245c6c9e6-000000000001",
      "emet_count": 0,
      "cmdline": "cmd /c \\"\\"C:\\\\ProgramData\\\\VMware\\\\VMware CAF\\\\pme\\\\\\\\config\\\\..\\\\scripts\\\\is-listener-running.bat\\" \\"",
      "filemod_count": 0,
      "id": "00000032-0000-0888-01d4-95e3b558aacb",
      "parent_name": "managementagenthost.exe",
      "parent_md5": "000000000000000000000000000000",
      "group": "mdr redlab",
      "parent_id": "00000032-0000-0a04-01d4-8bc245c6c9e6",
      "hostname": "redlab-vuln2",
      "last_update": "2018-12-17T08:37:13.396Z",
      "start": "2018-12-17T08:37:13.318Z",
      "comms_ip": 212262914,
      "regmod_count": 0,
      "interface_ip": 183439305,
      "process_pid": 2184,
      "username": "SYSTEM",
      "terminated": false,
      "process_name": "cmd.exe",
      "alliance_data_attackframework": [
        "565594"
      ],
      "emet_config": "",
      "last_server_update": "2019-02-01T18:50:32.875Z",
      "path": "c:\\\\windows\\\\system32\\\\cmd.exe",
      "alliance_score_attackframework": 1,
      "netconn_count": 0,
      "parent_pid": 2564,
      "crossproc_count": 2,
      "alliance_link_attackframework": "https://attack.mitre.org/wiki/Technique/T1082",
      "segment_id": 1549047032875,
      "watchlists": [
        {
          "segments_hit": [
            1549046650410
          ],
          "wid": "1154",
          "value": "2019-02-01T18:50:06.003Z"
        }
      ],
      "host_type": "workstation",
      "processblock_count": 0,
      "alliance_updated_attackframework": "2018-10-16T20:15:04Z",
      "os_type": "windows",
      "childproc_count": 8,
      "unique_id": "00000032-0000-0888-01d4-95e3b558aacb-0168aa65ec2b"
    }
  ],
  "elapsed": 0.023807048797607422,
  "comprehensive_search": true,
  "all_segments": true,
  "total_results": 77835,
  "highlights": [
    {
      "name": "PREPREPREcmd.exePOSTPOSTPOST",
      "ids": [
        "00000032-0000-0888-01d4-95e3b558aacb-0168aa60162a",
        "00000032-0000-0888-01d4-95e3b558aacb-0168aa65ec2b"
      ]
    },
    {
      "name": "C:\\\\Windows\\\\system32\\\\PREPREPREcmd.exePOSTPOSTPOST  /S /D /c\\" echo\\"",
      "ids": [
        "00000032-0000-0888-01d4-95e3b558aacb-0168aa60162a"
      ]
    },
    {
      "name": "c:\\\\windows\\\\system32\\\\PREPREPREcmd.exePOSTPOSTPOST",
      "ids": [
        "00000032-0000-0888-01d4-95e3b558aacb-0168aa60162a",
        "00000032-0000-0888-01d4-95e3b558aacb-0168aa65ec2b"
      ]
    }
  ],
  "facets": {},
  "tagged_pids": {},
  "start": 0,
  "incomplete_results": false,
  "filtered": {}
}
""")

binary_data_2 = json.loads("""
{
  "terms": [
    "observed_filename:notepad.exe"
  ],
  "total_results": 10,
  "highlights": [
    {
      "name": "c:\\\\windows\\\\system32\\\\PREPREPREnotepad.exePOSTPOSTPOST",
      "ids": [
        "FC2EA5BD5307D2CFA5AAA38E0C0DDCE9",
        "959A31D0CD013CEA0C66DB7C03BCBDDF"
      ]
    }
  ],
  "facets": {},
  "results": [
    {
      "host_count": 4,
      "alliance_updated_srstrust": "2017-11-05T07:05:38Z",
      "original_filename": "NOTEPAD.EXE",
      "legal_copyright": "\\u00a9 Microsoft Corporation. All rights reserved.",
      "digsig_result": "Signed",
      "observed_filename": [
        "c:\\\\windows\\\\system32\\\\notepad.exe"
      ],
      "product_version": "6.3.9600.17930",
      "alliance_score_srstrust": -100,
      "watchlists": [
        {
          "wid": "5",
          "value": "2017-03-14T10:10:05.217Z"
        }
      ],
      "facet_id": 2272,
      "copied_mod_len": 221184,
      "server_added_timestamp": "2017-03-14T10:04:35.779Z",
      "digsig_sign_time": "2015-07-11T00:18:00Z",
      "orig_mod_len": 221184,
      "alliance_data_srstrust": [
        "fc2ea5bd5307d2cfa5aaa38e0c0ddce9"
      ],
      "is_executable_image": true,
      "is_64bit": true,
      "md5": "FC2EA5BD5307D2CFA5AAA38E0C0DDCE9",
      "digsig_publisher": "Microsoft Corporation",
      "endpoint": [
        "REPO|29",
        "VSPHERE|28",
        "vsphere|28",
        "iestestmachine1|54"
      ],
      "group": [
        "CTF Lab",
        "ctf lab",
        "default group"
      ],
      "event_partition_id": [
        97777295491072,
        98439833845760,
        98847548112896,
        99679970852864,
        101310831263744
      ],
      "digsig_result_code": "0",
      "file_version": "6.3.9600.17930 (winblue_ltsb.150709-0600)",
      "signed": "Signed",
      "alliance_link_srstrust": "https://services.bit9.com/Services/extinfo.aspx?ak=b8b4e631d4884ad1c56f50e4a5ee9279&sg=0313e1735f6cec221b1d686bd4de23ee&md5=fc2ea5bd5307d2cfa5aaa38e0c0ddce9",
      "company_name": "Microsoft Corporation",
      "internal_name": "Notepad",
      "timestamp": "2017-03-14T10:04:35.779Z",
      "cb_version": 624,
      "os_type": "Windows",
      "file_desc": "Notepad",
      "product_name": "Microsoft\\u00ae Windows\\u00ae Operating System",
      "last_seen": "2018-12-29T12:41:54.355Z"
    },
    {
      "host_count": 1,
      "original_filename": "NOTEPAD.EXE",
      "legal_copyright": "\\u00a9 Microsoft Corporation. All rights reserved.",
      "digsig_result": "Signed",
      "observed_filename": [
        "c:\\\\windows\\\\system32\\\\notepad.exe"
      ],
      "product_version": "6.3.9600.17415",
      "watchlists": [
        {
          "wid": "5",
          "value": "2017-04-12T21:10:04.604Z"
        }
      ],
      "facet_id": 87425,
      "copied_mod_len": 221184,
      "server_added_timestamp": "2017-04-12T21:06:15.216Z",
      "digsig_sign_time": "2014-11-07T07:55:00Z",
      "orig_mod_len": 221184,
      "is_executable_image": true,
      "is_64bit": true,
      "md5": "959A31D0CD013CEA0C66DB7C03BCBDDF",
      "digsig_publisher": "Microsoft Corporation",
      "endpoint": [
        "REPO|31"
      ],
      "group": [
        "Default Group"
      ],
      "event_partition_id": [
        97777295491072
      ],
      "digsig_result_code": "0",
      "file_version": "6.3.9600.17415 (winblue_r4.141028-1500)",
      "signed": "Signed",
      "company_name": "Microsoft Corporation",
      "internal_name": "Notepad",
      "timestamp": "2017-04-12T21:06:15.216Z",
      "cb_version": 610,
      "os_type": "Windows",
      "file_desc": "Notepad",
      "product_name": "Microsoft\\u00ae Windows\\u00ae Operating System",
      "last_seen": "2017-04-12T21:10:06.095Z"
    }
  ],
  "elapsed": 0.011963844299316406,
  "start": 0
}
""")


class TestCarbonBlackTransformResults(unittest.TestCase, object):
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestCarbonBlackTransformResults.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    def test_change_cb_process_api_timestamp_regex(self):
        results = process_data_1["results"].copy()
        results[0]['start'] = "2019-01-22T00:04:52.87Z"
        timestamp_bug_options = {'cybox_default': True}
        result_bundle = json.loads(interface.translate_results(json.dumps(data_source), json.dumps(results), timestamp_bug_options))

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert(observed_data['created'] is not None)
        assert(observed_data['modified'] is not None)
        assert(observed_data['first_observed'] == "2019-01-22T00:04:52.87Z")
        assert(observed_data['last_observed'] == "2019-01-22T00:04:52.87Z")

    def test_change_cb_process_api_results_to_stix(self):

        results = process_data_1["results"]
        result_bundle = json.loads(interface.translate_results(json.dumps(data_source), json.dumps(results), options))

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        curr_obj = TestCarbonBlackTransformResults.get_first_of_type(objects.values(), 'file')
        file_obj = curr_obj  # used in later test
        assert(curr_obj is not None), 'file object type not found'
        assert(curr_obj.keys() == {'type', 'name', 'hashes'})
        assert(curr_obj['name'] == "cmd.exe")
        assert(curr_obj['hashes']['MD5'] == "5746bd7e255dd6a8afa06f7c42c1ba41")

        curr_obj = TestCarbonBlackTransformResults.get_first_of_type(objects.values(), 'user-account')
        user_obj = curr_obj  # used in later test
        assert(curr_obj is not None), 'user-account object type not found'
        assert(curr_obj.keys() == {'type', 'user_id'})
        assert(curr_obj['user_id'] == "SYSTEM")

        curr_obj = TestCarbonBlackTransformResults.get_first_of_type(objects.values(), 'network-traffic')
        network_obj = curr_obj  # used in later test
        assert(curr_obj is not None), 'network-traffic object type not found'
        assert(curr_obj.keys() == {'type', 'src_ref', 'dst_ref'})
        assert(objects[curr_obj['src_ref']]['value'] == "10.239.15.200")
        assert(objects[curr_obj['dst_ref']]['value'] == "193.86.73.118")

        curr_obj = TestCarbonBlackTransformResults.get_first_of_type(objects.values(), 'process')
        assert(curr_obj is not None), 'process object type not found'
        assert(curr_obj.keys() == {'type', 'command_line', 'creator_user_ref', 'binary_ref', 'parent_ref', 'created', 'name', 'pid', 'opened_connection_refs'})
        assert(curr_obj['command_line'] == "C:\\Windows\\system32\\cmd.exe /c tasklist")
        assert(curr_obj['created'] == "2019-01-22T00:04:52.875Z")
        assert(curr_obj['pid'] == 1896)

        assert(network_obj == objects[curr_obj['opened_connection_refs'][0]]), 'open_connection_refs does not point to the correct object'
        assert(file_obj == objects[curr_obj['binary_ref']]), 'process binary_ref does not point to the correct object'
        assert(user_obj == objects[curr_obj['creator_user_ref']]), 'process creator_user_ref does not point to the correct object'

        parent_index = curr_obj['parent_ref']
        curr_obj = objects[parent_index]
        assert(curr_obj is not None)
        assert(curr_obj.keys() == {'type', 'pid', 'name', 'binary_ref'})
        assert(curr_obj['pid'] == 2508)
        assert(curr_obj['name'] == "cmd.exe")
        assert(objects[curr_obj['binary_ref']]['name'] == "cmd.exe")

        assert(observed_data['created'] is not None)
        assert(observed_data['modified'] is not None)
        assert(observed_data['first_observed'] == "2019-01-22T00:04:52.875Z")
        assert(observed_data['last_observed'] == "2019-01-22T00:04:52.875Z")

    def test_change_cb_binary_api_results_to_stix(self):
        results = binary_data_1["results"]
        result_bundle = json.loads(interface.translate_results(json.dumps(data_source), json.dumps(results), options))

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        curr_obj = TestCarbonBlackTransformResults.get_first_of_type(objects.values(), 'file')
        file_obj = curr_obj  # used in later test
        assert(curr_obj is not None), 'file object type not found'
        assert(curr_obj.keys() == {'type', 'name', 'created', 'hashes'})
        assert(curr_obj['name'] == "Cmd.Exe.MUI")
        assert(curr_obj['hashes']['MD5'] == "F5AE03DE0AD60F5B17B82F2CD68402FE")

        assert(observed_data['created'] is not None)
        assert(observed_data['modified'] is not None)
        assert(observed_data['first_observed'] == "2016-10-19T10:00:25.734Z")
        assert(observed_data['last_observed'] == "2016-10-19T10:00:25.734Z")
        assert(observed_data['number_observed'] == 1)

    def test_merge_results_mixed_to_stix(self):
        results = process_data_2["results"] + binary_data_2["results"]  # we assume the data pipeline will combine the results in a list
        result_bundle = json.loads(interface.translate_results(json.dumps(data_source), json.dumps(results), options))

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        assert(len(result_bundle_objects) == 5)

        objects = result_bundle_objects[1]['objects']
        types = [o.get('type') for o in objects.values()]
        assert (types == ['file', 'process', 'file', 'process', 'domain-name', 'ipv4-addr', 'network-traffic', 'ipv4-addr', 'user-account'])
        assert (result_bundle_objects[1]['number_observed'] == 1)

        file_start_time = "2018-12-17T08:37:13.318Z"

        assert(result_bundle_objects[1]['created'] is not None)
        assert(result_bundle_objects[1]['modified'] is not None)
        assert(result_bundle_objects[1]['first_observed'] == file_start_time)
        assert(result_bundle_objects[1]['last_observed'] == file_start_time)

        objects = result_bundle_objects[4]['objects']
        types = [o.get('type') for o in objects.values()]
        assert (types == ['file'])

        binary_time = "2017-04-12T21:06:15.216Z"
        assert (result_bundle_objects[4]['number_observed'] == 1)

        assert(result_bundle_objects[4]['created'] is not None)
        assert(result_bundle_objects[4]['modified'] is not None)
        assert(result_bundle_objects[4]['first_observed'] == binary_time)
        assert(result_bundle_objects[4]['last_observed'] == binary_time)
