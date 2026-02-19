from stix_shifter_modules.cisco_secure_email.entry_point import EntryPoint
import unittest
from unittest.mock import patch
from stix_shifter.stix_transmission import stix_transmission
import json
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from tests.utils.async_utils import get_mock_response


class CiscoEmailMockResponse:
    """ class for Cisco Secure Email mock response"""

    def __init__(self, code, data, headers):
        self.code = code
        self.content = data
        self.headers = headers

    def read(self):
        return bytearray(self.content, 'utf-8')


class TestCiscoEmailConnection(unittest.TestCase, object):
    mocked_ping_response = {"data": ["e_message_tracking_messages",
                                     "e_message_tracking_detail",
                                     "e_message_tracking_amp_details",
                                     "e_message_tracking_connection_details"]
                            }
    mock_token_response = {"data": {"userName": "u",
                                    "is2FactorRedirectRequired": "false",
                                    "role": "HelpDeskUser",
                                    "jwtToken": "eyJhxxxxxxxxxxB7as"
                                    }
                           }
    mock_email_result = {
        "meta": {
            "num_bad_records": 0,
            "totalCount": 1
        },
        "data": [
            {
                "attributes": {
                    "hostName": "",
                    "mid": [
                        1619
                    ],
                    "isCompleteData": "N/A",
                    "messageStatus": {
                        "1619": "Dropped By Anti-Virus"
                    },
                    "recipientMap": {
                        "1619": [
                            "user1@isc.com"
                        ]
                    },
                    "senderIp": "1.1.1.1",
                    "mailPolicy": [
                        "DEFAULT"
                    ],
                    "senderGroup": "UNKNOWNLIST",
                    "subject": "virus mail",
                    "friendly_from": [
                        "user1@isc.com"
                    ],
                    "senderDomain": "isc.com",
                    "direction": "incoming",
                    "icid": 1350,
                    "morDetails": {},
                    "replyTo": "N/A",
                    "timestamp": "31 Jul 2023 15:20:45 (GMT +00:00)",
                    "messageID": {},
                    "verdictChart": {
                        "1619": "01500000"
                    },
                    "recipient": [
                        "user1@isc.com"
                    ],
                    "sender": "user2@isc.com",
                    "serialNumber": "EC2Cxxxx4D1B",
                    "allIcid": [
                        1350
                    ],
                    "sbrs": "None"
                }
            }
        ]
    }

    mock_email_result2 = {
        "meta": {
            "num_bad_records": 0,
            "totalCount": 1
        },
        "data": [
            {
                "attributes": {
                    "hostName": "",
                    "mid": [
                        1620
                    ],
                    "isCompleteData": "N/A",
                    "messageStatus": {
                        "1620": "Dropped By Anti-Virus"
                    },
                    "recipientMap": {
                        "1620": [
                            "user1@isc.com"
                        ]
                    },
                    "senderIp": "1.1.1.1",
                    "mailPolicy": [
                        "DEFAULT"
                    ],
                    "senderGroup": "UNKNOWNLIST",
                    "subject": "virus mail",
                    "friendly_from": [
                        "user1@isc.com"
                    ],
                    "senderDomain": "isc.com",
                    "direction": "incoming",
                    "icid": 1351,
                    "morDetails": {},
                    "replyTo": "N/A",
                    "timestamp": "31 Jul 2023 15:20:50 (GMT +00:00)",
                    "messageID": {},
                    "verdictChart": {
                        "1620": "01500000"
                    },
                    "recipient": [
                        "user1@isc.com"
                    ],
                    "sender": "user2@isc.com",
                    "serialNumber": "EC2Cxxxx4D1C",
                    "allIcid": [
                        1351
                    ],
                    "sbrs": "None"
                }
            }
        ]
    }

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
                "username": "u",
                "password": "p"
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
            get_mock_response(200, json.dumps(TestCiscoEmailConnection.mock_token_response), 'byte'),
            get_mock_response(200, json.dumps(TestCiscoEmailConnection.mocked_ping_response), 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_results(self, mock_result_response):
        """ test success result response"""
        query = "senderIP=1.1.1.1"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestCiscoEmailConnection.mock_token_response), 'byte'),
            get_mock_response(200, json.dumps(TestCiscoEmailConnection.mock_email_result), 'byte')]
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_results_pagination(self, mock_result_response):
        """ test success result response"""
        query = "senderIP=1.1.1.1"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestCiscoEmailConnection.mock_token_response), 'byte'),
            get_mock_response(200, json.dumps(TestCiscoEmailConnection.mock_email_result), 'byte'),
            get_mock_response(200, json.dumps(TestCiscoEmailConnection.mock_email_result2), 'byte')]
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
        offset = 0
        length = 2
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response
        assert result_response['data'][0] is not None
        assert result_response['data'][1] is not None
        assert 'metadata' in result_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_host(self, mock_result_response):
        """Test Invalid host for ping"""
        mock_result_response.side_effect = Exception("client_connector_error")
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "client_connector_error" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_auth(self, mock_results_response):
        """Test invalid authentication for ping"""
        error = json.dumps({"error": {"message": "Invalid username or passphrase.",
                                      "code": "401",
                                      "explanation": "401 = No permission -- see authorization schemes."}})
        mock_results_response.return_value = get_mock_response(401, error, 'byte')
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == "authentication_fail"
        assert "Invalid username" in ping_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_auth(self, mock_results_response):
        """Test invalid authentication for results"""
        error = json.dumps({"error": {"message": "Invalid username or passphrase.",
                                      "code": "401",
                                      "explanation": "401 = No permission -- see authorization schemes."}})
        query = "senderIP=1.1.1.1"
        mock_results_response.return_value = get_mock_response(401, error, 'byte')
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "authentication_fail"
        assert 'Invalid username' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_time_out_exception_for_results(self, mock_result_response):
        """Test timeout exception for results"""
        mock_result_response.side_effect = Exception("timeout_error")
        query = "senderIP=1.1.1.1"
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
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
        query = "senderIP=1.1.1.1"
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
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
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
        result_response = transmission.ping()
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'timeout_error' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_with_metadata_parameter(self, mock_result_response):
        """ test success result response with metadata parameter"""
        metadata = {'jwtToken': 'abcdxxxxxxdefg'}
        query = "senderIP=1.1.1.1"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestCiscoEmailConnection.mock_email_result), 'byte')]
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
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
        query = "senderIP=1.1.1.1"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestCiscoEmailConnection.mock_token_response), 'byte'),
            get_mock_response(200, json.dumps(TestCiscoEmailConnection.mock_email_result), 'byte')]
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length, metadata)
        assert result_response is not None
        assert result_response['success'] is False
        assert "Invalid metadata" in result_response['error']
        assert result_response['code'] == "invalid_parameter"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_query(self, mock_results_response):
        """Test invalid authentication for results"""
        error = json.dumps({'error': {'message': 'Missing attribute - startDate or endDate.', 'code': '404',
                                      'explanation': '404 = Nothing matches the given URI.'}})
        query = "senderIP=1.1.1.1"
        mock_results_response.side_effect = [
            get_mock_response(200, json.dumps(TestCiscoEmailConnection.mock_token_response), 'byte'),
            get_mock_response(404, error, 'byte')]
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "invalid_query"
        assert 'Nothing matches the given URI' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_certificate(self, mock_results_response):
        """Test invalid certificate for results"""
        mock_results_response.side_effect = Exception("[X509] PEM lib (_ssl.c:4293)")
        transmission = stix_transmission.StixTransmission('cisco_secure_email', self.connection(), self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results('', offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "certificate_fail"
        assert "Invalid Self Signed Certificate" in result_response['error']
