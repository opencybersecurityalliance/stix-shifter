
from stix_shifter.stix_transmission import stix_transmission
from unittest.mock import patch
import unittest
from collections import namedtuple
from types import SimpleNamespace
from dshield_test_json_transmission import *

MODULE_NAME = "dshield"
SAMPLE_DATA_IP = '{"data": "203.190.254.239", "dataType": "ip"}'
SAMPLE_DATA_HASH = '{"data": "16cda323189d8eba4248c0a2f5ad0d8f", "dataType": "hash"}'
SAMPLE_DATA_URL = '{"data": "linkprotect.cudasvc.com/url", "dataType": "url"}'
SAMPLE_DATA_DOMAIN = '{"data": "moncleroutlets.com", "dataType": "domain"}'

namespace = '9d4bedaf-d351-4f50-930f-f8eb121e5bae'

connection = {
    "namespace":namespace
}
config = {
    "auth": {
        "key": "testingKey"
    }
}
Response = namedtuple('Response', ['data', 'response_code'])
ResponseResult = namedtuple('ResponseResult', ['data', 'namespace'])

class MockHttpResponse:
    def __init__(self, string):
        self.string = string


@patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestDShieldConnection(unittest.TestCase, object):

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.ping_dshield')
    def test_dshield_ping(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        DATA = {'success': True}
        mock_ping_response.return_value = ResponseResult(DATA, 200)

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.ping_dshield')
    def test_dshield_ping_error(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value =  {"success":True, "code": 404}
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.ping_dshield')
    def test_dshield_ping_exception(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value =  {"success":True, "code": 404}
        mock_ping_response.side_effect = Exception('an error occured retriving ping information')
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.ping_dshield')
    def test_dshield_ping_exception2(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value =  {"success":False}
        mock_ping_response.side_effect = Exception('an error occured retriving ping information')
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_dshield_results_ip(self, mock_result_connection, mock_api_client):

        mock_api_client.return_value = None
        mock_result_connection.return_value = DATA.copy(), namespace

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA_IP)

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
    
    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_dshield_results_hash(self, mock_result_connection, mock_api_client):

        mock_api_client.return_value = None
        mock_result_connection.return_value = DATA.copy(), namespace

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA_HASH)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA_HASH

        search_results_response = transmission.results(
            query_response['search_id'], 0, 9)
        report = search_results_response['data'][0]

        assert 'data' in report
        assert 'dataType' in report
        assert 'success' in search_results_response
        assert search_results_response['success'] is True
        assert type(search_results_response['data']) is list

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_dshield_results_url(self, mock_result_connection, mock_api_client):

        mock_api_client.return_value = None
        mock_result_connection.return_value = DATA.copy(), namespace

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA_URL)

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

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_dshield_results_domain(self, mock_result_connection, mock_api_client):

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

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_dshield_results_error(self, mock_result_connection, mock_api_client):
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

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_dshield_results_error_code(self, mock_result_connection, mock_api_client):
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

        search_results_response = transmission.results(query_response['search_id'], 0, 9)
        assert 'success' in search_results_response
        assert search_results_response['success'] is False
        assert 'code' in search_results_response, search_results_response['code'] == 'invalid_query'

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    def test_delete_query(self, mock_delete_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_api_client.return_value = None
        mock_delete_response.return_value = {"code": 200, "success": True} 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete(SAMPLE_DATA_IP)
        assert 'success' in query_response, query_response['success'] is True

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    def test_delete_query_error(self, mock_delete_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_api_client.return_value =  None 
        mock_delete_response.return_value =  {"code": 404, "success": False} 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete(SAMPLE_DATA_IP)
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg

    @patch('stix_shifter_modules.dshield.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    def test_delete_query_exception(self, mock_delete_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_api_client.return_value = None
        mock_delete_response.return_value = False
        mock_delete_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete("")
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg


