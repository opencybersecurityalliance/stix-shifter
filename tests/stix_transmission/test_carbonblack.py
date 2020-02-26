from stix_shifter.stix_transmission.src.modules.carbonblack import carbonblack_connector
from stix_shifter.stix_transmission.src.modules.base.base_status_connector import Status
from unittest.mock import patch
import unittest
import json
from stix_shifter.stix_transmission.src.modules.utils.RestApiClient import ResponseWrapper


config = {
    "auth": {
        "token": "bla"
    }
}
connection = {
    "host": "hostbla",
    "port": "8080"
}


class RequestMockResponse:
    def __init__(self, status_code, content):
        self.status_code = status_code
        self.content = content


@patch('stix_shifter.stix_transmission.src.modules.utils.RestApiClient.requests.get', autospec=True)
class TestCarbonBlackConnection(unittest.TestCase, object):

    @staticmethod
    def _create_query_list(query_string, dialect="process"):
        return [json.dumps({"query": query_string, "dialect": dialect})]

    def test_ping_endpoint(self, mock_requests_response):
        ping_response = """ [
  {
    "systemvolume_total_size": "42939584512",
    "os_environment_display_string": "Windows XP Professional Service Pack 3",
    "sensor_uptime": "480763",
    "physical_memory_size": "536330240",
    "build_id": 1,
    "uptime": "480862",
    "event_log_flush_time": null,
    "computer_dns_name": "j-8205a0c27a0c4",
    "id": 1,
    "power_state": 0,
    "uninstalled": null,
    "systemvolume_free_size": "40083230720",
    "status": "Online",
    "num_eventlog_bytes": "22717",
    "sensor_health_message": "Healthy",
    "build_version_string": "004.000.000.30910",
    "computer_sid": "S-1-5-21-1715567821-507921405-682003330",
    "next_checkin_time": "2013-10-07 07:54:36.909657-07:00",
    "node_id": 0,
    "cookie": 556463980,
    "computer_name": "J-8205A0C27A0C4",
    "license_expiration": "1990-01-01 00:00:00-08:00",
    "network_adapters": "192.168.206.156,000c298a3613|",
    "sensor_health_status": 100,
    "registration_time": "2013-02-04 06:40:04.632053-08:00",
    "restart_queued": false,
    "notes": null,
    "num_storefiles_bytes": "446464",
    "os_environment_id": 1,
    "boot_id": "8",
    "last_checkin_time": "2013-10-07 07:54:06.919446-07:00",
    "group_id": 1,
    "display": true,
    "uninstall": false,
    "network_isolation_enabled": false,
    "is_isolating": false
  }
] """

        mock_requests_response.return_value = RequestMockResponse(200, ping_response.encode())

        module = carbonblack_connector
        ping_response = module.Connector(connection, config).ping()

        assert ping_response is not None
        assert ping_response['success']

    def test_status_endpoint(self, mock_api_client):
        mock_api_client.return_value = None

        module = carbonblack_connector
        search_id = self._create_query_list("process_name:notepad.exe")

        results_response = module.Connector(connection, config).create_status_connection(search_id)

        assert 'success' in results_response
        assert results_response['success'] == True
        assert 'status' in results_response
        assert results_response['status'] == 'COMPLETED'
        assert 'progress' in results_response
        assert results_response['progress'] == 100

    def test_create_query_connection(self, mock_api_client):
        mock_api_client.return_value = None

        module = carbonblack_connector
        query_expression = self._create_query_list("process_name:notepad.exe")

        results_response = module.Connector(connection, config).create_query_connection(query_expression)

        assert 'success' in results_response
        assert results_response['success'] == True
        assert 'search_id' in results_response
        assert results_response['search_id'] == query_expression

    def test_no_results_response(self, mock_requests_response):
        mocked_return_value = """
{"terms": ["process_name:notepad.exe"],
 "results": [],
 "elapsed": 0.01921701431274414,
 "comprehensive_search": true,
 "all_segments": true,
 "total_results": 0,
 "highlights": [],
 "facets": {},
 "tagged_pids": {"00000036-0000-0a02-01d4-97e70c22b346-0167c881d4b3": [{"name": "Default Investigation", "id": 1}, {"name": "Default Investigation", "id": 1}]},
 "start": 0,
 "incomplete_results": false,
 "filtered": {}
}
"""

        mock_requests_response.return_value = RequestMockResponse(200, mocked_return_value.encode())

        module = carbonblack_connector

        query_expression = self._create_query_list("process_name:notepad.exe")[0]
        results_response = module.Connector(connection, config).create_results_connection(query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == True
        assert 'data' in results_response
        assert len(results_response['data']) == 0

    def test_one_results_response(self, mock_requests_response):
        mocked_return_value = """
{
  "terms": [
    "process_name:cmd.exe",
    "start:[2019-01-22T00:00:00 TO *]"
  ],
  "results": [
    {
      "process_md5": "5746bd7e255dd6a8afa06f7c42c1ba41",
      "sensor_id": 49,
      "filtering_known_dlls": true,
      "modload_count": 3,
      "parent_unique_id": "00000031-0000-09cc-01d4-b1e61979dd7c-000000000001",
      "emet_count": 0,
      "alliance_score_srstrust": -100,
      "cmdline": "C:\\\\Windows\\\\system32\\\\cmd.exe /c tasklist",
      "alliance_updated_srstrust": "2018-04-05T16:04:34Z",
      "filemod_count": 0,
      "id": "00000031-0000-0768-01d4-b1e6197c3edd",
      "parent_name": "cmd.exe",
      "parent_md5": "000000000000000000000000000000",
      "group": "lab1",
      "parent_id": "00000031-0000-09cc-01d4-b1e61979dd7c",
      "hostname": "lab1-host1",
      "last_update": "2019-01-22T00:04:52.937Z",
      "start": "2019-01-22T00:04:52.875Z",
      "alliance_link_srstrust": "https://example.com",
      "comms_ip": 212262914,
      "regmod_count": 0,
      "interface_ip": 183439304,
      "process_pid": 1896,
      "username": "SYSTEM",
      "terminated": true,
      "alliance_data_srstrust": [
        "5746bd7e255dd6a8afa06f7c42c1ba41"
      ],
      "process_name": "cmd.exe",
      "emet_config": "",
      "last_server_update": "2019-01-22T00:07:07.064Z",
      "path": "c:\\\\windows\\\\system32\\\\cmd.exe",
      "netconn_count": 0,
      "parent_pid": 2508,
      "crossproc_count": 2,
      "segment_id": 1548115627056,
      "host_type": "workstation",
      "processblock_count": 0,
      "os_type": "windows",
      "childproc_count": 4,
      "unique_id": "00080031-0000-0748-01d4-b1e61c7c3edd-016872e1cb30"
    }
  ],

  "elapsed": 0.05147600173950195,
  "comprehensive_search": true,
  "all_segments": true,
  "total_results": 1,
  "highlights": [],
  "facets": {},
  "tagged_pids": {},
  "start": 0,
  "incomplete_results": false,
  "filtered": {}
}
"""

        mock_requests_response.return_value = RequestMockResponse(200, mocked_return_value.encode())

        module = carbonblack_connector

        query_expression = self._create_query_list("process_name:cmd.exe start:[2019-01-22 TO *]")[0]
        results_response = module.Connector(connection, config).create_results_connection(query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == True
        assert 'data' in results_response
        assert len(results_response['data']) == 1
        assert 'process_name' in results_response['data'][0]
        assert results_response['data'][0]['process_name'] == 'cmd.exe'

    def test_bad_token_response(self, mock_requests_response):
        mocked_return_value = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>401 Unauthorized</title>
<h1>Unauthorized</h1>
<p>The server could not verify that you are authorized to access the URL requested.  You either supplied the wrong credentials (e.g. a bad password), or your browser doesn't understand how to supply the credentials required.</p>
"""

        mock_requests_response.return_value = RequestMockResponse(401, mocked_return_value.encode())

        module = carbonblack_connector
        query_expression = self._create_query_list("process_name:cmd.exe")[0]
        results_response = module.Connector(connection, config).create_results_connection(query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == False
        assert 'error' in results_response
        assert results_response['error'] == mocked_return_value
        assert 'code' in results_response
        assert  results_response['code'] == 'authentication_fail'

    def test_binary_bad_parameter_search_response(self, mock_requests_response):
        mocked_return_value = "Unhandled exception. Check logs for details."

        mock_requests_response.return_value = RequestMockResponse(500, mocked_return_value.encode())

        module = carbonblack_connector
        query_expression = self._create_query_list("process_name:cmd.exe")[0]
        results_response = module.Connector(connection, config).create_results_connection(query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == False
        assert 'error' in results_response
        assert  results_response['error'] == mocked_return_value
        assert 'code' in results_response
        assert  results_response['code'] == 'unknown'  # we may be able to return a better error code

    def test_query_syntax_error_response(self, mock_requests_response):
        mocked_return_value = '{"reason": "query_syntax_error"}'

        mock_requests_response.return_value = RequestMockResponse(400, mocked_return_value.encode())

        module = carbonblack_connector
        query_expression = self._create_query_list("(process_name:cmd.exe")[0]
        results_response = module.Connector(connection, config).create_results_connection(query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == False
        assert 'error' in results_response
        assert  results_response['error'] == "query_syntax_error"
        assert 'code' in results_response
        assert  results_response['code'] == 'invalid_query'

    def test_transmit_limit_and_sort(self, mock_requests_response):
        mocked_return_value = '{"reason": "query_syntax_error"}'
        request_parameter_list = []

        mock_requests_response.return_value = RequestMockResponse(200, mocked_return_value.encode())

        module = carbonblack_connector
        query_expression = self._create_query_list("process_name:cmd.exe")[0]
        results_response = module.Connector(connection, config).create_results_connection(query_expression, 100, 2)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == True
        mock_requests_response.assert_called_with('https://hostbla:8080/api/v1/process?q=process_name%3Acmd.exe&start=100&rows=2&sort=start+asc', cert=None, data=None, headers={'X-Auth-Token': 'bla'}, timeout=None, verify=True)
