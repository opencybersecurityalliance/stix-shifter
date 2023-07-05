import unittest
import os
from unittest.mock import patch
from aiohttp.client_exceptions import ClientConnectionError
from stix_shifter_modules.splunk.entry_point import EntryPoint
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter.stix_transmission.stix_transmission import run_in_thread
from stix_shifter_utils.utils.error_response import ErrorCode
from tests.utils.async_utils import get_mock_response
from asyncio.exceptions import TimeoutError


class TestSplunkConnection(unittest.TestCase, object):
    """ class for test splunk connection"""

    def test_is_async(self):
        """check for synchronous or asynchronous"""
        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        entry_point = EntryPoint(connection, config)
        check_async = entry_point.is_async()

        assert check_async

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response):
        """test to check ping_data_source function"""
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = get_mock_response(200, mocked_return_value)

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint_exception(self, mock_ping_response):
        """test to check ping_data exception"""
        # mocked_return_value = '["mock", "placeholder"]'
        # mock_ping_response.return_value = get_mock_response(200, mocked_return_value)
        mock_ping_response.side_effect = Exception('exception')
        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.create_search')
    def test_query_response(self, mock_query_response):
        """test to check query response"""
        mocked_return_value = '{"sid":"1536672851.4012"}'
        mock_query_response.return_value = get_mock_response(201, mocked_return_value)

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        query = 'search eventtype=network_traffic | fields + tag| spath'
        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "1536672851.4012"

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.create_search')
    def test_query_response_exception(self, mock_query_response):
        """test to check query response exception"""
        # mocked_return_value = '{"sid":"1536672851.4012"}'
        # mock_query_response.return_value = get_mock_response(201, mocked_return_value)
        mock_query_response.side_effect = Exception('exception')

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        query = 'search eventtype=network_traffic | fields + tag| spath'

        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert query_response['success'] is False
        assert query_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.get_search',
           autospec=True)
    def test_status_response(self, mock_status_response):
        """test to check status response"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'status_by_sid.json')
        with open(file_path, 'r', encoding='utf-8') as file_obj:
            mocked_return_value = file_obj.read()

        mock_status_response.return_value = get_mock_response(200, mocked_return_value)

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        search_id = "1536832140.4293"
        entry_point = EntryPoint(connection, config)
        status_response = run_in_thread(entry_point.create_status_connection, search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'COMPLETED'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.get_search',
           autospec=True)
    def test_status_response_error(self, mock_status_response):
        """test to check status exception"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'status_by_sid_failed.json')
        with open(file_path, 'r', encoding='utf-8') as file_obj:
            mocked_return_value = file_obj.read()

        mock_status_response.return_value = get_mock_response(200, mocked_return_value)

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        search_id = "1536832140.4293"
        entry_point = EntryPoint(connection, config)
        status_response = run_in_thread(entry_point.create_status_connection, search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'ERROR'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.get_search',
           autospec=True)
    def test_status_response_running(self, mock_status_response):
        """test to check if status response running"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'status_by_sid_running.json')
        with open(file_path, 'r', encoding='utf-8') as file_obj:
            mocked_return_value = file_obj.read()

        mock_status_response.return_value = get_mock_response(200, mocked_return_value)

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        search_id = "1536832140.4293"
        entry_point = EntryPoint(connection, config)
        status_response = run_in_thread(entry_point.create_status_connection, search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'RUNNING'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.get_search',
           autospec=True)
    def test_status_response_cancelled(self, mock_status_response):
        """test to check if status response cancelled"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'status_by_sid_running_cancel.json')
        with open(file_path, 'r', encoding='utf-8') as file_obj:
            mocked_return_value = file_obj.read()

        mock_status_response.return_value = get_mock_response(200, mocked_return_value)

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        search_id = "1536832140.4293"
        entry_point = EntryPoint(connection, config)
        status_response = run_in_thread(entry_point.create_status_connection, search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'CANCELED'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.get_search',
           autospec=True)
    def test_status_response_exception(self, mock_status_response):
        """test to check status response exception"""
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # file_path = os.path.join(dir_path, 'api_response', 'status_by_sid.json')
        # mocked_return_value = open(file_path, 'r').read()

        # mock_status_response.return_value = get_mock_response(200, mocked_return_value)
        mock_status_response.side_effect = Exception('exception')

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        search_id = "1536832140.4293"

        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert status_response['success'] is False
        assert ErrorCode.TRANSMISSION_UNKNOWN.value == status_response['code']

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.get_search_results',
           autospec=True)
    def test_results_response(self, mock_results_response):
        """test to check result response"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'result_by_sid.json')
        with open(file_path, 'r', encoding='utf-8') as file_obj:
            mocked_return_value = file_obj.read()

        mock_results_response.return_value = get_mock_response(200, mocked_return_value)

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        search_id = "1536832140.4293"
        offset = 0
        length = 1

        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        results_response = transmission.results(search_id, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) > 0

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.get_search_results',
           autospec=True)
    def test_results_response_empty_list(self, mock_results_response):
        """test to check empty result response"""
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'empty_result_by_sid.json')
        with open(file_path, 'r', encoding='utf-8') as file_obj:
            mocked_return_value = file_obj.read()

        mock_results_response.return_value = get_mock_response(200, mocked_return_value)

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        search_id = "1536832140.4293"
        offset = 0
        length = 1
        entry_point = EntryPoint(connection, config)
        results_response = run_in_thread(entry_point.create_results_connection, search_id, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) == 0

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.get_search_results',
           autospec=True)
    def test_results_response_exception(self, mock_results_response):
        """test to result response exception"""
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        # file_path = os.path.join(dir_path, 'api_response', 'result_by_sid.json')
        # mocked_return_value = open(file_path, 'r').read()

        # mock_results_response.return_value = get_mock_response(200, mocked_return_value)
        mock_results_response.side_effect = Exception('exception')

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        search_id = "1536832140.4293"
        offset = 0
        length = 1

        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        results_response = transmission.results(search_id, offset, length)
        assert 'success' in results_response
        assert results_response['success'] is False
        assert results_response['code'] == ErrorCode.TRANSMISSION_UNKNOWN.value

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.create_search',
           autospec=True)
    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.get_search',
           autospec=True)
    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.get_search_results',
           autospec=True)
    def test_query_flow(self, mock_results_response, mock_status_response, mock_query_response):
        """test to check query flow"""
        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        query_mock = '{"sid":"1536832140.4293"}'
        mock_query_response.return_value = get_mock_response(201, query_mock)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'result_by_sid.json')
        with open(file_path, 'r') as file_obj:
            results_mock = file_obj.read()
        mock_results_response.return_value = get_mock_response(200, results_mock)

        status_file_path = os.path.join(dir_path, 'api_response', 'status_by_sid.json')
        with open(status_file_path, 'r', encoding='utf-8') as file_obj:
            status_mock = file_obj.read()

        mock_status_response.return_value = get_mock_response(200, status_mock)

        query = 'search eventtype=network_traffic | fields + tag| spath'
        entry_point = EntryPoint(connection, config)
        query_response = run_in_thread(entry_point.create_query_connection, query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "1536832140.4293"

        search_id = "1536832140.4293"
        status_response = run_in_thread(entry_point.create_status_connection, search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'COMPLETED'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True

        search_id = "1536832140.4293"
        offset = 0
        length = 1
        results_response = run_in_thread(entry_point.create_results_connection, search_id, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) > 0

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.delete_search',
           autospec=True)
    def test_delete_search(self, mock_results_delete):
        """test to check delete search"""
        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mocked_return_value = '{"messages":[{"type":"INFO","text":"Search job cancelled."}]}'
        mock_results_delete.return_value = get_mock_response(200, mocked_return_value)

        search_id = "1536832140.4293"
        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        results_response = transmission.delete(search_id)

        assert results_response is not None
        assert results_response['success'] is True

    @patch('stix_shifter_modules.splunk.stix_transmission.api_client.APIClient.delete_search',
           autospec=True)
    def test_delete_search_exception(self, mock_results_delete):
        """test to check delete search exception"""
        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mocked_return_value = '{"type":"Unknown_sid","messages":"Unknown sid"}'
        mock_results_delete.return_value = get_mock_response(404, mocked_return_value)
        search_id = "1536832140.4293"
        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        results_response = transmission.delete(search_id)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == ErrorCode.TRANSMISSION_SEARCH_DOES_NOT_EXISTS.value

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_result(self, mock_result):
        """Test Invalid host for transmit result"""

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mock_result.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('splunk', connection, config)

        search_id = "test"

        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] is not None
        assert "Invalid Host" in results_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_status(self, mock_ping):
        """Test Invalid host for transmit status"""

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mock_ping.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        search_id = "test"
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is False
        assert status_response['error'] is not None
        assert "Invalid Host" in status_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_ping(self, mock_ping):
        """Test Invalid host for ping connection"""

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mock_ping.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['error'] is not None
        assert "Invalid Host" in ping_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_quota_invalid_json_exception(self, mock_quota_response):
        """test invalid json exception"""

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mocked_return_value = "invalid json"
        mock_quota_response.return_value = get_mock_response(200, mocked_return_value)
        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        query_response = transmission.query({})
        assert query_response is not None
        assert query_response['success'] is False
        assert 'error' in query_response

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_timeout_error_in_ping(self, mock_ping):
        """test connection/timeout error in transmit ping"""

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mock_ping.side_effect = TimeoutError("TimeoutError")
        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['error'] is not None
        assert "TimeoutError" in ping_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_timeout_error_in_status(self, mock_ping):
        """test connection/timeout error in transmit status"""

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mock_ping.side_effect = TimeoutError("TimeoutError")
        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        search_id = "test"
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is False
        assert status_response['error'] is not None
        assert "TimeoutError" in status_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_timeout_error_in_result(self, mock_result):
        """test connection/timeout error in transmit result"""

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mock_result.side_effect = TimeoutError("TimeoutError")
        transmission = stix_transmission.StixTransmission('splunk', connection, config)

        search_id = "test"
        offset = 0
        length = 1
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] is not None
        assert "TimeoutError" in results_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_timeout_error_in_delete(self, mock_delete):
        """test connection/timeout error in delete module in transmit"""

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mock_delete.side_effect = TimeoutError("TimeoutError")
        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        search_id = "test"
        delete_response = transmission.delete(search_id)

        assert delete_response is not None
        assert delete_response['success'] is False
        assert delete_response['error'] is not None
        assert "TimeoutError" in delete_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_timeout_error_in_query(self, mock_query):
        """test connection/timeout error in transmit query"""

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mock_query.side_effect = TimeoutError("TimeoutError")
        transmission = stix_transmission.StixTransmission('splunk', connection, config)

        query = "test"
        results_response = transmission.query(query)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['error'] is not None
        assert "TimeoutError" in results_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_query(self, mock_query):
        """Test Invalid host for transmit query"""

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mock_query.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        query = "test"
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert query_response['error'] is not None
        assert "Invalid Host" in query_response['error']

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api')
    def test_invalid_host_delete(self, mock_delete):
        """Test Invalid host for delete module in transmit"""

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }
        connection = {
            "host": "host",
            "port": 8080
        }

        mock_delete.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('splunk', connection, config)
        search_id = "test"
        delete_response = transmission.delete(search_id)

        assert delete_response is not None
        assert delete_response['success'] is False
        assert delete_response['error'] is not None
        assert "Invalid Host" in delete_response['error']
