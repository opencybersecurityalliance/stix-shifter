import json
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.stix_transmission.utils.RestApiClient import ResponseWrapper
from unittest.mock import patch
import unittest
from collections import namedtuple

DATA = {
            "data": [
                {
                            "class": "network",
                            "score": 0,
                            "value": "linkprotect.cudasvc.com/url",
                            "expires_calculated_at": "2022-01-17 15:20:06",
                            "touched_at": "2022-01-18 15:17:48",
                            "id": 14213,
                            "updated_at": "2022-01-15 15:15:47",
                            "published_at": "2022-01-15 15:15:47",
                            "created_at": "2022-01-15 15:15:47",
                            "status_id": 1,
                            "hash": "d5bde55bcc50e107e68369e73124ffde",
                            "type_id": 30,
                            "adversaries": [],
                            "type": {
                                "name": "URL",
                                "id": 30,
                                "class": "network"
                            },
                            "status": {
                                "name": "Active",
                                "id": 1,
                                "description": "Poses a threat and is being exported to detection tools."
                            },
                            "attributes": [
                                {
                                    "value": "US",
                                    "created_at": "2022-01-15 15:15:50",
                                    "indicator_id": 14213,
                                    "updated_at": "2022-01-18 15:17:39",
                                    "attribute_id": 10,
                                    "id": 174338,
                                    "touched_at": "2022-01-18 15:17:39",
                                    "name": "Country"
                                }
                            ],
                            "sources": [
                                {
                                    "indicator_id": 14213,
                                    "indicator_status_id": 1,
                                    "published_at": "2022-01-15 15:15:50",
                                    "source_id": 16,
                                    "id": 101803,
                                    "created_at": "2022-01-15 15:15:50",
                                    "source_type": "connectors",
                                    "creator_source_id": 16,
                                    "indicator_type_id": 30,
                                    "reference_id": 5,
                                    "updated_at": "2022-01-18 15:17:48",
                                    "name": "PhishTank"
                                }
                            ],
                            "enrich_info": {
                                "attributes": [
                                    {
                                        "id": 174338,
                                        "indicator_id": 14213,
                                        "attribute_id": 10,
                                        "value": "US",
                                        "created_at": "2022-01-15 15:15:50",
                                        "updated_at": "2022-01-18 15:17:39",
                                        "touched_at": "2022-01-18 15:17:39.815",
                                        "name": "Country",
                                        "sources": [
                                            {
                                                "id": 16,
                                                "type": "connectors",
                                                "reference_id": 5,
                                                "name": "PhishTank",
                                                "tlp_id": "None",
                                                "created_at": "2022-01-15 15:15:50",
                                                "updated_at": "2022-01-18 15:17:39",
                                                "published_at": "None",
                                                "pivot": {
                                                    "indicator_attribute_id": 174338,
                                                    "source_id": 16,
                                                    "id": 174338,
                                                    "creator_source_id": 16
                                                }
                                            }
                                        ],
                                        "attribute": {
                                            "id": 10,
                                            "name": "Country",
                                            "created_at": "2022-01-13 15:13:55",
                                            "updated_at": "2022-01-13 15:13:55"
                                        }
                                    }
                                ],
                                "Comments": "Additional attribute information is available on the ThreatQ platform."
                            },
                            "relationships": {
                                "malware": [],
                                "attack_pattern": [],
                                "campaign": [],
                                "ttp": [],
                                "tool": []
                            }
                        }
            ],
            "code": 200
    }
namespace = "8bf42ea1-e30d-41a2-a3ee-1aec759cf409"
SAMPLE_DATA = '{"data": "google.com", "dataType": "url"}'
MODULE_NAME = 'threat_q'

connection = {"namespace":namespace}
config = {"auth": {"hostname": "localhost", "username" : "abc@test.com", "password": "test"}}
ResponseResult = namedtuple('ResponseResult', ['data', 'code'])

class MockResponse:
    def __init__(self, json_data, status_code):
        self.content = str.encode(json.dumps(json_data))
        self.status_code = status_code

class MockHttpResponse:
    def __init__(self, string):
        self.string = string

    def decode(self, string):
        return self.string

class ThreatQHttpResponse:
    def __init__(self, obj, response_code):
        self.code = response_code
        self.object = obj

    def read(self):
        return self.object


