from stix_shifter_modules.reaqta.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils.error_response import ErrorCode


import json
import unittest
from unittest.mock import patch

class ReaqtaMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object
    
    def read(self):
        return bytearray(self.object, 'utf-8')

@patch('stix_shifter_modules.reaqta.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestReaqtaConnection(unittest.TestCase, object):
    configuration = {
        "auth": {
            "app_id": "bla",
            "secret_key": "bla"
        }
    }

    connection = {
        'host': 'api.reaqta.com'
    }
    
    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection, self.configuration)
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_modules.reaqta.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping(self, mock_generate_token, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = {"code": 200, "token": "abcdef"}
        mock_generate_token.return_value = mocked_return_value
        entry_point = EntryPoint(self.connection, self.configuration)
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True
    
    @patch('stix_shifter_modules.reaqta.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_failure(self, mock_generate_token, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = {"code": 401, "message": 'Authentication Error: Token Generation Failed. Authentication failed'}
        mock_generate_token.return_value = mocked_return_value
        entry_point = EntryPoint(self.connection, self.configuration)
        ping_response = entry_point.ping_connection()
        
        assert ping_response["success"] is False
        assert ping_response['error'] == 'reaqta connector error => Invalid App Secret key provided. Authentication Error: Token Generation Failed. Authentication failed'
        assert ping_response['code'] == ErrorCode.TRANSMISSION_AUTH_CREDENTIALS.value
    
    @patch('stix_shifter_modules.reaqta.stix_transmission.api_client.APIClient.get_search_results')
    def test_results_reponse(self, mock_query, mock_api_client):
        mock_api_client.return_value = None
        payload = {"result": [{"eventId": "847828325903630337", "endpointId": "822862264951373824"},{"eventId": "84782832",
        "endpointId": "822862264951373824"}],"status_code": "200"}
        mock_query.side_effect = [ReaqtaMockResponse(200, json.dumps(payload))]
        transmission = stix_transmission.StixTransmission('reaqta', self.connection, self.configuration)
        results_response = transmission.results('$ip="172.16.60.184"', 0, 2)
        assert results_response["success"] is True
        assert results_response["data"] == payload["result"]
    
    @patch('stix_shifter_modules.reaqta.stix_transmission.api_client.APIClient.get_search_results')
    def test_results_failure(self, mock_query, mock_api_client):
        mock_api_client.return_value = None
        payload = {"message":"$ip1 is not a valid field.", "code": 422}
        mock_query.side_effect = [ReaqtaMockResponse(422, json.dumps(payload))]
        transmission = stix_transmission.StixTransmission('reaqta', self.connection, self.configuration)
        results_response = transmission.results('$ip1="172.16.60.184" and hasAlert=t', 0, 2)
        assert results_response["success"] is False
        assert results_response['code'] == 'invalid_query'
        assert results_response["error"] == 'reaqta connector error => query_syntax_error: $ip1 is not a valid field.'
    
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_query(self, mock_query, mock_api_client):
        mock_api_client.return_value = None
        query = '$ip="172.16.60.184"'
        mock_query.side_effect = [ReaqtaMockResponse(200, query)]
        transmission = stix_transmission.StixTransmission("reaqta", self.connection, self.configuration)
        query_response = transmission.query(query)
        self.assertTrue(query_response["success"])
        self.assertEqual(query_response["search_id"], query)
    
    def test_status(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission("reaqta", self.connection, self.configuration)
        status_response = transmission.status("search_id")
        # print(status_response)
        self.assertTrue(status_response["success"])
        self.assertEqual(status_response["status"], "COMPLETED")
        self.assertEqual(status_response["progress"], 100)

    def test_delete(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission("reaqta", self.connection, self.configuration)
        delete_response = transmission.delete("search_id")
        self.assertTrue(delete_response["success"])