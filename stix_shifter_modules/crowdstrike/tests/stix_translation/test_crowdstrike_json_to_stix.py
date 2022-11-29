from stix_shifter_utils.utils.async_utils import run_in_thread
from stix_shifter_modules.crowdstrike.entry_point import EntryPoint
import json
import logging
import unittest

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

entry_point = EntryPoint()
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "crowdstrike",
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
  "cid": "cfa41c5832b1435eb0a3a8df154d2ec8",
  "created_timestamp": "2021-03-27T20:44:23.299250217Z",
  "detection_id": "ldt:e71b6d8f42584c91babfb9f18bc8f2bf:343598804908",
  "device_id": "e71b6d8f42584c91babfb9f18bc8f2bf",
  "cid": "cfa41c5832b1435eb0a3a8df154d2ec8",
  "agent_load_flags": "1",
  "agent_local_time": "2021-03-28T02:07:30.692Z",
  "agent_version": "6.14.12806.0",
  "bios_manufacturer": "VMware, Inc.",
  "bios_version": "VMW71.00V.16221537.B64.2005150253",
  "config_id_base": "65994753",
  "config_id_build": "12806",
  "config_id_platform": "3",
  "external_ip": "49.206.231.58",
  "hostname": "XFESS-LAB3",
  "first_seen": "2020-12-30T19:09:53Z",
  "last_seen": "2021-03-27T20:37:49Z",
  "local_ip": "192.168.80.132",
  "mac_address": "00-0c-29-f2-9d-5f",
  "major_version": "10",
  "minor_version": "0",
  "os_version": "Windows 10",
  "platform_id": "0",
  "platform_name": "Windows",
  "product_type": "1",
  "product_type_desc": "Workstation",
  "status": "normal",
  "system_manufacturer": "VMware, Inc.",
  "system_product_name": "VMware7,1",
  "groups": [
    "b6048dee5366448abee6bdb78a40f850"
  ],
  "modified_timestamp": "2021-03-27T20:39:13Z",
