from stix_shifter_modules.reaqta.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from tests.utils.async_utils import get_mock_response


import json
import unittest
from unittest.mock import patch

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
    
    def test_is_async(self):
        entry_point = EntryPoint(self.connection, self.configuration)
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping(self, mock_generate_token):
        mocked_return_value = '{"token": "abcdef", "expiresAt": 1658954054.299}'
        mock_generate_token.return_value = get_mock_response(200, mocked_return_value, 'byte')
        
        entry_point = EntryPoint(self.connection, self.configuration)
        ping_result = run_in_thread(entry_point.ping_connection)

        assert ping_result["success"] is True
    
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_ping_failure(self, mock_generate_token):
        mocked_return_value = '{"message": "Authentication failed"}'
        mock_generate_token.return_value = get_mock_response(401, mocked_return_value)
        entry_point = EntryPoint(self.connection, self.configuration)
        ping_response = run_in_thread(entry_point.ping_connection)
        
        assert ping_response["success"] is False
        assert ping_response['error'] == 'reaqta connector error => Invalid App Secret key provided. Authentication Error: Token Generation Failed. Authentication failed'
        assert ping_response['code'] == ErrorCode.TRANSMISSION_AUTH_CREDENTIALS.value
    
    @patch('stix_shifter_modules.reaqta.stix_transmission.api_client.APIClient.get_search_results')
    def test_results_reponse(self, mock_query):
        
        payload = {"result": [{"eventId": "847828325903630337", "endpointId": "822862264951373824"},{"eventId": "84782832",
            "endpointId": "822862264951373824"}],"status_code": "200"}
        mock_query.side_effect = [get_mock_response(200, json.dumps(payload))]
        transmission = stix_transmission.StixTransmission('reaqta', self.connection, self.configuration)
        results_response = transmission.results('$ip="172.16.60.184"', 0, 2)
        assert results_response["success"] is True
        assert results_response["data"] == payload["result"]
    
    @patch('stix_shifter_modules.reaqta.stix_transmission.api_client.APIClient.get_search_results')
    def test_results_failure(self, mock_query):
        
        payload = {"message":"$ip1 is not a valid field.", "code": 422}
        mock_query.side_effect = [get_mock_response(422, json.dumps(payload))]
        transmission = stix_transmission.StixTransmission('reaqta', self.connection, self.configuration)
        results_response = transmission.results('$ip1="172.16.60.184" and hasAlert=t', 0, 2)
        assert results_response["success"] is False
        assert results_response['code'] == 'invalid_query'
        assert results_response["error"] == 'reaqta connector error => query_syntax_error: $ip1 is not a valid field.'
    
    def test_query(self):
        query = '$ip="172.16.60.184"'
        transmission = stix_transmission.StixTransmission("reaqta", self.connection, self.configuration)
        query_response = transmission.query(query)
        self.assertTrue(query_response["success"])
        self.assertEqual(query_response["search_id"], query)
    
    def test_status(self):
        transmission = stix_transmission.StixTransmission("reaqta", self.connection, self.configuration)
        status_response = transmission.status("search_id")
        self.assertTrue(status_response["success"])
        self.assertEqual(status_response["status"], "COMPLETED")
        self.assertEqual(status_response["progress"], 100)

    def test_delete(self):
        transmission = stix_transmission.StixTransmission("reaqta", self.connection, self.configuration)
        delete_response = transmission.delete("search_id")
        self.assertTrue(delete_response["success"])