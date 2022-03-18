import unittest
from unittest.mock import patch
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_modules.paloalto.entry_point import EntryPoint
import json


class PaloaltoMockResponse:
    """ class for Palo Alto mock response"""

    def __init__(self, response_code, txt):
        self.status_code = response_code
        self.content = txt

    def read(self):
        """ to read contents of results returned by api"""
        return bytearray(self.content, 'utf-8')


class StatusResponse:
    """ class for status response"""

    def __init__(self, code, txt):
        self.code = code
        self.content = txt

    def read(self):
        return bytearray(self.content, 'utf-8')


class PingResponse:
    """ class for ping outer response"""

    def __init__(self, response_object):
        self.response = response_object

    def read(self):
        return bytearray(self.response.content, 'utf-8')


class QuotaResponse:
    """ class for ping outer response"""

    def __init__(self, response_object):
        self.response = response_object


class TestPaloaltoConnection(unittest.TestCase, object):

    @staticmethod
    def connection():
        return {
            "host": "hostbla"
        }

    @staticmethod
    def configuration():
        return {
            "auth": {
                "api_key": "bla",
                "api_key_id": "bla",
                "tenant": "bla"
            }
        }
 
    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping(self, mock_ping_response):
        """test ping connection"""
        mocked_return_value = '{"reply":{"used_quota": 0.08015277777777775}}'
        mock_ping = PaloaltoMockResponse(200, mocked_return_value)
        mock_ping_response.return_value = PingResponse(mock_ping)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.create_search')
    def test_query_response(self, mock_search_response):
        """test create search query"""
        mocked_return_value = '{"reply": {"search_id": "07f63c733f5946_15006_inv"}}'
        mock_search = PaloaltoMockResponse(200, mocked_return_value)
        search_response = PingResponse(mock_search)
        mock_search_response.return_value = search_response

        query = json.dumps({"xdr_data": {"query": "dataset = xdr_data | filter ((action_process_image_name not in ("
                                                  "\"conhost.exe\",\"AtBroker.exe\") or actor_process_image_name not "
                                                  "in (\"conhost.exe\",\"AtBroker.exe\") or "
                                                  "causality_actor_process_image_name not in (\"conhost.exe\","
                                                  "\"AtBroker.exe\") or os_actor_process_image_name not in ("
                                                  "\"conhost.exe\",\"AtBroker.exe\"))  and (to_epoch(_time,"
                                                  "\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") <= "
                                                  "1644883200000)) or ((action_process_file_create_time = "
                                                  "1643704990003 or actor_process_file_create_time = 1643704990003 or "
                                                  "causality_actor_process_file_create_time = 1643704990003 or "
                                                  "os_actor_process_file_create_time = 1643704990003)  and (to_epoch("
                                                  "_time,\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") "
                                                  "<= 1644883200000)) or ((action_process_image_name ~= \"wildfire$\" "
                                                  "or actor_process_image_name ~= \"wildfire$\" or "
                                                  "causality_actor_process_image_name ~= \"wildfire$\" or "
                                                  "os_actor_process_image_name ~= \"wildfire$\")  and (to_epoch("
                                                  "_time,\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") "
                                                  "<= 1644883200000)) | alter dataset_name = \"xdr_data\" | fields "
                                                  "dataset_name,action_local_ip,action_remote_ip,"
                                                  "agent_ip_addresses_v6,dst_agent_ip_addresses_v6,action_local_port,"
                                                  "action_remote_port,action_network_protocol,action_file_name,"
                                                  "action_file_size,action_file_md5,action_module_md5,"
                                                  "action_process_image_md5,action_file_authenticode_sha1,"
                                                  "action_file_authenticode_sha2,action_file_sha256,"
                                                  "action_module_sha256,action_process_image_sha256,"
                                                  "action_file_access_time,actor_process_file_access_time,"
                                                  "os_actor_process_file_access_time,action_file_mod_time,"
                                                  "actor_process_file_mod_time,os_actor_process_file_mod_time,"
                                                  "action_file_create_time,action_file_path,"
                                                  "action_process_image_path,action_registry_file_path,"
                                                  "actor_process_image_path,causality_actor_process_image_path,"
                                                  "os_actor_process_image_path,action_process_image_command_line,"
                                                  "actor_process_command_line,causality_actor_process_command_line,"
                                                  "os_actor_process_command_line,action_process_file_create_time,"
                                                  "actor_process_file_create_time,"
                                                  "causality_actor_process_file_create_time,"
                                                  "os_actor_process_file_create_time,action_process_image_name,"
                                                  "actor_process_image_name,causality_actor_process_image_name,"
                                                  "os_actor_process_image_name,action_module_process_os_pid ,"
                                                  "action_process_os_pid,actor_process_os_pid,"
                                                  "causality_actor_process_os_pid,os_actor_process_os_pid,"
                                                  "action_process_requested_parent_pid,action_thread_parent_pid,"
                                                  "action_thread_child_pid,action_process_username,auth_domain,"
                                                  "dst_host_metadata_domain,host_metadata_domain,"
                                                  "dst_action_url_category ,action_registry_key_name,"
                                                  "action_registry_value_name,mac,associated_mac,dst_associated_mac ,"
                                                  "dst_mac,dst_user_id,user_id,action_username,"
                                                  "actor_primary_username,actor_process_logon_id | limit 10000 ",
                                         "timeframe": {"from": 1644451200000, "to": 1644883200000}}})

        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_status')
    def test_status_response(self, mock_status_response):
        mocked_return_value = '{"reply" : {"status": "SUCCESS","number_of_results":100}}'
        mock_status_response.return_value = StatusResponse(200, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert status_response['status'] == "COMPLETED"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_results')
    def test_result_response(self, mock_result_response):
        """test for valid result response"""
        mocked_return_value = json.dumps({"reply": {"status": "SUCCESS",
                                                    "number_of_results": 1,
                                                    "results": {"data": [{"dataset_name": "xdr_data",
                                                                          "causality_actor_process_image_name":
                                                                              "taskhostw.exe"}]}}})
        mock_result_response.return_value = StatusResponse(200, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        offset = 0
        length = 3
        result_response = transmission.results(search_id, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response
        assert result_response['data'] == [{'xdr_data': {'causality_actor_process_image_name': 'taskhostw.exe'}}]

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_results')
    def test_result_with_empty_nt_response(self, mock_result_response):
        """test for valid result response"""
        mocked_return_value = json.dumps({"reply": {"status": "SUCCESS",
                                                    "number_of_results": 1,
                                                    "results": {"data": [{"dataset_name": "xdr_data",
                                                                          'action_local_ip': '', 'action_remote_ip': '',
                                                                          'agent_ip_addresses_v6': None,
                                                                          'dst_agent_ip_addresses_v6': None,
                                                                          'action_local_port': 0,
                                                                          'action_remote_port': 0,
                                                                          'action_pkts_sent': None,
                                                                          'action_pkts_received': None,
                                                                          'action_network_protocol': "NULL",
                                                                          'actor_process_image_name': "lsass.exe"}]}}})
        mock_result_response.return_value = StatusResponse(200, mocked_return_value)
        search_id = "62428d95420f47_24655_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        offset = 0
        length = 3
        result_response = transmission.results(search_id, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response
        assert result_response['data'] == [{'xdr_data': {'actor_process_image_name': 'lsass.exe'}}]

    def test_delete_response(self):
        """test delete response"""
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        search_id = "e1d1b56ca81845_15180_inv"
        delete_response = transmission.delete(search_id)
        assert delete_response is not None
        assert delete_response['success'] is True
        assert delete_response['message'] == "Delete operation of a search id is not supported in Palo Alto Cortex XDR"

    def test_is_async(self):
        """check for synchronous or asynchronous"""
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async is True

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_400_exception(self, mock_ping_response):
        """Test ping response with 400 exception"""
        mocked_return_value = '{"reply":{"err_msg": "InvalidJson"}}'
        mock_ping = PaloaltoMockResponse(400, mocked_return_value)
        mock_ping_response.return_value = PingResponse(mock_ping)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert 'error' in ping_response
        assert ping_response['code'] == "invalid_query"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_401_auth_exception(self, mock_ping_response):
        """test 401 authentication error exception"""
        mocked_return_value = '{"reply": { "err_msg" : "auth Error"}}'
        mock_ping = PaloaltoMockResponse(401, mocked_return_value)
        mock_ping_response.return_value = PingResponse(mock_ping)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == "authentication_fail"
        assert "Invalid api_key" in ping_response['error']

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_500_exception(self, mock_ping_response):
        """check 500 bad query exception"""
        mocked_return_value = '{"reply": {"err_extra":{"parse_err" :"Internal server error" }}}'
        mock_ping = PaloaltoMockResponse(500, mocked_return_value)
        mock_ping_response.return_value = PingResponse(mock_ping)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "Bad query Syntax" in ping_response["error"]
        assert ping_response["code"] == "invalid_query"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_internal_server_exception(self, mock_ping_response):
        """check 500 bad query exception"""
        mocked_return_value = '{"reply": {"err_msg":"Internal server error","err_extra":"server error"}}'
        mock_ping = PaloaltoMockResponse(500, mocked_return_value)
        mock_ping_response.return_value = PingResponse(mock_ping)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "Internal server error" in ping_response["error"]
        assert ping_response["code"] == "invalid_parameter"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_402_license_exception(self, mock_ping_response):
        """Check 402 invalid license exception"""
        mocked_return_value = '{"reply": { "err_msg" : "Invalid license"}}'
        mock_ping = PaloaltoMockResponse(402, mocked_return_value)
        mock_ping_response.return_value = PingResponse(mock_ping)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert 'error' in ping_response
        assert ping_response['code'] == "service_unavailable"
        assert "User does not have the required license type to run this API" in ping_response['error']

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_status')
    def test_status_empty_result_exception(self, mock_status_response):
        """Test empty results exception"""
        mocked_return_value = '{"reply" : {"status": "SUCCESS"}}'
        mock_status_response.return_value = StatusResponse(200, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is False
        assert 'error' in status_response
        assert "Empty results received from Tenant" in status_response['error']
        assert status_response['code'] == "no_results"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_status')
    def test_status_partial_success_exception(self, mock_status_response):
        """Test partial success status response exception"""
        mocked_return_value = '{"reply" : {"status": "PARTIAL_SUCCESS"}}'
        mock_status_response.return_value = StatusResponse(200, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert status_response['message'] == "Partial Success -At least one tenant failed to execute the query"
        assert status_response['status'] == "COMPLETED"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_status')
    def test_status_fail_exception(self, mock_search_response):
        """Test status fail exception"""
        mocked_return_value = '{"reply" : {"status": "FAIL"}}'
        mock_search_response.return_value = StatusResponse(200, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is False
        assert "Tenant Query Failed" in status_response['error']
        assert status_response['code'] == "invalid_query"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_results')
    def test_failed_query_response(self, mock_result_response):
        """Test failed query result response"""
        mocked_return_value = json.dumps({"reply": {"status": "FAIL"}})
        mock_result_response.return_value = StatusResponse(200, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        offset = 0
        length = 3
        result_response = transmission.results(search_id, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert "Tenant Query Failed" in result_response['error']
        assert result_response['code'] == "invalid_query"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.create_search')
    def test_create_query_value_error_exception(self, mock_search_response):
        """test create query value error with invalid json"""
        mocked_return_value = "Invalid_json"
        mock_search = PaloaltoMockResponse(200, mocked_return_value)
        search_response = PingResponse(mock_search)
        mock_search_response.return_value = search_response
        query = ""
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert 'error' in query_response
        assert "Cannot parse response" in query_response["error"]

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_value_error_exception(self, mock_search_response):
        """test ping connector value error with invalid json"""
        mocked_return_value = "Invalid_json"
        mock_search = PaloaltoMockResponse(200, mocked_return_value)
        search_response = PingResponse(mock_search)
        mock_search_response.return_value = search_response
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        query_response = transmission.ping()
        assert query_response is not None
        assert query_response['success'] is False
        assert 'error' in query_response
        assert "Cannot parse response" in query_response["error"]

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.create_search')
    def test_create_query_exception(self, mock_search_response):
        """Test search response with 400 exception"""
        mocked_return_value = '{"reply": { "err_msg" : "400 error"}}'
        mock_ping = PaloaltoMockResponse(400, mocked_return_value)
        mock_search_response.return_value = PingResponse(mock_ping)
        query = "{}"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        ping_response = transmission.query(query)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert 'error' in ping_response
        assert ping_response['code'] == "invalid_query"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_results')
    def test_results_value_error_exception(self, get_search_results):
        """test results connector value error with invalid json"""
        mocked_return_value = "Invalid json"
        get_search_results.return_value = StatusResponse(200, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        offset = 0
        length = 3
        result_response = transmission.results(search_id, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'error' in result_response
        assert "Cannot parse response" in result_response["error"]

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_results')
    def test_results_401_exception(self, get_search_results):
        """test results with 401 exception"""
        mocked_return_value = '{"reply": { "err_msg" : "auth Error"}}'
        get_search_results.return_value = StatusResponse(401, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        offset = 0
        length = 3
        result_response = transmission.results(search_id, offset, length)
        assert result_response is not None
        assert result_response['success'] is False
        assert result_response['code'] == "authentication_fail"
        assert "Invalid api_key" in result_response['error']

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_status')
    def test_status_pending_response(self, mock_search_response):
        """Test status pending exception"""
        mocked_return_value = '{"reply" : {"status": "PENDING"}}'
        mock_search_response.return_value = StatusResponse(200, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert status_response['status'] == "RUNNING"
        assert status_response['progress'] == 100

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_status')
    def test_status_value_error_exception(self, mock_search_status):
        """test status connector value error with invalid json"""
        mocked_return_value = "Invalid json"
        mock_search_status.return_value = StatusResponse(200, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is False
        assert 'error' in status_response
        assert "Cannot parse response" in status_response["error"]

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_status')
    def test_status_403_exception(self, get_search_results):
        """test results with 403 exception"""
        mocked_return_value = '{"reply": { "err_msg" : "api permission exception"}}'
        get_search_results.return_value = StatusResponse(403, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is False
        assert status_response['code'] == "forbidden"
        assert "The provided API Key does not have the required RBAC permissions to run this API" in \
               status_response['error']

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_remaining_quota')
    def test_ping_invalid_host(self, mock_quota_response):
        """test ping connection with invalid host"""
        mock_quota = PaloaltoMockResponse(200, '{"reply":{"used_quota": 0.08015277777777775}}')
        mock_quota_response.return_value = PingResponse(mock_quota)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert any(i in ping_response['error'] for i in ["Invalid Host", "timeout error",
                                                         "Failed to establish a new connection"])
        assert any(i in ping_response['code'] for i in ["service_unavailable", "unknown"])

    def test_ping_timeout_error(self):
        """test ping connection timeout error"""
        connection = self.connection()
        connection["options"] = {"timeout": 1}
        transmission = stix_transmission.StixTransmission('paloalto', connection, self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "timeout_error (1 sec)" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_remaining_quota')
    def test_query_search_timeout_error(self, mock_quota_response):
        """test query search timeout error"""
        mock_quota_response.return_value = {"success": True}
        connection = self.connection()
        connection["options"] = {"timeout": 1}
        transmission = stix_transmission.StixTransmission('paloalto', connection, self.configuration())
        query = {"xdr_data": {"query": "dataset = xdr_data | filter ((action_process_image_name not in ("
                                       "\"conhost.exe\",\"AtBroker.exe\") or actor_process_image_name not in ("
                                       "\"conhost.exe\",\"AtBroker.exe\") or causality_actor_process_image_name not "
                                       "in (\"conhost.exe\",\"AtBroker.exe\") or os_actor_process_image_name not in ("
                                       "\"conhost.exe\",\"AtBroker.exe\"))  and (to_epoch(_time,\"millis\") >= "
                                       "1644451200000 and to_epoch(_time,\"millis\") <= 1644883200000)) or (("
                                       "action_process_file_create_time = 1643704990003 or "
                                       "actor_process_file_create_time = 1643704990003 or "
                                       "causality_actor_process_file_create_time = 1643704990003 or "
                                       "os_actor_process_file_create_time = 1643704990003)  and (to_epoch(_time,"
                                       "\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") <= "
                                       "1644883200000)) or ((action_process_image_name ~= \"wildfire$\" or "
                                       "actor_process_image_name ~= \"wildfire$\" or "
                                       "causality_actor_process_image_name ~= \"wildfire$\" or "
                                       "os_actor_process_image_name ~= \"wildfire$\")  and (to_epoch(_time,"
                                       "\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") <= "
                                       "1644883200000)) | alter dataset_name = \"xdr_data\" | fields dataset_name,"
                                       "action_local_ip,action_remote_ip,agent_ip_addresses_v6,"
                                       "dst_agent_ip_addresses_v6,action_local_port,action_remote_port,"
                                       "action_network_protocol,action_file_name,action_file_size,action_file_md5,"
                                       "action_module_md5,action_process_image_md5,action_file_authenticode_sha1,"
                                       "action_file_authenticode_sha2,action_file_sha256,action_module_sha256,"
                                       "action_process_image_sha256,action_file_access_time,"
                                       "actor_process_file_access_time,os_actor_process_file_access_time,"
                                       "action_file_mod_time,actor_process_file_mod_time,"
                                       "os_actor_process_file_mod_time,action_file_create_time,action_file_path,"
                                       "action_process_image_path,action_registry_file_path,actor_process_image_path,"
                                       "causality_actor_process_image_path,os_actor_process_image_path,"
                                       "action_process_image_command_line,actor_process_command_line,"
                                       "causality_actor_process_command_line,os_actor_process_command_line,"
                                       "action_process_file_create_time,actor_process_file_create_time,"
                                       "causality_actor_process_file_create_time,os_actor_process_file_create_time,"
                                       "action_process_image_name,actor_process_image_name,"
                                       "causality_actor_process_image_name,os_actor_process_image_name,"
                                       "action_module_process_os_pid ,action_process_os_pid,actor_process_os_pid,"
                                       "causality_actor_process_os_pid,os_actor_process_os_pid,"
                                       "action_process_requested_parent_pid,action_thread_parent_pid,"
                                       "action_thread_child_pid,action_process_username,auth_domain,"
                                       "dst_host_metadata_domain,host_metadata_domain,dst_action_url_category ,"
                                       "action_registry_key_name,action_registry_value_name,mac,associated_mac,"
                                       "dst_associated_mac ,dst_mac,dst_user_id,user_id,action_username,"
                                       "actor_primary_username,actor_process_logon_id | limit 10000 ",
                              "timeframe": {"from": 1644451200000, "to": 1644883200000}}}

        query = json.dumps(query)
        ping_response = transmission.query(query)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "timeout_error (1 sec)" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.ping_data_source')
    def test_query_invalid_host(self, mock_ping_response):
        """test query invalid host error"""
        mock_quota = PaloaltoMockResponse(200, '{"reply":{"used_quota": 0.08015277777777775}}')
        mock_ping_response.return_value = PingResponse(mock_quota)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        query = {"xdr_data": {"query": "dataset = xdr_data | filter ((action_process_image_name not in ("
                                       "\"conhost.exe\",\"AtBroker.exe\") or actor_process_image_name not in ("
                                       "\"conhost.exe\",\"AtBroker.exe\") or causality_actor_process_image_name not "
                                       "in (\"conhost.exe\",\"AtBroker.exe\") or os_actor_process_image_name not in ("
                                       "\"conhost.exe\",\"AtBroker.exe\"))  and (to_epoch(_time,\"millis\") >= "
                                       "1644451200000 and to_epoch(_time,\"millis\") <= 1644883200000)) or (("
                                       "action_process_file_create_time = 1643704990003 or "
                                       "actor_process_file_create_time = 1643704990003 or "
                                       "causality_actor_process_file_create_time = 1643704990003 or "
                                       "os_actor_process_file_create_time = 1643704990003)  and (to_epoch(_time,"
                                       "\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") <= "
                                       "1644883200000)) or ((action_process_image_name ~= \"wildfire$\" or "
                                       "actor_process_image_name ~= \"wildfire$\" or "
                                       "causality_actor_process_image_name ~= \"wildfire$\" or "
                                       "os_actor_process_image_name ~= \"wildfire$\")  and (to_epoch(_time,"
                                       "\"millis\") >= 1644451200000 and to_epoch(_time,\"millis\") <= "
                                       "1644883200000)) | alter dataset_name = \"xdr_data\" | fields dataset_name,"
                                       "action_local_ip,action_remote_ip,agent_ip_addresses_v6,"
                                       "dst_agent_ip_addresses_v6,action_local_port,action_remote_port,"
                                       "action_network_protocol,action_file_name,action_file_size,action_file_md5,"
                                       "action_module_md5,action_process_image_md5,action_file_authenticode_sha1,"
                                       "action_file_authenticode_sha2,action_file_sha256,action_module_sha256,"
                                       "action_process_image_sha256,action_file_access_time,"
                                       "actor_process_file_access_time,os_actor_process_file_access_time,"
                                       "action_file_mod_time,actor_process_file_mod_time,"
                                       "os_actor_process_file_mod_time,action_file_create_time,action_file_path,"
                                       "action_process_image_path,action_registry_file_path,actor_process_image_path,"
                                       "causality_actor_process_image_path,os_actor_process_image_path,"
                                       "action_process_image_command_line,actor_process_command_line,"
                                       "causality_actor_process_command_line,os_actor_process_command_line,"
                                       "action_process_file_create_time,actor_process_file_create_time,"
                                       "causality_actor_process_file_create_time,os_actor_process_file_create_time,"
                                       "action_process_image_name,actor_process_image_name,"
                                       "causality_actor_process_image_name,os_actor_process_image_name,"
                                       "action_module_process_os_pid ,action_process_os_pid,actor_process_os_pid,"
                                       "causality_actor_process_os_pid,os_actor_process_os_pid,"
                                       "action_process_requested_parent_pid,action_thread_parent_pid,"
                                       "action_thread_child_pid,action_process_username,auth_domain,"
                                       "dst_host_metadata_domain,host_metadata_domain,dst_action_url_category ,"
                                       "action_registry_key_name,action_registry_value_name,mac,associated_mac,"
                                       "dst_associated_mac ,dst_mac,dst_user_id,user_id,action_username,"
                                       "actor_primary_username,actor_process_logon_id | limit 10000 ",
                              "timeframe": {"from": 1644451200000, "to": 1644883200000}}}

        query = json.dumps(query)
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert any(i in query_response['error'] for i in ["Invalid Host", "timeout_error",
                                                          "Failed to establish a new connection"])
        assert any(i in query_response['code'] for i in ["service_unavailable", "unknown"])

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_remaining_quota')
    def test_status_timeout_error(self, mock_quota_response):
        """test status timeout error"""
        mock_quota = PaloaltoMockResponse(200, '{"reply":{"used_quota": 0.08015277777777775}}')
        mock_quota_response.return_value = PingResponse(mock_quota)
        connection = self.connection()
        connection["options"] = {"timeout": 1}
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', connection, self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is False
        assert "timeout_error (1 sec)" in status_response['error']
        assert status_response['code'] == "service_unavailable"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_remaining_quota')
    def test_status_invalid_host_error(self, mock_quota_response):
        """test status invalid host error"""
        mock_quota = PaloaltoMockResponse(200, '{"reply":{"used_quota": 0.08015277777777775}}')
        mock_quota_response.return_value = PingResponse(mock_quota)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is False
        assert any(i in status_response['error'] for i in ["Invalid Host", "timeout_error",
                                                           "Failed to establish a new connection"])
        assert any(i in status_response['code'] for i in ["service_unavailable", "unknown"])

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_remaining_quota')
    def test_results_invalid_host_error(self, mock_quota_response):
        """test results invalid error"""
        mock_quota = PaloaltoMockResponse(200, '{"reply":{"used_quota": 0.08015277777777775}}')
        mock_quota_response.return_value = PingResponse(mock_quota)
        search_id = "e1d1b56ca81845_15180_inv"
        offset = 0
        length = 3
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        results_response = transmission.results(search_id, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert any(i in results_response['error'] for i in ["Invalid Host", "timeout_error",
                                                            "Failed to establish a new connection"])
        assert any(i in results_response['code'] for i in ["service_unavailable", "unknown"])

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_remaining_quota')
    def test_results_timeout_error(self, mock_quota_response):
        """test results timeout error"""
        mock_quota = PaloaltoMockResponse(200, '{"reply":{"used_quota": 0.08015277777777775}}')
        mock_quota_response.return_value = PingResponse(mock_quota)
        connection = self.connection()
        connection["options"] = {"timeout": 1}
        search_id = "e1d1b56ca81845_15180_inv"
        offset = 0
        length = 3
        transmission = stix_transmission.StixTransmission('paloalto', connection, self.configuration())
        results_response = transmission.results(search_id, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert "timeout_error (1 sec)" in results_response['error']
        assert results_response['code'] == "service_unavailable"
