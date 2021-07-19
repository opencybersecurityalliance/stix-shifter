import json
import unittest
from unittest.mock import patch
from stix_shifter_modules.onelogin.entry_point import EntryPoint
from stix_shifter_utils.utils.error_response import ErrorCode



class OneloginMockResponse:

    def __init__(self, response_code, obj):
        self.code = response_code
        self.object = obj

    def read(self):
        return bytearray(self.object, 'utf-8')


@patch('stix_shifter_modules.onelogin.stix_transmission.results_connector.ResultsConnector.get_token')
@patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.__init__')
class TestOneloginConnection(unittest.TestCase, object):

    def connection(self):
        return {
            "host": "hostbla",
            "port": 8080,
        }

    def configuration(self):
        return {
            "auth": {
                "clientId": "u",
                "clientSecret": "pqwer"
            }
        }

    def test_is_async(self, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = {"access_token": "abcd1234", "code": 200}
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async == False

    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.generate_token')
    def test_ping(self, mock_ping_response, mock_api_client, mock_generate_token):
        mocked_return_value = '{"access_token":"abcd1234",' \
                              '"created_at":"2021-07-19T04:11:28.293Z","expires_in":36000,' \
                              '"refresh_token":"efgh1234",' \
                              '"token_type":"bearer","account_id":123456} '
        mock_ping_response.return_value = OneloginMockResponse(200, str(mocked_return_value))
        mock_api_client.return_value = None
        mock_generate_token.return_value = {"access_token": "abcd1234", "code": 200}
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True

    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.generate_token')
    def test_ping_endpoint_exception(self, mock_ping_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mock_generate_token.return_value = {"access_token": "abcd1234", "code": 200}
        mocked_return_value = {"status": {"error": True, "code": 401, "type": "Unauthorized", "message": "Authentication Failure"}}
        mock_ping_response.return_value = OneloginMockResponse(401, json.dumps(mocked_return_value))

        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = entry_point.ping_connection()

        assert ping_response['success'] is False
        assert ping_response['error'] == "Authentication Failure"
        assert ping_response['code'] == ErrorCode.TRANSMISSION_AUTH_CREDENTIALS.value

    def test_dummy_sync_results(self):
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = entry_point.create_results_connection("some query", 1, 1)
        response_code = results_response["success"]
        query_results = results_response["data"]

        assert response_code is True
        assert query_results == "Results from search"
