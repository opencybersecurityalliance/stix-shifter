""" test script to perform unit test case for nozomi vantage translate results """
import unittest
from stix_shifter_modules.nozomi_vantage.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "nozomi_vantage"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "nozomi_vantage",
    "identity_class": "events"
}
options = {}

nozomi_sample_response = [{
    'id': '12ee457d-ca1c-4d98-9430-96b56afc9f76',
    'time': 1702365057012,
    'name': 'Sigma rule match',
    'type_name': 'Sigma rule match',
    'threat_name': '',
    'counter': 0,
    'description': 'The following suspicious local event was detected on this host: "Detects the execution of renamed '
                   'PuTTY Plink to perform data exfiltration through tunnel port forwarding".',
    'ack': False,
    'note': None,
    'risk': 8.0,
    'id_src': '11.111.11.11',
    'id_dst': None,
    'ip_src': '11.111.11.11',
    'ip_src:info': None,
    'ip_dst': '',
    'ip_dst:info': None,
    'status': 'open',
    'mac_src': '01:01:01:01:01:01',
    'mac_dst': '02:02:02:02:02:02',
    'port_dst': 1122,
    'port_src': 2233,
    'protocol': 'tcp/1122',
    'transport_protocol': 'tcp',
    'severity': 0,
    'zone_dst': '123.01.01.0/910',
    'zone_src': 'other',
    'dst_roles': 'other',
    'src_roles': 'ABCD',
    'label_dst': None,
    'label_src': 'ABCD',
    'bpf_filter': '',
    'properties': {
        'cause': 'Rule-dependent. A suspicious local event has been detected on a machine.',
        'process': {
            'pid': '1234',
            'user': 'Administrator@ABCD',
            'ancestry': 'C:\\Windows\\System32\\cmd.exe',
            'image_path': 'C:\\Program Files\\Scripts\\pip.exe',
            'command_line': 'pip  install -r requirements-dev.txt',
            'image_hash_sha256': '0101010101010101010101010101010101010101010101010101010101010101'
        },
        'solution': 'Rule-dependent. Verify the device configuration and status, and the possible presence of '
                    'malicious processes.',
        'bad_actor': '01:01:01:01:01:01',
        'raised_by': 'n2os_ids',
        'is_src_public': False,
        'src_logged_in:info': {
            'source': 'arc'
        },
        'details_file_size': {
            'label': '',
            'value': ''
        },
        'details_hash_SHA256': {
            'label': 'SHA256',
            'value': '0101010101010101010101010101010101010101010101010101010101010101'
        },
        'src_logged_in_users': [
            'user@Hostname'
        ]
    },
    'closed_time': 1698836400000,
    'close_option': None,
    'is_incident': False,
    'is_security': True,
    'created_time': 1702365057012,
    'trigger_type': 'sigma_rules',
    'capture_device': '',
    'sec_profile_visible': True,
    'grouped_visible': True,
    'mitre_attack_techniques': None,
    'mitre_attack_tactics': None,
    'playbook_contents': None,
    'trace_status': 'state_not_created',
    'appliance_host': 'ABCD',
    'record_created_at': 1702365077784,
    'sensor:host': None,
    'site:name': None,
    'type_id': 'SIGN:SIGMA-RULE',
    'trigger_id': '5f9b24dd-fa05-401c-ad21-240b3f761c9f'
}]

nozomi_sample_response_2 = [
    {
        'id': 'dfd21c45-3958-5554-863a-6a2c42228ccf',
        'time': 1704792066000,
        'name': 'Malware detection',
        'threat_name': 'threat',
        'risk': '',
        'protocol': '',
        'transport_protocol': 'unknown',
        'severity': '',
        'mac_src': '01:01:01:01:01:01',
        'mac_dst': '02:02:02:02:02:02',
        'properties': {
            'sandbox_filename': '/var/sandbox/000012_CVcontrolEngineerdocx_2.dir/content',
            'details_file_size': {
                'label': 'File size',
                'value': '19261 bytes'
            },
            'details_hash_SHA1': {
                'label': 'SHA1',
                'value': '0101010101010101010101010101010101010101010101010101010101010101'
            },
            'bad_actor': '',
            'details_operation': {
                'label': 'Operation',
                'value': 'read'
            },
            'details_yara_file': {
                'label': 'Yara file name',
                'value': 'ENTERPRISE_RAT_(Dragonfly)Havex_TemplateAttack.yar'
            },

        },
        'closed_time': '',

    }
]


class TestNozomiResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for nozomi vantage translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """ return the obj in the itr if constraint is true """
        return next((obj for obj in itr if constraint(obj)), None)

    @staticmethod
    def get_first_of_type(itr, typ):
        """ check whether the object belongs to respective stix object """
        return TestNozomiResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def get_observed_data_objects(data):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, data, get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        return observed_data['objects']

    def test_ipv4_addr_json_to_stix(self):
        """test ipv4-addr stix object properties"""
        objects = TestNozomiResultsToStix.get_observed_data_objects(nozomi_sample_response)
        ipv4_obj = TestNozomiResultsToStix.get_first_of_type(objects.values(), 'ipv4-addr')
        ipv6_obj = TestNozomiResultsToStix.get_first_of_type(objects.values(), 'ipv6-addr')
        assert ipv4_obj is not None
        assert (ipv4_obj.keys() == {'type', 'value', 'resolves_to_refs', 'x_nozomi_info_ref'})
        assert ipv4_obj['type'] == 'ipv4-addr'
        assert ipv4_obj['value'] == '11.111.11.11'
        assert ipv6_obj is None

    def test_network_traffic_json_to_stix(self):
        """test network-traffic stix object properties"""
        objects = TestNozomiResultsToStix.get_observed_data_objects(nozomi_sample_response)
        network_obj = TestNozomiResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert network_obj is not None
        assert (network_obj.keys() == {'type', 'src_ref', 'dst_ref', 'dst_port', 'src_port', 'protocols'})
        assert network_obj['type'] == 'network-traffic'
        assert network_obj['src_ref'] == '1'
        assert network_obj['protocols'] == ['tcp', 'tcp']

    def test_mac_addr_json_to_stix(self):
        """test mac-addr stix object properties"""
        objects = TestNozomiResultsToStix.get_observed_data_objects(nozomi_sample_response)
        mac_addr_obj = TestNozomiResultsToStix.get_first_of_type(objects.values(), 'mac-addr')
        assert mac_addr_obj is not None
        assert (mac_addr_obj.keys() == {'type', 'value'})
        assert mac_addr_obj['type'] == 'mac-addr'
        assert mac_addr_obj['value'] == '01:01:01:01:01:01'

    def test_file_json_to_stix(self):
        """test file stix object properties"""
        objects = TestNozomiResultsToStix.get_observed_data_objects(nozomi_sample_response_2)
        file_obj = TestNozomiResultsToStix.get_first_of_type(objects.values(), 'file')
        assert file_obj is not None
        assert (file_obj.keys() == {'type', 'hashes', 'size', 'name'})
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'ENTERPRISE_RAT_(Dragonfly)Havex_TemplateAttack.yar'
        assert file_obj['size'] == 19261

    def test_process_json_to_stix(self):
        """test process stix object properties"""
        objects = TestNozomiResultsToStix.get_observed_data_objects(nozomi_sample_response)
        process_obj = TestNozomiResultsToStix.get_first_of_type(objects.values(), 'process')
        assert process_obj is not None
        assert (process_obj.keys() == {'type', 'pid', 'creator_user_ref', 'parent_ref', 'binary_ref', 'command_line'})
        assert process_obj['type'] == 'process'
        assert process_obj['pid'] == 1234
        assert process_obj['command_line'] == 'pip  install -r requirements-dev.txt'

    def test_user_account_json_to_stix(self):
        """test user-account stix object properties"""
        objects = TestNozomiResultsToStix.get_observed_data_objects(nozomi_sample_response)
        user_account_obj = TestNozomiResultsToStix.get_first_of_type(objects.values(), 'user-account')
        assert user_account_obj is not None
        assert (user_account_obj.keys() == {'type', 'user_id'})
        assert user_account_obj['type'] == 'user-account'
        assert user_account_obj['user_id'] == 'Administrator@ABCD'

    def test_directory_json_to_stix(self):
        """test directory stix object properties"""
        objects = TestNozomiResultsToStix.get_observed_data_objects(nozomi_sample_response)
        directory_obj = TestNozomiResultsToStix.get_first_of_type(objects.values(), 'directory')
        assert directory_obj is not None
        assert (directory_obj.keys() == {'type', 'path'})
        assert directory_obj['type'] == 'directory'
        assert directory_obj['path'] == 'C:\\Windows\\System32'

    def test_x_ibm_finding_obj_json_to_stix(self):
        """test x-ibm-finding stix object properties"""
        objects = TestNozomiResultsToStix.get_observed_data_objects(nozomi_sample_response)
        x_ibm_finding_obj = TestNozomiResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        assert x_ibm_finding_obj is not None
        assert (x_ibm_finding_obj.keys() == {'type', 'alert_id', 'time_observed', 'name', 'finding_type', 'description', 'x_is_acknowledged', 'severity', 'src_ip_ref', 'x_alert_status', 'x_cause', 'ioc_refs', 'x_solution', 'end', 'x_is_incident_alert', 'x_is_cybersecurity_alert', 'start', 'rule_names', 'x_sensor_host', 'x_alert_type_id', 'x_rule_id'})
        assert x_ibm_finding_obj['type'] == 'x-ibm-finding'
        assert x_ibm_finding_obj['name'] == 'Sigma rule match'
        assert x_ibm_finding_obj['finding_type'] == 'alert'
        assert x_ibm_finding_obj['severity'] == 80

    def test_x_ibm_ttp_tagging_obj_json_to_stix(self):
        """test x-ibm-ttp-tagging stix object properties"""
        nozomi_sample = [
            {
                'id': '69f609c3-6564-4d16-aa8e-1dc8746f41e1',
                'time': 1702545279802,
                'name': 'Bad IP reputation (new node)',
                'properties': {

                    'mitre_attack_for_ics': {
                        'software': [
                            'RDP bruteforce'
                        ],
                        'destination': {
                            'types': [
                                'Engineering Workstation'
                            ]
                        }
                    },
                    'is_dst_reputation_bad': False,
                    'is_src_reputation_bad': True,
                    'mitre_attack_enterprise': {
                        'techniques': [
                            {
                                'id': 'T123',
                                'name': 'Application Layer Protocol',
                                'tactic': 'Command and Control'
                            },
                            {
                                'id': 'T123',
                                'name': 'Non-Application Layer Protocol',
                                'tactic': 'Command and Control'
                            }
                        ]
                    },
                    'details_stix_indicator_id': {
                        'label': 'STIX indicator ID',
                        'value': 'indicator--469cf642-51e0-41e6-b1fb-3e112b60f79c'
                    }
                },
            }]
        objects = TestNozomiResultsToStix.get_observed_data_objects(nozomi_sample)
        x_ibm_ttp_tagging_obj = TestNozomiResultsToStix.get_first_of_type(objects.values(), 'x-ibm-ttp-tagging')
        assert x_ibm_ttp_tagging_obj is not None
        assert (x_ibm_ttp_tagging_obj.keys() == {'type', 'extensions', 'name', 'kill_chain_phases'})
        assert x_ibm_ttp_tagging_obj['type'] == 'x-ibm-ttp-tagging'
        assert x_ibm_ttp_tagging_obj['name'] == 'Application Layer Protocol'
        ibm_tagging = x_ibm_ttp_tagging_obj['kill_chain_phases']
        assert (ibm_tagging_objs['kill_chain_name'] == 'mitre-attack' and ibm_tagging_objs['phase_name'] ==
                'Command and Control' for ibm_tagging_objs in ibm_tagging)

    def test_x_nozomi_info_obj_json_to_stix(self):
        """test x-nozomi-info stix object properties"""
        objects = TestNozomiResultsToStix.get_observed_data_objects(nozomi_sample_response)
        x_nozomi_info_obj = TestNozomiResultsToStix.get_first_of_type(objects.values(), 'x-nozomi-info')
        assert x_nozomi_info_obj is not None
        assert (x_nozomi_info_obj.keys() == {'type', 'zone', 'roles'})
        assert x_nozomi_info_obj['type'] == 'x-nozomi-info'
        assert x_nozomi_info_obj['zone'] == '123.01.01.0/910'
        assert x_nozomi_info_obj['roles'] == 'other'
