
from stix_shifter.stix_transmission import stix_transmission
from unittest.mock import patch
import unittest
from collections import namedtuple
from types import SimpleNamespace
from virus_total_json_transmission import *
from unittest.mock import AsyncMock

MODULE_NAME = "virus_total"
SAMPLE_DATA_IP = '{"data": "20.110.52.48", "dataType": "ip"}'
SAMPLE_DATA_HASH = '{"data": "16cda323189d8eba4248c0a2f5ad0d8f", "dataType": "hash"}'
SAMPLE_DATA_URL = '{"data": "linkprotect.cudasvc.com/url", "dataType": "url"}'
SAMPLE_DATA_DOMAIN = '{"data": "moncleroutlets.com", "dataType": "domain"}'

namespace = '8af42ea1-e30d-41a2-a3ee-1aec759cf789'

connection = {
    "namespace":namespace
}
config = {
    "auth": {
        "key": "testingKey"
    }
}
Response = namedtuple('Response', ['data', 'response_code'])

class MockHttpResponse:
    def __init__(self, string):
        self.string = string


@patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestVirusTotalConnection(unittest.TestCase, object):

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.ping_virus_total')
    async def test_virus_total_ping(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mock_ping_response.return_value = {"success":True, "code": 200}

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        ping_response = await transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.ping_virus_total')
    async def test_virus_total_ping_error(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value = {"success":True, "code": 404}
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = await transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.ping_virus_total')
    async def test_virus_total_ping_exception(self, mock_ping_response, mock_api_client):
        response = MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value = {"success":True, "code": 404}
        mock_ping_response.side_effect = Exception('an error occured retriving ping information')
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = await transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.ping_virus_total')
    async def test_virus_total_ping_exception2(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value =  {"success":False}
        mock_ping_response.side_effect = Exception('an error occured retriving ping information')
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = await transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    async def test_virus_total_results_ip(self, mock_result_connection, mock_api_client):

        mock_api_client.return_value = None
        mock_result_connection.return_value = DATA.copy(), namespace

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        query_response = await transmission.query(SAMPLE_DATA_IP)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA_IP

        search_results_response = transmission.results(
            query_response['search_id'], 0, 9)
        report = search_results_response['data'][0]
      
        assert 'data' in report
        assert 'dataType' in report
        assert 'success' in search_results_response
        assert search_results_response['success'] is True
        assert type(search_results_response['data']) is list
    
    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    async def test_virus_total_results_hash(self, mock_result_connection, mock_api_client):

        mock_api_client.return_value = None
        mock_result_connection.return_value = DATA.copy(), namespace

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA_HASH)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA_HASH

        search_results_response = await transmission.results(
            query_response['search_id'], 0, 9)
        report = search_results_response['data'][0]

        assert 'data' in report
        assert 'dataType' in report
        assert 'success' in search_results_response
        assert search_results_response['success'] is True
        assert type(search_results_response['data']) is list

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    async def test_virus_total_results_url(self, mock_result_connection, mock_api_client):

        mock_api_client.return_value = None
        mock_result_connection.return_value = DATA.copy(), namespace

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        query_response = await transmission.query(SAMPLE_DATA_URL)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA_URL

        search_results_response = transmission.results(
            query_response['search_id'], 0, 9)
        report = search_results_response['data'][0]

        assert 'data' in report
        assert 'dataType' in report
        assert 'success' in search_results_response
        assert search_results_response['success'] is True
        assert type(search_results_response['data']) is list

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_virus_total_results_domain(self, mock_result_connection, mock_api_client):

        mock_api_client.return_value = None
        mock_result_connection.return_value = DATA.copy(), namespace

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA_DOMAIN)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA_DOMAIN

        search_results_response = transmission.results(
            query_response['search_id'], 0, 9)
        report = search_results_response['data'][0]

        assert 'data' in report
        assert 'dataType' in report
        assert 'success' in search_results_response
        assert search_results_response['success'] is True
        assert type(search_results_response['data']) is list

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_virus_total_results_error(self, mock_result_connection, mock_api_client):
        mock_api_client.return_value = None
        mock_data = DATA = {
            "error": "Invalid",
            "success": False,
            "code": 400
        }
        mock_result_connection.return_value = mock_data, namespace
        mock_result_connection.side_effect = Exception('an error occured retriving ping information')
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA_IP)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA_IP

        search_results_response = transmission.results(query_response['search_id'], 0, 9)
        assert 'success' in search_results_response
        assert search_results_response['success'] is False
        assert 'code' in search_results_response, search_results_response['code'] == 'invalid_query'

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    async def test_virus_total_results_error_code(self, mock_result_connection, mock_api_client):
        mock_api_client.return_value = None
        mock_data = DATA = {
            "error": "Invalid",
            "success": False,
            "code": 400
        }
        mock_result_connection.return_value = mock_data, namespace
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA_IP)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA_IP

        search_results_response = await transmission.results(query_response['search_id'], 0, 9)
        assert 'success' in search_results_response
        assert search_results_response['success'] is False
        assert 'code' in search_results_response, search_results_response['code'] == 'invalid_query'

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    async def test_delete_query(self, mock_delete_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_api_client.return_value = None
        mock_delete_response.return_value = {"code": 200, "success": True} 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = await transmission.delete(SAMPLE_DATA_IP)
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    async def test_delete_query_error(self, mock_delete_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_api_client.return_value =  None 
        mock_delete_response.return_value =  {"code": 404, "success": False} 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = await transmission.delete(SAMPLE_DATA_IP)
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg

    @patch('stix_shifter_modules.virus_total.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    async def test_delete_query_exception(self, mock_delete_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_api_client.return_value = None
        mock_delete_response.return_value = False
        mock_delete_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = await transmission.delete("")
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg


class TestMockingDemo(unittest.IsolatedAsyncioTestCase):
    async def test_virus_total_ping(self):
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = await transmission.ping_async()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert 'code' in ping_response and ping_response['code'] == 'unknown'
        assert 'connector' in ping_response and ping_response['connector'] == 'virus_total'

    async def test_virus_total_get_search_results(self):
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        results_response = await transmission.results_async(SAMPLE_DATA_IP, 1, 1)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'code' in results_response and results_response['code'] == 'unknown'
        assert 'connector' in results_response and results_response['connector'] == 'virus_total'

        results_response = await transmission.results_async(SAMPLE_DATA_HASH, 1, 1)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'code' in results_response and results_response['code'] == 'unknown'
        assert 'connector' in results_response and results_response['connector'] == 'virus_total'

        results_response = await transmission.results_async(SAMPLE_DATA_URL, 1, 1)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'code' in results_response and results_response['code'] == 'unknown'
        assert 'connector' in results_response and results_response['connector'] == 'virus_total'