""" test script to perform unit test case for vectra translate results """
import unittest
from stix_shifter_modules.vectra.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "vectra"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "vectra",
    "identity_class": "events"
}
options = {}

vectra_sample_response = {
    'summary': {
        'dst_ips': ['11.111.11.111'],
        'num_sessions': 4,
        'bytes_sent': 4053918,
        'bytes_received': 3186727,
        'description': 'This host communicated with an external destination using HTTPS where another protocol was '
                       'running over the top of the session. The host appeared to be under the control of the '
                       'external destination. '
    },
    'id': 10130,
    'category': 'COMMAND & CONTROL',
    'detection': 'Hidden HTTPS Tunnel',
    'detection_category': 'COMMAND & CONTROL',
    'detection_type': 'Hidden HTTPS Tunnel',
    'custom_detection': None,
    'description': None,
    'src_ip': '11.111.11.111',
    'state': 'inactive',
    'certainty': 0,
    'threat': 0,
    'created_timestamp': '2022-12-22T07:43:52Z',
    'first_timestamp': '2022-12-22T07:33:38Z',
    'last_timestamp': '2022-12-27T06:44:32Z',
    'targets_key_asset': False,
    'is_targeting_key_asset': False,
    'src_account': None,
    'src_host': {
        'id': 872,
        'ip': '11.111.11.111',
        'name': 'VMAL #2 windows 11.111.11.111 (higaki-ha11)',
        'is_key_asset': False,
        'groups': [{
            'id': 145,
            'name': 'Super Test domain group',
            'description': 'created during API testing',
            'last_modified': '2022-08-03T15:33:04Z',
            'last_modified_by': 'reliaquest',
            'type': 'host'
        }, {
            'id': 144,
            'name': 'Partner VLAB - User Devices',
            'description': '',
            'last_modified': '2022-01-27T12:05:24Z',
            'last_modified_by': 'user (Removed)',
            'type': 'ip'
        }],
        'threat': 82,
        'certainty': 71
    },
    'note': None,
    'note_modified_by': None,
    'note_modified_timestamp': None,
    'sensor': 'test',
    'sensor_name': 'test',
    'tags': [],
    'triage_rule_id': None,
    'assigned_to': 'vectra',
    'assigned_date': '2022-12-14T06:59:22Z',
    'groups': [{
        'id': 144,
        'name': 'Partner VLAB - User Devices',
        'description': '',
        'type': 'ip',
        'last_modified': '2022-01-27T12:05:24Z',
        'last_modified_by': 'user'
    }],
    'is_marked_custom': False,
    'is_custom_model': False,
    'src_linked_account': None,
    'campaign_summaries': [],
    'is_triaged': False,
    'filtered_by_ai': False,
    'filtered_by_user': False,
    'filtered_by_rule': False,
    '_doc_modified_ts': '2023-06-08T06:20:58.684936',
    'grouped_details_ex': [{
        'external_target': {
            'ip': '11.111.11.111',
            'name': ''
        },
        'num_sessions': 4,
        'bytes_received': 3186727,
        'bytes_sent': 4053918,
        'ja3_hashes': [''],
        'ja3s_hashes': [''],
        'sessions': [{
            'tunnel_type': 'Long TCP session - Command line',
            'protocol': 'tcp',
            'app_protocol': 'https',
            'dst_port': 222,
            'dst_ip': '11.111.11.111',
            'bytes_received': 361298,
            'bytes_sent': 309439,
            'first_timestamp': '2022-12-27T06:33:33Z',
            'last_timestamp': '2022-12-27T06:44:32Z',
            'dst_geo': None,
            'dst_geo_lat': None,
            'dst_geo_lon': None
        },
            {
                'tunnel_type': 'Long TCP session - Command line',
                'protocol': 'tcp',
                'app_protocol': 'https',
                'dst_port': [222],
                'dst_ip': '11.111.11.111',
                'bytes_received': 329386,
                'bytes_sent': 217025,
                'first_timestamp': '2022-12-27T06:14:33Z',
                'last_timestamp': '2022-12-27T06:24:33Z',
                'dst_geo': None,
                'dst_geo_lat': None,
                'dst_geo_lon': None
            }],
        'first_timestamp': '2022-12-22T07:33:38Z',
        'last_timestamp': '2022-12-27T06:44:32Z',
        'dst_ips': ['11.111.11.111'],
        'dst_ports': [222],
        'target_domains': ['']
    }]
}

