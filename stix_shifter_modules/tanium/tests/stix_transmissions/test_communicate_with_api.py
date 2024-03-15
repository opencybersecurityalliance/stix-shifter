import json
from stix_shifter_utils.utils.error_response import ErrorCode
from stix_shifter.stix_transmission import stix_transmission
import unittest
from unittest.mock import patch

SAMPLE_DATA_DICT = {
    "data":[{
        "id": 2,
        "eid": 1003,
        "state": "unresolved",
        "type": "detect.match",
        "guid": "00000000-0000-0000-114a-7429237cffc5",
        "priority": "high",
        "severity": "info",
        "details": "{\"match\":{\"hash\":\"17914125682699366401\",\"type\":\"process\",\"source\":\"recorder\",\"version\":1,\"contexts\":[{\"file\":{\"uniqueEventId\":\"4611686018427965350\"},\"event\":{\"fileMove\":{\"srcPath\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\ded2b98d-52fb-4b4a-832e-d09664b8099a.tmp\",\"destPath\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\eicar_com (2).zip.crdownload\"},\"timestampMs\":\"1697459178054\"}}],\"properties\":{\"pid\":9080,\"args\":\"\\\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\\\" --no-startup-window --continue-active-setup\",\"file\":{\"md5\":\"d193ea4b8d102d020c02dc45af23ff0d\",\"sha1\":\"469e259b884043aedac879a96356fb741f82daa8\",\"sha256\":\"9ba39dd15eff718ff357db346d0fda3a12c9dbb216511cbb41050fb0d6b3d9c9\",\"fullpath\":\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\"},\"name\":\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\",\"user\":\"hostname\\\\sample\",\"start_time\":\"2023-10-13T14:46:31.000Z\",\"recorder_unique_id\":\"3994044258139188996\"}},\"finding\":{\"whats\":[{\"source_name\":\"recorder\",\"intel_intra_ids\":[{\"id_v2\":\"901388892329936882\"}],\"artifact_activity\":{\"acting_artifact\":{\"process\":{\"pid\":9080,\"file\":{\"file\":{\"hash\":{\"md5\":\"d193ea4b8d102d020c02dc45af23ff0d\",\"sha1\":\"469e259b884043aedac879a96356fb741f82daa8\",\"sha256\":\"9ba39dd15eff718ff357db346d0fda3a12c9dbb216511cbb41050fb0d6b3d9c9\"},\"path\":\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\",\"signature_data\":{\"issuer\":\"Microsoft Code Signing PCA 2011\",\"status\":1,\"subject\":\"Microsoft Corporation\"}},\"artifact_hash\":\"15257803663505479322\",\"instance_hash\":\"15257803663505479322\"},\"user\":{\"user\":{\"name\":\"sample\",\"domain\":\"EndpointDevice-\",\"user_id\":\"1111\"}},\"handles\":[],\"arguments\":\"\\\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\\\" --no-startup-window --continue-active-setup\",\"start_time\":\"2023-10-13T14:46:31.000Z\",\"tanium_unique_id\":\"3994044258139188996\"},\"artifact_hash\":\"17914125682699366401\",\"instance_hash\":\"8890920941823507809\",\"is_intel_target\":true},\"relevant_actions\":[{\"verb\":7,\"origin\":{\"file\":{\"path\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\ded2b98d-52fb-4b4a-832e-d09664b8099a.tmp\"},\"artifact_hash\":\"642322984173040938\",\"instance_hash\":\"642322984173040938\"},\"target\":{\"file\":{\"path\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\eicar_com (2).zip.crdownload\"},\"artifact_hash\":\"11534804092509109490\",\"instance_hash\":\"11534804092509109490\"},\"timestamp\":\"2023-10-16T12:26:18.000Z\",\"tanium_recorder_context\":{\"file\":{\"unique_event_id\":\"4611686018427965350\"},\"event\":{\"file_move\":{\"src_path\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\ded2b98d-52fb-4b4a-832e-d09664b8099a.tmp\",\"dest_path\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\eicar_com (2).zip.crdownload\"},\"timestamp_ms\":\"1697459178054\"}},\"tanium_recorder_event_table_id\":\"4611686018427965350\"}]}}],\"domain\":\"threatresponse\",\"hunt_id\":\"2\",\"intel_id\":\"700:1:8ebe28bf-1acb-41b7-9f30-7b40a9145b1d\",\"last_seen\":\"2023-10-16T12:26:51.000Z\",\"threat_id\":\"901388892329936882\",\"finding_id\":\"1245935966959239109\",\"first_seen\":\"2023-10-16T12:26:51.000Z\",\"source_name\":\"recorder\",\"system_info\":{\"os\":\"Microsoft Windows 11 Pro\",\"bits\":64,\"platform\":\"Windows\",\"patch_level\":\"10.0.22621.0.0\",\"build_number\":\"22621\"},\"reporting_id\":\"reporting-id-placeholder\"},\"intel_id\":700,\"config_id\":2,\"config_rev_id\":1}",
        "intelDocId": 700,
        "groupingId": 2,
        "intelDocRevisionId": 1,
        "scanConfigId": 2,
        "scanConfigRevisionId": 1,
        "computerName": "Hostname",
        "computerIpAddress": "0.0.0.0",
        "matchType": "process",
        "path": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
        "receivedAt": "2023-10-16T12:29:34.609Z",
        "suppressedAt": None,
        "alertedAt": "2023-10-16T12:26:51.000Z",
        "findingId": "1245935966959239109",
        "ackedAt": "2023-10-16T12:38:03.961Z",
        "firstEIDResolutionAttempt": "2023-10-16T12:29:37.091Z",
        "lastEIDResolutionAttempt": "2023-10-16T12:29:37.091Z",
        "createdAt": "2023-10-16T12:29:34.849Z",
        "updatedAt": "2023-10-16T12:38:03.968Z"
        },
        {
            "id": 2,
            "eid": 1003,
            "state": "unresolved",
            "type": "detect.match",
            "guid": "00000000-0000-0000-114a-7429237cffc5",
            "priority": "high",
            "severity": "info",
            "details": "{\"match\":{\"hash\":\"17914125682699366401\",\"type\":\"process\",\"source\":\"recorder\",\"version\":1,\"contexts\":[{\"file\":{\"uniqueEventId\":\"4611686018427965350\"},\"event\":{\"fileMove\":{\"srcPath\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\ded2b98d-52fb-4b4a-832e-d09664b8099a.tmp\",\"destPath\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\eicar_com (2).zip.crdownload\"},\"timestampMs\":\"1697459178054\"}}],\"properties\":{\"pid\":9080,\"args\":\"\\\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\\\" --no-startup-window --continue-active-setup\",\"file\":{\"md5\":\"d193ea4b8d102d020c02dc45af23ff0d\",\"sha1\":\"469e259b884043aedac879a96356fb741f82daa8\",\"sha256\":\"9ba39dd15eff718ff357db346d0fda3a12c9dbb216511cbb41050fb0d6b3d9c9\",\"fullpath\":\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\"},\"name\":\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\",\"user\":\"hostname\\\\sample\",\"start_time\":\"2023-10-13T14:46:31.000Z\",\"recorder_unique_id\":\"3994044258139188996\"}},\"finding\":{\"whats\":[{\"source_name\":\"recorder\",\"intel_intra_ids\":[{\"id_v2\":\"901388892329936882\"}],\"artifact_activity\":{\"acting_artifact\":{\"process\":{\"pid\":9080,\"file\":{\"file\":{\"hash\":{\"md5\":\"d193ea4b8d102d020c02dc45af23ff0d\",\"sha1\":\"469e259b884043aedac879a96356fb741f82daa8\",\"sha256\":\"9ba39dd15eff718ff357db346d0fda3a12c9dbb216511cbb41050fb0d6b3d9c9\"},\"path\":\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\",\"signature_data\":{\"issuer\":\"Microsoft Code Signing PCA 2011\",\"status\":1,\"subject\":\"Microsoft Corporation\"}},\"artifact_hash\":\"15257803663505479322\",\"instance_hash\":\"15257803663505479322\"},\"user\":{\"user\":{\"name\":\"sample\",\"domain\":\"EndpointDevice-\",\"user_id\":\"1111\"}},\"handles\":[],\"arguments\":\"\\\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\\\" --no-startup-window --continue-active-setup\",\"start_time\":\"2023-10-13T14:46:31.000Z\",\"tanium_unique_id\":\"3994044258139188996\"},\"artifact_hash\":\"17914125682699366401\",\"instance_hash\":\"8890920941823507809\",\"is_intel_target\":true},\"relevant_actions\":[{\"verb\":7,\"origin\":{\"file\":{\"path\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\ded2b98d-52fb-4b4a-832e-d09664b8099a.tmp\"},\"artifact_hash\":\"642322984173040938\",\"instance_hash\":\"642322984173040938\"},\"target\":{\"file\":{\"path\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\eicar_com (2).zip.crdownload\"},\"artifact_hash\":\"11534804092509109490\",\"instance_hash\":\"11534804092509109490\"},\"timestamp\":\"2023-10-16T12:26:18.000Z\",\"tanium_recorder_context\":{\"file\":{\"unique_event_id\":\"4611686018427965350\"},\"event\":{\"file_move\":{\"src_path\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\ded2b98d-52fb-4b4a-832e-d09664b8099a.tmp\",\"dest_path\":\"C:\\\\Users\\\\sample\\\\Downloads\\\\eicar_com (2).zip.crdownload\"},\"timestamp_ms\":\"1697459178054\"}},\"tanium_recorder_event_table_id\":\"4611686018427965350\"}]}}],\"domain\":\"threatresponse\",\"hunt_id\":\"2\",\"intel_id\":\"700:1:8ebe28bf-1acb-41b7-9f30-7b40a9145b1d\",\"last_seen\":\"2023-10-16T12:26:51.000Z\",\"threat_id\":\"901388892329936882\",\"finding_id\":\"1245935966959239109\",\"first_seen\":\"2023-10-16T12:26:51.000Z\",\"source_name\":\"recorder\",\"system_info\":{\"os\":\"Microsoft Windows 11 Pro\",\"bits\":64,\"platform\":\"Windows\",\"patch_level\":\"10.0.22621.0.0\",\"build_number\":\"22621\"},\"reporting_id\":\"reporting-id-placeholder\"},\"intel_id\":700,\"config_id\":2,\"config_rev_id\":1}",
            "intelDocId": 700,
            "groupingId": 2,
            "intelDocRevisionId": 1,
            "scanConfigId": 2,
            "scanConfigRevisionId": 1,
            "computerName": "Hostname",
            "computerIpAddress": "0.0.0.0",
            "matchType": "process",
            "path": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
            "receivedAt": "2023-10-16T12:29:34.609Z",
            "suppressedAt": None,
            "alertedAt": "2023-10-16T12:26:51.000Z",
            "findingId": "1245935966959239109",
            "ackedAt": "2023-10-16T12:38:03.961Z",
            "firstEIDResolutionAttempt": "2023-10-16T12:29:37.091Z",
            "lastEIDResolutionAttempt": "2023-10-16T12:29:37.091Z",
            "createdAt": "2023-10-16T12:29:34.849Z",
            "updatedAt": "2023-10-16T12:38:03.968Z"
        }]
}
SAMPLE_DATA_STRING = json.dumps(SAMPLE_DATA_DICT)

