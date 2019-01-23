from stix_shifter.stix_transmission.src.modules.carbonblack import carbonblack_connector
from stix_shifter.stix_transmission.src.modules.base.base_status_connector import Status
from unittest.mock import patch
import unittest
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


class CarbonBlackMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return self.object

@patch('stix_shifter.stix_transmission.src.modules.carbonblack.carbonblack_api_client.APIClient.__init__', autospec=True)
class TestCarbonBlackConnection(unittest.TestCase, object):

    @patch('stix_shifter.stix_transmission.src.modules.carbonblack.carbonblack_api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = CarbonBlackMockResponse(200, mocked_return_value)

        module = carbonblack_connector
        ping_response = module.Connector(connection, config).ping()

        assert ping_response is not None
        assert ping_response['success']

    def test_create_query_connection(self, mock_api_client):
        mock_api_client.return_value = None

        module = carbonblack_connector
        query_expression = "process_name:notepad.exe"

        results_response = module.Connector(connection, config).create_query_connection(query_expression)

        assert 'success' in results_response
        assert results_response['success'] == True
        assert 'search_id' in results_response
        assert results_response['search_id'] == query_expression

    @patch('stix_shifter.stix_transmission.src.modules.carbonblack.carbonblack_api_client.APIClient.run_search')
    def test_no_results_response(self, mock_results_response, mock_api_client):

        mock_api_client.return_value = None
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

        mock_results_response.return_value = CarbonBlackMockResponse(200, mocked_return_value)

        module = carbonblack_connector

        query_expression = "process_name:notepad.exe"
        results_response = module.Connector(connection, config).create_results_connection(query_expression, None, None)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == True
        assert 'data' in results_response
        assert len(results_response['data']) == 0

    @patch('stix_shifter.stix_transmission.src.modules.carbonblack.carbonblack_api_client.APIClient.run_search')
    def test_one_results_response(self, mock_results_response, mock_api_client):

        mock_api_client.return_value = None
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

        mock_results_response.return_value = CarbonBlackMockResponse(200, mocked_return_value)

        module = carbonblack_connector

        query_expression = "process_name:cmd.exe start:[2019-01-22 TO *]"
        results_response = module.Connector(connection, config).create_results_connection(query_expression, None, None)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == True
        assert 'data' in results_response
        assert len(results_response['data']) == 1
        assert 'process_name' in results_response['data'][0]
        assert results_response['data'][0]['process_name'] == 'cmd.exe'
