from stix_shifter.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter.stix_translation.src import transformers
from stix_shifter.stix_translation import stix_translation
from stix_shifter.stix_translation.src.modules.carbonblack import carbonblack_translator
from stix2validator import validate_instance

import json
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

interface = carbonblack_translator.Translator()
map_file = open(interface.mapping_filepath).read()
map_data = json.loads(map_file)
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "CarbonBlack",
    "identity_class": "events"
}
options = {}


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

    def test_change_cb_to_stix(self):
        data = json.loads("""
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

        results = data["results"]
        result_bundle = json_to_stix_translator.convert_to_stix(data_source, map_data, results, transformers.get_all_transformers(), options)
        print(result_bundle)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        curr_obj = TestCarbonBlackTransformResults.get_first_of_type(objects.values(), 'file')
        assert(curr_obj is not None), 'file object type not found'
        assert(curr_obj.keys() == {'type', 'name', 'hashes'})
        assert(curr_obj['name'] == "cmd.exe")
        assert(curr_obj['hashes']['MD5'] == "5746bd7e255dd6a8afa06f7c42c1ba41")

        curr_obj = TestCarbonBlackTransformResults.get_first_of_type(objects.values(), 'ipv4-addr')
        assert(curr_obj is not None), 'file object type not found'
        assert(curr_obj.keys() == {'type', 'value'})
        assert(curr_obj['value'] == "12.166.224.2")
