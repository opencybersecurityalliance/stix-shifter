import unittest
from unittest.mock import patch

from stix_shifter_modules.cbcloud.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from tests.utils.async_utils import get_mock_response


class TestCbCloudConnection(unittest.TestCase, object):

    connection = {
        "host": "hostbla",
        "port": 443,
    }
    configuration = {
        "auth": {
                "org_key": "u",
                "token": "p"
        }
    }

    @patch('stix_shifter_modules.cbcloud.stix_transmission.api_client.APIClient.create_search')
    def test_cbcloud_query(self, mock_query_response):
        mocked_return_value = '{"job_id": "uuid_1234567890"}'
        mock_query_response.return_value = get_mock_response(200, mocked_return_value)
        entry_point = EntryPoint(self.connection, self.configuration)
        query = "placeholder query text"
        query_response = run_in_thread(entry_point.create_query_connection, query)

        assert query_response['search_id'] == "uuid_1234567890"

    @patch('stix_shifter_modules.cbcloud.stix_transmission.api_client.APIClient.get_search_status')
    def test_cbcloud_status(self, mock_status_response):
        mocked_return_value = '{"completed": "", "contacted": ""}'
        mock_status_response.return_value = get_mock_response(200, mocked_return_value)
        entry_point = EntryPoint(self.connection, self.configuration)
        query_id = "uuid_1234567890"
        status_response = run_in_thread(entry_point.create_status_connection, query_id)

        success = status_response["success"]
        assert success
        status = status_response["status"]
        assert status == Status.COMPLETED.value

    @patch('stix_shifter_modules.cbcloud.stix_transmission.api_client.APIClient.get_search_results')
    def test_cbcloud_results(self, mock_result_response):
        mocked_return_value = '{"results": "Results from search"}'
        mock_result_response.return_value = get_mock_response(200, mocked_return_value)
        entry_point = EntryPoint(self.connection, self.configuration)
        query_id = "uuid_1234567890"
        results_response = run_in_thread(entry_point.create_results_connection, query_id, 1, 1)

        success = results_response["success"]
        assert success
        data = results_response["data"]
        assert data == "Results from search"

    def test_is_async(self):
        entry_point = EntryPoint(self.connection, self.configuration)
        check_async = entry_point.is_async()

        assert check_async
   
    @patch('stix_shifter_modules.cbcloud.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping(self, mock_ping_response):
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = get_mock_response(200, mocked_return_value)

        transmission = stix_transmission.StixTransmission('cbcloud',  self.connection, self.configuration)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']
    
    @patch('stix_shifter_modules.cbcloud.stix_transmission.api_client.APIClient.create_search')
    def test_query(self, mock_query_response):
        mocked_return_value = '{"job_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211"}'
        mock_query_response.return_value = get_mock_response(200, mocked_return_value)

        entry_point = EntryPoint(self.connection, self.configuration)
        query = ["((process_name:test.exe) AND device_timestamp:[2021-01-15T19:17:12Z TO 2021-01-15T19:22:12Z]) AND -enriched:True"]
        query_response = run_in_thread(entry_point.create_query_connection, query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
    
