import os
import unittest
from unittest.mock import patch
from stix_shifter_modules.sumologic.entry_point import EntryPoint
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter.stix_transmission import stix_transmission


class SumoLogicMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object


@patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.__init__')
class TestSumoLogicConnection(unittest.TestCase, object):

    def connection(self):
        return {
            "region": "us1"
        }

    def configuration(self):
        return {
            "auth": {
                "access_id": "u",
                "access_key": "pqwer"
            }
        }

    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async is True

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping(self, mock_generate_token, mock_api_client):
        mocked_return_value = SumoLogicMockResponse(200, True)
        mock_generate_token.return_value = mocked_return_value
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_endpoint_exception(self, mock_generate_token, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = SumoLogicMockResponse(401, 'Authentication Failure')
        mock_generate_token.return_value = mocked_return_value

        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = entry_point.ping_connection()

        assert ping_response['success'] is False
        assert ping_response['connector'] == 'sumologic'
        assert ping_response['error'] == "sumologic connector error => Authentication Failure"
        assert ping_response['code'] == ErrorCode.TRANSMISSION_AUTH_CREDENTIALS.value

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.create_search')
    def test_query_response(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '257EAE83E02E9698'
        mock_query_response.return_value = SumoLogicMockResponse(200, mocked_return_value)

        query = "{\"query\": \"(_sourcehost = \\\"sumologic.domain_name.com\\\")\"," \
                "\n\"fromTime\": \"20211007T111938\",\n\"toTime\": \"20211007T113438\"}"

        transmission = stix_transmission.StixTransmission('sumologic', self.connection(), self.configuration())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "257EAE83E02E9698"

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.create_search')
    def test_query_response_exception(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '257EAE83E02E9698'
        mock_query_response.return_value = SumoLogicMockResponse(200, mocked_return_value)
        mock_query_response.side_effect = Exception('exception')

        query = "{\"query\": \"(_sourcehost = \\\"sumologic.domain_name.com\\\")\"," \
                "\n\"fromTime\": \"20211007T111938\",\n\"toTime\": \"20211007T113438\"}"
        transmission = stix_transmission.StixTransmission('sumologic', self.connection(), self.configuration())
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is False
        assert query_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.get_search_status', autospec=True)
    def test_status_response(self, mock_status_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = "DONE GATHERING RESULTS"
        mock_status_response.return_value = SumoLogicMockResponse(200, mocked_return_value)
        search_id = "27F369FB69B2458D"
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = entry_point.create_status_connection(search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'COMPLETED'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.get_search_status', autospec=True)
    def test_status_response_error(self, mock_status_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = "ERROR"

        mock_status_response.return_value = SumoLogicMockResponse(200, mocked_return_value)
        search_id = "27F369FB69B2458D"
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = entry_point.create_status_connection(search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'ERROR'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.get_search_status', autospec=True)
    def test_status_response_running(self, mock_status_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = "GATHERING RESULTS"
        mock_status_response.return_value = SumoLogicMockResponse(200, mocked_return_value)
        search_id = "27F369FB69B2458D"
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = entry_point.create_status_connection(search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'RUNNING'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.get_search_status', autospec=True)
    def test_status_response_running_cancelled(self, mock_status_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = "CANCELLED"

        mock_status_response.return_value = SumoLogicMockResponse(200, mocked_return_value)

        search_id = "27F369FB69B2458D"
        entry_point = EntryPoint(self.connection(), self.configuration())
        status_response = entry_point.create_status_connection(search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'CANCELED'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.get_search_status', autospec=True)
    def test_status_response_exception(self, mock_status_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = "DONE GATHERING RESULTS"
        mock_status_response.return_value = SumoLogicMockResponse(200, mocked_return_value)
        mock_status_response.side_effect = Exception('exception')
        search_id = "27F369FB69B2458D"
        transmission = stix_transmission.StixTransmission('sumologic', self.connection(), self.configuration())
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert status_response['success'] is False
        assert ErrorCode.TRANSMISSION_UNKNOWN.value == status_response['code']

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_results_response(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None

        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'result_by_sid.json')
        mocked_return_value = open(file_path, 'r').read()

        mock_results_response.return_value = SumoLogicMockResponse(200, mocked_return_value)

        search_id = "27F369FB69B2458D"
        offset = 0
        length = 1

        transmission = stix_transmission.StixTransmission('sumologic', self.connection(), self.configuration())
        results_response = transmission.results(search_id, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) > 0

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.get_search_results',  autospec=True)
    def test_results_response_empty_list(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = list()

        mock_results_response.return_value = SumoLogicMockResponse(200, mocked_return_value)

        search_id = "27F369FB69B2458D"
        offset = 0
        length = 1
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = entry_point.create_results_connection(search_id, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) == 0

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_results_response_exception(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None

        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'result_by_sid.json')
        mocked_return_value = open(file_path, 'r').read()

        mock_results_response.return_value = SumoLogicMockResponse(200, mocked_return_value)
        mock_results_response.side_effect = Exception('exception')
        search_id = "27F369FB69B2458D"
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('sumologic', self.connection(), self.configuration())
        results_response = transmission.results(search_id, offset, length)
        assert 'success' in results_response
        assert results_response['success'] is False
        assert results_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.create_search', autospec=True)
    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.get_search_status', autospec=True)
    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_query_flow(self, mock_results_response, mock_status_response, mock_query_response, mock_api_client):
        mock_api_client.return_value = None

        query_mock = "27F369FB69B2458D"
        mock_query_response.return_value = SumoLogicMockResponse(200, query_mock)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'result_by_sid.json')
        results_mock = open(file_path, 'r').read()
        mock_results_response.return_value = SumoLogicMockResponse(200, results_mock)

        status_mock = "DONE GATHERING RESULTS"
        mock_status_response.return_value = SumoLogicMockResponse(200, status_mock)

        query = "{\"query\": \"(_sourcehost = \\\"sumologic.domain_name.com\\\")\"," \
                "\n\"fromTime\": \"20211007T111938\",\n\"toTime\": \"20211007T113438\"}"
        entry_point = EntryPoint(self.connection(), self.configuration())
        query_response = entry_point.create_query_connection(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "27F369FB69B2458D"

        search_id = "27F369FB69B2458D"
        status_response = entry_point.create_status_connection(search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'COMPLETED'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True

        search_id = "27F369FB69B2458D"
        offset = 0
        length = 1
        results_response = entry_point.create_results_connection(search_id, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) > 0

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    def test_delete_search(self, mock_results_delete, mock_api_client):
        mock_api_client.return_value = None

        mocked_return_value = {'id': '27F369FB69B2458D'}
        mock_results_delete.return_value = SumoLogicMockResponse(200, mocked_return_value)

        search_id = "27F369FB69B2458D"
        transmission = stix_transmission.StixTransmission('sumologic', self.connection(), self.configuration())
        results_response = transmission.delete(search_id)

        assert results_response is not None
        assert results_response['success'] is True

    @patch('stix_shifter_modules.sumologic.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    def test_delete_search_exception(self, mock_results_delete, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = {
            "success": False,
            "error": "404 Client Error: {\n  \"status\" : 404,\n  \"id\" : \"ACFCS-COOIW-7O80O\",\n  \"code\" : \"searchjob.jobid.invalid\",\n  \"message\" : \"Job ID is invalid.\"\n} for url: https://api.in.sumologic.com/api/v1/search/jobs/7BF2DA687DE824DB",
            "code": "unknown"
        }
        mock_results_delete.return_value = SumoLogicMockResponse(200, mocked_return_value)
        search_id = "27F369FB69B2458D"
        transmission = stix_transmission.StixTransmission('sumologic', self.connection(), self.configuration())
        results_response = transmission.delete(search_id)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == ErrorCode.TRANSMISSION_SEARCH_DOES_NOT_EXISTS.value
