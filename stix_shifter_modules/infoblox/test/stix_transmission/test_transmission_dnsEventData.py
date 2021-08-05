# -*- coding: utf-8 -*-
import json
import unittest
from unittest.mock import patch

from stix_shifter.stix_transmission.stix_transmission import StixTransmission

from stix_shifter_modules.infoblox.entry_point import EntryPoint

from .utils import MockResponse, CONNECTION, CONFIG, MODULE


class TestTransmission(unittest.TestCase):
    def get_dialect(self):
        return "dnsEventData"

    ###############################
    ## RESULTS - dnsEventData
    ###############################
    def _get_query(self):
        query = {
            "offset": 0,
            "fields": [],
            "from": 1587892612,
            "to": 1592382065,
            "source": self.get_dialect(),
            "query": "hostName:*"
        }

        return json.dumps(query)

    @staticmethod
    def _get_response(count=1):
        response = {"result": []}
        for i in range(0, count):
            response["result"].append({
                "qip": "1.1.1.1"
            })

        return json.dumps(response)

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_invalid_param(self, mock_query):
        payload = {
            "error": [{"message": "Invalid arguments, t0/t1 are required parameters"}]
        }
        mock_query.side_effect = [MockResponse(400, json.dumps(payload))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 0, 10)
        self.assertEqual(results_response, {
            "code": "invalid_parameter",
            "error": payload["error"][0]["message"],
            "success": False
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_auth_failure(self, mock_query):
        payload = '<html><head><title>401 Authorization Required</title></head><body><center><h1>401 Authorization Required</h1></center><hr><center>nginx</center></body></html>'
        mock_query.side_effect = [MockResponse(401, payload)]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 0, 10)
        self.assertEqual(results_response, {
            "code": "authentication_fail",
            "error": payload,
            "success": False
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_no_results(self, mock_query):
        payload = {
            "result": [],
            "status_code": "200"
        }
        mock_query.side_effect = [MockResponse(200, json.dumps(payload))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 0, 10)
        self.assertEqual(results_response, {'data': [], 'success': True})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_all_results(self, mock_query):
        payload = {
            "result": [
                {"qip": "1.1.1.1"},
                {"qip": "1.1.1.2"}
            ],
            "status_code": "200"
        }
        mock_query.side_effect = [
                MockResponse(200, json.dumps(payload))
            ]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 0, 1)
        self.assertEqual(results_response, {
            "success": True,
            "data": [
                {"dnsEventData": {"qip": "1.1.1.1"}}
            ]
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_max_fetch(self, mock_query):
        mock_query.side_effect = [
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.1"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.2"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.3"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.4"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.5"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.6"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.7"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.8"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.9"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.10"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.11"}]}))
            ]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 0, 20)
        self.assertEqual(results_response, {
            "success": True,
            "data": [
                {"dnsEventData": {"qip": "1.1.1.1"}},
                {"dnsEventData": {"qip": "1.1.1.2"}},
                {"dnsEventData": {"qip": "1.1.1.3"}},
                {"dnsEventData": {"qip": "1.1.1.4"}},
                {"dnsEventData": {"qip": "1.1.1.5"}},
                {"dnsEventData": {"qip": "1.1.1.6"}},
                {"dnsEventData": {"qip": "1.1.1.7"}},
                {"dnsEventData": {"qip": "1.1.1.8"}},
                {"dnsEventData": {"qip": "1.1.1.9"}},
                {"dnsEventData": {"qip": "1.1.1.10"}}
            ]
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_too_many_results(self, mock_query):
        mock_query.side_effect = [
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.1"}, {"qip": "1.1.1.2"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.3"}, {"qip": "1.1.1.4"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.5"}, {"qip": "1.1.1.6"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.7"}, {"qip": "1.1.1.8"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.9"}, {"qip": "1.1.1.10"}]}))
            ]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 0, 4)
        self.assertEqual(results_response, {
            "success": True,
            "data": [
                {"dnsEventData": {"qip": "1.1.1.1"}},
                {"dnsEventData": {"qip": "1.1.1.2"}},
                {"dnsEventData": {"qip": "1.1.1.3"}},
                {"dnsEventData": {"qip": "1.1.1.4"}}
            ]
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_min_range(self, mock_query):
        mock_query.side_effect = [
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.5"}, {"qip": "1.1.1.6"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.7"}, {"qip": "1.1.1.8"}]})),
                MockResponse(200, json.dumps({"result": [{"qip": "1.1.1.9"}, {"qip": "1.1.1.10"}]}))
            ]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 4, 3)
        self.assertEqual(results_response, {
            "success": True,
            "data": [
                {"dnsEventData": {"qip": "1.1.1.5"}},
                {"dnsEventData": {"qip": "1.1.1.6"}},
                {"dnsEventData": {"qip": "1.1.1.7"}}
            ]
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_different_offsets(self, mock_results):
        mocks = [
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500))),
            (MockResponse(200, self._get_response(500)))
        ]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(), 0, 200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 200)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(), 0, 500)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 500)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(), 0, 1200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 1200)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(), 99, 200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 200)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(), 99, 500)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 500)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(), 99, 1200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 1200)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(), 600, 100)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 100)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(), 0, 5000)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 5000)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(), 0, 10000)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 5000)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(), 5000, 10000)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 5000)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(), 4999, 1)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 1)

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_exception(self, mock_ping):
        mock_ping.side_effect = ConnectionError("Failed to establish a new connection")
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 4, 3)
        self.assertEqual(results_response, {
            "success": False,
            "error": "Failed to establish a new connection",
            "code": "unknown"
        })
