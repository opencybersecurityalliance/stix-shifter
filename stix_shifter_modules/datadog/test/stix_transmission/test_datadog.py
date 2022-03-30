import unittest
from unittest.mock import patch
from stix_shifter_modules.datadog.entry_point import EntryPoint
from stix_shifter_utils.utils.error_response import ErrorCode


class DatadogMockEvent():
    def __init__(self, _data_store):
        self._data_store = _data_store


class TestDatadogConnection(unittest.TestCase, object):

    def connection(self):
        return {
            "site_url": "https://app.datadoghq.eu",
            "selfSignedCert": False
        }

    def configuration(self):
        return {
            "auth": {
                "api_key": "u",
                "application_key": "pqwer"
            }
        }

    def test_is_async(self):
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_modules.datadog.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping(self, mock_generate_token):
        mocked_return_value = {"code": 200}
        mock_generate_token.return_value = mocked_return_value
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True

    @patch('stix_shifter_modules.datadog.stix_transmission.api_client.APIClient.ping_data_source')
    def test_ping_endpoint_exception(self, mock_generate_token):
        mocked_return_value = {"code": 403, "message": "forbidden"}
        mock_generate_token.return_value = mocked_return_value

        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_response = entry_point.ping_connection()

        assert ping_response['success'] is False
        assert ping_response['error'] == "datadog connector error => forbidden"
        assert ping_response['code'] == ErrorCode.TRANSMISSION_FORBIDDEN.value

    @patch('stix_shifter_modules.datadog.stix_transmission.api_client.APIClient.ping_data_source')
    @patch('stix_shifter_modules.datadog.stix_transmission.api_client.APIClient.get_search_results',
           autospec=True)
    def test_results_all_response(self, mock_results_response, mock_generate_token):
        mocked_return_value = {"code": 200}
        mock_generate_token.return_value = mocked_return_value
        mocked_return_value = {"code": 200, "data": {"events": [DatadogMockEvent(_data_store={"host":"192.168.122.83", "is_aggregate": False}) for x in range(1000)]}}
        mock_results_response.return_value = mocked_return_value

        query = '{"query": {"host": "192.168.122.83", "unaggregated": "false", "start": 9580878, "end": 12345678}, "source": "events"}'
        offset = 0
        length = 1002
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = entry_point.create_results_connection(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.datadog.stix_transmission.api_client.APIClient.ping_data_source')
    @patch('stix_shifter_modules.datadog.stix_transmission.api_client.APIClient.get_search_results',
           autospec=True)
    def test_results_response_exception(self, mock_results_response, mock_generate_token):
        mocked_return_value = {"code": 200}
        mock_generate_token.return_value = mocked_return_value
        mocked_return_value = {
            "code": 400,
            "message": "Bad Request"
        }
        mock_results_response.return_value = mocked_return_value

        query = '{"query": {"host": "192.168.122.83", "start": 9580878, "end": 12345678}, "source": "events"}'
        offset = 0
        length = 1
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = entry_point.create_results_connection(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] == 'datadog connector error => Bad Request'
        assert results_response['code'] == ErrorCode.TRANSMISSION_INVALID_PARAMETER.value

    @patch('stix_shifter_modules.datadog.stix_transmission.api_client.APIClient.ping_data_source')
    @patch('stix_shifter_modules.datadog.stix_transmission.api_client.APIClient.get_processes_results',
           autospec=True)
    def test_results_processes_response(self, mock_results_response, mock_generate_token):
        mocked_return_value = {"code": 200}
        mock_generate_token.return_value = mocked_return_value
        mocked_return_value = {"code": 200, "data": {"data": [{"attributes": DatadogMockEvent(_data_store={"host": "192.168.122.83", "is_aggregate": False})} for x in range(1000)]}}
        mock_results_response.return_value = mocked_return_value

        query = '{"query": {"host": "192.168.122.83", "unaggregated": "false", "start": 9580878, "end": 12345678}, "source": "processes"}'
        offset = 0
        length = 1002
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = entry_point.create_results_connection(query, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.datadog.stix_transmission.api_client.APIClient.ping_data_source')
    @patch('stix_shifter_modules.datadog.stix_transmission.api_client.APIClient.get_processes_results',
           autospec=True)
    def test_results_processes_response_exception(self, mock_results_response, mock_generate_token):
        mocked_return_value = {"code": 200}
        mock_generate_token.return_value = mocked_return_value
        mocked_return_value = {
            "code": 400,
            "message": "Bad Request"
        }
        mock_results_response.return_value = mocked_return_value

        query = '{"query": {"host": "192.168.122.83", "start": 9580878, "end": 12345678}, "source": "processes"}'
        offset = 0
        length = 1
        entry_point = EntryPoint(self.connection(), self.configuration())
        results_response = entry_point.create_results_connection(query, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] == 'datadog connector error => Bad Request'
        assert results_response['code'] == ErrorCode.TRANSMISSION_INVALID_PARAMETER.value
