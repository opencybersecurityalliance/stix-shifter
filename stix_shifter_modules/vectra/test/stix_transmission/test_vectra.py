import json
import unittest
from unittest.mock import patch
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_modules.vectra.entry_point import EntryPoint
from tests.utils.async_utils import get_mock_response


class VectraMockResponse:
    """ class for vectra mock response"""

    def __init__(self, code, data, headers):
        self.code = code
        self.content = data
        self.headers = headers

    def read(self):
        return bytearray(self.content, 'utf-8')


class TestVectraConnection(unittest.TestCase, object):
    mocked_response = {
        'count': 23,
        'results': [{
            'summary': {
                'dst_ips': ['11.111.11.111'],
                'num_sessions': 16,
                'bytes_sent': 48927848,
                'bytes_received': 638510042,
                'description': 'This host communicated with an external destination using HTTPS.'
            },
            'id': 9124,
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
            'created_timestamp': '2022-12-15T09:28:39Z',
            'first_timestamp': '2022-12-15T09:18:32Z',
            'last_timestamp': '2022-12-16T01:33:25Z',
            'targets_key_asset': False,
            'is_targeting_key_asset': False,
            'src_account': None,
            'src_host': {
                'id': 1481,
                'ip': '11.111.11.111',
                'name': 'VMAL #2 windows 11.111.11.111 (fschmidt114)',
                'is_key_asset': False,
                'groups': [{
                    'id': 144,
                    'name': 'Partner VLAB - User Devices',
                    'description': '',
                    'last_modified': '2022-01-27T12:05:24Z',
                    'last_modified_by': 'user (Removed)',
                    'type': 'ip'
                }],
                'threat': 0,
                'certainty': 0
            },
            'note': None,
            'note_modified_by': None,
            'note_modified_timestamp': None,
            'sensor': 'test',
            'sensor_name': 'test',
            'tags': [],
            'triage_rule_id': None,
            'assigned_to': 'crest',
            'assigned_date': '2023-03-29T15:25:23Z',
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
            'grouped_details': [{
                'external_target': {
                    'ip': '11.111.11.111',
                    'name': ''
                },
                'num_sessions': 16,
                'bytes_received': 638510042,
                'bytes_sent': 48927848,
                'ja3_hashes': [''],
                'ja3s_hashes': [''],
                'sessions': [{
                    'tunnel_type': 'Long TCP session - Command line',
                    'dst_port': 222,
                    'dst_ip': '11.111.11.111',
                    'bytes_received': 40495217,
                    'bytes_sent': 4108613,
                    'first_timestamp': '2022-12-16T01:22:32Z',
                    'last_timestamp': '2022-12-16T01:33:25Z',
                    'dst_geo': None,
                    'dst_geo_lat': None,
                    'dst_geo_lon': None
                }, {
                    'tunnel_type': 'Long TCP session - Command line',
                    'protocol': 'tcp',
                    'app_protocol': 'https',
                    'dst_port': 222,
                    'dst_ip': '11.111.11.111',
                    'bytes_received': 40483751,
                    'bytes_sent': 4087475,
                    'first_timestamp': '2022-12-16T01:09:32Z',
                    'last_timestamp': '2022-12-16T01:20:25Z',
                    'dst_geo': None,
                    'dst_geo_lat': None,
                    'dst_geo_lon': None
                }],
                'first_timestamp': '2022-12-15T09:18:32Z',
                'last_timestamp': '2022-12-16T01:33:25Z',
                'dst_ips': ['11.111.11.111'],
                'dst_ports': [222],
                'target_domains': ['']
            }, {}],
            'campaign_summaries': [],
            'is_triaged': False,
            'filtered_by_ai': False,
            'filtered_by_user': False,
            'filtered_by_rule': False,
            '_doc_modified_ts': '2023-06-08T00:21:13.669422'
        }, {
                'id': 12052,
                'category': 'EXFILTRATION',
                'detection': 'Data Smuggler',
                'detection_category': 'EXFILTRATION',
                'detection_type': 'Data Smuggler',
                'custom_detection': None,
                'description': None,
                'src_ip': '11.111.11.111',
                'state': 'inactive',
                'certainty': 0,
                'threat': 0,
                'created_timestamp': '2023-01-12T14:14:38Z',
                'first_timestamp': '2023-01-12T13:51:28Z',
                'last_timestamp': '2023-01-12T14:09:10Z',
                'targets_key_asset': False,
                'is_targeting_key_asset': False,
                'src_account': None,
                'src_host': {
                    'id': 1586,
                    'ip': '11.111.11.111',
                    'name': '11.111.11.111',
                    'is_key_asset': False,
                    'groups': [{
                        'id': 144,
                        'name': 'Partner VLAB - User Devices',
                        'description': '',
                        'last_modified': '2022-01-27T12:05:24Z',
                        'last_modified_by': 'user (Removed)',
                        'type': 'ip'
                    }],
                    'threat': 0,
                    'certainty': 0
                },
                'note': '2023-01-24 01:52:14 - Vectra SIR Admin (Notes)\nNotes added from ServiceNow for testing.\n\n',
                'note_modified_by': 'crest',
                'note_modified_timestamp': '2023-01-24T09:52:16Z',
                'sensor': 'eti2pc2s',
                'sensor_name': 'Vec2c610896a947c5b5102c466a28f49a',
                'tags': ['test', 'test1'],
                'triage_rule_id': None,
                'assigned_to': 'test',
                'assigned_date': '2023-01-23T06:25:09Z',
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
                'grouped_details': [{
                    'events': [{
                        'grouping_field': 'multi_fields',
                        'multi_fields': '3yO12k8i',
                        'id': 1664746,
                        'subtype': 'pull',
                        'first_timestamp': '2023-01-12T13:51:28Z',
                        'last_timestamp': '2023-01-12T14:04:30Z',
                        'couch_note_id': ['3yO12k8i'],
                        'flex5': [],
                        'app_protocol': None,
                        'target_domains': ['test.com'],
                        'bytes_received': 3250323735,
                        'bytes_sent': 428748,
                        'proxy_ip': None,
                        'sessions': [{
                            'target_host': {
                                'id': 325,
                                'ip': '11.111.111.11',
                                'name': 'VMAL #2 - test',
                                'is_key_asset': False
                            },
                            'dst_ip': '11.111.111.11',
                            'dst_port': 444,
                            'protocol': 'tcp',
                            'app_protocol': 'test',
                            'bytes_received': 3249935855,
                            'first_timestamp': '2023-01-12T14:02:58Z',
                            'duration': 92
                        }],
                        'origin_ips': ['11.111.111.111'],
                        'target_summary': {
                            'dst_port': 22,
                            'protocol': 'tcp',
                            'app_protocol': 'sss',
                            'bytes_sent': 3313292524,
                            'first_timestamp': '2023-01-12T14:04:05Z',
                            'last_timestamp': '2023-01-12T14:09:10Z'
                        }
                    }],
                    'multi_fields': ['', '10.250.20.137'],
                    'first_timestamp': '2023-01-12T14:04:05Z',
                    'last_timestamp': '2023-01-12T14:09:10Z',
                    'app_protocol': None,
                    'dst_ips': ['11.111.11.11'],
                    'target_domains': [],
                    'bytes_received': 33621147,
                    'bytes_sent': 3313292524,
                    'proxy_ip': None
                }],
                'summary': {
                    'dst_ports': [222],
                    'protocols': ['tcp'],
                    'bytes_sent': 3313292524,
                    'dst_ips': ['11.111.11.111']
                },
                'campaign_summaries': [],
                'is_triaged': False,
                'filtered_by_ai': False,
                'filtered_by_user': False,
                'filtered_by_rule': False,
                '_doc_modified_ts': '2023-06-25T22:01:18.599393'
            },
            {
                'summary': {
                    'artifact': ['VMAL #2 windows 11.111.11.111'],
                    'last_timestamp': '2023-01-23T20:34:39Z',
                    'description': 'This is the first time this host has been seen on the network.'
                },
                'id': 12058,
                'category': 'INFO',
                'detection': 'New Host',
                'detection_category': 'INFO',
                'detection_type': 'New Host',
                'custom_detection': None,
                'description': None,
                'src_ip': '11.111.11.111',
                'state': 'inactive',
                'certainty': 0,
                'threat': 0,
                'created_timestamp': '2023-01-23T20:40:28Z',
                'first_timestamp': '2023-01-23T20:34:39Z',
                'last_timestamp': '2023-01-23T20:34:39Z',
                'targets_key_asset': False,
                'is_targeting_key_asset': False,
                'src_account': None,
                'src_host': {
                    'id': 1609,
                    'ip': '11.111.11.111',
                    'name': 'VMAL #2 windows 11.111.11.111 (test142)',
                    'is_key_asset': False,
                    'groups': [{
                        'id': 144,
                        'name': 'Partner VLAB - Devices',
                        'description': '',
                        'last_modified': '2022-01-27T12:05:24Z',
                        'last_modified_by': 'user (Removed)',
                        'type': 'ip'
                    }],
                    'threat': 0,
                    'certainty': 0
                },
                'note': None,
                'note_modified_by': None,
                'note_modified_timestamp': None,
                'sensor': 'None',
                'sensor_name': 'vlab',
                'tags': [],
                'triage_rule_id': None,
                'assigned_to': None,
                'assigned_date': None,
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
                'grouped_details': [{
                    'artifact': 'VMAL #2 windows 11.111.11.111 (test142)',
                    'via': 'AWS Name',
                    'last_timestamp': '2023-01-23T20:34:39Z'
                }, {
                    'artifact': 'test3',
                    'via': 'AWS Resource Name',
                    'last_timestamp': '2023-01-23T20:34:39Z'
                }, {
                    'artifact': 'test142',
                    'via': 'Ker',
                    'last_timestamp': '2023-01-23T20:34:39Z'
                }],
                'campaign_summaries': [],
                'is_triaged': False,
                'filtered_by_ai': False,
                'filtered_by_user': False,
                'filtered_by_rule': False,
                '_doc_modified_ts': '2023-06-25T22:01:19.318083'
            }
        ],
        'previous': None,
        'next': 'https://test1/api/v2.4/search/detections/?page_size=9&query_string=(detection.detection:"Hidden '
                'HTTPS Tunnel" AND &page=2'}

    def connection(self):
        """format for connection"""
        return {
            "host": "hostbla",
            "port": 443
        }

    def configuration(self):
        """format for configuration"""
        return {"auth": {"api_token": "u"}}

    def test_is_async(self):
        """check for synchronous or asynchronous"""
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_modules.vectra.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_results(self, mock_ping_response):
        """test ping connection"""
        mock_ping_response.return_value = get_mock_response(200, {}, 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_modules.vectra.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_invalid_auth(self, mock_ping_response):
        """test ping connection"""
        mock_ping_response.return_value = get_mock_response(401, {}, 'byte')
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == 'authentication_fail'
        assert 'vectra connector error => Invalid Authentication' == ping_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_timeout(self, mock_ping_response):
        """Test timeout exception for ping"""
        mock_ping_response.side_effect = Exception("timeout_error")
        transmission = stix_transmission.StixTransmission('vectra', self.connection(), self.configuration())
        result_response = transmission.ping()
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'vectra connector error => timeout_error' == result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_auth(self, mock_results_response):
        """Test invalid authentication for results"""
        query = 'query_string=(detection.certainty:"22" AND (detection.last_timestamp:[2023-06-07T0640 to ' \
                '2023-06-07T0645]))'
        mock_response = json.dumps({"count": 1, "results": [], "previous": None, "next": None})
        mock_results_response.return_value = get_mock_response(401, mock_response, 'byte')
        transmission = stix_transmission.StixTransmission('vectra', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == 'authentication_fail'
        assert 'vectra connector error => Invalid Authentication' == result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_result_timeout(self, mock_result_response):
        """Test timeout exception for results"""
        mock_result_response.side_effect = Exception("timeout_error")
        query = 'query_string=((detection.grouped_details.target_domains:google.com OR ' \
                'detection.grouped_details.origin_domain:google.com) AND (detection.last_timestamp:[2023-06-07T0808 ' \
                'to 2023-06-07T0813]))'
        transmission = stix_transmission.StixTransmission('vectra', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'vectra connector error => timeout_error' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_result_invalid_parameters(self, mock_results_response):
        """Test invalid parameters for results"""
        query = 'query_string=(NOT ((detection.description:"attack" OR detection.description:"cyber") OR (' \
                'detection.summary.description:"attack" OR detection.summary.description:"cyber")) AND (' \
                'detection.last_timestamp:[2023-06-07T0952 to 2023-06-07T0957]))'
        mock_response = json.dumps({'errors': [{'type': 'InvalidQueryParamsError', 'title': 'Invalid page_size'}]})
        mock_results_response.return_value = get_mock_response(422, mock_response, 'byte')
        transmission = stix_transmission.StixTransmission('vectra', self.connection(), self.configuration())
        offset = 16
        length = 10
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == 'invalid_parameter'
        assert 'vectra connector error => Invalid Parameters' == result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_result_invalid_query(self, mock_results_response):
        """Test invalid query for results"""
        query = 'query_string=(((detection.description:"vulnerability" OR detection.description:"threat") OR (' \
                'detection.summary.description:"vulnerbility" OR detection.summary.description:"threat")) AND (' \
                'detection.last_timestamp:[2023-06-07T1024 to 2023-06-07T1029]))'
        mock_response = json.dumps({'errors': [{'title': 'Field "detection1.last_timestamp" not found in "detections" '
                                                         'index', 'offset': 1,
                                                'field_name': 'detection1.last_timestamp'}]})
        mock_results_response.return_value = get_mock_response(422, mock_response, 'byte')
        transmission = stix_transmission.StixTransmission('vectra', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == 'invalid_query'
        assert 'vectra connector error => Invalid Query' == result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_result_response(self, mock_results_response):
        """Test valid query for results"""
        query = '(detection.detection:"Hidden HTTPS Tunnel" AND (detection.last_timestamp:[2022-11-16T0000 to ' \
                '2023-05-23T0000]))'
        mock_response_1 = json.dumps(self.mocked_response)
        self.mocked_response['next'] = None
        mock_response_2 = json.dumps(self.mocked_response)
        mock_results_response.side_effect = [get_mock_response(200, mock_response_1, 'byte'),
                                             get_mock_response(200, mock_response_2, 'byte')]
        transmission = stix_transmission.StixTransmission('vectra', self.connection(), self.configuration())
        offset = 0
        length = 4
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert result_response['data'] is not None
        assert result_response['metadata'] is not None
        assert result_response['metadata']['next_page_url'] is not None

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_result_response_with_metadata(self, mock_results_response):
        """Test using metadata to get the results"""
        metadata = {'result_count': 4, 'next_page_url': 'https://test1/api/v2.4/search/detections/?page_size=4'
                                                        '&query_string=detection.detection:"Hidden HTTPS Tunnel"'
                                                        '&page=2'}
        query = 'detection.detection:"Hidden HTTPS Tunnel"'
        mock_response_1 = json.dumps(self.mocked_response)
        self.mocked_response['next'] = None
        mock_response_2 = json.dumps(self.mocked_response)
        mock_results_response.side_effect = [get_mock_response(200, mock_response_1, 'byte'),
                                             get_mock_response(200, mock_response_2, 'byte')]
        transmission = stix_transmission.StixTransmission('vectra', self.connection(), self.configuration())
        offset = 4
        length = 4
        result_response = transmission.results(query, offset, length, metadata)
        assert result_response is not None
        assert result_response['success'] is True
        assert result_response['data'] is not None
