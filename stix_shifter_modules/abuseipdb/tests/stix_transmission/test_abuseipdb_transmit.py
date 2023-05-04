from stix_shifter.stix_transmission import stix_transmission
from unittest.mock import patch
from collections import namedtuple
import unittest

MODULE_NAME = "abuseipdb"
namespace = "8bf42ea1-e30d-41a2-a3ee-1aec759cf409"

SAMPLE_DATA = '{"data": "34.102.136.180", "dataType": "ip"}'

DATA = {
    "data": 
        [
                {
                    "ipAddress": "34.102.136.180",
                    "isPublic": True,
                    "ipVersion": 4,
                    "isWhitelisted": False,
                    "abuseConfidenceScore": 42,
                    "countryCode": "US",
                    "usageType": "Data Center/Web Hosting/Transit",
                    "isp": "Google LLC",
                    "domain": "google.com",
                    "hostnames": [
                        "180.136.102.34.bc.googleusercontent.com"
                    ],
                    "totalReports": 5,
                    "numDistinctUsers": 5,
                    "lastReportedAt": "2022-03-07T15:24:47+00:00"
                }
            ],
    "code": 200,
}

connection = {
    "namespace":namespace
}
config = {
    "auth": {
        "key": "k"
    }
}
Response = namedtuple('Response', ['data', 'response_code'])



class MockHttpResponse:
    def __init__(self, string):
        self.string = string

    def decode(self, string):
        return self.string

class AbuseIPDBHttpResponse:
    def __init__(self, obj, response_code):
        self.code = response_code
        self.object = obj

    def read(self):
        return self.object


@patch('stix_shifter_modules.abuseipdb.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestAbuseIPDBConnection(unittest.TestCase, object):
    @patch('stix_shifter_modules.abuseipdb.stix_transmission.api_client.APIClient.ping_abuseipdb')
    def test_abuseipdb_ping(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mock_ping_response.return_value = {'success': 'true', 'code': 200}

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']
    
    @patch('stix_shifter_modules.abuseipdb.stix_transmission.api_client.APIClient.ping_abuseipdb')
    def test_abuseipdb_ping_exception(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value = AbuseIPDBHttpResponse(response, 400)
        mock_ping_response.side_effect = Exception('an error occured retriving ping information')

        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        print(ping_response)
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.abuseipdb.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_abuseipdb_results(self, mock_result_connection, mock_api_client):

        mock_api_client.return_value = None
        mock_result_connection.return_value = DATA.copy(), namespace

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA

        search_results_response = transmission.results(
            query_response['search_id'], 0, 9)
        assert 'success' in search_results_response and search_results_response['success'] is True
        assert 'report' in search_results_response['data'][0]
        report = search_results_response['data'][0]['report']
        assert 'abuseConfidenceScore' in report[0]
        assert 'ipAddress' in report[0]
    
    @patch('stix_shifter_modules.abuseipdb.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_abuseipdb_results_error(self, mock_result_connection, mock_api_client):
        mock_api_client.return_value = None
        mock_data = DATA = {
            "error": "Invalid",
            "success": False,
            "code": 400
        }
        mock_result_connection.return_value = mock_data, namespace
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
    
    def test_abuseipdb_status(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.status(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is True
        assert 'status' in query_response, query_response['status'] == 'COMPLETED'
        assert 'progress' in query_response, query_response['progress'] == 100
    
    @patch('stix_shifter_utils.modules.base.stix_transmission.base_sync_connector.BaseSyncConnector.create_status_connection', autospec=True)
    def test_abuseipdb_status_exception(self, mock_status_response, mock_api_client):
        error_msg = 'an error occured while checking the status'
        mock_api_client.return_value = None
        mock_status_response.return_value = {'status':'FAILED', 'success':False}
        mock_status_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.status(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    @patch('stix_shifter_utils.modules.base.stix_transmission.base_sync_connector.BaseSyncConnector.create_query_connection', autospec=True)
    def test_abuseipdb_query_exception(self, mock_query_response, mock_api_client):
        error_msg = 'cannot create a query connection'
        mock_api_client.return_value = None
        mock_query_response.return_value = {'search_id':'', 'success':False}
        mock_query_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    def test_abuseipdb_is_async_query(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission("abc",  connection, config)
        is_async_result = transmission.is_async()
        assert 'success' in is_async_result
        assert is_async_result['success'] is False
        assert 'code' in is_async_result, is_async_result['code'] == 'unknown'

    @patch('stix_shifter_utils.utils.base_entry_point.BaseEntryPoint.is_async', autospec=True)
    def test_abuseipdb_is_async_query_exception(self, mock_async_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is async'
        mock_api_client.return_value = None
        mock_async_response.return_value = False
        mock_async_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.is_async()
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    def test_delete_query(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True
    
    @patch('stix_shifter_utils.utils.base_entry_point.BaseEntryPoint.delete_query_connection', autospec=True)
    def test_delete_query_exception(self, mock_delete_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_api_client.return_value = None
        mock_delete_response.return_value = False
        mock_delete_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete("")
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
