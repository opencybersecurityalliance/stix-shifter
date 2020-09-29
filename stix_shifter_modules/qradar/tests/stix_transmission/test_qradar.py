from stix_shifter_modules.qradar.entry_point import EntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter_utils.stix_transmission.utils.RestApiClient import RestApiClient
from stix_shifter.stix_transmission import stix_transmission
from unittest.mock import patch
import unittest


class QRadarMockResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):
        return self.object    

@patch('stix_shifter_modules.qradar.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestQRadarConnection(unittest.TestCase, object):
    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        entry_point = EntryPoint()

        config = {
            "auth": {
                "sec": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }
        check_async = entry_point.is_async()

        assert check_async

    @patch('stix_shifter_modules.qradar.stix_transmission.api_client.APIClient.ping_box')
    def test_ping_endpoint(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '["mock", "placeholder"]'
        mock_ping_response.return_value = QRadarMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "sec": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }
        
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter_modules.qradar.stix_transmission.api_client.APIClient.create_search')
    def test_query_response(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211"}'
        mock_query_response.return_value = QRadarMockResponse(201, mocked_return_value)

        config = {
            "auth": {
                "sec": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }

        query = '{"query":"SELECT sourceIP from events"}'        
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == "108cb8b0-0744-4dd9-8e35-ea8311cd6211"

    @patch('stix_shifter_modules.qradar.stix_transmission.api_client.APIClient.get_search', autospec=True)
    def test_status_response(self, mock_status_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = '{"search_id": "108cb8b0-0744-4dd9-8e35-ea8311cd6211", "status": "COMPLETED", "progress": "100"}'
        mock_status_response.return_value = QRadarMockResponse(200, mocked_return_value)

        config = {
            "auth": {
                "sec": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }
        
        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response['success']
        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == Status.COMPLETED.value

    @patch('stix_shifter_modules.qradar.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
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
                "sec": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
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

    @patch('stix_shifter_modules.qradar.stix_transmission.api_client.APIClient.create_search', autospec=True)
    @patch('stix_shifter_modules.qradar.stix_transmission.api_client.APIClient.get_search', autospec=True)
    @patch('stix_shifter_modules.qradar.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
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

        config = {
            "auth": {
                "sec": "bla"
            }
        }
        connection = {
            "host": "hostbla",
            "port": 8080,
            "selfSignedCert": "cert"
        }

        query = '{"query":"SELECT sourceIP from events"}'
        entry_point = EntryPoint(connection, config)

        query_response = entry_point.create_query_connection(query)
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == "108cb8b0-0744-4dd9-8e35-ea8311cd6211"

        search_id = "108cb8b0-0744-4dd9-8e35-ea8311cd6211"
        status_response = entry_point.create_status_connection(search_id)

        assert status_response is not None
        assert 'status' in status_response
        assert status_response['status'] == Status.COMPLETED.value

        offset = 0
        length = 1
        results_response = entry_point.create_results_connection(search_id, offset, length)

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

@patch('requests.post', autospec = True)
@patch('requests.get', autospec = True)
class TestQRadarCloudDataLake(unittest.TestCase, object):
    def test_query_response(self, mock_get, mock_post):
        mocked_return_value = '{"search_id":"1"}'
        mock_post.return_value = MockResponseWrapper(201, mocked_return_value)

        connection = {
            "host" : "somehost0",
            "port" : 15000,
            "selfSignedCert" : "somecert0",
            "data_lake": True
        }
        config = {
            "auth": {
                "sec": "sec0"
            }
        }
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        transmission.query('some-query')
        call_args = mock_post.call_args
        assert 'https://somehost0:15000/api/ariel/searches' in call_args[0]
        assert {'data_lake': '"qcdl"'} == call_args[1]['params']

    def test_status_response(self, mock_get, mock_post):
        mocked_return_value = '{"status": "COMPLETED", "progress":"100"}'
        mock_get.return_value = MockResponseWrapper(200, mocked_return_value)

        connection = {
            "host" : "somehost0",
            "port" : 15000,
            "selfSignedCert" : "somecert0",
            "data_lake": True
        }
        config = {
            "auth": {
                "sec": "sec0"
            }
        }
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        transmission.status('some-search-id')
        
        call_args = mock_get.call_args
        assert 'https://somehost0:15000/api/ariel/searches/some-search-id' in call_args[0]
        assert {'data_lake': '"qcdl"'} == call_args[1]['params']


    def test_results_response(self, mock_get, mock_post):
        mocked_return_value = '{"status": "COMPLETED", "progress":"100"}'
        mock_get.return_value = MockResponseWrapper(200, mocked_return_value)
        connection = {
            "host" : "somehost0",
            "port" : 15000,
            "selfSignedCert" : "somecert0",
            "data_lake": True
        }
        config = {
            "auth": {
                "sec": "sec0"
            }
        }
        transmission = stix_transmission.StixTransmission('qradar',  connection, config)
        transmission.results('some-search-id', 0, 1)

        call_args = mock_get.call_args
        assert 'https://somehost0:15000/api/ariel/searches/some-search-id/results' in call_args[0]
        assert {'data_lake': '"qcdl"'} == call_args[1]['params']
