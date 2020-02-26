from stix_shifter.stix_transmission.src.modules.qradar import qradar_connector
from stix_shifter.stix_transmission.src.modules.base.base_status_connector import Status
from unittest.mock import patch
import unittest
from stix_shifter.stix_transmission.src.modules.utils.RestApiClient import ResponseWrapper
from stix_shifter.stix_transmission import stix_transmission

class QRadarMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return self.object    


@patch('stix_shifter.stix_transmission.src.modules.qradar.arielapiclient.APIClient.__init__', autospec=True)
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

    @patch('stix_shifter.stix_transmission.src.modules.qradar.arielapiclient.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = QRadarMockResponse(200, mocked_return_value)

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
        
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter.stix_transmission.src.modules.qradar.arielapiclient.APIClient.create_search')
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
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == "108cb8b0-0744-4dd9-8e35-ea8311cd6211"

    @patch('stix_shifter.stix_transmission.src.modules.qradar.arielapiclient.APIClient.get_search', autospec=True)
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
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response['success']
        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == Status.COMPLETED.value

    @patch('stix_shifter.stix_transmission.src.modules.qradar.arielapiclient.APIClient.get_search_results', autospec=True)
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
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert results_response['success']
        assert 'data' in results_response
        assert 'events' in results_response['data']
        assert len(results_response['data']) > 0

    @patch('stix_shifter.stix_transmission.src.modules.qradar.arielapiclient.APIClient.create_search', autospec=True)
    @patch('stix_shifter.stix_transmission.src.modules.qradar.arielapiclient.APIClient.get_search', autospec=True)
    @patch('stix_shifter.stix_transmission.src.modules.qradar.arielapiclient.APIClient.get_search_results', autospec=True)
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
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        query_response = transmission.query(query)

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

class RequestsResponse():
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return self.object    

class MockResponseWrapper(QRadarMockResponse):
    @property 
    def status_code(self):
        return self.code

    @property
    def content(self):
        return self.object

    def raise_for_status(self):
        pass

@patch('requests.get', autospec = True)
class TestRequests(unittest.TestCase, object):
    def test_xforward_request(self, mock_get):
        mocked_return_value = '["mock", "placeholder"]'
        mock_get.return_value = MockResponseWrapper(200, mocked_return_value)

        connection = {
            "proxy" : {
                "url" : "proxy_url0:8088",
                "auth" : "proxy_auth_data0",
                "x_forward_proxy" : "x_forward_proxy_host1",
                "x_forward_proxy_auth" : "x_forward_proxy_auth_data1"
            },

            "host" : "somehost0",
            "port" : "15004",
            "cert" : "somecert0"
        }

        config = {
            "auth": {
                "SEC": "sec0"
            }
        }
        
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        transmission.ping()

        mock_get.assert_called_with('x_forward_proxy_host1', cert=None, data=None, headers={'version': '8.0', 'accept': 'application/json', \
                                    'sec': 'sec0', 'proxy': 'proxy_url0:8088', 'proxy-authorization': 'Basic proxy_auth_data0', \
                                    'x-forward-url': 'https://somehost0:15004/api/help/resources', 'x-forward-auth': 'x_forward_proxy_auth_data1', 'user-agent': 'UDS'}, timeout=10, verify=True)


@patch('requests.post', autospec = True)
@patch('requests.get', autospec = True)
class TestQRadarCloudDataLake(unittest.TestCase, object):
    def test_query_response(self, mock_get, mock_post):
        connection = {
            "host" : "somehost0",
            "port" : "15000",
            "cert" : "somecert0",
            "data_lake": True
        }
        config = {
            "auth": {
                "SEC": "sec0"
            }
        }
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        transmission.query('some-query')
        assert 'https://somehost0:15000/api/ariel/searches?data_lake=%22qcdl%22' in mock_post.call_args[0]

    def test_status_response(self, mock_get, mock_post):
        connection = {
            "host" : "somehost0",
            "port" : "15000",
            "cert" : "somecert0",
            "data_lake": True
        }
        config = {
            "auth": {
                "SEC": "sec0"
            }
        }
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        transmission.status('some-search-id')
        assert 'https://somehost0:15000/api/ariel/searches/some-search-id?data_lake=%22qcdl%22' in mock_get.call_args[0]

    def test_results_response(self, mock_get, mock_post):
        connection = {
            "host" : "somehost0",
            "port" : "15000",
            "cert" : "somecert0",
            "data_lake": True
        }
        config = {
            "auth": {
                "SEC": "sec0"
            }
        }
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        transmission.results('some-search-id', 0, 1)
        assert 'https://somehost0:15000/api/ariel/searches/some-search-id/results?data_lake=%22qcdl%22' in mock_get.call_args[0]
