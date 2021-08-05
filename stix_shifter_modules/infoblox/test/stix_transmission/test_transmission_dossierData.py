# -*- coding: utf-8 -*-
import json
import unittest
from unittest.mock import patch

from stix_shifter.stix_transmission.stix_transmission import StixTransmission

from stix_shifter_modules.infoblox.entry_point import EntryPoint

from .utils import MockResponse, CONNECTION, CONFIG, MODULE


class TestTransmission(unittest.TestCase):
    def get_dialect(self):
        return "dossierData"

    ###############################
    ## RESULTS - dossierData
    ###############################
    def _get_query(self, threat_type=None):
        query = {
            "offset": 0,
            "fields": [],
            "from": 1587892612,
            "to": 1592382065,
            "source": self.get_dialect(),
            "query": "hostName:*"
        }

        if threat_type:
            query["threat_type"] = threat_type

        return json.dumps(query)

    @staticmethod
    def _get_response(count=1):
        response = {
            "status": "success",
            "job": {
                "create_time": "2021-08-01T20:55:48.542Z"
            },
            "results": [
                {
                    "status": "success",
                    "data": {
                        "duration": 243602755,
                        "items": []
                    }
                }
            ]
        }

        for i in range(0, count):
            response["results"][0]["data"]["items"].append({
                "Hostname": "example-{}.com".format(i),
                "Last_Seen": 1619600000 + i
            })

        return json.dumps(response)

    def test_results_missing_threat_type(self):
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 0, 10)
        self.assertEqual(results_response, {'code': 'unknown', 'error': "'threat_type'", 'success': False})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_invalid_param(self, mock_query):
        payload = {
            "status": "error",
            "error": "unknown target type"
        }
        mock_query.side_effect = [MockResponse(400, json.dumps(payload))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(threat_type="unknown_type"), 0, 10)
        self.assertEqual(results_response, {
            'code': 'invalid_parameter',
            'error': 'unknown target type',
            'success': False
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_auth_failure(self, mock_query):
        payload = '<html><head><title>401 Authorization Required</title></head><body><center><h1>401 Authorization Required</h1></center><hr><center>nginx</center></body></html>'
        mock_query.side_effect = [MockResponse(401, payload)]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(threat_type="unknown_type"), 0, 10)
        self.assertEqual(results_response, {
            'code': 'authentication_fail',
            'error': payload,
            'success': False
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_no_results_1(self, mock_query):
        payload = {
            "status": "success",
            "job": {
                "create_time": "2021-08-01T20:55:48.542Z"
            },
            "results": []
        }
        mock_query.side_effect = [MockResponse(200, json.dumps(payload))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(threat_type="host"), 0, 10)
        self.assertEqual(results_response, {'data': [], 'success': True})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_no_results_2(self, mock_query):
        payload = {
            "status": "success",
            "job": {
                "create_time": "2021-08-01T20:55:48.542Z"
            },
            "results": [
                {
                    "status": "success",
                    "data": {
                        "duration": 243602755,
                        "items": []
                    }
                }
            ]
        }
        mock_query.side_effect = [MockResponse(200, json.dumps(payload))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(threat_type="host"), 0, 10)
        self.assertEqual(results_response, {'data': [], 'success': True})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_all_results(self, mock_query):
        payload = {
            "status": "success",
            "job": {
                "create_time": "2021-08-01T20:55:48.542Z"
            },
            "results": [
                {
                    "status": "success",
                    "data": {
                        "duration": 243602755,
                        "items": [
                            {
                                "Domain": "",
                                "Hostname": "example.com",
                                "IP": "1.1.1.1",
                                "Last_Seen": 1627808194,
                                "NameServer": "",
                                "Record_Type": "A"
                            }
                        ]
                    }
                }
            ]
        }
        mock_query.side_effect = [MockResponse(200, json.dumps(payload))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(threat_type="host"), 0, 10)
        self.assertEqual(results_response, {
            "success": True,
            "data": [
                {
                    "dossierData": {
                        "job": {"create_time": "2021-08-01T20:55:48.542Z"},
                        "results": [{"data": {"items": [{
                            "Domain": "",
                            "Hostname": "example.com",
                            "IP": "1.1.1.1",
                            "Last_Seen": 1627808194,
                            "NameServer": "",
                            "Record_Type": "A"
                        }]}}]
                    }
                }]})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_too_many_results(self, mock_query):
        payload = {
            "status": "success",
            "job": {
                "create_time": "2021-08-01T20:55:48.542Z"
            },
            "results": [
                {
                    "status": "success",
                    "data": {
                        "duration": 243602755,
                        "items": [
                            {"Hostname": "example.com", "IP": "1.1.1.1"},
                            {"Hostname": "example.com", "IP": "1.1.1.2"},
                            {"Hostname": "example.com", "IP": "1.1.1.3"},
                            {"Hostname": "example.com", "IP": "1.1.1.4"},
                            {"Hostname": "example.com", "IP": "1.1.1.5"}
                        ]
                    }
                }
            ]
        }
        mock_query.side_effect = [MockResponse(200, json.dumps(payload))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(threat_type="host"), 0, 2)
        self.assertEqual(results_response, {
            "success": True,
            "data": [
                {
                    "dossierData": {
                        "job": {"create_time": "2021-08-01T20:55:48.542Z"},
                        "results": [{"data": {"items": [{"Hostname": "example.com", "IP": "1.1.1.1"}]}}]
                    }
                },
                {
                    "dossierData": {
                        "job": {"create_time": "2021-08-01T20:55:48.542Z"},
                        "results": [{"data": {"items": [{"Hostname": "example.com", "IP": "1.1.1.2"}]}}]
                    }
                }
            ]
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_min_range(self, mock_query):
        payload = {
            "status": "success",
            "job": {
                "create_time": "2021-08-01T20:55:48.542Z"
            },
            "results": [
                {
                    "status": "success",
                    "data": {
                        "duration": 243602755,
                        "items": [
                            {"Hostname": "example.com", "IP": "1.1.1.1"},
                            {"Hostname": "example.com", "IP": "1.1.1.2"},
                            {"Hostname": "example.com", "IP": "1.1.1.3"},
                            {"Hostname": "example.com", "IP": "1.1.1.4"},
                            {"Hostname": "example.com", "IP": "1.1.1.5"}
                        ]
                    }
                }
            ]
        }
        mock_query.side_effect = [MockResponse(200, json.dumps(payload))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(threat_type="host"), 4, 10)
        self.assertEqual(results_response, {
            "success": True,
            "data": [
                {
                    "dossierData": {
                        "job": {"create_time": "2021-08-01T20:55:48.542Z"},
                        "results": [{"data": {"items": [{"Hostname": "example.com", "IP": "1.1.1.5"}]}}]
                    }
                }
            ]
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_different_offsets(self, mock_results):
        mocks = [
            (MockResponse(200, self._get_response(1000))),
        ]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(threat_type="host"), 0, 200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 200)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(threat_type="host"), 0, 500)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 500)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(threat_type="host"), 0, 1200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 1000)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(threat_type="host"), 99, 200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 200)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(threat_type="host"), 99, 500)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 500)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(threat_type="host"), 99, 1200)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 901)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(threat_type="host"), 600, 100)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 100)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(threat_type="host"), 0, 5000)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 1000)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(threat_type="host"), 0, 10000)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 1000)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(threat_type="host"), 5000, 10000)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 0)

        mock_results.side_effect = mocks
        result_response = transmission.results(self._get_query(threat_type="host"), 999, 1)
        self.assertTrue(result_response["success"])
        self.assertEqual(len(result_response["data"]), 1)

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_exception(self, mock_ping):
        mock_ping.side_effect = ConnectionError("Failed to establish a new connection")
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(threat_type="host"), 4, 3)
        self.assertEqual(results_response, {
            "success": False,
            "error": "Failed to establish a new connection",
            "code": "unknown"
        })
