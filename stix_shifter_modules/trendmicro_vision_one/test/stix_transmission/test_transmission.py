# -*- coding: utf-8 -*-
import json
import unittest
from unittest.mock import patch

from stix_shifter.stix_transmission.stix_transmission import StixTransmission

from stix_shifter_modules.trendmicro_vision_one.entry_point import EntryPoint

CONNECTION = {
    "host": "visionone-host.test",
    "port": 443,
    "options": {"timeout": 60}
}
CONFIG = {
    "auth": {
        "token": "token"
    }
}


class MockResponse:
    def __init__(self, response_code, obj):
        self.code = response_code
        self.object = obj

    def read(self):
        return bytearray(self.object, 'utf-8')


class TestTransmission(unittest.TestCase):
    def test_is_async(self):
        entry_point = EntryPoint(CONNECTION, CONFIG)
        check_async = entry_point.is_async()
        self.assertFalse(check_async)

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping(self, mock_ping):
        response = {
            "data": [
                {
                    "modelId": "modelId",
                    "name": "name",
                    "enabled": False
                }
            ]
        }
        mock_ping.side_effect = [MockResponse(200, json.dumps(response))]
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertTrue(ping_response["success"])

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_failure(self, mock_ping):
        response = {
            "error": {
                "code": "Unsupported",
                "message": "The specified search parameters are invalid. Verify the parameters and try again."
            }
        }
        mock_ping.side_effect = [MockResponse(400, json.dumps(response))]
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertFalse(ping_response["success"])
        self.assertEqual(ping_response["code"], "invalid_parameter")

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_auth_failure(self, mock_ping):
        response = {
            "error": {
                "code": "Unauthorized",
                "message": "No authorization token was found",
                "innererror": {
                    "code": "InvalidToken",
                    "innererror": {
                        "code": "CredentialsRequired",
                        "service": "svp"
                    }
                }
            }
        }
        mock_ping.side_effect = [MockResponse(401, json.dumps(response))]
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertFalse(ping_response["success"])
        self.assertEqual(ping_response["code"], "authentication_fail")

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_unknown_failure(self, mock_ping):
        response = {
            "error": {
                "code": "InternalError",
            }
        }
        mock_ping.side_effect = [MockResponse(503, json.dumps(response))]
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertFalse(ping_response["success"])
        self.assertEqual(ping_response["code"], "unknown")

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_unknown_code(self, mock_ping):
        response = {
            "error": {
                "code": "InternalError",
            }
        }
        mock_ping.side_effect = [MockResponse(None, json.dumps(response))]
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertFalse(ping_response["success"])
        self.assertEqual(ping_response["code"], "unknown")

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_exception(self, mock_ping):
        mock_ping.side_effect = ConnectionError("Failed to establish a new connection")
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertFalse(ping_response["success"])

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_query(self, mock_query):
        mock_query.side_effect = [MockResponse(200, self._get_query())]
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        query_response = transmission.query(self._get_query())
        self.assertTrue(query_response["success"])
        self.assertEqual(query_response["search_id"], self._get_query())

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_param_failure(self, mock_query):
        payload = {
            "error": {
                "code": "Unsupported",
                "message": "The specified search parameters are invalid. Verify the parameters and try again."
            }
        }
        mock_query.side_effect = [MockResponse(400, json.dumps(payload))]
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 0, 10)
        self.assertFalse(results_response["success"])
        self.assertEqual(results_response["code"], "invalid_parameter")
        self.assertEqual(results_response["error"], "trendmicro_vision_one connector error => " + payload["error"]["message"])

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_auth_failure(self, mock_query):
        payload = {
            "error": {
                "code": "Unauthorized",
                "message": "No authorization token was found",
                "innererror": {
                    "code": "InvalidToken",
                    "innererror": {
                        "code": "CredentialsRequired",
                        "service": "svp"
                    }
                }
            }
        }
        mock_query.side_effect = [MockResponse(401, json.dumps(payload))]
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 0, 10)
        self.assertFalse(results_response["success"])
        self.assertEqual(results_response["code"], 'authentication_fail')
        self.assertEqual(results_response["error"], "trendmicro_vision_one connector error => " + payload["error"]["message"])

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_timeout(self, mock_query):
        payload = {
            "error": {
                "code": "RequestTimeout",
                "message": "timeout"
            }
        }
        mock_query.side_effect = [MockResponse(408, json.dumps(payload))]
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 0, 10)
        self.assertFalse(results_response["success"])
        self.assertEqual(results_response["code"], "unknown")
        self.assertEqual(results_response["error"], "trendmicro_vision_one connector error => " + payload["error"]["message"])

    @staticmethod
    def _get_query():
        return json.dumps({
            "offset": 0,
            "fields": [],
            "from": 1587892612,
            "to": 1592382065,
            "source": "endpointActivityData",
            "query": "hostName:*"
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_reach_max_fetch_count(self, mock_results):
        mock_responses = []
        for i in range(0, 20):
            mock_responses.append(MockResponse(200, self._get_response(1, i)))
        mock_results.side_effect = mock_responses
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        result_response = transmission.results(self._get_query(), 0, 20)
        self.assertTrue(result_response["success"])
        # 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 + 1 -> reach max_fetch_count -> break
        self.assertEqual(len(result_response["data"]), 10)

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_last_partial(self, mock_results):
        mock_responses = []
        for i in range(0, 20):
            mock_responses.append(MockResponse(200, self._get_response(3, i)))
        mock_results.side_effect = mock_responses
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        result_response = transmission.results(self._get_query(), 0, 20)
        self.assertTrue(result_response["success"])
        # 3 + 3 + 3 + 3 + 3 + 3 + 2 -> break
        self.assertEqual(len(result_response["data"]), 20)

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_insufficient(self, mock_results):
        mock_responses = []
        for i in range(0, 6):
            mock_responses.append(MockResponse(200, self._get_response(3, i)))
        mock_responses.append(MockResponse(200, self._get_response(0)))
        mock_results.side_effect = mock_responses
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        result_response = transmission.results(self._get_query(), 0, 20)
        self.assertTrue(result_response["success"])
        # 3 + 3 + 3 + 3 + 3 + 3 + 0-> break
        self.assertEqual(len(result_response["data"]), 18)

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_sufficient(self, mock_results):
        mock_responses = []
        for i in range(0, 6):
            mock_responses.append(MockResponse(200, self._get_response(4, i)))
        mock_results.side_effect = mock_responses
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        result_response = transmission.results(self._get_query(), 0, 20)
        self.assertTrue(result_response["success"])
        # 4 + 4 + 4 + 4 + 4 -> break
        self.assertEqual(len(result_response["data"]), 20)

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_last_empty(self, mock_results):
        mock_responses = []
        for i in range(0, 3):
            mock_responses.append(MockResponse(200, self._get_response(4, i)))
        mock_responses.append(MockResponse(200, self._get_response(0, 4)))
        mock_results.side_effect = mock_responses
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        result_response = transmission.results(self._get_query(), 0, 20)
        self.assertTrue(result_response["success"])
        # 4 + 4 + 4 + 0 -> break
        self.assertEqual(len(result_response["data"]), 12)

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_exceed_length_limit(self, mock_results):
        mock_responses = []
        for i in range(0, 4):
            mock_responses.append(MockResponse(200, self._get_response(500, i)))
        mock_results.side_effect = mock_responses
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        result_response = transmission.results(self._get_query(), 0, 1200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 1000)

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_no_offset(self, mock_results):
        mock_results.side_effect = [
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
        ]
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        result_response = transmission.results(self._get_query(), 0, 200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 200)

        result_response = transmission.results(self._get_query(), 0, 500)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 500)

        result_response = transmission.results(self._get_query(), 0, 1200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 500)

        result_response = transmission.results(self._get_query(), 99, 200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 200)

        result_response = transmission.results(self._get_query(), 99, 500)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 401)

        result_response = transmission.results(self._get_query(), 99, 1200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 401)

        result_response = transmission.results(self._get_query(), 600, 100)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 0)

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_result_exception(self, mock_ping):
        mock_ping.side_effect = ConnectionError("Failed to establish a new connection")
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        ping_response = transmission.results(self._get_query(), 600, 100)
        self.assertFalse(ping_response["success"])

    @staticmethod
    def _get_response(count=1, sequence=-1):
        response = {
            "status": 200,
            "data": {
                "logs": [
                ]
            },
        }
        for i in range(0, count):
            response["data"]["logs"].append({
                "endpointGuid": "473d1039-df00-3184-0eb0-b723168bce06",
                "eventTime": 1619600000 + i
            })
        if sequence >= 0:
            response["data"]["offset"] = sequence * count
        return json.dumps(response)

    def test_status(self):
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        status_response = transmission.status("search_id")
        self.assertTrue(status_response["success"])
        self.assertEqual(status_response["status"], "COMPLETED")
        self.assertEqual(status_response["progress"], 100)

    def test_delete(self):
        transmission = StixTransmission("trendmicro_vision_one", CONNECTION, CONFIG)
        status_response = transmission.delete("search_id")
        self.assertTrue(status_response["success"])
