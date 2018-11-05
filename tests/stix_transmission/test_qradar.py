from stix_transmission.src.modules.qradar import qradar_connector
from stix_transmission.src.modules.base.base_status_connector import Status
from unittest.mock import patch
import unittest


class QRadarMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return self.object


@patch('stix_transmission.src.modules.qradar.arielapiclient.APIClient.__init__', autospec=True)
class TestQRadarConnection(unittest.TestCase, object):
    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        module = qradar_connector

        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }
        check_async = module.Connector(connection, config).is_async

        assert check_async

    @patch('stix_transmission.src.modules.qradar.arielapiclient.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = QRadarMockResponse(200, mocked_return_value)

        module = qradar_connector
        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }
        ping_response = module.Connector(connection, config).ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_transmission.src.modules.qradar.arielapiclient.APIClient.create_search')
    def test_query_response(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211"}'
        mock_query_response.return_value = QRadarMockResponse(201, mocked_return_value)

        module = qradar_connector
        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }
        query = '{"query":"SELECT sourceIP from events"}'
        query_response = module.Connector(connection, config).create_query_connection(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == "108cb8b0-0744-4dd9-8e35-ea8311cd6211"

    @patch('stix_transmission.src.modules.qradar.arielapiclient.APIClient.get_search', autospec=True)
    def test_status_response(self, mock_status_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211", "status": "COMPLETED", "progress": "100"}'
        mock_status_response.return_value = QRadarMockResponse(200, mocked_return_value)

        module = qradar_connector
        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }
        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        status_response = module.Connector(connection, config).create_status_connection(search_id)

        assert status_response['success']
        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == Status.COMPLETED.value

    @patch('stix_transmission.src.modules.qradar.arielapiclient.APIClient.get_search_results', autospec=True)
    def test_results_response(self, mock_results_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = """{
            "search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211",
            "events": {
                "events": [
                    {
                        "sourceIP":"9.21.122.81"
                    },
                    {
                        "sourceIP":"9.21.122.81"
                    }
                ]
            }
        }"""
        mock_results_response.return_value = QRadarMockResponse(200, mocked_return_value)

        module = qradar_connector
        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }
        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        offset = 0
        length = 1
        results_response = module.Connector(connection, config).create_results_connection(search_id, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert 'events' in results_response['data']
        assert len(results_response['data']) > 0

    @patch('stix_transmission.src.modules.qradar.arielapiclient.APIClient.create_search', autospec=True)
    @patch('stix_transmission.src.modules.qradar.arielapiclient.APIClient.get_search', autospec=True)
    @patch('stix_transmission.src.modules.qradar.arielapiclient.APIClient.get_search_results', autospec=True)
    def test_query_flow(self, mock_results_response, mock_status_response, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        query_mock = '{"search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211"}'
        status_mock = '{"search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211", "status": "COMPLETED", "progress": "100"}'
        results_mock = """{
            "search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211",
            "events": {
                "events": [
                    {
                        "sourceIP":"9.21.122.81"
                    },
                    {
                        "sourceIP":"9.21.122.81"
                    }
                ]
            }
        }"""
        mock_results_response.return_value = QRadarMockResponse(200, results_mock)
        mock_status_response.return_value = QRadarMockResponse(200, status_mock)
        mock_query_response.return_value = QRadarMockResponse(201, query_mock)
        module = qradar_connector

        config = {
            "auth": {
                "SEC": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": "8080",
            "ceft": "cert"
        }

        query = '{"query":"SELECT sourceIP from events"}'

        query_response = module.Connector(connection, config).create_query_connection(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == "108cb8b0-0744-4dd9-8e35-ea8311cd6211"

        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        status_response = module.Connector(connection, config).create_status_connection(search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == Status.COMPLETED.value

        offset = 0
        length = 1
        results_response = module.Connector(connection, config).create_results_connection(search_id, offset, length)

        assert results_response is not None
        assert 'data' in results_response
        assert 'events' in results_response['data']
        assert len(results_response['data']) > 0