@patch('stix_shifter_modules.threat_q.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestThreatQConnection(unittest.TestCase, object):
    @patch('stix_shifter_modules.threat_q.stix_transmission.api_client.APIClient.ping_threatQ')
    def test_threat_q_ping(self, mock_ping_response, mock_api_client):
        response = {'success': True, "code": 200}
        mock_api_client.return_value = None
        # mock_ping_response.return_value = ResponseResult(DATA, 200)
        # mock_ping_response.return_value = ThreatQHttpResponse(response, 200)
        mock_ping_response.return_value = response

        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()

        assert ping_response is not None
        assert ping_response['success']

    @patch('stix_shifter_modules.threat_q.stix_transmission.api_client.APIClient.ping_threatQ')
    def test_threat_q_ping_exception(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value = ThreatQHttpResponse(response, 400)
        mock_ping_response.side_effect = Exception('an error occured retriving ping information')
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.threat_q.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_threat_q_results(self, mock_result_connection, mock_api_client):
        mock_api_client.return_value = None
        mock_result_connection.return_value = DATA, namespace
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA

        search_results_response = transmission.results(query_response['search_id'], 0, 9)
        report = search_results_response['data'][0]

        assert 'data' in report
        assert 'dataType' in report
        assert 'report' in report
        assert 'success' in search_results_response
        assert search_results_response['success'] is True
        assert type(search_results_response['data']) is list
    
    @patch('stix_shifter_modules.threat_q.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_threat_q_results_error(self, mock_result_connection, mock_api_client):
        mock_api_client.return_value = None
        mock_data = DATA = {
            "error": "Invalid",
            "success": False,
            "code": 400
        }
        mock_result_connection.return_value = mock_data, namespace
        mock_result_connection.side_effect = Exception('an error occured retriving ping information')
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA

        search_results_response = transmission.results(query_response['search_id'], 0, 9)
        
        assert 'success' in search_results_response
        assert search_results_response['success'] is False
        assert 'code' in search_results_response, search_results_response['code'] == 'invalid_query'
    
    @patch('stix_shifter_modules.threat_q.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_threat_q_results_exception(self, mock_result_connection, mock_api_client):
        mock_api_client.return_value = None
        mock_data = DATA = {
            "error": "Invalid",
            "success": False,
            "code": 400
        }
        mock_result_connection.return_value = mock_data, namespace
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA

        search_results_response = transmission.results(query_response['search_id'], 0, 9)
        
        assert 'success' in search_results_response
        assert search_results_response['success'] is False
        assert 'code' in search_results_response, search_results_response['code'] == 'invalid_query'
    
    def test_threat_q_status(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.status(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is True
        assert 'status' in query_response, query_response['status'] == 'COMPLETED'
        assert 'progress' in query_response, query_response['progress'] == 100
    
    @patch('stix_shifter_utils.modules.base.stix_transmission.base_sync_connector.BaseSyncConnector.create_status_connection', autospec=True)
    def test_threat_q_status_exception(self, mock_status_response, mock_api_client):
        error_msg = 'an error occured while checking the status'
        mock_api_client.return_value = None
        mock_status_response.return_value = {'status':'FAILED', 'success':False}
        mock_status_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.status(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    @patch('stix_shifter_utils.modules.base.stix_transmission.base_sync_connector.BaseSyncConnector.create_query_connection', autospec=True)
    def test_threat_q_query_exception(self, mock_query_response, mock_api_client):
        error_msg = 'cannot create a query connection'
        mock_api_client.return_value = None
        mock_query_response.return_value = {'search_id':'', 'success':False}
        mock_query_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg
    
    def test_threat_q_is_async_query(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission("abc",  connection, config)
        is_async_result = transmission.is_async()
        assert 'success' in is_async_result
        assert is_async_result['success'] is False
        assert 'code' in is_async_result, is_async_result['code'] == 'unknown'

    @patch('stix_shifter_utils.utils.base_entry_point.BaseEntryPoint.is_async', autospec=True)
    def test_threat_q_is_async_query_exception(self, mock_async_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is async'
        mock_api_client.return_value = None
        mock_async_response.return_value = False
        mock_async_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.is_async()
        assert query_response is not None
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg

    def test_delete_query(self, mock_api_client):
        mock_api_client.return_value = None
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete(SAMPLE_DATA)
        assert query_response is not None
        assert 'success' in query_response
        assert query_response['success'] is True
    
    @patch('stix_shifter_utils.utils.base_entry_point.BaseEntryPoint.delete_query_connection', autospec=True)
    def test_delete_query_exception(self, mock_delete_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_api_client.return_value = None
        mock_delete_response.return_value = False
        mock_delete_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete("")
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg 

def test_ping_threat_q():
    transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
    ping_response = transmission.ping()

    assert 'success' in ping_response
    assert 'connector' in ping_response
    assert 'code' in ping_response
    assert ping_response['success'] is False
    assert ping_response['connector'] is 'threat_q'
