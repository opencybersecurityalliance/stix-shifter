from aiohttp.client_exceptions import ClientConnectionError
import json
import unittest
from unittest.mock import patch

from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_modules.paloalto.entry_point import EntryPoint
from tests.utils.async_utils import get_mock_response, RequestMockResponse


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
        mock_ping = RequestMockResponse(200, mocked_return_value)
        mock_ping_response.return_value = get_mock_response(200, mocked_return_value, 'byte', response=mock_ping)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.create_search')
    def test_query_response(self, mock_search_response):
        """test create search query"""
        mocked_return_value = '{"reply": {"search_id": "07f63c733f5946_15006_inv"}}'
        mock_search = RequestMockResponse(200, mocked_return_value)
        search_response = get_mock_response(200, mocked_return_value, 'byte',response=mock_search)
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
        """test status response"""
        mocked_return_value = '{"reply" : {"status": "SUCCESS","number_of_results":100}}'
        mock_status_response.return_value = get_mock_response(200, mocked_return_value)
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
        mock_result_response.return_value = get_mock_response(200, mocked_return_value, 'byte')
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
        mock_result_response.return_value = get_mock_response(200, mocked_return_value, 'byte')
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
        mock_ping = RequestMockResponse(400, mocked_return_value)
        mock_ping_response.return_value = get_mock_response(400, mocked_return_value, 'byte', response=mock_ping)
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
        mock_ping = RequestMockResponse(401, mocked_return_value)
        mock_ping_response.return_value = get_mock_response(401, mocked_return_value, 'byte', response=mock_ping)
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
        mock_ping = RequestMockResponse(500, mocked_return_value)
        mock_ping_response.return_value = get_mock_response(500, mocked_return_value, 'byte', response=mock_ping)
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
        mock_ping = RequestMockResponse(500, mocked_return_value)
        mock_ping_response.return_value = get_mock_response(500, mocked_return_value, 'byte', response=mock_ping)
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
        mock_ping = RequestMockResponse(402, mocked_return_value)
        mock_ping_response.return_value = get_mock_response(402, mocked_return_value, 'byte', response=mock_ping)
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
        mock_status_response.return_value = get_mock_response(200, mocked_return_value)
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
        mock_status_response.return_value = get_mock_response(200, mocked_return_value)
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
        mock_search_response.return_value = get_mock_response(200, mocked_return_value)
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
        mock_result_response.return_value = get_mock_response(200, mocked_return_value, 'byte')
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
        mock_search = RequestMockResponse(200, mocked_return_value)
        mock_search_response.return_value = get_mock_response(200, mocked_return_value, 'byte', response=mock_search)
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
        mock_search = RequestMockResponse(200, mocked_return_value)
        mock_search_response.return_value = get_mock_response(200, mocked_return_value, 'byte', response=mock_search)
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
        mock_search = RequestMockResponse(400, mocked_return_value)
        mock_search_response.return_value = get_mock_response(400, mocked_return_value, 'byte', response=mock_search)
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
        get_search_results.return_value = get_mock_response(200, mocked_return_value, 'byte')
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
        get_search_results.return_value = get_mock_response(401, mocked_return_value, 'byte')
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
        mock_search_response.return_value = get_mock_response(200, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True
        assert status_response['status'] == "RUNNING"
        assert status_response['progress'] == 50

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_status')
    def test_status_value_error_exception(self, mock_search_status):
        """test status connector value error with invalid json"""
        mocked_return_value = "Invalid json"
        mock_search_status.return_value = get_mock_response(200, mocked_return_value)
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
        get_search_results.return_value = get_mock_response(403, mocked_return_value)
        search_id = "e1d1b56ca81845_15180_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is False
        assert status_response['code'] == "forbidden"
        assert "The provided API Key does not have the required RBAC permissions to run this API" in \
               status_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_max_quota_exception(self, mock_quota_response):
        """test maximum quota threshold exception"""
        response = {'reply': {'license_quota': 5, 'additional_purchased_quota': 0.0, 'used_quota': 5.01, 'eval_quota': 0.0}}
        mocked_return_value = json.dumps(response)
        mock_search = RequestMockResponse(200, mocked_return_value)
        mock_quota_response.return_value = get_mock_response(200, mocked_return_value, 'byte', response=mock_search)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        query_response = transmission.query({})
        assert query_response is not None
        assert query_response['success'] is False
        assert query_response['code'] == "service_unavailable"
        assert "query usage exceeded max daily quota" in query_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_max_additional_quota_exception(self, mock_quota_response):
        """test maximum additional quota threshold exception"""
        response = {'reply': {'license_quota': 5, 'additional_purchased_quota': 10.0, 'used_quota': 12, 'eval_quota': 0.0}}
        mocked_return_value = json.dumps(response)
        mock_search = RequestMockResponse(200, mocked_return_value)
        mock_quota_response.return_value = get_mock_response(200, mocked_return_value, 'byte', response=mock_search)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        query_response = transmission.query({})
        assert query_response is not None
        assert query_response['success'] is False
        assert query_response['code'] == "service_unavailable"
        assert "query usage exceeded max daily quota" in query_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_quota_invalid_json_exception(self, mock_quota_response):
        """test quota invalid json exception"""
        mocked_return_value = "invalid json"
        mock_search = RequestMockResponse(200, mocked_return_value)
        mock_quota_response.return_value = get_mock_response(200, mocked_return_value, 'byte', response=mock_search)
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        query_response = transmission.query({})
        assert query_response is not None
        assert query_response['success'] is False
        assert 'error' in query_response
        assert "Cannot parse response" in query_response["error"]

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host(self, mock_ping):
        """Test Invalid host"""
        mock_ping.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "Invalid Host" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_for_status(self, mock_query):
        """Test Invalid host for Status API"""
        mock_query.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        status_response = transmission.status("123_inv")
        assert status_response is not None
        assert status_response['success'] is False
        assert "Invalid Host" in status_response['error']
        assert status_response['code'] == "service_unavailable"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_for_results(self, mock_query):
        """Test Invalid host for Results API"""
        mock_query.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        results_response = transmission.results("123_inv", 0, 2)
        assert results_response is not None
        assert results_response['success'] is False
        assert "Invalid Host" in results_response['error']
        assert results_response['code'] == "service_unavailable"

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_timeout_error(self, mock_ping):
        """Test Timeout Error"""
        mock_ping.side_effect = TimeoutError("timeout_error (30 sec)")
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "timeout_error (30 sec)" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_stream_results')
    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_results')
    def test_format_stream_data(self, mock_search_response, mock_stream_response):
        stream_id = "123"
        mocked_return_value = json.dumps({"reply": {"status": "SUCCESS",
                                                    "number_of_results": 10001,
                                                    "results": {"stream_id": stream_id}}})
        mock_search_response.return_value = get_mock_response(200, mocked_return_value, 'byte')
        search_id = "e1d1b56ca81845_15180_inv"
        stream_return_value = '{"dataset_name":"xdr_data","action_local_ip":"65.0.202.35","action_remote_ip":' \
                              '"172.31.90.48","action_local_port":"50893","action_remote_port":"3389",' \
                              '"action_network_protocol":"TCP"}'
        mock_stream_response.return_value = get_mock_response(200, stream_return_value, 'byte')
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        offset = 0
        length = 3
        result_response = transmission.results(search_id, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response
        assert result_response['data'] == [{'xdr_data': {'action_local_ip': '65.0.202.35',
                                                         'action_network_protocol': 'TCP',
                                                         'action_remote_ip': '172.31.90.48',
                                                         'action_local_port': '50893',
                                                         'action_remote_port': '3389'}}]

    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.get_search_results')
    def test_result_with_empty_user_response(self, mock_result_response):
        """test for valid result response"""
        mocked_return_value = json.dumps({"reply": {"status": "SUCCESS",
                                                    "number_of_results": 1,
                                                    "results": {"data": [{"dataset_name": "xdr_data",
                                                                          "actor_primary_user_sid": "S123",
                                                                          "actor_primary_username": "username",
                                                                          "actor_process_logon_id": "id12"}]}}})
        mock_result_response.return_value = get_mock_response(200, mocked_return_value, 'byte')
        search_id = "62428d95420f47_24655_inv"
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), self.configuration())
        offset = 0
        length = 3
        result_response = transmission.results(search_id, offset, length)
        assert result_response is not None
        assert result_response['success'] is True
        assert 'data' in result_response
        assert result_response['data'] == [{'xdr_data': {'actor_primary_user_sid': 'S123',
                                                         'actor_primary_username': 'username',
                                                         'actor_process_logon_id': 'id12'}}]


    @patch('stix_shifter_modules.paloalto.stix_transmission.api_client.APIClient.create_search')
    def test_query_response_no_tenant_id(self, mock_search_response):
        """test create search query"""
        mocked_return_value = '{"reply": {"search_id": "07f63c733f5946_15006_inv"}}'
        mock_search = RequestMockResponse(200, mocked_return_value)
        search_response = get_mock_response(200, mocked_return_value, 'byte',response=mock_search)
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

        configuration_local = self.configuration()
        configuration_local["auth"]["tenant"] = ""
        transmission = stix_transmission.StixTransmission('paloalto', self.connection(), configuration_local)
        query_response = transmission.query(query)
        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True