from stix_shifter_modules.carbonblack.entry_point import EntryPoint
import json
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

entry_point = EntryPoint()
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

    @staticmethod
    def get_first_process(itr, typ):
        return TestCarbonBlackTransformResults.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ and "parent_ref" in o)

    def test_change_cb_process_api_timestamp_regex(self):
        results = process_data_1["results"].copy()
        results[0]['start'] = "2019-01-22T00:04:52.87Z"
        result_bundle = entry_point.translate_results(data_source, results)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert(observed_data['created'] is not None)
        assert(observed_data['modified'] is not None)
        assert(observed_data['first_observed'] == "2019-01-22T00:04:52.87Z")
        assert(observed_data['last_observed'] == "2019-01-22T00:04:52.937Z")

    def test_change_cb_process_api_results_to_stix(self):

        results = process_data_1["results"]
        result_bundle = entry_point.translate_results(data_source, results)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        curr_obj = TestCarbonBlackTransformResults.get_first_of_type(objects.values(), 'file')
        file_obj = curr_obj  # used in later test
        assert(curr_obj is not None), 'file object type not found'
        assert(curr_obj.keys() == {'type', 'name', 'hashes', 'parent_directory_ref'})
        assert(curr_obj['name'] == "cmd.exe")
        assert(curr_obj['hashes']['MD5'] == "5746bd7e255dd6a8afa06f7c42c1ba41")

        curr_obj = TestCarbonBlackTransformResults.get_first_of_type(objects.values(), 'user-account')
        user_obj = curr_obj  # used in later test
        assert(curr_obj is not None), 'user-account object type not found'
        assert(curr_obj.keys() == {'type', 'user_id'})
        assert(curr_obj['user_id'] == "SYSTEM")

        curr_obj = TestCarbonBlackTransformResults.get_first_process(objects.values(), 'process')
        assert(curr_obj is not None), 'process object type not found'
        assert(curr_obj.keys() == {'type', 'command_line', 'creator_user_ref', 'binary_ref', 'parent_ref', 'created', 'name', 'pid', 'x_id', 'x_unique_id'})
        assert(curr_obj['command_line'] == "C:\\Windows\\system32\\cmd.exe /c tasklist")
        assert(curr_obj['created'] == "2019-01-22T00:04:52.875Z")
        assert(curr_obj['pid'] == 1896)

        assert(file_obj == objects[curr_obj['binary_ref']]), 'process binary_ref does not point to the correct object'
        assert(user_obj == objects[curr_obj['creator_user_ref']]), 'process creator_user_ref does not point to the correct object'

        parent_index = curr_obj['parent_ref']
        curr_obj = objects[parent_index]
        assert(curr_obj is not None)
        assert(curr_obj.keys() == {'type', 'pid', 'name', 'x_id', 'x_unique_id'})
        assert(curr_obj['pid'] == 2508)
        assert(curr_obj['name'] == "cmd.exe")

        assert(observed_data['created'] is not None)
        assert(observed_data['modified'] is not None)
        assert(observed_data['first_observed'] == "2019-01-22T00:04:52.875Z")
        assert(observed_data['last_observed'] == "2019-01-22T00:04:52.937Z")

    def test_merge_results_mixed_to_stix(self):
        results = process_data_2["results"]
        result_bundle = entry_point.translate_results(data_source, results)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        assert(len(result_bundle_objects) == 3)

        objects = result_bundle_objects[1]['objects']
        types = [o.get('type') for o in objects.values()]
        assert (types == ['file', 'x-cb-response', 'process', 'process', 'x-oca-asset', 'ipv4-addr', 'user-account', 'directory'])
        assert (result_bundle_objects[1]['number_observed'] == 1)

        start_time = "2018-12-17T08:37:13.318Z"
        last_time = "2018-12-17T08:37:13.396Z"

        assert(result_bundle_objects[1]['created'] is not None)
        assert(result_bundle_objects[1]['modified'] is not None)
        assert(result_bundle_objects[1]['first_observed'] == start_time)
        assert(result_bundle_objects[1]['last_observed'] == last_time)
