# -*- coding: utf-8 -*-
import json
import unittest
from unittest.mock import patch

from stix_shifter.stix_transmission.stix_transmission import StixTransmission

from stix_shifter_modules.infoblox.entry_point import EntryPoint

from .utils import MockResponse, CONNECTION, CONFIG, MODULE


class TestTideDbTransmission(unittest.TestCase):
    def get_dialect(self):
        return "tideDbData"

    ###############################
    ## RESULTS - tideDbData
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
        response = {"threat": []}
        for i in range(0, count):
            response["threat"].append({
                "ip": "1.1.1.1"
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
    def test_results_no_results(self, mock_query):
        payload = {
            "threat": []
        }
        mock_query.side_effect = [MockResponse(200, json.dumps(payload))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(threat_type="host"), 0, 10)
        self.assertEqual(results_response, {'data': [], 'success': True})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_all_results(self, mock_query):
        payload = {
            "threat": [
                {
                    "id": "1af2936f-9d33-11eb-8943-6962d4bdf9de",
                    "type": "HOST",
                    "host": "1-lntesasanpaolo-portaleweb.xyz",
                    "domain": "1-lntesasanpaolo-portaleweb.xyz",
                    "tld": "xyz",
                    "profile": "IID",
                    "property": "Phishing_Generic",
                    "class": "Phishing",
                    "threat_level": 100,
                    "confidence": 100,
                    "detected": "2021-04-14T15:04:26.116Z",
                    "received": "2021-04-14T15:07:18.592Z",
                    "imported": "2021-04-14T15:07:18.592Z",
                    "expiration": "2022-04-14T15:04:26.116Z",
                    "dga": False,
                    "up": True,
                    "batch_id": "1af24549-9d33-11eb-8943-6962d4bdf9de",
                    "threat_score": 6,
                    "threat_score_rating": "Medium",
                    "threat_score_vector": "TSIS:1.0/AV:N/AC:L/PR:L/UI:R/EX:H/MOD:N/AVL:N/CI:N/ASN:N/TLD:H/DOP:N/P:F",
                    "confidence_score": 8.2,
                    "confidence_score_rating": "High",
                    "confidence_score_vector": "COSIS:1.0/SR:H/POP:N/TLD:H/CP:F",
                    "risk_score": 7.9,
                    "risk_score_rating": "High",
                    "risk_score_vector": "RSIS:1.0/TSS:M/TLD:H/CVSS:L/EX:H/MOD:N/AVL:N/T:M/DT:L",
                    "extended": {
                        "cyberint_guid": "dadbdde3eaf7fd97bae0bdec8c6ceb07"
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
                    "tideDbData": {
                        "id": "1af2936f-9d33-11eb-8943-6962d4bdf9de",
                        "type": "HOST",
                        "host": "1-lntesasanpaolo-portaleweb.xyz",
                        "domain": "1-lntesasanpaolo-portaleweb.xyz",
                        "tld": "xyz",
                        "profile": "IID",
                        "property": "Phishing_Generic",
                        "class": "Phishing",
                        "threat_level": 100,
                        "confidence": 100,
                        "detected": "2021-04-14T15:04:26.116Z",
                        "received": "2021-04-14T15:07:18.592Z",
                        "imported": "2021-04-14T15:07:18.592Z",
                        "expiration": "2022-04-14T15:04:26.116Z",
                        "dga": False,
                        "up": True,
                        "batch_id": "1af24549-9d33-11eb-8943-6962d4bdf9de",
                        "threat_score": 6,
                        "threat_score_rating": "Medium",
                        "threat_score_vector": "TSIS:1.0/AV:N/AC:L/PR:L/UI:R/EX:H/MOD:N/AVL:N/CI:N/ASN:N/TLD:H/DOP:N/P:F",
                        "confidence_score": 8.2,
                        "confidence_score_rating": "High",
                        "confidence_score_vector": "COSIS:1.0/SR:H/POP:N/TLD:H/CP:F",
                        "risk_score": 7.9,
                        "risk_score_rating": "High",
                        "risk_score_vector": "RSIS:1.0/TSS:M/TLD:H/CVSS:L/EX:H/MOD:N/AVL:N/T:M/DT:L",
                        "extended": {
                            "cyberint_guid": "dadbdde3eaf7fd97bae0bdec8c6ceb07"
                        }
                    }
                }
            ]
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_too_many_results(self, mock_query):
        payload = {
            "threat": [
                {"ip": "1.1.1.1"},
                {"ip": "1.1.1.2"},
                {"ip": "1.1.1.3"},
                {"ip": "1.1.1.4"},
                {"ip": "1.1.1.5"}
            ]
        }
        mock_query.side_effect = [MockResponse(200, json.dumps(payload))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(threat_type="host"), 0, 2)

        print("\n\n\n\nresult")
        print(results_response)
        self.assertEqual(results_response, {
            "success": True,
            "data": [
                {"tideDbData": {"ip": "1.1.1.1"}},
                {"tideDbData": {"ip": "1.1.1.2"}}
            ]
        })

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_results_min_range(self, mock_query):
        payload = {
            "threat": [
                {"ip": "1.1.1.1"},
                {"ip": "1.1.1.2"},
                {"ip": "1.1.1.3"},
                {"ip": "1.1.1.4"},
                {"ip": "1.1.1.5"}
            ]
        }
        mock_query.side_effect = [MockResponse(200, json.dumps(payload))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(threat_type="host"), 4, 10)
        self.assertEqual(results_response, {
            "success": True,
            "data": [
                {"tideDbData": {"ip": "1.1.1.5"}}
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
