from stix_shifter_modules.gcp_chronicle.entry_point import EntryPoint
import unittest
from unittest.mock import patch
from stix_shifter.stix_transmission import stix_transmission
import json
from aiogoogle.excs import HTTPError
from aiohttp.client_exceptions import ClientConnectionError
from asyncio.exceptions import TimeoutError


class MockCodeResponse:
    def __init__(self, code, content={}):
        self.status_code = code
        self.content = content


@patch('aiogoogle.client.Aiogoogle.as_service_account')
class TestGCPChronicleConnection(unittest.TestCase, object):

    @staticmethod
    def connection():
        return {
            "host": "hostbla"
        }

    @staticmethod
    def configuration():
        return {
            "auth": {
                "client_email": "hostbla",
                "private_key": "privatebla"
            }
        }

    @patch('stix_shifter_modules.gcp_chronicle.stix_transmission.api_client.APIClient.__init__')
    def test_is_async(self, mock_api, *args):
        mock_api.return_value = None
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async

    def test_ping(self, mock_http):
        """test ping connection"""
        mock_http.return_value = MockCodeResponse(200, {"rules": [{"ruleId": "ru_123abcd"}]})
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is True

    def test_transmit_query(self, mock_http):
        """test query connection"""
        query = json.dumps({
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        })
        mocked_create_rule = MockCodeResponse(200, {"ruleId": "ru_1234"})

        mock_query_output_response = {"retrohuntId": "oh_1234", "ruleId": "ru_1234", "versionId": "ru_1234",
                                      "eventStartTime": "2022-06-28T00:00:00.030Z",
                                      "eventEndTime": "2022-06-29T00:00:00.030Z",
                                      "retrohuntStartTime": "2022-07-07T06:43:40.983372Z",
                                      "state": "RUNNING"}

        mocked_create_search = MockCodeResponse(200, mock_query_output_response)

        mock_http.side_effect = [mocked_create_rule, mocked_create_search]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is True
        assert query_response['search_id'] == "oh_1234:ru_1234"

    def test_status_response(self, mock_http):
        """test status response """
        search_id = "oh_1234:ru_1234"
        mock_status_output = {"retrohuntId": "oh_1234", "ruleId": "ru_1234", "versionId": "ru_1234",
                              "eventStartTime": "2022-06-28T00:00:00.030Z",
                              "eventEndTime": "2022-06-29T00:00:00.030Z",
                              "retrohuntStartTime": "2022-07-07T06:43:40.983372Z",
                              "retrohuntEndTime": "2022-07-07T06:43:58.750611Z", "state": "DONE",
                              "progressPercentage": 100}
        mock_http.return_value = MockCodeResponse(200, mock_status_output)
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is True
        assert status_response['progress'] == 100
        assert status_response['status'] == "COMPLETED"

    def test_result_with_metadata_in_response(self, mock_http):
        """test result response connection"""
        search_id = "oh_1234:ru_1234"
        output = {
            "detections":
                [{
                    "type": "RULE_DETECTION",
                    "detection": [{
                        "ruleName": "rule_1657020065",
                        "urlBackToProduct": "url",
                        "ruleId": "ru_1234",
                        "ruleVersion": "ru_1234",
                        "alertState": "NOT_ALERTING",
                        "ruleType": "SINGLE_EVENT",
                        "ruleLabels": [{
                            "key": "author",
                            "value": "ibm cp4s user"
                        }, {
                            "key": "description",
                            "value": "Create event rule that should generate detections"
                        }]
                    }],
                    "createdTime": "2022-07-07T08:01:24.869956Z",
                    "id": "de_38c2972e-ec99-8c0c-4dbe-3b350294b2bb",
                    "timeWindow": {
                        "startTime": "2022-06-28T09:49:09.460001Z",
                        "endTime": "2022-06-28T09:49:09.460001Z"
                    },
                    "collectionElements": [{
                        "references": [{
                            "event": {
                                "metadata": {
                                    "productLogId": "823rb4e123k4"
                                },
                                "securityResult": [
                                    {
                                        "severity": "LOW"
                                    }
                                ],
                                "network": {
                                    "email": {
                                        "from": "010001818b271091-e32fa873-1a72-4d6f-8eab-29c09637402f-000000"
                                                "@amazonses.com",
                                        "mailId": "010001818b271091-e32fa873-1a72-4d6f-8eab-29c09637402f-000000@email"
                                                  ".amazonses.com",
                                        "subject": [
                                            "https://testurl.com test"
                                        ],
                                        "to": [
                                            "ravithummala@iscgalaxy.com"
                                        ]
                                    },
                                    "dns": {
                                        "authoritative": True,
                                        "questions": [{
                                            "name": "www.a2k2.in",
                                            "type": 1
                                        }],
                                        "responseCode": 3
                                    },
                                    "ipProtocol": "UDP"
                                },
                                "target": {
                                    "hostname": "v20.events.data.microsoft.com",
                                    "ip": [
                                        "13.89.178.26"
                                    ],
                                    "url": "v20.events.data.microsoft.com",
                                    "registry": {
                                        "registryKey": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Advanced "
                                                       "Threat Protection",
                                        "registryValueData": "132996043194369129",
                                        "registryValueName": "CrashHeartbeat"
                                    }
                                }

                            }
                        }],
                        "label": "udm"
                    }],
                    "detectionTime": "2022-06-28T09:49:09.460001Z"
                }],
            "nextPageToken": "12345"
        }
        mocked_result_response = MockCodeResponse(200, output)
        mocked_delete_response = MockCodeResponse(200)
        mock_http.side_effect = [mocked_result_response, mocked_delete_response]
        connection_with_result_limit = {
            "host": "hostbla",
            "options": {"result_limit": 3}
        }
        transmission = stix_transmission.StixTransmission('gcp_chronicle', connection_with_result_limit,
                                                          self.configuration())
        result_response = transmission.results(search_id, 0, 1)
        assert result_response is not None
        assert result_response['success'] is True
        assert result_response["data"][0]["event"]["metadata"]["productLogId"] == "823rb4e123k4"
        assert result_response["data"][0]["detection"]["ruleName"] == "rule_1657020065"
        assert result_response["data"][0]["event"]["network"]["email"]["isMultipart"] is False
        assert result_response["data"][0]["event"]["network"]["ipProtocol"] == "UDP"
        assert result_response["data"][0]["event"]["securityResult"][0]["severity"] == 48
        assert result_response["metadata"] == {'result_count': 1, 'next_page_token': '12345'}

    def test_delete_response(self, mock_http):
        """test delete response connection"""
        search_id = "oh_1234:ru_1234"
        mock_http.return_value = MockCodeResponse(200)
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        delete_response = transmission.delete(search_id)
        assert delete_response is not None
        assert delete_response['success'] is True

    def test_result_response_with_next_page_token(self, mock_http):
        """test result response connection having next page token"""
        search_id = "oh_1234:ru_1234"
        output_1 = {
            "detections":
                [{
                    "type": "RULE_DETECTION",
                    "detection": [{
                        "ruleName": "rule_1657020065"
                    }],
                    "createdTime": "2022-07-07T08:01:24.869956Z",
                    "id": "de_38c2972e-ec99-8c0c-4dbe-3b350294b2bb",
                    "timeWindow": {
                        "startTime": "2022-06-28T09:49:09.460001Z",
                        "endTime": "2022-06-28T09:49:09.460001Z"
                    },
                    "collectionElements": [{
                        "references": [{
                            "event": {
                                "metadata": {
                                    "productLogId": "823rb4e123k4"
                                }
                            }
                        }],
                        "label": "udm"
                    }],
                    "detectionTime": "2022-06-28T09:49:09.460001Z"
                }],
            "nextPageToken": "12345"
        }
        output_2 = {
            "detections":
                [{
                    "type": "RULE_DETECTION",
                    "detection": [{
                        "ruleName": "rule_1657032243"
                    }],
                    "createdTime": "2022-07-07T08:01:24.869956Z",
                    "id": "de_38c2972e-ec99-8c0c-4dbe-3b350294b2bb",
                    "timeWindow": {
                        "startTime": "2022-06-28T09:49:09.460001Z",
                        "endTime": "2022-06-28T09:49:09.460001Z"
                    },
                    "collectionElements": [{
                        "references": [{
                            "event": {
                                "metadata": {
                                    "productLogId": "2js34kn45b3n7"
                                }
                            }
                        }],
                        "label": "udm"
                    }],
                    "detectionTime": "2022-06-28T09:49:09.460001Z"
                }]
        }
        mocked_result_response_1 = MockCodeResponse(200, output_1)
        mocked_result_response_2 = MockCodeResponse(200, output_2)
        mocked_delete_response = MockCodeResponse(200)
        mock_http.side_effect = [mocked_result_response_1, mocked_result_response_2, mocked_delete_response]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        result_response = transmission.results(search_id, 0, 2)
        assert result_response is not None
        assert result_response['success'] is True
        assert result_response["data"][0]["event"]["metadata"]["productLogId"] == "823rb4e123k4"
        assert result_response["data"][0]["detection"]["ruleName"] == "rule_1657020065"
        assert result_response["data"][1]["event"]["metadata"]["productLogId"] == "2js34kn45b3n7"
        assert result_response["data"][1]["detection"]["ruleName"] == "rule_1657032243"

    def test_invalid_client_email_for_ping(self, mock_http):
        """ test invalid  client email for ping"""
        mock_http.side_effect = HTTPError("invalid_grant")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "Invalid Client Email" in ping_response['error']
        assert ping_response['code'] == "authentication_fail"

    def test_invalid_host_for_ping(self, mock_http):
        """ test invalid host for ping"""
        mock_http.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "Invalid Host" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    def test_invalid_client_email_for_transmit_query(self, mock_http):
        """ test invalid  client email for transmit query"""
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        }
        mock_http.side_effect = HTTPError("invalid_grant")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "Invalid Client Email" in query_response['error']
        assert query_response['code'] == "authentication_fail"

    def test_invalid_host_for_transmit_query(self, mock_http):
        """ test invalid host for transmit query"""
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        }
        mock_http.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "Invalid Host" in query_response['error']
        assert query_response['code'] == "service_unavailable"

    def test_query_raise_create_rule_query_error(self, mock_http):
        """raise 400 invalid argument error by applying any to field type other than list"""
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: (any $udm.network.http.user_agent "
                        "= /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        }

        mock_http.return_value = MockCodeResponse(400, {
            "error": {"code": 400,
                      "status": "INVALID_ARGUMENT",
                      "message": "generic::invalid_argument: "
                                 "compiling rule: validating repeated fields: applying any/all to a non-repeated field"
                      }})
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "invalid_argument" in query_response['error']
        assert query_response['code'] == "invalid_parameter"

    def test_value_error_for_transmit_query(self, mock_http):
        """test query value error connection"""
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        }
        mocked_create_rule = MockCodeResponse(200, {"ruleId": "ru_1234"})
        mock_http.side_effect = [mocked_create_rule, ValueError("Invalid json")]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "Invalid json" in query_response["error"]
        assert query_response['code'] == "unknown"

    def test_transmit_query_with_key_error(self, mock_http):
        """test key error for input query having invalid key """
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "start_Time": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        }
        mocked_create_rule = MockCodeResponse(200, {"ruleId": "ru_1234"})
        mock_http.return_value = mocked_create_rule
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "startTime" in query_response["error"]
        assert query_response['code'] == "unknown"

    def test_query_with_base_exception(self, mock_http):
        """test transmit query with base exception"""
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        }
        mocked_create_rule = MockCodeResponse(200, {"ruleId": "ru_1234"})
        mock_http.side_effect = [mocked_create_rule, Exception("Unknown Error")]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "Unknown Error" in query_response["error"]
        assert query_response['code'] == "unknown"

    def test_400_error_with_invalid_timestamp_format(self, mock_http):
        """test 400 code with invalid timestamp error from run retrohunt api """
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29TT00:00:00.030Z"
        }
        mock_create_rule_response = MockCodeResponse(200, {"ruleId": "ru_1234"})
        mock_create_search_error_response = MockCodeResponse(400, {
            "error": {"code": 400,
                      "status": "INVALID_ARGUMENT",
                      "message": "Invalid time format"
                      }})
        mock_http.side_effect = [mock_create_rule_response, mock_create_search_error_response]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "Invalid time format" in query_response['error']
        assert query_response['code'] == "invalid_parameter"

    def test_create_search_with_return_200_and_invalid_response(self, mock_http):
        """ test Run retrohunt with 200 response code and invalid json response"""
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        }
        mock_create_rule_response = MockCodeResponse(200, {"ruleId": "ru_1234"})
        mock_create_search_error_response = MockCodeResponse(200, {"Invalid": "Response"})
        mock_http.side_effect = [mock_create_rule_response, mock_create_search_error_response]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "InvalidResponse" in query_response['error']
        assert query_response['code'] == "invalid_parameter"

    def test_invalid_query_for_retrohunt_api(self, mock_http):
        """ test invalid host for run retorhunt api"""
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        }
        mock_create_rule_response = MockCodeResponse(200, {"ruleId": "ru_1234"})
        mock_http.side_effect = [mock_create_rule_response, ClientConnectionError("Invalid Host")]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "Invalid Host" in query_response['error']
        assert query_response['code'] == "service_unavailable"

    def test_invalid_client_email_for_retrohunt(self, mock_http):
        """ test invalid client email for run retrohunt api call"""
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        }
        mock_create_rule_response = MockCodeResponse(200, {"ruleId": "ru_1234"})
        mock_http.side_effect = [mock_create_rule_response, HTTPError("invalid_grant")]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "Invalid Client Email" in query_response['error']
        assert query_response['code'] == "authentication_fail"

    def test_invalid_response_for_400_error_code(self, mock_http):
        """test value error exception in create search through json loads providing
        invalid json in retrohunt response"""
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        }
        mocked_create_rule = MockCodeResponse(200, {"ruleId": "ru_1234"})
        mocked_retrohunt_value_error = ValueError('Expecting value')
        mock_http.side_effect = [mocked_create_rule, mocked_retrohunt_value_error]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "cannot parse Expecting value" in query_response["error"]
        assert query_response['code'] == "unknown"

    def test_timeout_error_in_ping(self, mock_http):
        """test connection/timeout error in transmit ping"""
        mock_http.side_effect = TimeoutError("connection attempt failed")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "connection attempt failed" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    def test_ping_value_error(self, mock_http):
        """test value error in transmit ping"""
        mock_http.side_effect = ValueError('Expecting value')
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "cannot parse" in ping_response['error']
        assert ping_response['code'] == "unknown"

    def test_ping_raise_429_error(self, mock_http):
        """test  resource exhausted error in ping"""
        mock_http.return_value = MockCodeResponse(429, {"error": {"code": 429, "message": "RESOURCE_EXHAUSTED"}})
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "RESOURCE_EXHAUSTED" in ping_response['error']
        assert ping_response['code'] == "service_unavailable"

    def test_delete_query_404_error(self, mock_http):
        """test 404 error with invalid rule id in transmit delete"""
        search_id = "oh_1234:ru_1234"
        mock_http.return_value = MockCodeResponse(404,
                                                  {"error": {
                                                      "code": 404,
                                                      "message": "rule with ID ru_1234 could not be found",
                                                      "status": "NOT_FOUND"}})
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        delete_response = transmission.delete(search_id)
        assert delete_response is not None
        assert delete_response['success'] is False
        assert "rule with ID ru_1234 could not be found" in delete_response['error']
        assert delete_response['code'] == "invalid_parameter"

    def test_delete_query_with_invalid_client_email(self, mock_http):
        """ test invalid email in transmit delete"""
        search_id = "oh_1234:ru_1234"
        mock_http.side_effect = HTTPError("invalid_grant")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        delete_response = transmission.delete(search_id)
        assert delete_response is not None
        assert delete_response['success'] is False
        assert "Invalid Client Email" in delete_response['error']
        assert delete_response['code'] == "authentication_fail"

    def test_delete_with_server_not_found_error(self, mock_http):
        """ test invalid host in transmit delete"""
        search_id = "oh_1234:ru_1234"
        mock_http.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        delete_response = transmission.delete(search_id)
        assert delete_response is not None
        assert delete_response['success'] is False
        assert "Invalid Host" in delete_response['error']
        assert delete_response['code'] == "service_unavailable"

    def test_delete_with_timeout_exception(self, mock_http):
        """ test timeout error in transmit delete """
        search_id = "oh_1234:ru_1234"
        mock_http.side_effect = TimeoutError("connection attempt failed")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        delete_response = transmission.delete(search_id)
        assert delete_response is not None
        assert delete_response['success'] is False
        assert "connection attempt failed" in delete_response['error']
        assert delete_response['code'] == "service_unavailable"

    def test_delete_with_invalid_searchid(self, mock_http):
        """ test timeout error in transmit delete """
        search_id = "oh_1234:ru_1234"
        mock_http.side_effect = HTTPError("generic::not_found: rule with ID ru_1234")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        delete_response = transmission.delete(search_id)
        assert delete_response is not None
        assert delete_response['success'] is False
        assert "Could not find search id" in delete_response['error']
        assert delete_response['code'] == "no_results"

    def test_results_with_invalid_client_email(self, mock_http):
        """ test invalid client email in transmit results"""
        search_id = "oh_1234:ru_1234"
        mock_http.side_effect = HTTPError("invalid_grant")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        result_response = transmission.results(search_id, 0, 2)
        assert result_response is not None
        assert result_response['success'] is False
        assert "Invalid Client Email" in result_response['error']
        assert result_response['code'] == "authentication_fail"

    def test_results_with_invalid_host(self, mock_http):
        """ test invalid host in transmit results"""
        search_id = "oh_1234:ru_1234"
        mock_http.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        result_response = transmission.results(search_id, 0, 2)
        assert result_response is not None
        assert result_response['success'] is False
        assert "Invalid Host" in result_response['error']
        assert result_response['code'] == "service_unavailable"

    def test_results_with_404_error(self, mock_http):
        """test 404 error with invalid rule id in transmit results"""
        search_id = "oh_1234:ru_1234"
        mock_http.return_value = MockCodeResponse(404, {"error": {
            "code": 404,
            "message": "rule with ID ru_1234 could not be found",
            "status": "NOT_FOUND"}})
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        result_response = transmission.results(search_id, 0, 2)
        assert result_response is not None
        assert result_response['success'] is False
        assert "rule with ID ru_1234 could not be found" in result_response['error']
        assert result_response['code'] == "invalid_parameter"

    def test_404_in_next_page_result(self, mock_http):
        """test 404 error in result response during pagination in transmit results"""
        search_id = "oh_1234:ru_1234"
        output_1 = {
            "detections":
                [{
                    "type": "RULE_DETECTION",
                    "detection": [{
                        "ruleName": "rule_1657020065"
                    }],
                    "createdTime": "2022-07-07T08:01:24.869956Z",
                    "id": "de_38c2972e-ec99-8c0c-4dbe-3b350294b2bb",
                    "timeWindow": {
                        "startTime": "2022-06-28T09:49:09.460001Z",
                        "endTime": "2022-06-28T09:49:09.460001Z"
                    },
                    "collectionElements": [{
                        "references": [{
                            "event": {
                                "metadata": {
                                    "productLogId": "823rb4e123k4"
                                }
                            }
                        }],
                        "label": "udm"
                    }],
                    "detectionTime": "2022-06-28T09:49:09.460001Z"
                }],
            "nextPageToken": "12345"
        }
        mocked_result_response_1 = MockCodeResponse(200, output_1)
        mocked_delete_response = MockCodeResponse(200)
        mocked_result_with_invalid_rule_id = MockCodeResponse(404, {"error": {
            "code": 404,
            "message": "rule with ID ru_1234 could not be found",
            "status": "NOT_FOUND"}})
        mock_http.side_effect = [mocked_result_response_1, mocked_result_with_invalid_rule_id, mocked_delete_response]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        result_response = transmission.results(search_id, 0, 2)
        assert result_response is not None
        assert result_response['success'] is False
        assert "rule with ID ru_1234 could not be found" in result_response['error']

    def test_status_response_with_state_running(self, mock_http):
        """test running status for transmit status"""
        search_id = "oh_1234:ru_1234"
        mock_status_output = {"retrohuntId": "oh_1234", "ruleId": "ru_1234", "versionId": "ru_1234",
                              "eventStartTime": "2022-06-28T00:00:00.030Z",
                              "eventEndTime": "2022-06-29T00:00:00.030Z",
                              "retrohuntStartTime": "2022-07-07T06:43:40.983372Z",
                              "retrohuntEndTime": "2022-07-07T06:43:58.750611Z", "state": "RUNNING",
                              "progressPercentage": 42.86}
        mock_http.return_value = MockCodeResponse(200, mock_status_output)
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is True
        assert status_response['progress'] == 42.86
        assert status_response['status'] == "RUNNING"

    def test_status_response_with_state_cancelled(self, mock_http):
        """test status response with cancelled state"""
        search_id = "oh_1234:ru_1234"
        mock_status_output = {"retrohuntId": "oh_1234", "ruleId": "ru_1234", "versionId": "ru_1234",
                              "eventStartTime": "2022-06-28T00:00:00.030Z",
                              "eventEndTime": "2022-06-29T00:00:00.030Z",
                              "retrohuntStartTime": "2022-07-07T06:43:40.983372Z",
                              "retrohuntEndTime": "2022-07-07T06:43:58.750611Z", "state": "CANCELLED",
                              "progressPercentage": 77.45}
        mock_http.return_value = MockCodeResponse(200, mock_status_output)
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is True
        assert status_response['progress'] == 77.45
        assert status_response['status'] == "CANCELED"

    def test_status_with_invalid_client_email(self, mock_http):
        """ test invalid client email for transmit status"""
        search_id = "oh_1234:ru_1234"
        mock_http.side_effect = HTTPError("invalid_grant")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is False
        assert "Invalid Client Email" in status_response['error']
        assert status_response['code'] == "authentication_fail"

    def test_status_with_invalid_host(self, mock_http):
        """ test invalid host for transmit status"""
        search_id = "oh_1234:ru_1234"
        mock_http.side_effect = ClientConnectionError("Invalid Host")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is False
        assert "Invalid Host" in status_response['error']
        assert status_response['code'] == "service_unavailable"

    def test_status_response_with_no_state_response(self, mock_http):
        """test error when status response having response code 200 without state as key"""
        search_id = "oh_1234:ru_1234"
        mock_status_output = {"retrohuntId": "oh_1234", "ruleId": "ru_1234", "versionId": "ru_1234",
                              "eventStartTime": "2022-06-28T00:00:00.030Z",
                              "eventEndTime": "2022-06-29T00:00:00.030Z",
                              "retrohuntStartTime": "2022-07-07T06:43:40.983372Z",
                              "retrohuntEndTime": "2022-07-07T06:43:58.750611Z"}
        mock_http.return_value = MockCodeResponse(200, mock_status_output)
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is False
        assert "Invalid Response" in status_response['error']
        assert status_response['code'] == "invalid_parameter"

    def test_status_response_429_resource_exhausted(self, mock_http):
        """status with 429 resource exhausted"""
        search_id = "oh_1234:ru_1234"
        resource_exhausted_response = {'error': {'code': 429,
                                                 'message': 'generic::resource_exhausted: '
                                                            'insufficient quota for method '
                                                            'quota is 60 queries per 60 seconds',
                                                 'status': 'RESOURCE_EXHAUSTED'}}
        mocked_resource_exhausted_response = MockCodeResponse(429, resource_exhausted_response)
        mock_http.return_value = mocked_resource_exhausted_response
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['status'] == "RUNNING"

    def test_security_result_response(self, mock_http):
        """test security result response """
        search_id = "oh_1234:ru_1234"
        output = {
            "detections":
                [{
                    "type": "RULE_DETECTION",
                    "detection": [{
                        "ruleName": "rule_1657020065",
                        "urlBackToProduct": "url",
                        "ruleId": "ru_1234",
                        "ruleVersion": "ru_1234",
                        "alertState": "NOT_ALERTING",
                        "ruleType": "SINGLE_EVENT",
                        "ruleLabels": [{
                            "key": "author",
                            "value": "ibm cp4s user"
                        }, {
                            "key": "description",
                            "value": "Create event rule that should generate detections"
                        }]
                    }],
                    "createdTime": "2022-07-07T08:01:24.869956Z",
                    "id": "de_38c2972e-ec99-8c0c-4dbe-3b350294b2bb",
                    "timeWindow": {
                        "startTime": "2022-06-28T09:49:09.460001Z",
                        "endTime": "2022-06-28T09:49:09.460001Z"
                    },
                    "collectionElements": [{
                        "references": [{
                            "event": {
                                "metadata": {
                                    "productLogId": "823rb4e123k4",
                                    "eventType": "GENERIC_EVENT"
                                },
                                "principal": {
                                    "asset": {
                                        "platformSoftware": {
                                            "platformVersion": "windows10"
                                        },
                                        "software": {
                                            "version": "5.6"
                                        }
                                    }
                                },
                                "securityResult": [
                                    {
                                        "severity": "LOW",
                                        "category": ["SOFTWARE_SUSPICIOUS"]
                                    }
                                ],
                                "network": {
                                    "http": {
                                        "userAgent": "hhtpuseragent"
                                    }
                                },
                                "target": {
                                    "hostname": "v20.events.data.microsoft.com",
                                    "ip": [
                                        "13.89.178.26"
                                    ],
                                    "url": "v20.events.data.microsoft.com"
                                }

                            }
                        }],
                        "label": "udm"
                    }],
                    "detectionTime": "2022-06-28T09:49:09.460001Z"
                }]}
        mocked_result_response = MockCodeResponse(200, output)
        mocked_delete_response = MockCodeResponse(200)
        mock_http.side_effect = [mocked_result_response, mocked_delete_response]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        result_response = transmission.results(search_id, 0, 2)
        assert result_response is not None
        assert result_response['success'] is True
        assert result_response["data"][0]["event"]["metadata"]["productLogId"] == "823rb4e123k4"
        assert result_response["data"][0]["event"]["securityResult"][0]["category"] == "alert"
        assert result_response["data"][0]["event"]["securityResult"][0]["severity"] == 48
        assert result_response["data"][0]["event"]["metadata"]["eventType"] == "GENERIC_EVENT"

    def test_security_and_registry_response(self, mock_http):
        """test security result and registry response"""
        search_id = "oh_1234:ru_1234"
        output = {
            "detections":
                [{
                    "type": "RULE_DETECTION",
                    "detection": [{
                        "ruleName": "rule_1657020065",
                        "urlBackToProduct": "url",
                        "ruleId": "ru_1234",
                        "ruleVersion": "ru_1234",
                        "alertState": "NOT_ALERTING",
                        "ruleType": "SINGLE_EVENT",
                        "ruleLabels": [{
                            "key": "author",
                            "value": "ibm cp4s user"
                        }, {
                            "key": "description",
                            "value": "Create event rule that should generate detections"
                        }]
                    }],
                    "createdTime": "2022-07-07T08:01:24.869956Z",
                    "id": "de_38c2972e-ec99-8c0c-4dbe-3b350294b2bb",
                    "timeWindow": {
                        "startTime": "2022-06-28T09:49:09.460001Z",
                        "endTime": "2022-06-28T09:49:09.460001Z"
                    },
                    "collectionElements": [{
                        "references": [{
                            "event": {
                                'metadata': {
                                    'eventTimestamp': '2022-06-24T11:29:28.336Z',
                                    'eventType': 'REGISTRY_MODIFICATION'
                                },
                                "principal": {
                                    'hostname': 'alert-windows',
                                    'assetId': 'DeviceId:4f22ab5dc4be96566ee3c9adb3b77280dc08bfdb',
                                    'user': {
                                        'windowsSid': 'S-1-5-18'
                                    }
                                },
                                "securityResult": [
                                    {
                                        "summary": "registry modified"
                                    }
                                ],
                                "target": {
                                    'registry': {
                                        'registryValueName': 'CrashHeartbeat',
                                        'registryValueData': '132996043194369129'
                                    }
                                }
                            }
                        }],
                        "label": "udm"
                    }],
                    "detectionTime": "2022-06-28T09:49:09.460001Z"
                }]}
        mocked_result_response = MockCodeResponse(200, output)
        mocked_delete_response = MockCodeResponse(200)
        mock_http.side_effect = [mocked_result_response, mocked_delete_response]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        result_response = transmission.results(search_id, 0, 2)
        assert result_response is not None
        assert result_response['success'] is True
        assert result_response["data"][0]["event"]["securityResult"][0]['summary'] == "registry modified"
        assert "registry" not in result_response["data"][0]["event"]["target"]
        assert result_response["data"][0]["event"]["principal"]["user"]["userid"] == "UNAVAILABLE"

    def test_generic_event_with_protocol_response(self, mock_http):
        """test generic event response """
        search_id = "oh_1234:ru_1234"
        output = {
            "detections":
                [{
                    "type": "RULE_DETECTION",
                    "detection": [{
                        "ruleName": "rule_1657020065",
                        "urlBackToProduct": "url",
                        "ruleId": "ru_1234",
                        "ruleVersion": "ru_1234",
                        "alertState": "NOT_ALERTING",
                        "ruleType": "SINGLE_EVENT",
                        "ruleLabels": [{
                            "key": "author",
                            "value": "ibm cp4s user"
                        }, {
                            "key": "description",
                            "value": "Create event rule that should generate detections"
                        }]
                    }],
                    "createdTime": "2022-07-07T08:01:24.869956Z",
                    "id": "de_38c2972e-ec99-8c0c-4dbe-3b350294b2bb",
                    "timeWindow": {
                        "startTime": "2022-06-28T09:49:09.460001Z",
                        "endTime": "2022-06-28T09:49:09.460001Z"
                    },
                    "collectionElements": [{
                        "references": [{
                            "event": {
                                "metadata": {
                                    "productLogId": "823rb4e123k4",
                                    "eventType": "GENERIC_EVENT"
                                },
                                "principal": {
                                    "asset": {
                                        "platformSoftware": {
                                            "platformVersion": "windows10"
                                        },
                                        "software": {
                                            "version": "5.6"
                                        }
                                    }
                                },
                                "securityResult": [
                                    {
                                        "severity": "LOW",
                                        "category": ["SOFTWARE_SUSPICIOUS"]
                                    }
                                ],
                                "network": {
                                    "http": {
                                        "userAgent": "httpuseragent"
                                    },
                                    'applicationProtocol': 'HTTP'
                                },
                                "target": {
                                    "hostname": "v20.events.data.microsoft.com",
                                    "url": "v20.events.data.microsoft.com"
                                }

                            }
                        }],
                        "label": "udm"
                    }],
                    "detectionTime": "2022-06-28T09:49:09.460001Z"
                }]}
        mocked_result_response = MockCodeResponse(200, output)
        mocked_delete_response = MockCodeResponse(200)
        mock_http.side_effect = [mocked_result_response, mocked_delete_response]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        result_response = transmission.results(search_id, 0, 2)
        assert result_response is not None
        assert result_response['success'] is True
        assert result_response["data"][0]["event"]["network"] == {}

    def test_invalid_email_addresses_response(self, mock_http):
        """test email addresses response """
        search_id = "oh_1234:ru_1234"
        output = {
            "detections":
                [{
                    "type": "RULE_DETECTION",
                    "detection": [{
                        "ruleName": "rule_1657020065",
                        "urlBackToProduct": "url",
                        "ruleId": "ru_1234",
                        "ruleVersion": "ru_1234",
                        "alertState": "NOT_ALERTING",
                        "ruleType": "SINGLE_EVENT",
                        "ruleLabels": [{
                            "key": "author",
                            "value": "ibm cp4s user"
                        }, {
                            "key": "description",
                            "value": "Create event rule that should generate detections"
                        }]
                    }],
                    "createdTime": "2022-07-07T08:01:24.869956Z",
                    "id": "de_38c2972e-ec99-8c0c-4dbe-3b350294b2bb",
                    "timeWindow": {
                        "startTime": "2022-06-28T09:49:09.460001Z",
                        "endTime": "2022-06-28T09:49:09.460001Z"
                    },
                    "collectionElements": [{
                        "references": [{
                            "event": {
                                "metadata": {
                                    "productLogId": "823rb4e123k4"
                                },
                                'principal': {
                                    'user': {
                                        'emailAddresses': ['user:user1iscgalaxy.com']
                                    },
                                    'ip': ['54.240.11.121']
                                },
                                'target': {
                                    'user': {
                                        'emailAddresses': ['user:user2@iscgalaxy.com',
                                                           "targetuser.com"]
                                    }
                                },
                                "securityResult": [
                                    {
                                        "severity": "LOW"
                                    }
                                ],
                                "network": {
                                    "email": {
                                        "from": "010001818b271091-e32fa873-1a72-4d6f-8eab-29c09637402f-000000"
                                                "@amazonses.com",
                                        "mailId": "010001818b271091-e32fa873-1a72-4d6f-8eab-29c09637402f-000000@email"
                                                  ".amazonses.com",
                                        "subject": [
                                            "https://testurl.com test"
                                        ],
                                        "to": [
                                            "xyziscgalaxy.com"
                                        ],
                                        "cc": [
                                            "abc@user.com",
                                            "service:test@galaxy.com",
                                            "ccuser.com"
                                        ]
                                    },
                                    "dns": {
                                        "authoritative": True,
                                        "questions": [{
                                            "name": "www.a2k2.in",
                                            "type": 1
                                        }],
                                        "responseCode": 3
                                    },
                                    "ipProtocol": "UDP"
                                }

                            }
                        }],
                        "label": "udm"
                    }],
                    "detectionTime": "2022-06-28T09:49:09.460001Z"
                }]}
        mocked_result_response = MockCodeResponse(200, output)
        mocked_delete_response = MockCodeResponse(200)
        mock_http.side_effect = [mocked_result_response, mocked_delete_response]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        result_response = transmission.results(search_id, 0, 1)
        assert result_response is not None
        assert result_response['success'] is True
        assert result_response["data"][0]["event"]["target"]["user"]["emailAddresses"] == ['user2@iscgalaxy.com']
        assert result_response["data"][0]["event"]["network"]["email"]["cc"] == ['abc@user.com', 'test@galaxy.com']
        assert 'to' not in result_response["data"][0]["event"]["network"]["email"].keys()
        assert 'emailAddresses' not in result_response["data"][0]["event"]["principal"]["user"].keys()

    def test_invalid_private_key_for_ping(self, mock_http):
        """ test invalid private key for ping"""
        mock_http.side_effect = ValueError("Could not deserialize key data")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        ping_response = transmission.ping()
        assert ping_response is not None
        assert ping_response['success'] is False
        assert "Could not deserialize key data" in ping_response['error']
        assert ping_response['code'] == "authentication_fail"

    def test_invalid_private_key_for_transmit_query(self, mock_http):
        """ test invalid private key for transmit query"""
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"}
        mock_http.side_effect = ValueError("Could not deserialize key data")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "Could not deserialize key data" in query_response['error']
        assert query_response['code'] == "authentication_fail"

    def test_results_with_invalid_private_key(self, mock_http):
        """ test invalid private key in transmit results"""
        search_id = "oh_1234:ru_1234"
        mock_http.side_effect = ValueError("Could not deserialize key data")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        result_response = transmission.results(search_id, 0, 2)
        assert result_response is not None
        assert result_response['success'] is False
        assert "Could not deserialize key data" in result_response['error']
        assert result_response['code'] == "authentication_fail"

    def test_invalid_private_key_for_retrohunt(self, mock_http):
        """ test invalid private key for run retrohunt api call"""
        query = {
            "ruleText": "rule rule_1657176728 { meta: author = \"ibm cp4s user\" description = \"Create event rule "
                        "that should generate detections\" events: ($udm.network.http.user_agent = /(?s)glbc\\/v0.0.0 "
                        "\\(linux\\/amd64\\) kubernetes\\/\\$Format\\/leader-election/ nocase) condition: $udm}",
            "startTime": "2022-06-28T00:00:00.030Z",
            "endTime": "2022-06-29T00:00:00.030Z"
        }
        mock_create_rule_response = MockCodeResponse(200, {"ruleId": "ru_1234"})
        mock_http.side_effect = [mock_create_rule_response, ValueError("Could not deserialize key data")]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        query_response = transmission.query(query)
        assert query_response is not None
        assert query_response['success'] is False
        assert "Could not deserialize key data" in query_response['error']
        assert query_response['code'] == "authentication_fail"

    def test_status_with_invalid_private_key(self, mock_http):
        """ test invalid private key for transmit status"""
        search_id = "oh_1234:ru_1234"
        mock_http.side_effect = ValueError("Could not deserialize key data")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        status_response = transmission.status(search_id)
        assert status_response is not None
        assert status_response['success'] is False
        assert "Could not deserialize key data" in status_response['error']
        assert status_response['code'] == "authentication_fail"

    def test_delete_query_with_invalid_private_key(self, mock_http):
        """ test invalid private key in transmit delete"""
        search_id = "oh_1234:ru_1234"
        mock_http.side_effect = ValueError("Could not deserialize key data")
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        delete_response = transmission.delete(search_id)
        assert delete_response is not None
        assert delete_response['success'] is False
        assert "Could not deserialize key data" in delete_response['error']
        assert delete_response['code'] == "authentication_fail"

    def test_429_exception_in_results(self, mock_http):
        """test  resource exhausted error in results"""
        search_id = "oh_1234:ru_1234"
        mock_http.return_value = MockCodeResponse(429, {"error": {"code": 429, "message": "RESOURCE_EXHAUSTED"}})
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(), self.configuration())
        result_response = transmission.results(search_id, 0, 1)
        assert result_response is not None
        assert result_response['success'] is False
        assert "RESOURCE_EXHAUSTED" in result_response['error']
        assert result_response['code'] == "service_unavailable"

    def test_invalid_metadata(self, mock_http):
        """test invalid metadata"""
        search_id = "oh_1234:ru_1234"
        metadata = "1:123"
        output = json.dumps({
            "detections":
                [{
                    "type": "RULE_DETECTION",
                    "detection": [{
                        "ruleName": "rule_1657020065",
                        "urlBackToProduct": "url",
                        "ruleId": "ru_1234",
                        "ruleVersion": "ru_1234",
                        "alertState": "NOT_ALERTING",
                        "ruleType": "SINGLE_EVENT",
                        "ruleLabels": [{
                            "key": "author",
                            "value": "ibm cp4s user"
                        }, {
                            "key": "description",
                            "value": "Create event rule that should generate detections"
                        }]
                    }],
                    "createdTime": "2022-07-07T08:01:24.869956Z",
                    "id": "de_38c2972e-ec99-8c0c-4dbe-3b350294b2bb",
                    "timeWindow": {
                        "startTime": "2022-06-28T09:49:09.460001Z",
                        "endTime": "2022-06-28T09:49:09.460001Z"
                    },
                    "collectionElements": [{
                        "references": [{
                            "event": {
                                "metadata": {
                                    "productLogId": "823rb4e123k4"
                                },
                                "securityResult": [
                                    {
                                        "severity": "LOW"
                                    }
                                ],
                                "network": {
                                    "email": {
                                        "from": "010001818b271091-e32fa873-1a72-4d6f-8eab-29c09637402f-000000"
                                                "@amazonses.com",
                                        "mailId": "010001818b271091-e32fa873-1a72-4d6f-8eab-29c09637402f-000000@email"
                                                  ".amazonses.com",
                                        "subject": [
                                            "https://testurl.com test"
                                        ],
                                        "to": [
                                            "ravithummala@iscgalaxy.com"
                                        ]
                                    },
                                    "dns": {
                                        "authoritative": True,
                                        "questions": [{
                                            "name": "www.a2k2.in",
                                            "type": 1
                                        }],
                                        "responseCode": 3
                                    },
                                    "ipProtocol": "UDP"
                                },
                                "target": {
                                    "hostname": "v20.events.data.microsoft.com",
                                    "ip": [
                                        "13.89.178.26"
                                    ],
                                    "url": "v20.events.data.microsoft.com",
                                    "registry": {
                                        "registryKey": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Advanced "
                                                       "Threat Protection",
                                        "registryValueData": "132996043194369129",
                                        "registryValueName": "CrashHeartbeat"
                                    }
                                }

                            }
                        }],
                        "label": "udm"
                    }],
                    "detectionTime": "2022-06-28T09:49:09.460001Z"
                }],
            "nextPageToken": "12345"
        })
        mocked_result_response = MockCodeResponse(200, output)
        mocked_delete_response = MockCodeResponse(200)
        mock_http.side_effect = [mocked_result_response, mocked_delete_response]
        transmission = stix_transmission.StixTransmission('gcp_chronicle', self.connection(),
                                                          self.configuration())
        result_response = transmission.results(search_id, 0, 1, metadata)
        assert result_response is not None
        assert result_response['success'] is False
        assert 'Invalid metadata' in result_response['error']
        assert result_response['code'] == 'invalid_parameter'