EXCEPTION_401_MESSAGE = "User is not authorized to access this resource with an explicit deny"
EXCEPTION_404_MESSAGE = "/api/v1/tyryt does not exist"

#Cannot be recreated in a real environment. The Message does not reflect a real environment. Some of these may not actually occur in the real environment.
EXCEPTION_403_MESSAGE = "Provided token does not have permission to access the endpoint."
EXCEPTION_500_501_502_503_504_MESSAGE = "The server may not be available."
EXCEPTION_400_404_405_411_MESSAGE = "The request failed to resolve correctly. There is an issue with the endpoint or query."
EXCEPTION_429_MESSAGE = "Too many request were made to the API"
                
EXCEPTION_401_FORMAT = {"Message":"errorMessage"}
EXCEPTION_404_FORMAT = {"errors": [{"code":"errortitle","description":"errordescription"}]}


CONNECTION= {
        "host": "sanatized",
        "port": 443
    }


CONFIG = {
        "auth":
        {
            "accessToken": "sanatized"
        }
    }

class TestTaniumTransmission(unittest.TestCase, object):
    def test_ping_endpoint(self):
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as mock_get:
            test_results = list()
            for i in range(100):
                obj = lambda: None
                obj.content = SAMPLE_DATA_STRING.encode("utf-8")
                obj.code = 200
                test_results.append(obj)
            mock_get.side_effect = test_results
            
            transmission = stix_transmission.StixTransmission('tanium', CONNECTION, CONFIG)
            ping_response = transmission.ping()

            assert ping_response is not None
            assert ping_response['success']
    
    def test_ping_endpoint_connect_failure(self):
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as mock_get:
            mock_get.side_effect = Exception('client_connector_error: Cannot connect to host hostname:443 ssl:True [nodename nor servname provided, or not known]')

            transmission = stix_transmission.StixTransmission('tanium', CONNECTION, CONFIG)
            ping_response = transmission.ping()

            assert ping_response is not None
            assert "service_unavailable" in ping_response["code"]
            assert "Cannot connect" in ping_response["error"] 
            assert not ping_response['success']
    
    
    def test_results_connection(self):
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as mock_get:
            test_results = list()
            for i in range(100):
                obj = lambda: None
                obj.content = SAMPLE_DATA_STRING.encode("utf-8")
                obj.code = 200
                test_results.append(obj)
            
            mock_get.side_effect = test_results
            
            transmission = stix_transmission.StixTransmission('tanium', CONNECTION, CONFIG)
            create_results_connection = transmission.results("computerIpAddress=10.0.0.4", 0, 50)
            
            temp_details = SAMPLE_DATA_DICT["data"][0]["details"]
            SAMPLE_DATA_DICT["data"][0]["details"] = create_results_connection["data"][0]["details"]
            assert create_results_connection is not None
            assert create_results_connection["data"][0] == SAMPLE_DATA_DICT["data"][0]
            assert isinstance(create_results_connection["data"][0]["details"], dict)
            assert create_results_connection['success']
            SAMPLE_DATA_DICT["data"][0]["details"] = create_results_connection["data"][0]["details"] = temp_details

    
    def test_results_connection_bad_host(self):
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as mock_get:
            mock_get.side_effect = Exception('client_connector_error: Cannot connect to host hostname:443 ssl:True [nodename nor servname provided, or not known]')
            
            transmission = stix_transmission.StixTransmission('tanium', CONNECTION, CONFIG)
            create_results_connection = transmission.results("computerIpAddress=10.0.0.4", 0, 50)
            assert create_results_connection is not None
            assert "service_unavailable" in create_results_connection["code"]
            assert "Cannot connect" in create_results_connection["error"] 
            assert not create_results_connection['success']
        
    def test_results_connection_bad_port(self):
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as mock_get:
            mock_get.side_effect = Exception('server timeout_error (2 sec)')
            
            transmission = stix_transmission.StixTransmission('tanium', CONNECTION, CONFIG)
            create_results_connection = transmission.results("computerIpAddress=10.0.0.4", 0, 50)
            assert create_results_connection is not None
            assert "service_unavailable" in create_results_connection["code"]
            assert "server timeout" in create_results_connection["error"] 
            assert not create_results_connection['success']
    
    def test_results_connection_error_auth(self):
        self.helper_401_format_exception(401, EXCEPTION_401_MESSAGE, ErrorCode.TRANSMISSION_AUTH_CREDENTIALS.value)
        self.helper_401_format_exception(407, EXCEPTION_401_MESSAGE, ErrorCode.TRANSMISSION_AUTH_CREDENTIALS.value)

    def test_results_connection_error_forbidden(self):
        self.helper_401_format_exception(403, EXCEPTION_403_MESSAGE, ErrorCode.TRANSMISSION_FORBIDDEN.value)
    
    def test_results_connection_connect_fail(self):
        self.helper_401_format_exception(500, EXCEPTION_500_501_502_503_504_MESSAGE, ErrorCode.TRANSMISSION_CONNECT.value)
        self.helper_401_format_exception(501, EXCEPTION_500_501_502_503_504_MESSAGE, ErrorCode.TRANSMISSION_CONNECT.value)
        self.helper_401_format_exception(502, EXCEPTION_500_501_502_503_504_MESSAGE, ErrorCode.TRANSMISSION_CONNECT.value)
        self.helper_401_format_exception(503, EXCEPTION_500_501_502_503_504_MESSAGE, ErrorCode.TRANSMISSION_CONNECT.value)
        self.helper_401_format_exception(504, EXCEPTION_500_501_502_503_504_MESSAGE, ErrorCode.TRANSMISSION_CONNECT.value)

    def test_results_connection_error_query(self):
        self.helper_404_format_exception(400, EXCEPTION_400_404_405_411_MESSAGE, ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR.value)
        self.helper_404_format_exception(404, EXCEPTION_400_404_405_411_MESSAGE, ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR.value)
        self.helper_404_format_exception(405, EXCEPTION_400_404_405_411_MESSAGE, ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR.value)
        self.helper_404_format_exception(411, EXCEPTION_400_404_405_411_MESSAGE, ErrorCode.TRANSMISSION_QUERY_LOGICAL_ERROR.value)
        
    def test_results_connection_error_to_many_request(self):
        self.helper_404_format_exception(429, EXCEPTION_429_MESSAGE, ErrorCode.TRANSMISSION_TOO_MANY_REQUESTS.value)
    
    def helper_401_format_exception(self, code, message, expected_code):
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as mock_get:
            obj = lambda: None
            obj.content = json.dumps(self.create_exception_response(EXCEPTION_401_FORMAT, message)).encode("utf-8")
            obj.code = code
            mock_get.return_value = obj
            
            transmission = stix_transmission.StixTransmission('tanium', CONNECTION, CONFIG)
            create_results_connection = transmission.results("type=444", 0, 50)
            
            assert create_results_connection is not None
            assert message in create_results_connection["error"]
            assert expected_code in create_results_connection["code"]
            assert not create_results_connection['success']
            
    def helper_404_format_exception(self, code, message, expected_code):
        with patch("stix_shifter_utils.stix_transmission.utils.RestApiClientAsync.RestApiClientAsync.call_api") as mock_get:
            obj = lambda: None
            obj.content = json.dumps(self.create_exception_response(EXCEPTION_404_FORMAT, message)).encode("utf-8")
            obj.code = code
            mock_get.return_value = obj
            
            transmission = stix_transmission.StixTransmission('tanium', CONNECTION, CONFIG)
            create_results_connection = transmission.results("type=444", 0, 50)
            
            assert create_results_connection is not None
            assert message in create_results_connection["error"]
            assert expected_code in create_results_connection["code"]
            assert not create_results_connection['success']
            
    def create_exception_response(self, format, message):
        if("Message" in format):
            format["Message"] = message
        elif("errors" in format):
            format["errors"][0]["description"] = message
        return format