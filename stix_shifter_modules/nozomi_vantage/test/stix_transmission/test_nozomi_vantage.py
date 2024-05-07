from stix_shifter_modules.nozomi_vantage.entry_point import EntryPoint
import unittest
from unittest.mock import patch
from stix_shifter.stix_transmission import stix_transmission
import json
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from tests.utils.async_utils import get_mock_response


class NozomiMockResponse:
    """ class for nozomi vantage mock response"""

    def __init__(self, code, data, headers):
        self.code = code
        self.content = data
        self.headers = headers

    def read(self):
        return bytearray(self.content, 'utf-8')


class TestNozomiConnection(unittest.TestCase, object):
    mocked_ping_response = {
        "data": [],
        "links": {
            "self": "/api/v1/health_logs"
        },
        "meta": {
            "sdr": "r",
            "count": 0
        },
        "included": []
    }

    mock_token_response = {
        "data": {
            "id": "38c075f1-8764-452f-bea3-fa52e32c697b",
            "type": "api_keys",
            "attributes": {
                "key_name": "keyname",
                "allowed_ips": "",
                "description": "CF Nozomi Vantage",
                "last_sign_in_at": "2023-12-19T05:55:25.348Z",
                "last_sign_in_ip": "111.111.111.11"
            },
            "relationships": {
                "user": {
                    "links": {
                        "related": "/api/v1/admin/users/12345"
                    },
                    "data": {
                        "type": "users",
                        "id": "12345"
                    }
                },
                "linked_organization": {
                    "links": {
                        "related": "/api/v1/admin/organizations/11111"
                    },
                    "data": {
                        "type": "organizations",
                        "id": "11111"
                    }
                }
            },
            "links": {
                "self": "/api/v1/api_keys/22222",
                "collection": "/api/v1/api_keys"
            }
        },
        "links": {
            "self": "/api/v1/keys/sign_in"
        },
        "meta": {
            "sdr": "w"
        }
    }

    mocked_response = {
        "result": [
            {
                "id": "132d015e-29de-41ae-88cc-5c5eaf0029e6",
                "time": 1702444878020,
                "name": "Sigma rule match",
                "type_name": "Sigma rule match",
                "threat_name": "",
                "counter": 0,
                "description": "The following suspicious local event was detected on this host: \"Detects the "
                               "execution of renamed PuTTY Plink to perform data exfiltration through tunnel port "
                               "forwarding\".",
                "ack": "false",
                "note": "null",
                "risk": 8.0,
                "id_src": "111.11.11.111",
                "id_dst": "null",
                "ip_src": "111.11.11.111",
                "ip_src:info": "null",
                "ip_dst": "null",
                "ip_dst:info": "null",
                "status": "open",
                "mac_src": "null",
                "mac_dst": "null",
                "port_dst": "null",
                "port_src": "null",
                "protocol": "",
                "transport_protocol": "unknown",
                "severity": 0,
                "zone_dst": "null",
                "zone_src": "null",
                "dst_roles": "null",
                "src_roles": "null",
                "label_dst": "null",
                "label_src": "ABCD",
                "bpf_filter": "",
                "properties": {
                    "cause": "Rule-dependent. A suspicious local event has been detected on a machine.",
                    "process": {
                        "pid": "1010",
                        "user": "user@Hostname",
                        "ancestry": "C:\\Windows\\System32\\cmd.exe",
                        "image_path": "C:\\Program Files\\Scripts\\pip.exe",
                        "command_line": "pip  install -r requirements-dev.txt",
                        "image_hash_sha256": "0101010101010101010101010101010101010101010101010101010101010101"
                    },
                    "solution": "Rule-dependent. Verify the device configuration and status, and the possible "
                                "presence of malicious processes.",
                    "raised_by": "n2os_ids",
                    "is_src_public": "false",
                    "src_logged_in:info": {
                        "source": "arc"
                    },
                    "details_hash_SHA256": {
                        "label": "SHA256",
                        "value": "0101010101010101010101010101010101010101010101010101010101010101"
                    },
                    "src_logged_in_users": [
                        "user@Hostname"
                    ]
                },
                "closed_time": 0,
                "close_option": "null",
                "is_incident": "false",
                "is_security": "true",
                "created_time": 1702444878020,
                "trigger_type": "sigma_rules",
                "capture_device": "",
                "sec_profile_visible": "true",
                "grouped_visible": "true",
                "mitre_attack_techniques": "null",
                "mitre_attack_tactics": "null",
                "playbook_contents": "null",
                "trace_status": "state_not_created",
                "appliance_host": "HOST",
                "record_created_at": 1702445039912,
                "sensor:host": "null",
                "site:name": "null",
                "type_id": "SIGN:SIGMA-RULE",
                "trigger_id": "5f9b24dd-fa05-401c-ad2"
            }
        ],
        "header": [
            "id",
            "time",
            "name",
            "type_name",
            "threat_name",
            "counter",
            "description",
            "ack",
            "note",
            "risk",
            "id_src",
            "id_dst",
            "ip_src",
            "ip_src:info",
            "ip_dst",
            "ip_dst:info",
            "status",
            "mac_src",
            "mac_dst",
            "port_dst",
            "port_src",
            "protocol",
            "transport_protocol",
            "severity",
            "zone_dst",
            "zone_src",
            "dst_roles",
            "src_roles",
            "label_dst",
            "label_src",
            "bpf_filter",
            "properties",
            "closed_time",
            "close_option",
            "is_incident",
            "is_security",
            "created_time",
            "trigger_type",
            "capture_device",
            "sec_profile_visible",
            "grouped_visible",
            "mitre_attack_techniques",
            "mitre_attack_tactics",
            "playbook_contents",
            "trace_status",
            "appliance_host",
            "record_created_at",
            "sensor:host",
            "site:name",
            "type_id",
            "trigger_id"
        ],
        "total": 86
    }
    replicated_data = []
    for _ in range(5):
        replicated_data += mocked_response['result']
    mocked_response['result'] = replicated_data
    invalid_query = {'result': [], 'header': [], 'error': 'Query is not valid.', 'total': 0}

    def connection(self):
        """format for connection"""
        return {
            "host": "hostbla",
            "port": 443
        }

    def configuration(self):
        """format for configuration"""
        return {
            "auth": {
                "key_name": "keyname",
                "key_token": "keytoken"
            }
        }

    def test_is_async(self):
        """check for synchronous or asynchronous"""
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_get_ping_results(self, mock_ping_response):
        """test ping connection"""
        mock_ping_response.side_effect = [
            get_mock_response(200, json.dumps(TestNozomiConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(200, json.dumps(TestNozomiConnection.mocked_ping_response), 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_results(self, mock_result_response):
        """ test success result response"""
        query = "alerts | where properties/process/user include? \"user@Hostname\" OR " \
                "port_dst==\"444\" | where properties/process/pid==\"1010\" OR port_dst==\"444\" | where " \
                "record_created_at>=1701388800000 | where record_created_at<=1704106800000"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestNozomiConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(200, json.dumps(TestNozomiConnection.mocked_response), 'byte')]
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_results_pagination(self, mock_result_response):
        """ test success pagination result response"""
        query = "query=alerts | where record_created_at>=1698836400000"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestNozomiConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(200, json.dumps(TestNozomiConnection.mocked_response), 'byte'),
            get_mock_response(200, json.dumps(TestNozomiConnection.mocked_response), 'byte')]
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        offset = 0
        length = 10
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_host(self, mock_result_response):
        """Test Invalid host for ping"""
        mock_result_response.side_effect = Exception("client_connector_error")
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "client_connector_error" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_url(self, mock_results_response):
        """Test invalid host for ping"""
        error = json.dumps({"errors": {"success": "false",
                                       "connector": "nozomi_vantage",
                                       "error": "nozomi connector error => Invalid Host: {'email': ['Invalid URL "
                                                "\"https://engineering-tpnovovq.customers.us1.vantage.nozominetworks"
                                                ".io\". Please contact Customer Support for assistance']}",
                                       "code": "service_unavailable"}})
        mock_results_response.return_value = get_mock_response(408, error, 'byte')
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == "service_unavailable"
        assert "Invalid Host" in ping_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_auth(self, mock_results_response):
        """Test invalid authentication for ping"""
        error = json.dumps({"errors": {"success": "false",
                                       "connector": "nozomi_vantage",
                                       "error": "nozomi_vantage connector error => Invalid Authentication: {'key_name': ['is "
                                                "invalid'], 'key_token': ['is invalid']}",
                                       "code": "authentication_fail"}})
        mock_results_response.return_value = get_mock_response(401, error, 'byte')
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == "authentication_fail"
        assert "Invalid Authentication" in ping_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_auth(self, mock_results_response):
        """Test invalid authentication for results"""
        error = json.dumps({"errors": {"success": "false",
                                       "connector": "nozomi_vantage",
                                       "error": "nozomi connector error => Invalid Authentication: {'key_name': ['is "
                                                "invalid'], 'key_token': ['is invalid']}",
                                       "code": "authentication_fail"}})
        query = "alerts | where properties/process/user include? \"user@Hostname\" OR " \
                "port_dst==\"444\" | where properties/process/pid==\"1010\" OR port_dst==\"444\" | where " \
                "record_created_at>=1701388800000 | where record_created_at<=1704106800000"
        mock_results_response.return_value = get_mock_response(401, error, 'byte')
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "authentication_fail"
        assert 'Invalid Authentication' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_host(self, mock_results_response):
        """Test invalid host for results"""
        error = json.dumps({"errors": {"success": "false",
                                       "connector": "nozomi_vantage",
                                       "error": "nozomi connector error => client_connector_error: (Cannot connect to "
                                                "host "
                                                "nozomi-sales-engineering-tpnovovqcustomers.us1.vantage"
                                                ".nozominetworks.io:443 ssl:True [getaddrinfo failed])",
                                       "code": "service_unavailable"}})
        query = "alerts | where properties/process/user include? \"user@Hostname\" OR " \
                "port_dst==\"444\" | where properties/process/pid==\"1010\" OR port_dst==\"444\" | where " \
                "record_created_at>=1701388800000 | where record_created_at<=1704106800000"
        mock_results_response.return_value = get_mock_response(401, error, 'byte')
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "service_unavailable"
        assert 'client_connector_error' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_query(self, mock_result_response):
        """Test invalid query for results"""
        query = "alerts | where properties/process/user include? \"user@Hostname\" OR " \
                "port_dst==\"444\" | where properties/process/pid==\"1010\" OR port_dst==\"444\" | where " \
                "record_created_at=1701388800000 | where record_created_at<=1704106800000"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestNozomiConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(200, json.dumps(TestNozomiConnection.invalid_query), 'byte')]
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "invalid_query"
        assert 'Query is not valid' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_url(self, mock_results_response):
        """Test invalid host for results"""
        error = json.dumps({"errors": {"success": "false",
                                       "connector": "nozomi_vantage",
                                       "error": "nozomi connector error => Invalid Host: {'email': ['Invalid URL "
                                                "\"https://engineering-tpnovovq.customers.us1.vantage.nozominetworks"
                                                ".io\". Please contact Customer Support for assistance']}",
                                       "code": "service_unavailable"}})
        query = "alerts | where properties/process/user include? \"user@Hostname\" OR " \
                "port_dst==\"444\" | where properties/process/pid==\"1010\" OR port_dst==\"444\" | where " \
                "record_created_at=1701388800000 | where record_created_at<=1704106800000"

        mock_results_response.return_value = get_mock_response(408, error, 'byte')
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "service_unavailable"
        assert 'Invalid Host' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_query_length(self, mock_results_response):
        """Test invalid host for results"""
        error = json.dumps({"errors": {"success": "false",
                                       "connector": "nozomi_vantage",
                                       "error": "nozomi connector error => Query length is too long or Invalid Query",
                                       "code": "invalid_query"}})
        query = "query=alerts | where risk<=\"1.0\" OR properties/cause==\"An IP address which is known to be " \
                "malicious has appeared in the network. Likely some kind of malware is attempting to perform " \
                "malicious activity\" | where appliance_host include? \"Hostname\" OR properties/cause==\"An " \
                "IP address which is known to be malicious has appeared in the network. Likely some kind of malware " \
                "is attempting to perform malicious activity\" | where trigger_id==\"null\" OR " \
                "properties/cause==\"An " \
                "IP address which is known to be malicious has appeared in the network. Likely some kind of malware " \
                "is attempting to perform malicious activity\" | where threat_name==\"RDP bruteforce\" OR " \
                "properties/cause==\"An IP address which is known to be malicious has " \
                "appeared in the network. Likely " \
                "some kind of malware is attempting to perform malicious activity\" | where status==\"open\" OR " \
                "properties/cause==\"An IP address which is known to be " \
                "malicious has appeared in the network. Likely " \
                "some kind of malware is attempting to perform malicious activity\" | where " \
                "type_id==\"VI:NEW-NODE:MALICIOUS-IP\" OR properties/cause==\"An IP address which is known to be " \
                "malicious has appeared in the network. Likely some kind of malware is attempting to perform " \
                "malicious activity\" | where type_name==\"Bad IP reputation (new node)\" OR properties/cause==\"An " \
                "IP address which is known to be malicious has appeared in the network. Likely some kind of malware " \
                "is attempting to perform malicious activity   \" | where record_created_at>=1698836400000 | where " \
                "record_created_at<=1706183640000"
        mock_results_response.side_effect = [
            get_mock_response(200, json.dumps(TestNozomiConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(403, error, 'byte')]
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "invalid_query"
        assert 'Query length is too long or Invalid Query' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_time_out_exception_for_results(self, mock_result_response):
        """Test timeout exception for results"""
        mock_result_response.side_effect = Exception("timeout_error")
        query = "alerts | where properties/process/user include? \"user@Hostname\" OR " \
                "port_dst==\"444\" | where properties/process/pid==\"1010\" OR port_dst==\"444\" | where " \
                "record_created_at>=1701388800000 | where record_created_at<=1704106800000"
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'timeout_error' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_server_time_out_exception_for_results(self, mock_result_response):
        """Test timeout exception for results"""
        mock_result_response.side_effect = Exception("server timeout_error (2 sec)")
        query = "alerts | where properties/process/user include? \"user@Hostname\" OR " \
                "port_dst==\"444\" | where properties/process/pid==\"1010\" OR port_dst==\"444\" | where " \
                "record_created_at>=1701388800000 | where record_created_at<=1704106800000"
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'server timeout_error (2 sec)' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_time_out_exception_for_ping(self, mock_ping_response):
        """Test timeout exception for ping"""
        mock_ping_response.side_effect = Exception("timeout_error")
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        result_response = transmission.ping()
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'timeout_error' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_with_metadata_parameter(self, mock_result_response):
        """ test success result response with metadata parameter"""
        metadata = {"page_number": 2, "page_index": 0}
        query = "query=alerts | where threat_name==\"\" | where record_created_at>=1698836400000 | where " \
                "record_created_at<=1704344040000"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestNozomiConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(200, json.dumps(TestNozomiConnection.mocked_response), 'byte')]
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length, metadata)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_with_invalid_metadata_parameter(self, mock_result_response):
        """ test invalid metadata parameter"""
        metadata = {'next_page_token': '123a'}
        query = "alerts | where properties/process/user include? \"user@Hostname\" OR " \
                "port_dst==\"444\" | where properties/process/pid==\"1010\" OR port_dst==\"444\" | where " \
                "record_created_at>=1701388800000 | where record_created_at<=1704106800000"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestNozomiConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(200, json.dumps(TestNozomiConnection.mocked_response), 'byte')]
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length, metadata)
        assert result_response is not None
        assert result_response['success'] is False
        assert "Invalid metadata" in result_response['error']
        assert result_response['code'] == "invalid_parameter"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_with_expired_jwt_token(self, mock_result_response):
        """ test expired jwt token"""
        metadata = {"page_number": 2, "page_index": 0}
        query = "alerts | where port_dst>\"22\" | where record_created_at>=1701388800000 | where " \
                "record_created_at<=1704106800000 "
        mock_result_response.side_effect = [get_mock_response(200, json.dumps(TestNozomiConnection.mock_token_response),
                                                              'byte', headers={'Authorization': "****"}),
                                            get_mock_response(401, '', 'byte'),
                                            get_mock_response(200, json.dumps(TestNozomiConnection.mock_token_response),
                                                              'byte', headers={'Authorization': "****"}),
                                            get_mock_response(401, '', 'byte')]
        transmission = stix_transmission.StixTransmission('nozomi_vantage', self.connection(), self.configuration())
        result_response = transmission.results(query, 1, 1, metadata)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "authentication_fail"
