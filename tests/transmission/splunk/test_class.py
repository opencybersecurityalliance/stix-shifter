from stix_transmission.src.modules.splunk import splunk_connector
from unittest.mock import patch
import unittest
import json
import os


class SplunkMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return self.object


@patch('stix_transmission.src.modules.splunk.spl_api_client.APIClient.__init__')
class TestSplunkConnection(unittest.TestCase, object):
    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        module = splunk_connector
        
        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }      
        connection = {
            "host": "host",
            "port": "8080"
        }

        check_async = module.Connector(connection, config).is_async

        assert check_async

    @patch('stix_transmission.src.modules.splunk.spl_api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = SplunkMockResponse(200, mocked_return_value)

        module = splunk_connector
        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }      
        connection = {
            "host": "host",
            "port": "8080"
        }

        ping_response = module.Connector(connection, config).ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_transmission.src.modules.splunk.spl_api_client.APIClient.create_search')
    def test_query_response(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"sid":"1536672851.4012"}'
        mock_query_response.return_value = SplunkMockResponse(201, mocked_return_value)

        module = splunk_connector
        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }      
        connection = {
            "host": "host",
            "port": "8080"
        }

        query = 'search eventtype=network_traffic | fields + tag| spath'
        query_response = module.Connector(connection, config).create_query_connection(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "1536672851.4012"
 
    @patch('stix_transmission.src.modules.splunk.spl_api_client.APIClient.get_search', autospec=True)
    def test_status_response(self, mock_status_response, mock_api_client):
        mock_api_client.return_value = None

        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'status_by_sid.json')
        mocked_return_value = open(file_path, 'r').read()

        mock_status_response.return_value = SplunkMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }      
        connection = {
            "host": "host",
            "port": "8080"
        }

        search_id = "1536832140.4293"
        module = splunk_connector
        status_response = module.Connector(connection, config).create_status_connection(search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == 'COMPLETED'
        assert 'progress' in status_response
        assert status_response['progress'] == 100
        assert 'success' in status_response
        assert status_response['success'] is True
       
    @patch('stix_transmission.src.modules.splunk.spl_api_client.APIClient.get_search_results', autospec=True)
    def test_results_response(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'result_by_sid.json')
        mocked_return_value = open(file_path, 'r').read()

        mock_results_response.return_value = SplunkMockResponse(200, mocked_return_value)

        module = splunk_connector
        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }      
        connection = {
            "host": "host",
            "port": "8080"
        }
        
        search_id = "1536832140.4293"
        offset = 0
        length = 1
        results_response = module.Connector(connection, config).create_results_connection(search_id, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) > 0
    
    @patch('stix_transmission.src.modules.splunk.spl_api_client.APIClient.create_search', autospec=True)
    @patch('stix_transmission.src.modules.splunk.spl_api_client.APIClient.get_search', autospec=True)
    @patch('stix_transmission.src.modules.splunk.spl_api_client.APIClient.get_search_results', autospec=True)
    def test_query_flow(self, mock_results_response, mock_status_response, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        
        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }      
        connection = {
            "host": "host",
            "port": "8080"
        }

        query_mock = '{"sid":"1536832140.4293"}'
        mock_query_response.return_value = SplunkMockResponse(201, query_mock)
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(dir_path, 'api_response', 'result_by_sid.json')
        results_mock = open(file_path, 'r').read()
        mock_results_response.return_value = SplunkMockResponse(200, results_mock)
        
        status_file_path = os.path.join(dir_path, 'api_response', 'status_by_sid.json')
        status_mock = open(status_file_path, 'r').read()
        mock_status_response.return_value = SplunkMockResponse(200, status_mock)

        module = splunk_connector

        query = 'search eventtype=network_traffic | fields + tag| spath'
        query_response = module.Connector(connection, config).create_query_connection(query)

        assert query_response is not None
        assert query_response['success'] is True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "1536832140.4293"

        search_id = "1536832140.4293"
        status_response = module.Connector(connection, config).create_status_connection(search_id)

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
        results_response = module.Connector(connection, config).create_results_connection(search_id, offset, length)

        assert 'success' in results_response
        assert results_response['success'] is True
        assert 'data' in results_response
        assert len(results_response['data']) > 0

    @patch('stix_transmission.src.modules.splunk.spl_api_client.APIClient.delete_search', autospec=True)
    def test_delete_search(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None
        
        config = {
            "auth": {
                "username": "",
                "password": ""
            }
        }      
        connection = {
            "host": "host",
            "port": "8080"
        }
        
        mocked_return_value = '{"messages":[{"type":"INFO","text":"Search job cancelled."}]}'
        mock_results_response.return_value = SplunkMockResponse(200, mocked_return_value)

        module = splunk_connector
        search_id = "1536832140.4293"
        results_response = module.Connector(connection, config).delete_query_connection(search_id)
        
        assert results_response is not None
        assert results_response['success'] is True