from stix_shifter.stix_transmission.src.modules.bigfix import bigfix_connector
from unittest.mock import patch
import unittest
import json
from stix_shifter.stix_transmission import stix_transmission

class BigFixMockJsonResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object.encode()
    
    def read(self):
        return self.object


class MockHttpResponse:
    def __init__(self, string):
        self.string = string

    def decode(self, string):
        return self.string


class BigFixMockHttpXMLResponse:
    def __init__(self, response_code, object):
        self.code = response_code
        self.object = object

    def read(self):

        return self.object


config = {
            "auth": {
                "user_name": "fake",
                "password": "fake"
            }
}

connection = {
            "host": "fake",
            "port": "fake",
            "cert": "fake"
}


@patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.__init__', autospec=True)
class TestBigfixConnection(unittest.TestCase):
    def test_is_async(self, mock_api_client):
        mock_api_client.return_value = None
        module = bigfix_connector

        check_async = module.Connector(connection, config).is_async
        assert check_async

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.ping_box')
    def test_ping_endpoint_good_return(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = MockHttpResponse('/api/clientquery')
        mock_ping_response.return_value = BigFixMockHttpXMLResponse(200, mocked_return_value)

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success']

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.ping_box')
    def test_ping_endpoint_not_working_return(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = MockHttpResponse('/missing')
        mock_ping_response.return_value = BigFixMockHttpXMLResponse(200, mocked_return_value)

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] == False

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.ping_box')
    def test_ping_endpoint_exception(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = MockHttpResponse('/exception')
        mock_ping_response.return_value = BigFixMockHttpXMLResponse(200, mocked_return_value)
        mock_ping_response.side_effect = Exception('an error occured retriving ping information')

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] == False
        assert ping_response['error'] is not None

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.ping_box')
    def test_ping_endpoint_bad_return_code(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        mocked_return_value = MockHttpResponse('/exception')
        mock_ping_response.return_value = BigFixMockHttpXMLResponse(500, mocked_return_value)

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert 'success' in ping_response
        assert ping_response['success'] == False
        assert ping_response['error'] is not None

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.create_search')
    def test_query_response_found(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        big_fix_return_value = '<?xml version="1.0" encoding="UTF-8"?>'\
                                    '<BESAPI xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"' \
                                    ' xsi:noNamespaceSchemaLocation="BESAPI.xsd">'\
                                    '<ClientQuery ' \
                                    'Resource="https://fake.computer.name:52311/api/clientquery/105">' \
                                    '<ID>105</ID></ClientQuery></BESAPI>'

        mocked_return_value = MockHttpResponse(big_fix_return_value)
        mock_query_response.return_value = BigFixMockHttpXMLResponse(200, mocked_return_value)

        query = 'bigfix query text'
        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] == True
        assert 'search_id' in query_response
        assert query_response['search_id'] == "105"

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.create_search')
    def test_query_response_not_found(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        big_fix_return_value = 'big fix did not return proper value'
        mocked_return_value = MockHttpResponse(big_fix_return_value)
        mock_query_response.return_value = BigFixMockHttpXMLResponse(200, mocked_return_value)
        
        query = 'bigfix query text'

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        query_response = transmission.query(query)
        
        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] == False
        assert 'error' in query_response
        assert 'search_id' in query_response
        assert query_response['search_id'] == "UNKNOWN"

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.create_search')
    def test_query_response_exception(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        big_fix_return_value = 'big fix did not return proper value'
        mocked_return_value = MockHttpResponse(big_fix_return_value)
        mock_query_response.return_value = BigFixMockHttpXMLResponse(200, mocked_return_value)
        mock_query_response.side_effect = Exception('an error occured creating search')

        query = 'bigfix query text'

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        query_response = transmission.query(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] == False
        assert 'error' in query_response

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.create_search')
    def test_query_response_bad_return_code(self, mock_query_response, mock_api_client):
        mock_api_client.return_value = None
        big_fix_return_value = 'big fix did not return proper value'
        mocked_return_value = MockHttpResponse(big_fix_return_value)
        mock_query_response.return_value = BigFixMockHttpXMLResponse(200, mocked_return_value)
        module = bigfix_connector

        query = 'bigfix query text'

        query_response = module.Connector(connection, config).create_query_connection(query)

        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] == False
        assert 'error' in query_response

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_sync_query_results')
    def test_status_response_completed(self, mock_sync_query_results, mock_status_response, mock_api_client):
        mock_api_client.return_value = None

        mocked_sync_query_return_value = MockHttpResponse('<Answer type="integer">2</Answer>')
        mock_sync_query_results.return_value = BigFixMockHttpXMLResponse(200, mocked_sync_query_return_value)

        mocked_search_results_status = '{"reportingAgents": "2", "totalResults": "100"}'
        mock_status_response.return_value=BigFixMockJsonResponse(200,mocked_search_results_status)

        search_id = "104"

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] == True
        assert 'status' in status_response
        assert status_response['status'] == "COMPLETED"
        assert 'progress' in status_response
        assert status_response['progress'] == 100

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_sync_query_results')
    def test_status_response_running(self, mock_sync_query_results, mock_status_response, mock_api_client):
        mock_api_client.return_value = None

        mocked_sync_query_return_value = MockHttpResponse('<Answer type="integer">2</Answer>')
        mock_sync_query_results.return_value = BigFixMockHttpXMLResponse(200, mocked_sync_query_return_value)

        mocked_search_results_status = '{"reportingAgents": "0", "totalResults": "100"}'
        mock_status_response.return_value=BigFixMockJsonResponse(200,mocked_search_results_status)

        search_id = "104"

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] == True
        assert 'status' in status_response
        assert status_response['status'] == "RUNNING"
        assert 'progress' in status_response
        assert status_response['progress'] == 0

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_sync_query_results')
    def test_status_response_running_50_complete(self, mock_sync_query_results, mock_status_response, mock_api_client):
        mock_api_client.return_value = None

        mocked_sync_query_return_value = MockHttpResponse('<Answer type="integer">2</Answer>')
        mock_sync_query_results.return_value = BigFixMockHttpXMLResponse(200, mocked_sync_query_return_value)

        mocked_search_results_status = '{"reportingAgents": "1", "totalResults": "100"}'
        mock_status_response.return_value=BigFixMockJsonResponse(200,mocked_search_results_status)

        search_id = "104"

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] == True
        assert 'status' in status_response
        assert status_response['status'] == "RUNNING"
        assert 'progress' in status_response
        assert status_response['progress'] == 50

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_sync_query_results')
    def test_status_response_running_75_complete(self, mock_sync_query_results, mock_status_response, mock_api_client):
        mock_api_client.return_value = None

        mocked_sync_query_return_value = MockHttpResponse('<Answer type="integer">10000</Answer>')
        mock_sync_query_results.return_value = BigFixMockHttpXMLResponse(200, mocked_sync_query_return_value)

        mocked_search_results_status = '{"reportingAgents": "7500", "totalResults": "100"}'
        mock_status_response.return_value=BigFixMockJsonResponse(200,mocked_search_results_status)

        search_id = "104"

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] == True
        assert 'status' in status_response
        assert status_response['status'] == "RUNNING"
        assert 'progress' in status_response
        assert status_response['progress'] == 75

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_sync_query_results')
    def test_status_response_error(self, mock_sync_query_results, mock_status_response, mock_api_client):
        mock_api_client.return_value = None

        mocked_sync_query_return_value = MockHttpResponse('<Answer type="integer">2</Answer>')
        mock_sync_query_results.return_value = BigFixMockHttpXMLResponse(200, mocked_sync_query_return_value)

        mocked_search_results_status = '{"reportingAgents": "2", "totalResults": "0"}'
        mock_status_response.return_value=BigFixMockJsonResponse(200,mocked_search_results_status)

        search_id = "104"

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] == True
        assert 'status' in status_response
        assert status_response['status'] == "ERROR"
        assert 'progress' in status_response
        assert status_response['progress'] == 100

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_sync_query_results')
    def test_status_response_running_bad_client_query(self, mock_sync_query_results, mock_status_response,
                                                      mock_api_client):
        mock_api_client.return_value = None

        mocked_sync_query_return_value = MockHttpResponse('bad answer')
        mock_sync_query_results.return_value = BigFixMockHttpXMLResponse(200, mocked_sync_query_return_value)

        mocked_search_results_status = '{"reportingAgents": "2", "totalResults": "0"}'
        mock_status_response.return_value=BigFixMockJsonResponse(200,mocked_search_results_status)

        search_id = "104"

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] == True
        assert 'status' in status_response
        assert status_response['status'] == "RUNNING"
        assert 'progress' in status_response
        assert status_response['progress'] == 0

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_sync_query_results')
    def test_status_response_error_exception_status(self, mock_sync_query_results, mock_status_response,
                                             mock_api_client):
        mock_api_client.return_value = None

        mocked_sync_query_return_value = MockHttpResponse('bad answer')
        mock_sync_query_results.return_value = BigFixMockHttpXMLResponse(200, mocked_sync_query_return_value)

        mocked_search_results_status = '{"reportingAgents": "2", "totalResults": "0"}'
        mock_status_response.return_value=BigFixMockJsonResponse(200,mocked_search_results_status)
        mock_status_response.side_effect = Exception('an error getting status')

        search_id = "104"

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] == False
        assert 'error' in status_response
        assert 'progress' not in status_response

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_sync_query_results')
    def test_status_response_error_exception_result(self, mock_sync_query_results, mock_status_response,
                                             mock_api_client):
        mock_api_client.return_value = None

        mocked_sync_query_return_value = MockHttpResponse('bad answer')
        mock_sync_query_results.return_value = BigFixMockHttpXMLResponse(200, mocked_sync_query_return_value)
        mock_sync_query_results.side_effect = Exception('an error occurred executing sync query')
        mocked_search_results_status = '{"reportingAgents": "2", "totalResults": "0"}'
        mock_status_response.return_value=BigFixMockJsonResponse(200,mocked_search_results_status)

        search_id = "104"

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] == False
        assert 'error' in status_response
        assert 'progress' not in status_response

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_sync_query_results')
    def test_status_response_error_exception_result_bad_return_code(self, mock_sync_query_results,
                                                                    mock_status_response,
                                                                    mock_api_client):
        mock_api_client.return_value = None

        mocked_sync_query_return_value = MockHttpResponse('<Answer type="integer">2</Answer>')
        mock_sync_query_results.return_value = BigFixMockHttpXMLResponse(200, mocked_sync_query_return_value)

        mocked_search_results_status = '{"reportingAgents": "2", "totalResults": "0"}'
        mock_status_response.return_value=BigFixMockJsonResponse(500,mocked_search_results_status)

        search_id = "104"

        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        status_response = transmission.status(search_id)

        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] == False
        assert 'error' in status_response
        assert 'progress' not in status_response

    def test_delete_query(self, mock_api_client):
        mock_api_client.return_value = None

        search_id = "104"

        module = bigfix_connector
        status_response = module.Connector(connection, config).delete_query_connection(search_id)
        assert status_response is not None
        assert 'success' in status_response
        assert status_response['success'] == True

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    def test_results_response(self, mock_results_response, mock_api_client):

        mock_api_client.return_value = None
        mocked_return_value = """{
                                    "reportingAgents": 2,
                                    "totalResults": 2,
                                    "results": [
                                        {
                                        "computerID": 12369754,
                                        "computerName": "bigdata4545.canlab.ibm.com",
                                        "subQueryID": 1,
                                        "isFailure": false,
                                        "result": "file, .X0-lock, sha256, 7236f966f07259a1de3ee0d48a3ef0ee47c4a551af7f0d76dcabbbb9d6e00940, sha1, 8b5e953be1db90172af66631132f6f27dda402d2, md5, e5307d27f0eb9a27af8597a1ddc51e89, /tmp/.X0-lock, 1541424894",
                                        "ResponseTime": 0
                                        },
                                        {
                                        "computerID": 14821900,
                                        "computerName": "DESKTOP-C30V1JF",
                                        "subQueryID": 1,
                                        "isFailure": true,
                                        "result": "Singular expression refers to nonexistent object.",
                                        "ResponseTime": 1000
                                        }
                                    ]
                                }"""
        mock_results_response.return_value = BigFixMockJsonResponse(200, mocked_return_value)

        
        search_id = "102"
        offset = "0"
        length = "100"
        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        results_response = transmission.results(search_id, offset, length)
        json_response = json.loads(results_response)

        assert results_response is not None
        assert 'success' in json_response
        assert json_response['success'] == True
        assert 'data' in json_response
        assert len(json_response['data']) == 1

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    def test_results_response_exeception(self, mock_results_response, mock_api_client):

        mock_api_client.return_value = None
        mock_results_response.side_effect = Exception('an error getting data')

        search_id = "102"
        offset = "0"
        length = "100"
        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        results_response = transmission.results(search_id, offset, length)

        assert results_response is not None
        assert 'success' in results_response
        assert results_response['success'] == False
        assert 'error' in results_response

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    def test_results_response_bad_return_code(self, mock_results_response, mock_api_client):

        mock_api_client.return_value = None
        mocked_return_value = """{
                                    "reportingAgents": "100",
                                    "totalResults": "201",
                                    "results": 
                                    [
                                        {
                                            "computerID":12369754,
                                            "computerName":"fake.computer.name",
                                            "subQueryID":1,"isFailure":false,
                                            "result":".err, d41d8cd98f00b204e9800998ecf8427e, u002f.err","ResponseTime":0
                                        },
                                        {
                                            "computerID":14821900,
                                            "computerName":"DESKTOP-C30V1JF",
                                            "subQueryID":1,
                                            "isFailure":true,
                                            "result":"12520437.cpx, 0a0feb9eb28bde8cd835716343b03b14, C:\\\\Windows\\\\system32\\\\12520437.cpx","ResponseTime":62000
                                        }
                                    ]
                                }"""
        mock_results_response.return_value = BigFixMockJsonResponse(500, mocked_return_value)

        search_id = "102"
        offset = "0"
        length = "100"
        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        results_response = transmission.results(search_id, offset, length)
        json_response = json.loads(results_response)

        assert results_response is not None
        assert 'success' in json_response
        assert json_response['success'] == False
        assert 'error' in json_response

    @patch('stix_shifter.stix_transmission.src.modules.bigfix.bigfix_api_client.APIClient.get_search_results')
    def test_results_response_bad_json(self, mock_results_response, mock_api_client):

        mock_api_client.return_value = None
        mocked_return_value = """{
                                    "reportingAgents": "100",
                                    "totalResults": "201",
                                    "results": 
                                    [aDAsdadDAS
                                        {
                                            "computerID":12369754,
                                            "computerName":"fake.computer.name",
                                            "subQueryID":1,"isFailure":false,
                                            "result":".err, d41d8cd98f00b204e9800998ecf8427e, u002f.err","ResponseTime":0
                                        },
                                        {
                                            "computerID":14821900,
                                            "computerName":"DESKTOP-C30V1JF",
                                            "subQueryID":1,
                                            "isFailure":true,
                                            "result":"12520437.cpx, 0a0feb9eb28bde8cd835716343b03b14, C:\\\\Windows\\\\system32\\\\12520437.cpx","ResponseTime":62000
                                        }
                                    ]
                                }"""
        mock_results_response.return_value = BigFixMockJsonResponse(200, mocked_return_value)

        search_id = "102"
        offset = "0"
        length = "100"
        transmission = stix_transmission.StixTransmission('bigfix',  connection, config)
        results_response = transmission.results(search_id, offset, length)

        json_response = json.loads(results_response)

        assert results_response is not None
        assert 'success' in json_response
        assert json_response['success'] == False
        assert 'error' in json_response
