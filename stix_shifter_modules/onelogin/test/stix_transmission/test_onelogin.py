import datetime
import unittest
from unittest.mock import patch
from stix_shifter_modules.onelogin.entry_point import EntryPoint
from stix_shifter_utils.utils.error_response import ErrorCode


class OneloginMockEvent():
    def __init__(self, id, created_at, account_id, ipaddr):
        self.id = id
        self.created_at = created_at
        self.account_id = account_id
        self.ipaddr = ipaddr


@patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.__init__')
class TestOneloginConnection(unittest.TestCase, object):

    def connection(self):
        return {
            "region": "us"
        }

    def configuration(self):
        return {
            "auth": {
                "clientId": "u",
                "clientSecret": "pqwer"
            }
        }

    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.generate_token')
    def test_ping(self, mock_generate_token, mock_api_client):
        mocked_return_value = {"code": 200}
        mock_generate_token.return_value = mocked_return_value
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True

    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.generate_token')
    def test_ping_endpoint_exception(self, mock_generate_token, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = {"code": 401, "message": "Authentication Failure"}
        mock_generate_token.return_value = mocked_return_value

        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = entry_point.ping_connection()

        assert ping_response['success'] is False
        assert ping_response['error'] == "onelogin connector error => Authentication Failure"
        assert ping_response['code'] == ErrorCode.TRANSMISSION_AUTH_CREDENTIALS.value

    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.generate_token')
    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_all_response(self, mock_results_response, mock_generate_token, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = {"code": 200}
        mock_generate_token.return_value = mocked_return_value
        mocked_return_value = {"code": 200, "data": [
            OneloginMockEvent(id=123, created_at=datetime.datetime.now(), account_id=123, ipaddr="12.22.33.44")]}
        mock_results_response.return_value = mocked_return_value

        query = "client_id=12345678&ipaddr=52.34.255.228&limit=100"

        offset = 0
        length = 101
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = entry_point.create_results_connection(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.generate_token')
    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_response_exception(self, mock_results_response, mock_generate_token, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = {"code": 200}
        mock_generate_token.return_value = mocked_return_value
        mocked_return_value = {
            "code": 400,
            "message": "user_id has incorrect data type. It should be -> integer"
        }
        mock_results_response.return_value = mocked_return_value

        query = "user_id=abc&limit=50"
        offset = 0
        length = 1
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = entry_point.create_results_connection(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] == 'onelogin connector error => user_id has incorrect data type. It should be -> integer'
        assert results_response['code'] == ErrorCode.TRANSMISSION_INVALID_PARAMETER.value