"timestamp": "2021-03-27T20:44:16Z",
"template_instance_id": "204",
"behavior_id": "10166",
"filename": "powershell.exe",
"filepath": "\\\\Device\\\\HarddiskVolume3\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0\\\\powershell.exe",
"alleged_filetype": "exe",
"cmdline": "c:\\\\windows\\\\system32\\\\cmd.exe",
"scenario": "attacker_methodology",
"objective": "Follow Through",
"tactic": "Execution",
"tactic_id": "TA0002",
"technique": "PowerShell",
"technique_id": "T1086",
"display_name": "PShellDownloadRun",
"description": "A PowerShell process downloaded and launched a remote file. This is often the result of a malicious macro designed to drop a variety of second stage payloads. Review the command line.",
"severity": 70,
"confidence": 80,
"ioc_type": "hash_sha256",
"ioc_value": "9f914d42706fe215501044acd85a32d58aaef1419d404fddfa5d3b48f66ccd9f",
"ioc_source": "library_load",
"ioc_description": "\\\\Device\\\\HarddiskVolume3\\\\Windows\\\\System32\\\\WindowsPowerShell\\\\v1.0\\\\powershell.exe",
"user_name": "crowdstrike",
"user_id": "S-1-5-21-4124038817-4173282017-4184401995-1001",
"control_graph_id": "ctg:e71b6d8f42584c91babfb9f18bc8f2bf:343598804908",
"triggering_process_graph_id": "pid:e71b6d8f42584c91babfb9f18bc8f2bf:378184249708",
"sha256": "9f914d42706fe215501044acd85a32d58aaef1419d404fddfa5d3b48f66ccd9f",
"md5": "04029e121a0cfa5991749937dd22a1d9",
"parent_sha256": "35ef26f4e71a40d0fd09939e29d39704e6fac8c0289d15108219228b4d3afe5d",
"parent_md5": "a19d650f03bcffda514b068cf2df61ba",
"parent_cmdline": "C:\\\\Windows\\\\Explorer.EXE",
"parent_process_graph_id": "pid:e71b6d8f42584c91babfb9f18bc8f2bf:378031837869",
"pattern_disposition": 2048,
"email_sent": true,
"first_behavior": "2021-03-27T20:44:16Z",
"last_behavior": "2021-03-27T20:44:16Z",
"max_confidence": 80,
"max_severity": 70,
"max_severity_displayname": "High",
"show_in_ui": true,
"status": "in_progress",
"hostinfo": {
"domain": ""
},
"seconds_to_triaged": 3761636,
"seconds_to_resolved": 0,
"behaviors_processed": [
"pid:e71b6d8f42584c91babfb9f18bc8f2bf:378184249708:10166"
]
}]}""", strict=False)


class TestCrowdStrikeTransformResults(unittest.TestCase, object):
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestCrowdStrikeTransformResults.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    @staticmethod
    def get_first_process(itr, typ):
        return TestCrowdStrikeTransformResults.get_first(itr, lambda o: type(o) == dict and o.get(
            'type') == typ and "parent_ref" in o)

    def test_change_crowdstrike_process_api_timestamp_regex(self):
        results = process_data_1["results"].copy()
        results[0]['start'] = "2019-01-22T00:04:52.87Z"
        result_bundle = run_in_thread(entry_point.translate_results, data_source, results)

        assert (result_bundle['type'] == 'bundle')

    def test_change_crowdstrike_process_api_results_to_stix(self):
        results = process_data_1["results"]
        result_bundle = run_in_thread(entry_point.translate_results, data_source, results)

        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        curr_obj = TestCrowdStrikeTransformResults.get_first_of_type(objects.values(), 'file')
        file_obj = curr_obj  # for later
        assert (curr_obj is not None), 'file object type not found'
        assert (curr_obj.keys() == {'type', 'name', 'hashes', 'parent_directory_ref'})
        assert (curr_obj['name'] == "powershell.exe")
        assert (curr_obj['hashes']['MD5'] == '04029e121a0cfa5991749937dd22a1d9')
        assert (curr_obj['hashes']['SHA-256'] == '9f914d42706fe215501044acd85a32d58aaef1419d404fddfa5d3b48f66ccd9f')

        curr_obj = TestCrowdStrikeTransformResults.get_first_of_type(objects.values(), 'x-oca-event')
        event_obj = curr_obj  # used in later test
        assert (curr_obj is not None), 'file object type not found'
        assert (curr_obj.keys() == {'type', 'host_ref', 'created', 'process_ref', 'action', 'outcome', 'severity', 'parent_process_ref'})
        assert (curr_obj['action'] == 'PShellDownloadRun')
        assert (curr_obj['severity'] == 70)

        curr_obj = objects[event_obj['host_ref']]
        assert (curr_obj is not None), 'file object type not found'
        assert (curr_obj.keys() == {'type', 'ip_refs', 'hostname', 'mac_refs', 'os_version', 'os_platform'})
        assert (curr_obj['hostname'] == 'XFESS-LAB3')
        assert (curr_obj['os_version'] == 'Windows 10')
        assert (curr_obj['os_platform'] == 'Windows')

        curr_obj = TestCrowdStrikeTransformResults.get_first_of_type(objects.values(), 'user-account')
        assert (curr_obj is not None), 'user-account object type not found'
        assert (curr_obj.keys() == {'type', 'user_id', 'account_login'})
        assert (curr_obj['account_login'] == 'crowdstrike')
        assert (curr_obj['user_id'] == 'S-1-5-21-4124038817-4173282017-4184401995-1001')

        curr_obj = TestCrowdStrikeTransformResults.get_first_process(objects.values(), 'process')
        assert (curr_obj is not None), 'process object type not found'
        assert (curr_obj.keys() == {'type', 'binary_ref', 'name', 'command_line', 'creator_user_ref', 'pid', 'parent_ref'})
        assert (curr_obj['command_line'] == 'c:\\windows\\system32\\cmd.exe')
        assert (curr_obj['name'] == 'powershell.exe')

        assert (file_obj == objects[curr_obj['binary_ref']]), 'process binary_ref does not point to the correct object'

        parent_index = curr_obj['parent_ref']
        curr_obj = objects[parent_index]
        assert (curr_obj is not None)
        assert (curr_obj.keys() == {'type', 'binary_ref', 'command_line', 'pid'})
        assert (curr_obj['command_line'] == 'C:\\Windows\\Explorer.EXE')


