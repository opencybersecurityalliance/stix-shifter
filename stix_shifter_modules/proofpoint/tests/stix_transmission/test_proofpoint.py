
import unittest
from unittest.mock import patch
import json
import os

from stix_shifter_modules.proofpoint.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from tests.utils.async_utils import get_mock_response


CONNECTION= {
        "host": "host",
        "port": 8080,
    }


CONFIG = {
        "auth": {
            "principal": "principal",
            "secret": "secret"
        }
    }

searchid = "sinceSeconds=3600"
query_mock = "?format=json&interval=PT30M/2016-05-01T12:30:00Z&threatStatus=falsePositive&threatStatus=active&threatStatus=cleared"


class TestProofpointConnection(unittest.TestCase, object):

    @patch('stix_shifter_modules.proofpoint.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_endpoint(self, mock_ping_response):
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = get_mock_response(200, mocked_return_value)

        transmission = stix_transmission.StixTransmission('proofpoint', CONNECTION, CONFIG)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter_modules.proofpoint.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_endpoint_exception(self, mock_ping_response):
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.side_effect = Exception('exception')

        transmission = stix_transmission.StixTransmission('proofpoint', CONNECTION, CONFIG)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value

    @patch('stix_shifter_modules.proofpoint.stix_transmission.api_client.APIClient.get_search_status', autospec=True)
    def test_status_response(self, mock_status_response):
        response = {"success": True, "status": "COMPLETED", "progress": 100}
        mock_status_response.return_value = response

        entry_point = EntryPoint(CONNECTION, CONFIG)
        status_response = run_in_thread(entry_point.create_status_connection, searchid)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'COMPLETED'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('stix_shifter_modules.proofpoint.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_results_response(self, mock_results_response):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'proofpoint_results.json')
        mocked_return_value = open(file_path, 'r').read()

        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte')
        offset = 0
        length = 1

        transmission = stix_transmission.StixTransmission('proofpoint', CONNECTION, CONFIG)
        results_response = transmission.results(query_mock, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) > 0

    @patch('stix_shifter_modules.proofpoint.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_results_response_empty(self, mock_results_response):

        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'proofpoint_result_empty.json')
        mocked_return_value = open(file_path, 'r').read()

        mock_results_response.return_value = get_mock_response(200, mocked_return_value, 'byte')
        offset = 0
        length = 1

        transmission = stix_transmission.StixTransmission('proofpoint', CONNECTION, CONFIG)
        results_response = transmission.results(searchid, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) == 0

    @patch('stix_shifter_modules.proofpoint.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_results_response_exception(self, mock_results_response):
        mock_results_response.side_effect = Exception('exception')
        offset = 0
        length = 1

        transmission = stix_transmission.StixTransmission('proofpoint', CONNECTION, CONFIG)
        results_response = transmission.results(searchid, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is False
        assert results_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value


    @patch('stix_shifter_modules.proofpoint.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_query_flow(self, mock_results_response):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'proofpoint_results.json')
        results_mock = open(file_path, 'r').read()
        mock_results_response.return_value = get_mock_response(200, results_mock, 'byte')


        entry_point = EntryPoint(CONNECTION, CONFIG)
        query_response = run_in_thread(entry_point.create_query_connection, searchid)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == searchid


        status_response = run_in_thread(entry_point.create_status_connection, query_mock)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'COMPLETED'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True


        offset = 0
        length = 1
        results_response = run_in_thread(entry_point.create_results_connection, searchid, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) > 0