import json
import unittest
from unittest.mock import ANY
from unittest.mock import patch
from stix_shifter_modules.crowdstrike.entry_point import EntryPoint
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter_utils.stix_transmission.utils.RestApiClient import ResponseWrapper
import asyncio
from asyncinit import asyncinit


config = {
        "auth": {
            "client_id": "bla",
            "client_secret": "bla"
        }
    }

connection = {
    'host': 'api.crowdstrike.com'
}


@asyncinit
class RequestMockResponse:
    def __init__(self, status_code, content):
        self.code = status_code
        self.content = content

    def read(self):
        return self.content   


class TestCrowdStrikeConnection(unittest.TestCase, object):

    @staticmethod
    def _create_query_list(query_string):
        return [query_string]

    def test_status_endpoint(self):

        entry_point = EntryPoint(connection, config)
        search_id = self._create_query_list("process_name:notepad.exe")
        results_response = run_in_thread(entry_point.create_status_connection, search_id)

        assert 'success' in results_response
        assert results_response['success'] == True
        assert 'status' in results_response
        assert results_response['status'] == 'COMPLETED'
        assert 'progress' in results_response
        assert results_response['progress'] == 100

    def test_create_query_connection(self):

        entry_point = EntryPoint(connection, config)
        query_expression = self._create_query_list("process_name:notepad.exe")
        results_response = run_in_thread(entry_point.create_query_connection, query_expression)

        assert 'success' in results_response
        assert results_response['success'] == True
        assert 'search_id' in results_response
        assert results_response['search_id'] == query_expression

    @patch('stix_shifter_modules.crowdstrike.stix_transmission.api_client.APIClient.get_detections_IDs')
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

        entry_point = EntryPoint(connection, config)
        query_expression = self._create_query_list("process_name:notepad.exe")[0]
        results_response = run_in_thread(entry_point.create_results_connection, query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == True
        assert 'data' in results_response
        assert len(results_response['data']) == 0

    @patch('stix_shifter_modules.crowdstrike.stix_transmission.api_client.APIClient.get_detections_IDs')
    def test_one_results_response(self, mock_requests_response):
        mocked_return_value = """
{
  "terms": [
    "process_name:cmd.exe",
    "start:[2019-01-22T00:00:00 TO *]"
  ],
  "results": [],
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

        entry_point = EntryPoint(connection, config)
        query_expression = self._create_query_list("process_name:cmd.exe start:[2019-01-22 TO *]")[0]
        results_response = run_in_thread(entry_point.create_results_connection, query_expression, 0, 10)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == True
        assert 'data' in results_response
        assert len(results_response['data']) == 0

    @patch('stix_shifter_modules.crowdstrike.stix_transmission.api_client.APIClient.get_detections_IDs')
    def test_transmit_limit_and_sort(self, mock_requests_response):
        mocked_return_value = '{"reason": "query_syntax_error"}'

        mock_requests_response.return_value = RequestMockResponse(200, mocked_return_value.encode())

        entry_point = EntryPoint(connection, config)
        query_expression = self._create_query_list("process_name:cmd.exe")[0]
        results_response = run_in_thread(entry_point.create_results_connection, query_expression, 100, 2)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == True
