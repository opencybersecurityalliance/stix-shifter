import json
import os
import unittest
from unittest.mock import Mock, patch

from requests import Response
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.stix_transmission.utils.RestApiClientAsync import ResponseWrapper
from tests.utils.async_utils import get_mock_response
from stix_shifter_modules.crowdstrike.entry_point import EntryPoint
from stix_shifter.stix_transmission.stix_transmission import run_in_thread


config = {
        "auth": {
            "client_id": "bla",
            "client_secret": "bla"
        }
    }

connection = {
    'host': 'api.crowdstrike.com',
    "options":
    {
        "batch_size":1000,
        "result_limit":1000
    }
}

connection_batchsize_10 = {
    'host': 'api.crowdstrike.com',
    "options":
    {
        "batch_size":10,
        "result_limit":1000
    }
}

headers = {'Content-Type': 'application/json'}
class TestCrowdStrikeConnection(unittest.TestCase, object):

    @staticmethod
    def _get_sample_response(sample_response_filename):    
        if os.path.exists(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_transmission/sample_responses/" + sample_response_filename):
            with open(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_transmission/sample_responses/" + sample_response_filename, "r", encoding='utf-8') as file:
                return file.read()

    def _create_response_object(content_filepath, response_code, content_type_header):
        response = ResponseWrapper(Response())
        response_text = TestCrowdStrikeConnection._get_sample_response(content_filepath)
        response.code = response_code
        response.content = bytes(response_text, 'utf-8')
        
        headers = dict()
        headers['Content-Type'] = content_type_header
        response.headers = headers
        
        return response
            
    def _get_ping_results():
        transmission = stix_transmission.StixTransmission('crowdstrike_alerts', connection, config)
        return transmission.ping()
    
    def _get_results():
        transmission = stix_transmission.StixTransmission('crowdstrike_alerts', connection, config)
        return transmission.results("test", 0, 100, None)
    
    def _get_results_10_batchsize():
        transmission = stix_transmission.StixTransmission('crowdstrike_alerts', connection_batchsize_10, config)
        return transmission.results("test", 0, 100, None)
    
    def _get_results_10_offset_1_length_10():
        transmission = stix_transmission.StixTransmission('crowdstrike_alerts', connection, config)
        return transmission.results("test", 1, 10, None)

    @staticmethod
    def test_ping_datasource_success():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            ping_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_200.json", 200, "application/json")
            
            rest_api_mock.side_effect = [authentication_response, ping_response]
            results = TestCrowdStrikeConnection._get_ping_results()
            assert results["success"]
            
    @staticmethod
    def test_ping_datasource_403():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_403.json", 403, "application/json")
                        
            rest_api_mock.side_effect = [authentication_response]
            results = TestCrowdStrikeConnection._get_ping_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => Failed to issue access token - Client authentication failed (e.g., unknown client, no client authentication included, or unsupported authentication method)'
            assert results["code"] == 'authentication_fail'
            
    @staticmethod
    def test_ping_datasource_406():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_406.json", 406, "application/json")
                        
            rest_api_mock.side_effect = [authentication_response]
            results = TestCrowdStrikeConnection._get_ping_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => 406: Not Acceptable\n\nAvailable representations: '
            assert results["code"] == 'unknown'
            
    @staticmethod
    def test_ping_datasource_415():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_415.json", 415, "application/json")
                        
            rest_api_mock.side_effect = [authentication_response]
            results = TestCrowdStrikeConnection._get_ping_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => 415: Unsupported Media Type'
            assert results["code"] == 'unknown'
            
    @staticmethod
    def test_ping_datasource_results_fails():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_400_invalid_filter.json", 400, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response]
            results = TestCrowdStrikeConnection._get_ping_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => invalid query filter in request'
            assert results["code"] == 'invalid_query'
            
    @staticmethod
    def test_successful_request():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_200.json", 200, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_200.json", 200, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert results["success"]
            assert results["metadata"] == None
            assert len(results["data"]) == 58
    
    @staticmethod
    def test_get_ids_invalid_filter():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_400_invalid_filter.json", 400, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_200.json", 200, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => invalid query filter in request'
            assert results["code"] == 'invalid_query'
            
    @staticmethod
    def test_get_ids_invalid_limit():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_400_invalid_limit.json", 400, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_200.json", 200, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => limit must be greater than 1 and less than 10000'
            assert results["code"] == 'invalid_query'

    @staticmethod
    def test_get_ids_401():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_401.json", 401, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_200.json", 200, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => access denied, invalid bearer token'
            assert results["code"] == 'authentication_fail'
            
    @staticmethod
    def test_get_ids_403():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_403_invalid_roles.json", 403, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_200.json", 200, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => access denied, authorization failed'
            assert results["code"] == 'authentication_fail'
            
    @staticmethod
    def test_get_ids_500():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_500_invalid_offset.json", 500, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_200.json", 200, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert not results["success"]
            assert results["error"] == "crowdstrike_alerts connector error => Internal Server Error: Please provide trace-id='9e24dfb7-4ccb-44ed-838b-d3699a5d2fab' to support"
            assert results["code"] == 'unknown'
            
    @staticmethod
    def test_get_detection_400_invalid_CID():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_200.json", 200, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_400_invalid_CID.json", 400, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => invalid CID provided'
            assert results["code"] == 'invalid_query'
            
    @staticmethod
    def test_get_detection_400_invalid_offset():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_200.json", 200, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_400_invalid_json.json", 400, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => failed to read and parse request'
            assert results["code"] == 'invalid_query'
            
    @staticmethod
    def test_get_detection_401_invalid_auth():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_200.json", 200, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_401_invalid_auth.json", 401, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => access denied, invalid bearer token'
            assert results["code"] == 'authentication_fail'
            
    @staticmethod
    def test_get_ids_413_invalid_request():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_200.json", 200, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_413_invalid_request.json", 413, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => request too large'
            assert results["code"] == 'unknown'
            
    @staticmethod
    def test_content_type_html():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 500, "text/html")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_200.json", 200, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_200.json", 200, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert not results["success"]
            assert results["code"] == 'service_unavailable'
            
    @staticmethod
    def test_content_type_unknown():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 500, "content_type")
            authentication_response.content = "unexpected error."
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_200.json", 200, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_200.json", 200, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results()
            
            assert not results["success"]
            assert results["error"] == 'crowdstrike_alerts connector error => unexpected error.'
            assert results["code"] == 'unknown'
            
    @staticmethod
    def test_successful_batch_10():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_200.json", 200, "application/json")
            get_detections_response_batch_1 = TestCrowdStrikeConnection._create_response_object("sample_get_detection_200_10_results.json", 200, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response_batch_1, get_detections_response_batch_1, get_detections_response_batch_1,get_detections_response_batch_1, get_detections_response_batch_1, get_detections_response_batch_1,get_detections_response_batch_1,get_detections_response_batch_1]
            results = TestCrowdStrikeConnection._get_results_10_batchsize()
            
            assert results["success"]
            assert results["metadata"] == None
            assert len(results["data"]) == 80
            
    @staticmethod
    def test_successful_result_limit_10():
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as rest_api_mock:
            authentication_response = TestCrowdStrikeConnection._create_response_object("sample_authentication_200.json", 200, "application/json")
            get_ids_response = TestCrowdStrikeConnection._create_response_object("sample_get_ids_200.json", 200, "application/json")
            get_detections_response = TestCrowdStrikeConnection._create_response_object("sample_get_detection_200_10_results.json", 200, "application/json")

            rest_api_mock.side_effect = [authentication_response, get_ids_response, get_detections_response]
            results = TestCrowdStrikeConnection._get_results_10_offset_1_length_10()
            
            assert results["success"]
            assert results["metadata"] == {'result_count': 0, 'offset': 11}
            assert len(results["data"]) == 10