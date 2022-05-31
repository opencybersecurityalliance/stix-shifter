from stix_shifter_modules.azure_sentinel.entry_point import EntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
import unittest
from unittest.mock import patch
import json
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils.error_response import ErrorCode
import os
from collections import Iterable

CONNECTION= {
        "host": "host",
        "port": 443,
        "workspaceId": "e00daaf8-d6a4-4410-b50b-f5ef61c9cb45"
    }


CONFIG = {
        "auth": {
            "tenant": "924f8a12-f6bd-4b8d-93bf-9fa6e26cbf8b",
            "clientId": "15566bc1-0098-4e79-80a1-6390b97440ee",
            "clientSecret": "0fE7Q~X7G5eVBkJA4rphGAumh4.aDrT-VU9x6"
        }
    }


class AzureSentinelMockResponse:
    def __init__(self, response_code, obj):
        self.code = response_code
        self.object = obj

    def read(self):
        return self.object

class TestAzureDataResponse():
    def __init__(self, tenant_id, time ):
        self.tenant_id = tenant_id
        self.time = time
        

@patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.__init__')
class TestAzureSentinalConnection(unittest.TestCase, object):

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.__init__')
    def test_is_async(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = AzureSentinelMockResponse(200, mocked_return_value)
        entry_point = EntryPoint(CONNECTION, CONFIG)
        check_async = entry_point.is_async()

        assert check_async is False

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = AzureSentinelMockResponse(200, mocked_return_value)

        transmission = stix_transmission.StixTransmission('azure_sentinel', CONNECTION, CONFIG)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_exception(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = AzureSentinelMockResponse(200, mocked_return_value)
        mock_ping_response.side_effect = Exception('exception')

        transmission = stix_transmission.StixTransmission('azure_sentinel', CONNECTION, CONFIG)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.run_search')
    def test_query_connection(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        query = "SecurityEvent | where IpAddress == '80.66.76.145'"
        mock_ping_response.return_value = AzureSentinelMockResponse(200, mocked_return_value)

        transmission = stix_transmission.StixTransmission('azure_sentinel', CONNECTION, CONFIG)
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == query

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.api_client.APIClient.run_search')
    def test_status_query(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = AzureSentinelMockResponse(200, mocked_return_value)

        search_id = "SecurityEvent | where IpAddress == '80.66.76.145'"

        entry_point = EntryPoint(CONNECTION, CONFIG)
        status_response = entry_point.create_status_connection(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] is True


    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.connector.Connector.create_results_connection', autospec=True)
    def test_results_all_response(self, mock_results_response, mock_api_client):
        
        mock_api_client.return_value = None
        mocked_return_value = {"success": True, "data": [
            TestAzureDataResponse(tenant_id="e00daaf8-d6a4-4410-b50b-f5ef61c9cb45", time= "2022-05-25 12:12:09.111000+00:00")]}
        mock_results_response.return_value = mocked_return_value
        offset = 0
        length = 1
        search_id = "SecurityAlert | where AlertName == 'AlertLog' | limit {len}".format(len=length)
        entry_point = EntryPoint(CONNECTION, CONFIG)
        offset = 0
        length = 1
        results_response = entry_point.create_results_connection(search_id, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None


    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.connector.Connector.create_results_connection')
    def test_results_all_response_empty(self, mock_results_response, mock_api_client):
        
        mock_api_client.return_value = None
        mocked_return_value = {"success": True, "data": [ ]}  
        mock_results_response.return_value =  mocked_return_value
        offset = 0
        length = 1
        search_id = "SecurityAlert | where AlertName == 'AlertLog' | limit {len}".format(len=length)
        entry_point = EntryPoint(CONNECTION, CONFIG)
        results_response = entry_point.create_results_connection(search_id, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) == 0

    @patch('stix_shifter_modules.azure_sentinel.stix_transmission.connector.Connector.create_results_connection')
    def test_results_response_exception(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None

        mocked_return_value = {"success": True, "data": [
            TestAzureDataResponse(tenant_id="e00daaf8-d6a4-4410-b50b-f5ef61c9cb45", time= "2022-05-25 12:12:09.111000+00:00")]}
        mock_results_response.return_value = mocked_return_value
        mock_results_response.side_effect = Exception('exception')

        search_id = "'SecurityEvent | where IpAddress == '66.76.45'"
        offset = 0
        length = 1
        transmission = stix_transmission.StixTransmission('azure_sentinel',  CONNECTION, CONFIG)
        results_response = transmission.results(search_id, offset, length)
        assert 'success' in results_response
        assert results_response['success'] is False
        assert results_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value