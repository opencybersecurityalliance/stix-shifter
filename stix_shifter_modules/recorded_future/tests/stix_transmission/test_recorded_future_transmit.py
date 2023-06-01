
from stix_shifter.stix_transmission import stix_transmission
from unittest.mock import patch
import unittest
from collections import namedtuple
from types import SimpleNamespace

MODULE_NAME = "recorded_future"
SAMPLE_DATA = '{"data": "2.81.219.150", "dataType": "ip"}'
namespace = '8af42ea1-e30d-41a2-a3ee-1aec759cf789'
DATA = {
    "code": 200,
    "data": {
        "success": True,
        "full": {
            "data": {
                "intelCard": "https://app.recordedfuture.com/live/sc/entity/ip%3A2.81.219.150",
                "timestamps": {
                    "firstSeen": "2019-03-26T16:58:58.989Z"
                },
                "risk": {
                    "criticalityLabel": "Suspicious",
                    "riskString": "5/54",
                    "rules": 5,
                    "criticality": 2,
                    "riskSummary": "5 of 54 Risk Rules currently observed.",
                    "score": 32,
                    "evidenceDetails": [
                        {
                            "mitigationString": "",
                            "evidenceString": "3 sightings on 2 sources: @InternetBadness, @sdpcthreatintel. Most recent tweet: 2.81.219.150 attempted MYSQL exploitation 2 time(s), DShield attacks: 1, Country: PT. Most recent link (Jul 17, 2021): https://twitter.com/sdpcthreatintel/statuses/1416444108772581381",
                            "rule": "Historical Honeypot Sighting",
                            "criticality": 1,
                            "timestamp": "2021-07-17T17:06:06.000Z",
                            "criticalityLabel": "Unusual"
                        },
                    ]
                },
                "metrics": [
                    {
                        "type": "unusualIPSightings",
                        "value": 1
                    },
                    {
                        "type": "technicalReportingHits",
                        "value": 194
                    }
                ]
            }
        }
    },
    "data": "2.81.219.150",
    "dataType": "ip"
}

connection = {
    "namespace":namespace
}
config = {
    "auth": {
        "key": "testingKey"
    }
}
Response = namedtuple('Response', ['data', 'response_code'])
ResponseResult = namedtuple('ResponseResult', ['data', 'namespace'])
class MockHttpResponse:
    def __init__(self, string):
        self.string = string


@patch('stix_shifter_modules.recorded_future.stix_transmission.api_client.APIClient.__init__', autospec=True)
class TestRecordedFutureConnection(unittest.TestCase, object):

    @patch('stix_shifter_modules.recorded_future.stix_transmission.api_client.APIClient.ping_recorded_future')
    def test_recoded_future_ping(self, mock_ping_response, mock_api_client):
        mock_api_client.return_value = None
        DATA = {'success': True}
        mock_ping_response.return_value = ResponseResult(DATA, 200)

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_modules.recorded_future.stix_transmission.api_client.APIClient.ping_recorded_future')
    def test_recoded_future_ping_error(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value =  {"success":True, "code": 404}
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.recorded_future.stix_transmission.api_client.APIClient.ping_recorded_future')
    def test_recoded_future_ping_exception(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value =  {"success":True, "code": 404}
        mock_ping_response.side_effect = Exception('a mock-exception occured retriving ping information')
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.recorded_future.stix_transmission.api_client.APIClient.ping_recorded_future')
    def test_recoded_future_ping_exception2(self, mock_ping_response, mock_api_client):
        response =  MockHttpResponse('/exception')
        mock_api_client.return_value = None
        mock_ping_response.return_value =  {"success":False}
        mock_ping_response.side_effect = Exception('an mock-exception-2 occured retriving ping information')
 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False

    @patch('stix_shifter_modules.recorded_future.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_recoded_future_results(self, mock_result_connection, mock_api_client):

        mock_api_client.return_value = None
        mock_result_connection.return_value = DATA.copy(), namespace

        transmission = stix_transmission.StixTransmission(
            MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA

        search_results_response = transmission.results(
            query_response['search_id'], 0, 9)
        report = search_results_response['data'][0]
        assert 'data' in report
        assert 'dataType' in report
        assert 'success' in search_results_response
        assert search_results_response['success'] is True
        assert type(search_results_response['data']) is list

    @patch('stix_shifter_modules.recorded_future.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_recoded_future_results_error(self, mock_result_connection, mock_api_client):
        mock_api_client.return_value = None
        mock_data = DATA = {
            "error": "Invalid",
            "success": False,
            "code": 400
        }
        mock_result_connection.return_value = mock_data, namespace
        mock_result_connection.side_effect = Exception('an mock exception occured invalid query')
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.query(SAMPLE_DATA)

        assert query_response is not None
        assert 'search_id' in query_response
        assert query_response['search_id'] == SAMPLE_DATA

        search_results_response = transmission.results(query_response['search_id'], 0, 9)
        assert 'success' in search_results_response
        assert search_results_response['success'] is False
        assert 'code' in search_results_response, search_results_response['code'] == 'invalid_query'

    @patch('stix_shifter_modules.recorded_future.stix_transmission.api_client.APIClient.get_search_results', autospec=True)
    def test_recoded_future_results_error_code(self, mock_result_connection, mock_api_client):
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

    @patch('stix_shifter_modules.recorded_future.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    def test_delete_query(self, mock_delete_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_api_client.return_value = None
        mock_delete_response.return_value = {"code": 200, "success": True} 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete(SAMPLE_DATA)
        assert 'success' in query_response, query_response['success'] is True

    @patch('stix_shifter_modules.recorded_future.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    def test_delete_query_error(self, mock_delete_response, mock_api_client):
        error_msg = 'an error occured while checking the if the query is deleted'
        mock_api_client.return_value =  None 
        mock_delete_response.return_value =  {"code": 404, "success": False} 
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete(SAMPLE_DATA)
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg

    @patch('stix_shifter_modules.recorded_future.stix_transmission.api_client.APIClient.delete_search', autospec=True)
    def test_delete_query_exception(self, mock_delete_response, mock_api_client):
        error_msg = 'an mock-exception occured while checking the if the query is deleted'
        mock_api_client.return_value = None
        mock_delete_response.return_value = False
        mock_delete_response.side_effect = Exception(error_msg)
        transmission = stix_transmission.StixTransmission(MODULE_NAME,  connection, config)
        query_response = transmission.delete("")
        assert 'success' in query_response, query_response['success'] is False
        assert 'error' in query_response, query_response['error'] == error_msg