vectra_sample_grouped_response = {
    "id": 8111,
    "category": "COMMAND & CONTROL",
    "detection": "PowershellEmpire",
    "detection_category": "COMMAND & CONTROL",
    "detection_type": "PowershellEmpire",
    "custom_detection": None,
    "description": "c3483e00759211eda7e9ab6654adc2f1",
    "src_ip": "11.111.11.111",
    "state": "inactive",
    "certainty": 0,
    "threat": 0,
    "created_timestamp": "2022-12-06T21:11:20Z",
    "first_timestamp": "2022-12-06T19:57:59Z",
    "last_timestamp": "2022-12-07T07:09:39Z",
    "targets_key_asset": False,
    "is_targeting_key_asset": False,
    "src_account": None,
    "src_host": {
        "id": 1543,
        "ip": "11.111.11.111",
        "name": "VMAL #2 windows 11.111.11.111 (kgalloway141)",
        "is_key_asset": False,
        "groups": [
            {
                "id": 144,
                "name": "Partner VLAB - User Devices",
                "description": "",
                "last_modified": "2022-01-27T12:05:24Z",
                "last_modified_by": "user (Removed)",
                "type": "ip"
            }
        ],
        "threat": 0,
        "certainty": 0
    },
    "note": None,
    "note_modified_by": None,
    "note_modified_timestamp": None,
    "sensor": "None",
    "sensor_name": "test",
    "tags": [],
    "triage_rule_id": None,
    "assigned_to": "test",
    "assigned_date": "2022-12-14T06:58:53Z",
    "groups": [
        {
            "id": 144,
            "name": "Partner VLAB - User Devices",
            "description": "",
            "type": "ip",
            "last_modified": "2022-01-27T12:05:24Z",
            "last_modified_by": "user"
        }
    ],
    "is_marked_custom": False,
    "is_custom_model": True,
    "src_linked_account": None,
    "grouped_details": [
        {
            "description": "PowershellEmpire",
            "dst_geo": None,
            "dst_geo_lat": None,
            "dst_geo_lon": None,
            "first_timestamp": "2022-12-07T07:09:39Z",
            "last_timestamp": "2022-12-07T07:09:39Z",
            "count": 1,
            "reason": None,
            "identity": None,
            "flex_json": {},
            "detection_guid": None,
            "distilled_context": {},
            "sequence_id": None,
            "is_host_detail": True,
            "is_account_detail": False,
            "account_uid": None,
            "account_detection": None,
            "host_detection": 8111,
            "src_ip": "11.111.11.111",
            "user_agent": "\"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko\"",
            "status_code": "200",
            "uri": "\"/admin/get.php\"",
            "metadata": {
                "user_agent": "\"Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko\"",
                "status_code": "200",
                "uri": "\"/admin/get.php\"",
                "resp_h": "11.111.11.111",
                "resp_p": 80,
                "orig_h": "11.111.11.111",
                "orig_ip_bytes": 1427994,
                "resp_ip_bytes": 17600003,
                "resp_hostname": "VMAL #2 windows 11.111.11.111 (kgalloway141)",
                "orig_sluid": "test",
                "resp_sluid": None
            },
            "accounts": [],
            "target_domains": [
                "VMAL #2 windows 11.111.11.111 (kgalloway141)"
            ],
            "dst_ips": [
                "11.111.11.111"
            ],
            "dst_ports": [
                80
            ],
            "protocol": None,
            "bytes_received": 17600003,
            "bytes_sent": 1427994
        }
    ],
    "summary": {
        "custom_model_query": "Search: None\n\nFilters: uri: /admin/get.php",
        "bytes_received": 986581476,
        "bytes_sent": 85530107,
        "matches": 100,
        "first_matched": "2022-12-06T22:00:00+00:00",
        "last_matched": "2022-12-07T07:09:39+00:00",
        "description": ""
    },
    "campaign_summaries": [],
    "is_triaged": False,
    "filtered_by_ai": False,
    "filtered_by_user": False,
    "filtered_by_rule": False,
    "_doc_modified_ts": "2023-05-17T22:35:14.497368"
}


class TestVectraResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for vectra translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """ return the obj in the itr if constraint is true """
        return next((obj for obj in itr if constraint(obj)), None)

    @staticmethod
    def get_first_of_type(itr, typ):
        """ check whether the object belongs to respective stix object """
        return TestVectraResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

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
        """test ipv4-addr stix object properties"""
        objects = TestVectraResultsToStix.get_observed_data_objects(vectra_sample_response)
        ipv4_obj = TestVectraResultsToStix.get_first_of_type(objects.values(), 'ipv4-addr')
        assert (ipv4_obj is not None), 'ipv4 object type not found'
        assert ipv4_obj['type'] == 'ipv4-addr'
        assert ipv4_obj['value'] == '11.111.11.111'

    def test_network_traffic_json_to_stix(self):
        """test network_traffic stix object properties"""
        objects = TestVectraResultsToStix.get_observed_data_objects(vectra_sample_response)
        network_traffic_obj = TestVectraResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert (network_traffic_obj.keys() == {'type', 'x_tunnel_type', 'protocols', 'dst_port', 'dst_ref',
                                               'dst_byte_count', 'src_byte_count', 'start', 'end'})
        assert (network_traffic_obj is not None), 'network-traffic object type not found'
        assert network_traffic_obj['type'] == 'network-traffic'
        assert network_traffic_obj['x_tunnel_type'] == 'Long TCP session - Command line'
        assert network_traffic_obj['protocols'] == ['tcp', 'https']

    def test_x_grouped_details(self):
        """test x-grouped-details stix object properties"""
        objects = TestVectraResultsToStix.get_observed_data_objects(vectra_sample_response)
        x_grouped_obj = TestVectraResultsToStix.get_first_of_type(objects.values(), 'x-grouped-details')
        assert (x_grouped_obj.keys() == {'type', 'num_sessions', 'dst_byte_count', 'src_byte_count', 'ja3_hashes',
                                         'ja3s_hashes', 'session_refs', 'start', 'end'})
        assert (x_grouped_obj is not None), 'x-grouped-details object type not found'
        assert x_grouped_obj['type'] == 'x-grouped-details'
        assert x_grouped_obj['num_sessions'] == 4
        assert x_grouped_obj['dst_byte_count'] == 3186727

    def test_x_ibm_finding(self):
        """test x-ibm-finding stix object properties"""
        objects = TestVectraResultsToStix.get_observed_data_objects(vectra_sample_response)
        x_ibm_obj = TestVectraResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        assert (x_ibm_obj.keys() == {'type', 'type', 'event_count', 'description', 'alert_id', 'ttp_tagging_refs',
                                     'name', 'finding_type', 'src_ip_ref', 'x_state', 'confidence', 'severity',
                                     'time_observed', 'start', 'end', 'x_sensor_name', 'x_assigned_to',
                                     'x_assigned_date', 'x_is_triaged', 'ioc_refs'})
        assert (x_ibm_obj is not None), 'x-ibm-finding object type not found'
        assert x_ibm_obj['type'] == 'x-ibm-finding'
        assert x_ibm_obj['alert_id'] == 10130

    def test_x_oca_asset(self):
        """test x-oca-asset stix object properties"""
        objects = TestVectraResultsToStix.get_observed_data_objects(vectra_sample_response)
        x_oca_obj = TestVectraResultsToStix.get_first_of_type(objects.values(), 'x-oca-asset')
        assert (x_oca_obj.keys() == {'type', 'ip_refs', 'device_id', 'hostname', 'x_is_key_asset', 'x_threat',
                                     'x_certainty'})
        assert (x_oca_obj is not None), 'x-oca-asset object type not found'
        assert x_oca_obj['type'] == 'x-oca-asset'
        assert x_oca_obj['ip_refs'] == ['2']
        assert x_oca_obj['hostname'] == 'VMAL #2 windows 11.111.11.111 (higaki-ha11)'

    def test_domain_name(self):
        """test domain-name stix object properties"""
        objects = TestVectraResultsToStix.get_observed_data_objects(vectra_sample_grouped_response)
        domain_obj = TestVectraResultsToStix.get_first_of_type(objects.values(), 'domain-name')
        assert (domain_obj.keys() == {'type', 'value'})
        assert (domain_obj is not None), 'domain-name object type not found'
        assert domain_obj['type'] == 'domain-name'
        assert domain_obj['value'] == '11.111.11.111'

    def test_invalid_ipv6(self):
        """test invalid ipv6 stix object properties"""
        objects = TestVectraResultsToStix.get_observed_data_objects(vectra_sample_grouped_response)
        ipv6_obj = TestVectraResultsToStix.get_first_of_type(objects.values(), 'ipv6-addr')
        assert (ipv6_obj is None), 'ipv6 object type not found'
