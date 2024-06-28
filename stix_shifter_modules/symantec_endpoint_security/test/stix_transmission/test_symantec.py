from stix_shifter_modules.symantec_endpoint_security.entry_point import EntryPoint
import unittest
from unittest.mock import patch
from stix_shifter.stix_transmission import stix_transmission
import json
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from tests.utils.async_utils import get_mock_response


class SymantecMockResponse:
    """ class for symantec mock response"""

    def __init__(self, code, data, headers):
        self.code = code
        self.content = data
        self.headers = headers

    def read(self):
        return bytearray(self.content, 'utf-8')


class TestSymantecConnection(unittest.TestCase, object):
    mocked_ping_response = {
        "access_token": "eyJraWQiOiI3b9TCMsn_0AONWzahwHjHwSdyOq2NqDCcviaV-T5W2A5Bu5197Q",
        "token_type": "Bearer",
        "expires_in": 3600
    }

    mock_token_response = {
        "access_token": "eyJraWQiOiI3b9TCMsn_0AONWzahwHjHwSdyOq2NqDCcviaV-T5W2A5Bu5197Q",
        "token_type": "Bearer",
        "expires_in": 3600
    }

    mocked_response = {
        "total": 14952,
        "events": [
            {
                "device_os_type_id": 100,
                "lineage": [
                    "C:\\Windows\\System32\\services.exe",
                    "C:\\Windows\\System32\\wininit.exe"
                ],
                "feature_uid": "1DF0351C-146D-4F07-B155-BF5C7077FF40",
                "type": "event_query_results",
                "seq_num": 1,
                "ref_uid": "1A45B466-EA3C-4101-A570-4FD3C19C51DD",
                "legacy_product_uid": "ad66b334-9eb8-bf35-3f4e-f172b06200b0",
                "id": 1,
                "product_uid": "31B0C880-0229-49E8-94C5-48D56B1BD7B9",
                "feature_name": "DETECTION_RESPONSE",
                "device_group": "Default/TestEDRGroup",
                "product_name": "Symantec Endpoint Security",
                "version": "1.0.0",
                "command_uid": "",
                "device_ip": "1.1.1.1",
                "device_vhost": 12,
                "user_name": "SYSTEM",
                "timezone": 0,
                "device_domain": "WORKGROUP",
                "product_ver": "14.3.10148.8000",
                "device_name": "HOST_NAME",
                "category_id": 5,
                "device_networks": [
                    {
                        "ipv4": "1.1.1.1",
                        "ipv6": "xx00:0000:0000:0000:000x:xx0x:0000:00x0",
                        "mac": "0x:0x:00:00:0x:00"
                    }
                ],
                "device_os_name": "",
                "type_id": 8001,
                "actor": {
                    "session_id": 0,
                    "pid": 836,
                    "uid": "C03AA2F5-0907-F1EF-848A-EAEACDB378C2",
                    "tid": 5092,
                    "start_time": "2024-05-03T04:44:03.418Z",
                    "cmd_line": "C:\\Windows\\system32\\services.exe",
                    "integrity_id": 6,
                    "file": {
                        "type_id": 1,
                        "created": "2024-03-20T09:45:38.416Z",
                        "modified": "2024-03-20T09:45:38.447Z",
                        "md5": "0x000x0xx0x0000000x0xx00xxx0x00x00",
                        "sha2": "222e222c222b2b2222e2dd22d2df222222222cc2222222222ed22222b22d22b",
                        "size": 686968,
                        "security_descriptor": "O:BAG:SYD:(A;;0x1fffff;;;SY)(A;;0x121411;;;BA)S:AI",
                        "normalized_path": "CSIDL_SYSTEM\\services.exe",
                        "path": "c:\\windows\\system32\\services.exe",
                        "uid": "281474977475580",
                        "name": "services.exe",
                        "folder": "c:\\windows\\system32",
                        "original_name": "services.exe"
                    },
                    "user": {
                        "name": "SYSTEM",
                        "sid": "X-1-1-11",
                        "domain": "NT AUTHORITY"
                    },
                    "cmd_line_raw_length": 32
                },
                "device_mac": "1x:1x:11:11:1x:11",
                "device_uid": "X4oOxiAoQO6SuZAfO6lm4Q",
                "org_unit_uid": "_RE5UsoeSKSrteDkP3U2Mw",
                "severity_id": 1,
                "logging_device_post_time": "2024-05-03T04:55:21.550Z",
                "device_time": "2024-05-03T04:55:21.553Z",
                "process": {
                    "session_id": 0,
                    "pid": 4012,
                    "uid": "C03AACCB-0907-F1EF-848A-EAEACDB378C2",
                    "start_time": "2024-05-03T04:55:21.553Z",
                    "cmd_line": "C:\\Windows\\System32\\svchost.exe -k LocalSystemNetworkRestricted -p -s StorSvc",
                    "integrity_id": 6,
                    "file": {
                        "type_id": 1,
                        "created": "2022-09-14T16:17:52.744Z",
                        "modified": "2022-09-14T16:17:52.744Z",
                        "md5": "1xx11x111xx11x1x11x11x11x1xx1111",
                        "sha2": "3x333xx333x3xxx333x33333333x3x33x33x333xxx3333x3xx3333x3333xxx3x",
                        "size": 51736,
                        "signature_company_name": "Microsoft Windows Publisher",
                        "signature_value_ids": [
                            3,
                            5
                        ],
                        "security_descriptor": "O:S-1-1-1-0-1894134G:SYD:"
                                               "(A;;0x1fffff;;;S-1-1-1-0-1894134)(A;;0x1400;;;BA)S:AI",
                        "normalized_path": "CSIDL_SYSTEM\\svchost.exe",
                        "path": "c:\\windows\\system32\\svchost.exe",
                        "uid": "281474976968790",
                        "name": "svchost.exe",
                        "folder": "c:\\windows\\system32",
                        "original_name": "svchost.exe",
                        "signature_level_id": 60
                    },
                    "user": {
                        "name": "SYSTEM",
                        "sid": "S-1-1-11",
                        "domain": "NT AUTHORITY"
                    },
                    "cmd_line_raw_length": 77
                },
                "edr_enriched_data": {
                    "category_name": "Process Launch",
                    "category_id": 2,
                    "event_group_id": "A3FA2AA2-B890-4074-814A-072F53BF83BF",
                    "suspicion_score": 0,
                    "rule_id": 1351,
                    "rule_name": "eGenericProcessLaunch",
                    "rule_description": "Generic process launch event"
                },
                "feature_ver": "edr/1.3.0",
                "event_data_type": "fdr",
                "user": {
                    "domain": "NT AUTHORITY",
                    "name": "SYSTEM",
                    "sid": "S-1-1-11"
                },
                "device_os_ver": "10.0.17763",
                "policy": {
                    "uid": "a7124b68-abc1-43a4-8e44-716fb1966646",
                    "name": "Default Detection and Response Policy",
                    "version": "1"
                },
                "trans_event_raw_length": 3493,
                "attacks": [
                    {
                        "technique_uid": "T1569",
                        "technique_name": "System Services",
                        "tactic_ids": [
                            2
                        ],
                        "tactic_uids": [
                            "TA0002"
                        ],
                        "sub_technique_name": "Service Execution",
                        "sub_technique_uid": "T1569.002"
                    }
                ],
                "customer_uid": "IKhSB-yfRK2xeUR-xyCK2g",
                "device_public_ip": "4.4.4.4",
                "domain_uid": "B3dKzLSzR9CScPYAGhkgxA",
                "time": "2024-05-03T04:55:21.553Z",
                "log_time": "2024-05-03T04:56:19.400Z",
                "uuid": "8001:587a2410-0909-11ef-deb7-0000061b19b4",
                "indexDate": "2024-05-03",
                "indexHash": "fdr_4_t2",
                "log_name": "c1.fdr_4_t2_2024-05-03",
                "es.mapping.id": "uuid",
                "epochLogTime": 1714712179400,
                "es.mapping.version": "epochLogTime"
            }
        ],
        "next": 1001
    }

    replicated_data = []
    for _ in range(5):
        replicated_data += mocked_response['events']
    mocked_response['events'] = replicated_data
    invalid_query = {"message": "Invalid query. Search is not allowed on field 'Sdevice_location.desc'"}

    @staticmethod
    def connection():
        """format for connection"""
        return {
            "host": "hostbla",
            "port": 443
        }

    @staticmethod
    def configuration():
        """format for configuration"""
        return {
            "auth": {
                "oauth_credentials": "auth_token"
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
            get_mock_response(200, json.dumps(TestSymantecConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(200, json.dumps(TestSymantecConnection.mocked_ping_response), 'byte')]
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_results(self, mock_result_response):
        """ test success result response"""
        query = "{\"feature_name\":\"ALL\",\"query\":\"uuid:4\\\:71f801e0-0905-11ef-f724-000001ce90c3\"," \
                " \"start_date\":\"2024-05-01T00:00:00.000+05:30\", \"end_date\": \"2024-05-09T03:00:00.000+05:30\"," \
                "\"product\":\"SAEP\",\"limit\":1}"

        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestSymantecConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(200, json.dumps(TestSymantecConnection.mocked_response), 'byte')]
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_results_pagination(self, mock_result_response):
        """ test success pagination result response"""
        query = "{\"feature_name\": \"ALL\",\"product\": \"SAEP\", " \
                "\"query\": \"device_name:HOST_NAME\"," \
                "\"start_date\": \"2024-05-01T11:00:00.000+00:00\", \"end_date\": \"2024-05-13T04:00:00.000+00:00\"," \
                "\"limit\":1000, \"next\":1}"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestSymantecConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(200, json.dumps(TestSymantecConnection.mocked_response), 'byte'),
            get_mock_response(200, json.dumps(TestSymantecConnection.mocked_response), 'byte')]
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
        offset = 9999
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_host(self, mock_result_response):
        """Test Invalid host for ping"""
        mock_result_response.side_effect = Exception("client_connector_error")
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "client_connector_error" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_url(self, mock_results_response):
        """Test invalid host for ping"""
        error = json.dumps({"fault": {"faultstring": "Unable to identify proxy for host: secure and "
                                                     "url: \\/v1\\/oauth2\\/token",
                                      "detail": {"errorcode": "messaging.adaptors.http.flow.ApplicationNotFound"}}})
        mock_results_response.return_value = get_mock_response(404, error, 'byte')
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == "service_unavailable"
        assert "Unable to identify proxy for host" in ping_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_invalid_auth(self, mock_results_response):
        """Test invalid authentication for ping"""
        error = json.dumps({"message": "No client_id found [M2ID.XuSKt5Q3Rb6wSujIS9Rh7Q.PJblnny1Q4G26epFnNsnWg."
                                       "201ol7b749n8446694c3hid7a7]"})
        mock_results_response.return_value = get_mock_response(401, error, 'byte')
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == "authentication_fail"
        assert "No client_id found" in ping_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_query(self, mock_result_response):
        """Test invalid query for results"""
        query = "{\"feature_name\": \"ALL\",\"product\": \"SAEP\", " \
                "\"query\": \"device_name:HOST_NAME\"," \
                "\"start_date\": \"2024-05-01T11:00:00.000+00:00\", \"end_date\": \"2024-05-13T04:00:00.000+00:00\"," \
                "\"limit\":1000, \"next\":1}"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestSymantecConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(400, json.dumps(TestSymantecConnection.invalid_query), 'byte')]
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "invalid_query"
        assert 'Invalid query' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_results_invalid_url(self, mock_results_response):
        """Test invalid url for results"""
        error = json.dumps({"fault": {"faultstring": "Unable to identify proxy for host: secure and"
                                                     " url: \\/v1\\/oauth2\\/token",
                                      "detail": {"errorcode": "messaging.adaptors.http.flow.ApplicationNotFound"}}})
        query = "{\"feature_name\": \"ALL\",\"product\": \"SAEP\", " \
                "\"query\": \"device_name:HOST_NAME\"," \
                "\"start_date\": \"2024-05-01T11:00:00.000+00:00\", \"end_date\": \"2024-05-13T04:00:00.000+00:00\"," \
                "\"limit\":1000, \"next\":1}"

        mock_results_response.return_value = get_mock_response(404, error, 'byte')
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "service_unavailable"
        assert 'Unable to identify proxy for host' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_time_out_exception_for_results(self, mock_result_response):
        """Test timeout exception for results"""
        mock_result_response.side_effect = Exception("timeout_error")
        query = "{\"feature_name\": \"ALL\",\"product\": \"SAEP\", " \
                "\"query\": \"device_name:HOST_NAME\"," \
                "\"start_date\": \"2024-05-01T11:00:00.000+00:00\", \"end_date\": \"2024-05-13T04:00:00.000+00:00\"," \
                "\"limit\":1000, \"next\":1}"
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
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
        query = "{\"feature_name\": \"ALL\",\"product\": \"SAEP\", " \
                "\"query\": \"device_name:HOST_NAME\"," \
                "\"start_date\": \"2024-05-01T11:00:00.000+00:00\", \"end_date\": \"2024-05-13T04:00:00.000+00:00\"," \
                "\"limit\":1000, \"next\":1}"
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
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
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
        result_response = transmission.ping()
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert 'timeout_error' in result_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_success_query_with_metadata_parameter(self, mock_result_response):
        """ test success result response with metadata parameter"""
        metadata = {
            "start_date": "2024-05-03T04:55:21.553Z",
            "start_date_event_count": 1
        }
        query = "{\"feature_name\": \"ALL\",\"product\": \"SAEP\", " \
                "\"query\": \"device_name:HOST_NAME\"," \
                "\"start_date\": \"2024-05-01T11:00:00.000+00:00\", \"end_date\": \"2024-05-13T04:00:00.000+00:00\"," \
                "\"limit\":1000, \"next\":1}"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestSymantecConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(200, json.dumps(TestSymantecConnection.mocked_response), 'byte')]
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length, metadata)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_with_invalid_metadata_parameter(self, mock_result_response):
        """ test invalid metadata parameter"""
        metadata = {'mext_page': '123a'}
        query = "{\"feature_name\": \"ALL\",\"product\": \"SAEP\", " \
                "\"query\": \"device_name:HOST_NAME\"," \
                "\"start_date\": \"2024-05-01T11:00:00.000+00:00\", \"end_date\": \"2024-05-13T04:00:00.000+00:00\"," \
                "\"limit\":1000, \"next\":1}"
        mock_result_response.side_effect = [
            get_mock_response(200, json.dumps(TestSymantecConnection.mock_token_response), 'byte',
                              headers={'Authorization': "****"}),
            get_mock_response(200, json.dumps(TestSymantecConnection.mocked_response), 'byte')]
        transmission = stix_transmission.StixTransmission('symantec_endpoint_security', self.connection(),
                                                          self.configuration())
        offset = 0
        length = 1
        result_response = transmission.results(query, offset, length, metadata)
        assert result_response is not None
        assert result_response['success'] is False
        assert "{'mext_page': '123a'}" in result_response['error']
        assert result_response['code'] == "unknown"
