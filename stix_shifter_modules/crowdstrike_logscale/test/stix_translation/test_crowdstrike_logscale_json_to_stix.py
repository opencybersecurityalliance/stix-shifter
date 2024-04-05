""" test script to perform unit test case for CrowdStrike Falcon LogScale translate results """
import unittest
from stix_shifter_modules.crowdstrike_logscale.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "crowdstrike_logscale"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "crowdstrike_logscale",
    "identity_class": "events"
}
options = {}

logscale_sample_response = {
    'crowdstrikeedr': {
        '@timestamp': 1700059736377,
        '@timestamp.nanos': '312000',
        '#repo': 'TestRepository',
        '#type': 'CrowdStrike_Spotlight',
        '@id': '3sAoxxxxWl4Y_3_190_17xxxx36',
        '@ingesttimestamp': '1700059737501',
        '@rawstring': '{"cid": "ef21xxxxxxxxxxxxxxxxxxxxxxxxxxx440d",'
                      '"created_timestamp": "2023-09-12T11:46:19.787962809Z",'
                      ' "detection_id": "ldt:7adbxxxxxxxx0d49:103079284165",'
                      ' "device": {"device_id": "7adbxxxxxxxx0d49",'
                      ' "cid": "ef21xxxxxxxxxxxxxxxxxxxxxxxxxxx440d", "agent_load_flags": "1",'
                      ' "agent_local_time": "2023-09-12T08:30:15.487Z", "agent_version": "6.58.17212.0",'
                      ' "bios_manufacturer": "Xen", "bios_version": "4.11.hp",'
                      ' "config_id_base": "65994763", "config_id_build": "17212", "config_id_platform": "3",'
                      ' "external_ip": "1.1.2.2", "hostname": "CROWDST",'
                      ' "first_seen": "2023-05-16T05:10:55Z", "last_seen": "2023-09-12T11:24:19Z",'
                      ' "local_ip": "172.0.0.1", "mac_address": "12-11-11-11-11-11",'
                      ' "major_version": "10", "minor_version": "0", "os_version": "Windows Server 2022",'
                      ' "platform_id": "0", "platform_name": "Windows", "product_type": "3",'
                      ' "product_type_desc": "Server", "status": "normal", "system_manufacturer": "Xen",'
                      ' "system_product_name": "HVM domU",'
                      ' "groups": ["97350feebe4541e8a615c0d3f18acdf3","bb1exxxxxxxxxxxxxxxxxxxxxxxxxxb23d"],'
                      ' "modified_timestamp": "2023-09-12T11:45:57Z", "instance_id": "065fxxxxxxxxxx27ce",'
                      ' "service_provider": "WINDOWS_V2", "service_provider_account_id": "1xxxxxxxxxxxx2"},'
                      ' "behaviors": [{"device_id": "7adbxxxxxxxx0d49",'
                      ' "timestamp": "2023-09-12T11:46:12Z", "template_instance_id": "3",'
                      ' "behavior_id": "41002", "filename": "calc.exe",'
                      ' "filepath": "\\\\Device\\\\HarddiskVolume1\\\\Windows\\\\System32\\\\calc.exe",'
                      ' "alleged_filetype": "exe", "cmdline": "calc", "scenario": "suspicious_activity",'
                      ' "objective": "Falcon Detection Method", "tactic": "Custom Intelligence",'
                      ' "tactic_id": "CSTA0005", "technique": "Indicator of Attack", "technique_id": "CST0004",'
                      ' "display_name": "CustomIOAWinMedium",'
                      ' "description": "A process triggered a medium severity custom rule.",'
                      ' "severity": 50, "confidence": 100, "ioc_type": "hash_sha256",'
                      ' "ioc_value": "4208xxxx2554da89f45xxxx3bbd",'
                      ' "ioc_source": "library_load",'
                      ' "ioc_description": "\\\\Device\\\\HarddiskVolume1\\\\Windows\\\\System32\\\\calc.exe",'
                      ' "user_name": "testuser", "user_id": "S-1-5-21-xxxx-16xxxx15-312xxxx6-500",'
                      ' "control_graph_id": "ctg:7adbxxxx0d49:1030xxxx4165",'
                      ' "triggering_process_graph_id": "pid:7adbxxxxxxxx0d49:103512883608",'
                      ' "sha256": "4208xxxx2554da89f45xxxx3bbd",'
                      ' "md5": "1fd4xxxxxxxxxxxxxxxxxxxxxxxxxx86231e",'
                      ' "parent_details": '
                      '{"parent_sha256":"eb71xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxc208",'
                      ' "parent_md5": "e7a6xxxxxxxxxxxxxxxxxxxxxxxxxxxx90f4",'
                      ' "parent_cmdline": "\\"C:\\\\Windows\\\\system32\\\\cmd.exe\\" ",'
                      ' "parent_process_graph_id": "pid:7adbxxxxxxxx0d49:103472906247"},'
                      ' "pattern_disposition": 2048,'
                      ' "pattern_disposition_details": {"indicator": false, "detect": false, "inddet_mask": false,'
                      ' "sensor_only": false, "rooting": false, "kill_process": false, "kill_subprocess": false,'
                      ' "quarantine_machine": false, "quarantine_file": false, "policy_disabled": false,'
                      ' "kill_parent": false, "operation_blocked": false, "process_blocked": true,'
                      ' "registry_operation_blocked": false, "critical_process_disabled": false,'
                      ' "bootup_safeguard_enabled": false, "fs_operation_blocked": false,'
                      ' "handle_operation_downgraded": false, "kill_action_failed": false,'
                      ' "blocking_unsupported_or_disabled": false, "suspend_process": false,'
                      ' "suspend_parent": false}, "rule_instance_id": "3", "rule_instance_version": 2}],'
                      ' "email_sent": true, "first_behavior": "2023-09-12T11:46:12Z",'
                      ' "last_behavior": "2023-09-12T11:46:12Z", "max_confidence": 100, "max_severity": 50,'
                      ' "max_severity_displayname": "Medium", "show_in_ui": true, "status": "new",'
                      ' "hostinfo": {"domain": ""}, "seconds_to_triaged": 0, "seconds_to_resolved": 0,'
                      ' "behaviors_processed": ["pid:7adbxxxxxxxx0d49:103512883608:41002"],'
                      ' "date_updated": "2023-11-15T14:48:56.377312Z"}', '@timezone': 'Z',
        'behaviors': [
            {
                'alleged_filetype': 'exe',
                'behavior_id': '41002',
                'cmdline': 'calc',
                'confidence': '100',
                'control_graph_id': 'ctg:7adbxxxx0d49:1030xxxx4165',
                'description': 'A process triggered a medium severity custom rule.',
                'device_id': '7adbxxxxxxxx0d49',
                'display_name': 'CustomIOAWinMedium',
                'filename': 'calc.exe',
                'filepath': '\\Device\\HarddiskVolume1\\Windows\\System32\\calc.exe',
                'ioc_description': '\\Device\\HarddiskVolume1\\Windows\\System32\\calc.exe',
                'ioc_source': 'library_load',
                'ioc_type': 'hash_sha256',
                'ioc_value': '4208xxxx2554da89f45xxxx3bbd',
                'md5': '1fd4xxxxxxxxxxxxxxxxxxxxxxxxxx86231e',
                'objective': 'Falcon Detection Method',
                'parent_details':
                    {
                        'parent_cmdline': '"C:\\Windows\\system32\\cmd.exe" ',
                        'parent_md5': 'e7a6xxxxxxxxxxxxxxxxxxxxxxxxxxxx90f4',
                        'parent_process_graph_id': 'pid:7adbxxxxxxxx0d49:103472906247',
                        'parent_sha256': 'eb71xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxc208'
                    },
                'pattern_disposition': '2048',
                'pattern_disposition_details':
                    {
                        'blocking_unsupported_or_disabled': 'false',
                        'bootup_safeguard_enabled': 'false',
                        'critical_process_disabled': 'false',
                        'detect': 'false',
                        'fs_operation_blocked': 'false',
                        'handle_operation_downgraded': 'false',
                        'inddet_mask': 'false',
                        'indicator': 'false',
                        'kill_action_failed': 'false',
                        'kill_parent': 'false',
                        'kill_process': 'false',
                        'kill_subprocess': 'false',
                        'operation_blocked': 'false',
                        'policy_disabled': 'false',
                        'process_blocked': 'true',
                        'quarantine_file': 'false',
                        'quarantine_machine': 'false',
                        'registry_operation_blocked': 'false',
                        'rooting': 'false',
                        'sensor_only': 'false',
                        'suspend_parent': 'false',
                        'suspend_process': 'false'
                    },
                'rule_instance_id': '3',
                'rule_instance_version': '2',
                'scenario': 'suspicious_activity',
                'severity': '50',
                'sha256': '4208xxxx2554da89f45xxxx3bbd',
                'tactic': 'Custom Intelligence',
                'tactic_id': 'CSTA0005',
                'technique': 'Indicator of Attack',
                'technique_id': 'CST0004',
                'template_instance_id': '3',
                'timestamp': '2023-09-12T11:46:12Z',
                'triggering_process_graph_id': 'pid:7adbxxxxxxxx0d49:103512883608',
                'user_id': 'S-1-5-21-xxxx-16xxxx15-312xxxx6-500',
                'user_name': 'testuser'
            }
        ],
        'behaviors_processed': 'pid:7adbxxxxxxxx0d49:103512883608:41002',
        'cid': 'ef21xxxxxxxxxxxxxxxxxxxxxxxxxxx440d',
        'created_timestamp': '2023-09-12T11:46:19.787962809Z',
        'date_updated': '2023-11-15T14:48:56.377312Z',
        'detection_id': 'ldt:7adbxxxxxxxx0d49:103079284165',
        'device': {
            'agent_load_flags': '1',
            'agent_local_time': '2023-09-12T08:30:15.487Z',
            'agent_version': '6.58.17212.0',
            'bios_manufacturer': 'Xen',
            'bios_version': '4.11.hp',
            'cid': 'ef21xxxxxxxxxxxxxxxxxxxxxxxxxxx440d',
            'config_id_base': '65994763',
            'config_id_build': '17212',
            'config_id_platform': '3',
            'device_id': '7adbxxxxxxxx0d49',
            'external_ip': '1.1.2.2',
            'first_seen': '2023-05-16T05:10:55Z',
            'groups': 'bb1exxxxxxxxxxxxxxxxxxxxxxxxxxb23d',
            'hostname': 'CROWDST',
            'instance_id': '065fxxxxxxxxxx27ce',
            'last_seen': '2023-09-12T11:24:19Z',
            'local_ip': '172.0.0.1',
            'mac_address': '12-11-11-11-11-11',
            'major_version': '10',
            'minor_version': '0',
            'modified_timestamp': '2023-09-12T11:45:57Z',
            'os_version': 'Windows Server 2022',
            'platform_id': '0',
            'platform_name': 'Windows',
            'product_type': '3',
            'product_type_desc': 'Server',
            'service_provider': 'WINDOWS_V2',
            'service_provider_account_id': '1xxxxxxxxxxxx2',
            'status': 'normal',
            'system_manufacturer': 'Xen',
            'system_product_name': 'HVM domU'
        },
        'email_sent': 'true',
        'first_behavior': '2023-09-12T11:46:12Z',
        'hostinfo': {
            'domain': ''
        },
        'last_behavior': '2023-09-12T11:46:12Z',
        'max_confidence': '100',
        'max_severity': '50',
        'max_severity_displayname': 'Medium',
        'seconds_to_resolved': '0',
        'seconds_to_triaged': '0',
        'show_in_ui': 'true',
        'status': 'new'
    }
}


class TestLogScaleResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for CrowdStrike LogScale translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """
        return the obj in the itr if constraint is true
        """
        return next((obj for obj in itr if constraint(obj)), None)

    @staticmethod
    def get_first_of_type(itr, typ):
        """
        to check whether the object belongs to respective stix object
        """
        return TestLogScaleResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def get_observed_data_objects(data):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        return observed_data['objects']

    def test_ipv4_addr_json_to_stix(self):
        """
        to test ipv4-addr stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        ipv4_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'ipv4-addr')
        ipv6_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'ipv6-addr')
        assert (ipv4_obj is not None), 'ipv4 object type not found'
        assert ipv4_obj['type'] == 'ipv4-addr'
        assert ipv4_obj['value'] == '1.1.2.2'
        assert ipv6_obj is None


    def test_file_json_to_stix(self):
        """
        to test file stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        file_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'file')
        assert (file_obj.keys() == {'type', 'name', 'x_path', 'x_extension', 'parent_directory_ref', 'hashes'})
        assert (file_obj is not None), 'file object type not    found'
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'calc.exe'
        assert file_obj['x_extension'] == 'exe'
        assert file_obj['hashes']['MD5'] == '1fd4xxxxxxxxxxxxxxxxxxxxxxxxxx86231e'
        assert file_obj['hashes']['SHA-256'] == '4208xxxx2554da89f45xxxx3bbd'

    def test_process_json_to_stix(self):
        """
        to test process stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        process_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'process')
        assert (process_obj.keys() == {'type', 'name', 'binary_ref', 'parent_ref', 'x_process_graph_id',
                                       'command_line', 'creator_user_ref'})
        assert (process_obj is not None), 'process object type not found'
        assert process_obj['type'] == 'process'
        assert process_obj['name'] == 'calc.exe'
        assert process_obj['command_line'] == 'calc'
        assert process_obj['x_process_graph_id'] == 'pid:7adbxxxxxxxx0d49:103512883608'
        assert (all(index in objects for ref, index in process_obj.items() if '_ref' in ref and
                    not isinstance(index, list))), "one of the references in process object is not found"

    def test_x_crowdstrike_behavior_json_to_stix(self):
        """
        to test behavior stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        behavior_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'x-crowdstrike-detection-behavior')
        assert (behavior_obj.keys() == {'type', 'display_name', 'behavior_id', 'confidence', 'control_graph_id',
                                        'description', 'objective', 'pattern_disposition',
                                        'pattern_disposition_details',
                                        'rule_instance_id', 'rule_instance_version', 'scenario', 'severity',
                                        'created_time', 'user_ref', 'process_ref', 'ttp_tagging_ref', 'ioc_description',
                                        'ioc_source', 'ioc_type', 'ioc_value', 'template_instance_id'})
        assert (behavior_obj is not None), 'behavior object type not found'
        assert behavior_obj['type'] == 'x-crowdstrike-detection-behavior'
        assert behavior_obj['display_name'] == 'CustomIOAWinMedium'
        assert behavior_obj['behavior_id'] == '41002'
        assert behavior_obj['confidence'] == 100
        assert behavior_obj['control_graph_id'] == 'ctg:7adbxxxx0d49:1030xxxx4165'
        assert behavior_obj['objective'] == 'Falcon Detection Method'
        assert (all(index in objects for ref, index in behavior_obj.items() if '_ref' in ref and
                    not isinstance(index, list))), "one of the references in behavior object is not found"

    def test_directory_json_to_stix(self):
        """
        to test directory stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        directory_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'directory')
        assert (directory_obj.keys() == {'type', 'path'})
        assert (directory_obj is not None), 'directory object type not found'
        assert directory_obj['type'] == 'directory'
        assert directory_obj['path'] == '\\Device\\HarddiskVolume1\\Windows\\System32'

    def test_x_ibm_ttp_tagging_json_to_stix(self):
        """
        to test x-ibm-ttp-tagging stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        ttp_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'x-ibm-ttp-tagging')
        assert (ttp_obj.keys() == {'type', 'name', 'extensions'})
        assert (ttp_obj is not None), 'x-ibm-ttp-tagging object type not found'
        assert ttp_obj['type'] == 'x-ibm-ttp-tagging'
        assert ttp_obj['name'] == 'Custom Intelligence'
        assert ttp_obj['extensions']['mitre-attack-ext']['tactic_id'] == 'CSTA0005'
        assert ttp_obj['extensions']['mitre-attack-ext']['technique_name'] == 'Indicator of Attack'
        assert ttp_obj['extensions']['mitre-attack-ext']['technique_id'] == 'CST0004'

    def test_user_account_json_to_stix(self):
        """
        to test user-account stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        user_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'user-account')
        assert (user_obj.keys() == {'type', 'user_id', 'display_name'})
        assert (user_obj is not None), 'user-account object type not found'
        assert user_obj['type'] == 'user-account'
        assert user_obj['user_id'] == 'S-1-5-21-xxxx-16xxxx15-312xxxx6-500'
        assert user_obj['display_name'] == 'testuser'

    def test_x_ibm_finding_json_to_stix(self):
        """
        to test x-ibm-finding stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        finding_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        assert (finding_obj.keys() == {'type', 'name', 'x_behavior_refs', 'ttp_tagging_refs', 'x_behaviors_processed',
                                       'time_observed', 'x_last_updated', 'src_os_ref',
                                       'src_ip_ref', 'x_is_email_sent', 'x_first_behavior_observed',
                                       'x_last_behavior_observed', 'confidence', 'severity',
                                       'x_severity_name', 'x_seconds_to_resolved', 'x_seconds_to_triaged', 'x_status',
                                       'x_logscale_repository','x_logscale_event_id'})
        assert (finding_obj is not None), 'x-ibm-finding object type not found'
        assert finding_obj['type'] == 'x-ibm-finding'
        assert finding_obj['name'] == 'ldt:7adbxxxxxxxx0d49:103079284165'
        assert finding_obj['x_behaviors_processed'] == 'pid:7adbxxxxxxxx0d49:103512883608:41002'
        assert finding_obj['time_observed'] == '2023-09-12T11:46:19.787Z'
        assert finding_obj['x_last_updated'] == '2023-11-15T14:48:56.377312Z'
        assert finding_obj['x_is_email_sent'] == 'true'
        assert finding_obj['confidence'] == 100
        assert finding_obj['severity'] == 50
        assert finding_obj['x_status'] == 'new'
        assert (all(index in objects for ref, index in finding_obj.items() if '_ref' in ref and
                    not isinstance(index, list))), "one of the references in finding object is not found"
        assert (all(x_behavior_ref in objects for x_behavior_ref in finding_obj['x_behavior_refs'])),\
            "behavior object is not found"
        assert (all(ttp_tagging_ref in objects for ttp_tagging_ref in finding_obj['ttp_tagging_refs'])),\
            "ttp_tagging object is not found"

    def test_x_crowdstrike_edr_agent_json_to_stix(self):
        """
        to test x-crowdstrike-edr-agent stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        edr_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'x-crowdstrike-edr-agent')
        assert (edr_obj.keys() == {'type', 'load_flags', 'local_time', 'version',
                                   'config_id_base', 'config_id_build', 'config_id_platform'})
        assert (edr_obj is not None), 'x-crowdstrike-edr object type not found'
        assert edr_obj['type'] == 'x-crowdstrike-edr-agent'
        assert edr_obj['load_flags'] == '1'
        assert edr_obj['local_time'] == '2023-09-12T08:30:15.487Z'
        assert edr_obj['version'] == '6.58.17212.0'
        assert edr_obj['config_id_base'] == '65994763'

    def test_x_ocs_asset_json_to_stix(self):
        """
        to test x-oca-asset stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        asset_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'x-oca-asset')
        assert (asset_obj.keys() == {'type', 'x_cid', 'x_device_groups', 'x_agent_ref', 'x_bios_manufacturer',
                                     'x_bios_version', 'device_id', 'ip_refs',
                                     'x_first_seen', 'hostname', 'x_instance_id', 'x_last_seen', 'mac_refs',
                                     'x_last_modified', 'os_ref', 'x_host_type_number', 'host_type',
                                     'x_service_provider', 'x_service_account_id', 'x_status', 'x_system_manufacturer',
                                     'x_system_product_name'})
        assert (asset_obj is not None), 'x-oca-asset object type not found'
        assert asset_obj['type'] == 'x-oca-asset'
        assert asset_obj['device_id'] == '7adbxxxxxxxx0d49'
        assert asset_obj['x_bios_version'] == '4.11.hp'
        assert asset_obj['hostname'] == 'CROWDST'
        assert asset_obj['x_instance_id'] == '065fxxxxxxxxxx27ce'
        assert asset_obj['x_last_seen'] == '2023-09-12T11:24:19Z'
        assert asset_obj['host_type'] == 'Server'
        assert asset_obj['x_system_product_name'] == 'HVM domU'
        assert (all(index in objects for ref, index in asset_obj.items() if '_ref' in ref and
                    not isinstance(index, list))), "one of the references in oca asset object is not found"
        assert (all(ip_ref in objects for ip_ref in asset_obj['ip_refs'])), "ip object is not found"
        assert (all(mac_ref in objects for mac_ref in asset_obj['mac_refs'])), "mac object is not found"

    def test_mac_addr_json_to_stix(self):
        """
        to test mac-addr stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        mac_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'mac-addr')
        assert (mac_obj.keys() == {'type', 'value'})
        assert (mac_obj is not None), 'mac-addr object type not found'
        assert mac_obj['type'] == 'mac-addr'
        assert mac_obj['value'] == '12:11:11:11:11:11'

    def test_software_json_to_stix(self):
        """
        to test software stix object properties
        """
        objects = TestLogScaleResultsToStix.get_observed_data_objects(logscale_sample_response)
        software_obj = TestLogScaleResultsToStix.get_first_of_type(objects.values(), 'software')
        assert (software_obj.keys() == {'type', 'name', 'version', 'x_minor_version', 'x_major_version', 'x_id'})
        assert (software_obj is not None), 'software object type not found'
        assert software_obj['type'] == 'software'
        assert software_obj['name'] == 'Windows'
        assert software_obj['version'] == 'Windows Server 2022'
        assert software_obj['x_major_version'] == '10'
