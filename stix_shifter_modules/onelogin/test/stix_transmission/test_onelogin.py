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


@patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.generate_token')
@patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.__init__')
class TestOneloginConnection(unittest.TestCase, object):

    def connection(self):
        return {
            "host": "hostbla",
            "port": 443,
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
        mocked_return_value = '{"access_token":"abcd1234",' \
                              '"created_at":"2021-07-19T04:11:28.293Z","expires_in":36000,' \
                              '"refresh_token":"efgh1234",' \
                              '"token_type":"bearer","account_id":123456}'
        mock_generate_token.return_value = OneloginMockResponse(200, str(mocked_return_value))
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async is False

    def test_ping(self, mock_api_client, mock_generate_token):
        mocked_return_value = '{"access_token":"abcd1234",' \
                              '"created_at":"2021-07-19T04:11:28.293Z","expires_in":36000,' \
                              '"refresh_token":"efgh1234",' \
                              '"token_type":"bearer","account_id":123456}'
        mock_generate_token.return_value = OneloginMockResponse(200, str(mocked_return_value))
        mock_api_client.return_value = None
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True

    def test_ping_endpoint_exception(self, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mocked_return_value = {
            "status": {"error": True, "code": 401, "type": "Unauthorized", "message": "Authentication Failure"}}
        mock_generate_token.return_value = OneloginMockResponse(401, json.dumps(mocked_return_value))

        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = entry_point.ping_connection()

        assert ping_response['success'] is False
        assert ping_response['error'] == "Authentication Failure"
        assert ping_response['code'] == ErrorCode.TRANSMISSION_AUTH_CREDENTIALS.value

    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_all_response(self, mock_results_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mocked_return_value = '{"access_token":"abcd1234",' \
                              '"created_at":"2021-07-19T04:11:28.293Z","expires_in":36000,' \
                              '"refresh_token":"efgh1234",' \
                              '"token_type":"bearer","account_id":123456}'
        mock_generate_token.return_value = OneloginMockResponse(200, mocked_return_value)
        mocked_return_value = {
            "status": {
                "error": False,
                "code": 200,
                "type": "success",
                "message": "Success"
            },
            "pagination": {
                "before_cursor": None,
                "after_cursor": "cGFnZV9udW1iZXI6Ojoy",
                "previous_link": None,
                "next_link": "https://gslab-stix-dev.onelogin.com/api/1/events?client_id=&directory_id=&created_at"
                             "=&id=&until=&event_type_id=&limit=1&resolution=&user_id=&after_cursor"
                             "=cGFnZV9udW1iZXI6Ojoy "
            },
            "data": [
                {
                    "id": 81004691744,
                    "created_at": "2021-06-22T13:12:06.437Z",
                    "account_id": 192204,
                    "user_id": 138593517,
                    "event_type_id": 149,
                    "notes": None,
                    "ipaddr": "52.34.255.228",
                    "actor_user_id": 12345,
                    "assuming_acting_user_id": 12345,
                    "role_id": 441778,
                    "app_id": None,
                    "group_id": None,
                    "otp_device_id": None,
                    "policy_id": 123,
                    "actor_system": "Mapping",
                    "custom_message": None,
                    "role_name": "Default",
                    "app_name": None,
                    "group_name": None,
                    "actor_user_name": "Mapping",
                    "user_name": "Akshay P",
                    "policy_name": "policy_name",
                    "otp_device_name": None,
                    "operation_name": None,
                    "directory_sync_run_id": None,
                    "directory_id": 12345678,
                    "resolution": "resolution",
                    "client_id": 12345678,
                    "resource_type_id": None,
                    "error_description": "error_description",
                    "proxy_ip": "127.0.0.1",
                    "risk_score": 2,
                    "risk_reasons": "risk_reasons",
                    "risk_cookie_id": 123,
                    "browser_fingerprint": None
                }
            ]
        }
        mock_results_response.return_value = OneloginMockResponse(200, json.dumps(mocked_return_value))

        query = "client_id=12345678&ipaddr=52.34.255.228&limit=50"

        offset = 0
        length = 1
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = entry_point.create_results_connection(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_response_exception(self, mock_results_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mocked_return_value = '{"access_token":"abcd1234",' \
                              '"created_at":"2021-07-19T04:11:28.293Z","expires_in":36000,' \
                              '"refresh_token":"efgh1234",' \
                              '"token_type":"bearer","account_id":123456}'
        mock_generate_token.return_value = OneloginMockResponse(200, mocked_return_value)
        mocked_return_value = {
            "status": {
                "error": True,
                "code": 400,
                "type": "bad request",
                "message": {
                    "attribute": "user_id",
                    "description": "user_id has incorrect data type. It should be -> integer"
                }
            }
        }
        mock_results_response.return_value = OneloginMockResponse(400, json.dumps(mocked_return_value))

        query = "user_id=abc&limit=50"
        offset = 0
        length = 1
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = entry_point.create_results_connection(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] == 'user_id has incorrect data type. It should be -> integer'
        assert results_response['code'] == ErrorCode.TRANSMISSION_INVALID_PARAMETER.value


    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient'
           '.next_page_run_search', autospec=True)
    @patch('stix_shifter_modules.onelogin.stix_transmission.api_client.APIClient.run_search',
           autospec=True)
    def test_results_paging_response(self, mock_results_response, mock_next_page_response, mock_api_client, mock_generate_token):
        mock_api_client.return_value = None
        mocked_return_value = '{"access_token":"abcd1234",' \
                              '"created_at":"2021-07-19T04:11:28.293Z","expires_in":36000,' \
                              '"refresh_token":"efgh1234",' \
                              '"token_type":"bearer","account_id":123456}'
        mock_generate_token.return_value = OneloginMockResponse(200, mocked_return_value)
        mocked_return_value = {

            "status": {
                "error": False,
                "code": 200,
                "type": "success",
                "message": "Success"
            },
                    "pagination": {
                "before_cursor": None,
                "after_cursor": "cGFnZV9udW1iZXI6Ojoy",
                "previous_link": None,
                "next_link": "https://gslab-stix-dev.onelogin.com/api/1/events?client_id=&directory_id=&created_at=&id=&until"
                             "=&event_type_id=&limit=1&resolution=&user_id=12345678&after_cursor=cGFnZV9udW1iZXI6Ojoy "
            },
            "data": [
                {
                    "id": 81004691744,
                    "created_at": "2021-06-22T13:12:06.437Z",
                    "account_id": 192204,
                    "user_id": 12345678,
                    "event_type_id": 149,
                    "notes": None,
                    "ipaddr": "52.34.255.228",
                    "actor_user_id": 12345,
                    "assuming_acting_user_id": 12345,
                    "role_id": 441778,
                    "app_id": None,
                    "group_id": None,
                    "otp_device_id": None,
                    "policy_id": 123,
                    "actor_system": "Mapping",
                    "custom_message": None,
                    "role_name": "Default",
                    "app_name": None,
                    "group_name": None,
                    "actor_user_name": "Mapping",
                    "user_name": "Akshay P",
                    "policy_name": "policy_name",
                    "otp_device_name": None,
                    "operation_name": None,
                    "directory_sync_run_id": None,
                    "directory_id": 12345678,
                    "resolution": "resolution",
                    "client_id": 12345678,
                    "resource_type_id": None,
                    "error_description": "error_description",
                    "proxy_ip": "127.0.0.1",
                    "risk_score": 2,
                    "risk_reasons": "risk_reasons",
                    "risk_cookie_id": 123,
                    "browser_fingerprint": None
                }
            ]
        }
        mocked_next_page_value = {
            "status": {
                "error": False,
                "code": 200,
                "type": "success",
                "message": "Success"
            },
            "pagination": {
                "before_cursor": None,
                "after_cursor": "cGFnZV9udW1iZXI6Ojoy",
                "previous_link": None,
                "next_link": "https://gslab-stix-dev.onelogin.com/api/1/events?client_id=&directory_id=&created_at"
                             "=&id=&until=&event_type_id=&limit=1&resolution=&user_id=12345678&after_cursor"
                             "=cGFnZV9udW1iZXI6Ojoy "
            },
            "data": [
                {
                    "id": 81004691744,
                    "created_at": "2021-06-22T13:12:06.437Z",
                    "account_id": 192204,
                    "user_id": 12345678,
                    "event_type_id": 149,
                    "notes": None,
                    "ipaddr": "52.34.255.228",
                    "actor_user_id": 12345,
                    "assuming_acting_user_id": 12345,
                    "role_id": 441778,
                    "app_id": None,
                    "group_id": None,
                    "otp_device_id": None,
                    "policy_id": 123,
                    "actor_system": "Mapping",
                    "custom_message": None,
                    "role_name": "Default",
                    "app_name": None,
                    "group_name": None,
                    "actor_user_name": "Mapping",
                    "user_name": "Akshay P",
                    "policy_name": "policy_name",
                    "otp_device_name": None,
                    "operation_name": None,
                    "directory_sync_run_id": None,
                    "directory_id": 12345678,
                    "resolution": "resolution",
                    "client_id": 12345678,
                    "resource_type_id": None,
                    "error_description": "error_description",
                    "proxy_ip": "127.0.0.1",
                    "risk_score": 2,
                    "risk_reasons": "risk_reasons",
                    "risk_cookie_id": 123,
                    "browser_fingerprint": None
                }
            ]
        }
        mock_results_response.return_value = OneloginMockResponse(200, json.dumps(mocked_return_value))
        mock_next_page_response.return_value = OneloginMockResponse(200, json.dumps(mocked_next_page_value))

        query = "user_id=12345678&ipaddr=52.34.255.228&limit=50"

        offset = 0
        length = 2
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = entry_point.create_results_connection(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None