from stix_shifter_utils.utils.async_utils import run_in_thread
from stix_shifter_modules.carbonblack.entry_point import EntryPoint
import json
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
options = {
    "events_mode": True
}
entry_point = EntryPoint(options=options)
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "CarbonBlack",
    "identity_class": "events"
}


event_data_1 = json.loads(
    """
[{
  "device_os": "windows",
  "device_name": "il009210-tp",
  "host_type": "workstation",
  "process_pid": 25160,
  "process_name": "wermgr.exe",
  "parent_pid": 2040,
  "parent_name": "svchost.exe",
  "process_cmdline": "C:\\\\WINDOWS\\\\system32\\\\wermgr.exe -upload",
  "interface_ip": -1062728174,
  "device_external_ip": 1833104680,
  "provider": "Carbon Black Response",
  "event_type": "filemod",
  "event_timestamp": "2021-04-04T20:17:38.590000Z",
  "filemod_name": "c:\\\\programdata\\\\microsoft\\\\windows\\\\wer\\\\temp\\\\7fb39f69-3a0a-4b59-8afb-0bd9667730d1",
  "filemod_action": "Created the file",
  "filemod_md5": ""
}]
    """)

event_data_2 = json.loads(
    """
[{
  "device_os": "windows",
  "device_name": "win01",
  "host_type": "server",
  "process_pid": 2636,
  "process_name": "conhost.exe",
  "parent_pid": 2552,
  "parent_name": "cscript.exe",
  "process_cmdline": "C:\\\\Windows\\\\system32\\\\conhost.exe 0xffffffff -ForceV1",
  "interface_ip": 160756778,
  "device_external_ip": -1626848542,
  "provider": "Carbon Black Response",
  "event_type": "crossproc",
  "event_timestamp": "2021-04-05T01:52:46.594000Z",
  "crossproc_name": "c:\\\\program files (x86)\\\\bigfix enterprise\\\\bes client\\\\besclient.exe",
  "crossproc_action": "ProcessOpen",
  "crossproc_md5": "f0012c0845a1b35357603ad4079eef28"
}]
    """
)


class TestCarbonBlackTransformEventsResults(unittest.TestCase, object):
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestCarbonBlackTransformEventsResults.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    @staticmethod
    def get_first_process(itr, typ):
        return TestCarbonBlackTransformEventsResults.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ and "parent_ref" in o)

    def test_change_cb_process_api_timestamp_regex(self):
        results = event_data_1.copy()
        results[0]['event_timestamp'] = "2021-04-05T01:52:46.594000Z"
        result_bundle = run_in_thread(entry_point.translate_results, data_source, results)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert(observed_data['created'] is not None)
        assert(observed_data['modified'] is not None)
        assert(observed_data['first_observed'] == "2021-04-05T01:52:46.594000Z")
        assert(observed_data['last_observed'] =="2021-04-05T01:52:46.594000Z")

    def test_change_cb_process_api_results_to_stix(self):

        results = event_data_2.copy()
        result_bundle = run_in_thread(entry_point.translate_results, data_source, results)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        curr_obj = TestCarbonBlackTransformEventsResults.get_first_of_type(objects.values(), 'x-oca-event')
        event_obj = curr_obj  # used in later test
        assert(event_obj is not None), 'file object type not found'
        assert(event_obj.keys() == {'type', 'host_ref', 'process_ref','provider','category','created','cross_process_target_ref', 'action'})
        assert(curr_obj['action'] == "ProcessOpen")
        assert(curr_obj['category'] == "crossproc")

        curr_obj = TestCarbonBlackTransformEventsResults.get_first_of_type(objects.values(), 'file')
        file_obj = curr_obj  # used in later test
        assert(curr_obj is not None), 'user-account object type not found'
        assert(curr_obj.keys() == {'type', 'name'})
        assert(curr_obj['name'] == "conhost.exe")

        curr_obj = TestCarbonBlackTransformEventsResults.get_first_process(objects.values(), 'process')
        process_obj = curr_obj
        assert(process_obj is not None), 'process object type not found'
        assert(process_obj.keys() == {'type', 'command_line', 'binary_ref', 'parent_ref', 'name', 'pid'})
        assert(process_obj['command_line'] == "C:\\Windows\\system32\\conhost.exe 0xffffffff -ForceV1")
        assert(process_obj['pid'] == 2636)

        assert(process_obj == objects[event_obj['process_ref']]), 'process binary_ref does not point to the correct object'
        assert(file_obj == objects[process_obj['binary_ref']]), 'process creator_user_ref does not point to the correct object'

        parent_index = process_obj['parent_ref']
        curr_obj = objects[parent_index]
        assert(curr_obj is not None)
        assert(curr_obj.keys() == {'type', 'pid', 'name'})
        assert(curr_obj['pid'] == 2552)
        assert(curr_obj['name'] == "cscript.exe")

        assert(observed_data['created'] is not None)
        assert(observed_data['modified'] is not None)
        assert(observed_data['first_observed'] == "2021-04-05T01:52:46.594000Z")
        assert(observed_data['last_observed'] == "2021-04-05T01:52:46.594000Z")

    def test_merge_results_mixed_to_stix(self):
        results = event_data_2.copy()
        result_bundle = run_in_thread(entry_point.translate_results, data_source, results)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        assert(len(result_bundle_objects) == 2)

        objects = result_bundle_objects[1]['objects']
        types = [o.get('type') for o in objects.values()]
        assert (types == ['x-oca-asset', 'x-oca-event', 'process', 'file', 'process', 'ipv4-addr', 'x-cb-response', 'file', 'directory', 'process'])
        assert (result_bundle_objects[1]['number_observed'] == 1)

        start_time = "2021-04-05T01:52:46.594000Z"
        last_time = "2021-04-05T01:52:46.594000Z"

        assert(result_bundle_objects[1]['created'] is not None)
        assert(result_bundle_objects[1]['modified'] is not None)
        assert(result_bundle_objects[1]['first_observed'] == start_time)
        assert(result_bundle_objects[1]['last_observed'] == last_time)
