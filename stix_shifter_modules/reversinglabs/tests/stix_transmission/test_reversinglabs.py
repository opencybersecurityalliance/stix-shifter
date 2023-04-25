import json

from unittest.mock import patch
import unittest

from stix_shifter.stix_transmission import stix_transmission
from tests.utils.async_utils import get_mock_response

MODULE_NAME = "reversinglabs"
domain_name = "www.cnn.com"
namespace = "8bf42ea1-e30d-41a2-a3ee-1aec759cf409"
DATA = {
    "data": [
        {
            "rl": [
                {
                    "uri_state": {
                        "domain": domain_name,
                        "sha1": "7b4a76680ca0c0f04fae3d461128a0a02d23136e",
                                "uri_type": "domain",
                                "counters": {
                                    "known": 172906,
                                    "malicious": 24350,
                                    "suspicious": 1089
                                }
                    }
                }
            ],
            "namespace": namespace,
            "data": domain_name,
            "dataType": "domain"
        }
    ]
}
SAMPLE_DATA = "{'data': '"+domain_name+"', 'dataType': 'domain'}"

connection = {
    "host": "www.data.com",
    "port": 443,
    "namespace":namespace
}
config = {
    "auth": {
        "username": "u",
        "password": "p"
    }
}


class TestReversingLabsConnection(unittest.TestCase, object):
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_reversinglabs_ping(self, mock_ping_response):
        mock_ping_response.return_value = get_mock_response(200, '', 'byte')

        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']
    
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_reversinglabs_ping_exception(self, mock_ping_response):
        mock_ping_response.side_effect = Exception('an error occured retriving ping information')
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_reversinglabs_results(self, mock_result_connection):
        mock_result_connection.return_value = get_mock_response(200, json.dumps(DATA), 'byte')

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA

        search_results_response = transmission.results(query_response['search_id'], 0, 9)

        report = search_results_response['data'][0]
        assert 'data' in report
        assert 'dataType' in report
        assert 'rl' in report
        assert 'success' in search_results_response
        assert search_results_response['success'] is True
        assert type(search_results_response['data']) is list
    
    @patch('stix_shifter_modules.reversinglabs.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_reversinglabs_results_error(self, mock_result_connection):
        mock_data = DATA = {
            "error": "Invalid",
            "success": False,
            "code": 400
        }
        mock_result_connection.side_effect = Exception('an error occured retriving ping information')
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA

        search_results_response = transmission.results(query_response['search_id'], 0, 9)
        
        assert 'success' in search_results_response
        assert search_results_response['success'] is False
        assert 'code' in search_results_response, search_results_response['code'] == 'invalid_query'
    
    def test_reversinglabs_status(self):
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.status(SAMPLE_DATA)

        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is True
        assert 'status' in query_response, query_response['status'] == 'COMPLETED'
        assert 'progress' in query_response, query_response['progress'] == 100
    
    @patch('stix_shifter_utils.modules.base.stix_transmission.base_sync_connector.BaseSyncConnector.create_status_connection', autospec=True)
    def test_reversinglabs_status_exception(self, mock_status_response):
        error_msg = 'an error occured while checking the status'
        mock_status_response.return_value = {'status':'FAILED', 'success':False}
        mock_status_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.status(SAMPLE_DATA)

        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    @patch('stix_shifter_utils.modules.base.stix_transmission.base_sync_connector.BaseSyncConnector.create_query_connection', autospec=True)
    def test_reversinglabs_query_exception(self, mock_query_response):
        error_msg = 'cannot create a query connection'
        mock_query_response.return_value = {'search_id':'', 'success':False}
        mock_query_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)

        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    def test_reversinglabs_is_async_query(self):
        transmission = stix_transmission.StixTransmission("abc",  connection, config)
        is_async_result = transmission.is_async()

        assert 'success' in is_async_result
        assert is_async_result['success'] is False
        assert 'code' in is_async_result, is_async_result['code'] == 'unknown'

    @patch('stix_shifter_utils.utils.base_entry_point.BaseEntryPoint.is_async', autospec=True)
    def test_reversinglabs_is_async_query_exception(self, mock_async_response):
        error_msg = 'an error occured while checking the if the query is async'
        mock_async_response.return_value = False
        mock_async_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.is_async()

        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    def test_delete_query(self):
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete(SAMPLE_DATA)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True
    
    @patch('stix_shifter_utils.utils.base_entry_point.BaseEntryPoint.delete_query_connection', autospec=True)
    def test_delete_query_exception(self, mock_delete_response):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_delete_response.return_value = False
        mock_delete_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete("")

        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
