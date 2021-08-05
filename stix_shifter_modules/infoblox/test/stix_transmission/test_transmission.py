# -*- coding: utf-8 -*-
import json
import unittest
from unittest.mock import patch

from stix_shifter.stix_transmission.stix_transmission import StixTransmission

from stix_shifter_modules.infoblox.entry_point import EntryPoint

from .utils import MockResponse, CONNECTION, CONFIG, MODULE


class TestTransmission(unittest.TestCase):
    def test_is_async(self):
        entry_point = EntryPoint(CONNECTION, CONFIG)
        check_async = entry_point.is_async()
        self.assertFalse(check_async)

    ###############################
    ## PING
    ###############################
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping(self, mock_ping):
        response = {
            "threat": [
                {
                    "id": "3a7c0318-e985-11eb-93d6-438342be5508",
                    "type": "HOST",
                    "host": "xbug.uk.to"
                }
            ],
            "record_count": 1
        }
        mock_ping.side_effect = [MockResponse(200, json.dumps(response))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertEqual(ping_response, {'success': True})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_failure(self, mock_ping):
        response = {
            "error": [
                {
                    "message": "Invalid type hst --- type must be one of (host, ip, url, email, hash)"
                }
            ]
        }
        mock_ping.side_effect = [MockResponse(400, json.dumps(response))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertEqual(ping_response, {'code': 'invalid_parameter', 'error': "{'code': 400}", 'success': False})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_auth_failure(self, mock_ping):
        response = '<html><head><title>401 Authorization Required</title></head><body><center><h1>401 Authorization Required</h1></center><hr><center>nginx</center></body></html>'
        mock_ping.side_effect = [MockResponse(401, response)]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertEqual(ping_response, {'code': 'authentication_fail', 'error': "{'code': 401}", 'success': False})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_unknown_failure(self, mock_ping):
        response = {
            "error": {
                "code": "InternalError",
            }
        }
        mock_ping.side_effect = [MockResponse(503, json.dumps(response))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertEqual(ping_response, {'code': 'unknown', 'error': "{'code': 503}", 'success': False})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_unknown_code(self, mock_ping):
        response = {
            "error": {
                "code": "InternalError",
            }
        }
        mock_ping.side_effect = [MockResponse(None, json.dumps(response))]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertEqual(ping_response, {'code': 'unknown', 'error': "{'code': None}", 'success': False})

    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_ping_exception(self, mock_ping):
        mock_ping.side_effect = ConnectionError("Failed to establish a new connection")
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        ping_response = transmission.ping()
        self.assertEqual(ping_response, {'code': 'unknown', 'error': "Failed to establish a new connection", 'success': False})

    ###############################
    ## QUERY
    ###############################
    @patch('stix_shifter_utils.stix_transmission.utils.RestApiClient.RestApiClient.call_api')
    def test_query(self, mock_query):
        # tests QueryConnector.create_query_connection
        mock_query.side_effect = [MockResponse(200, self._get_query())]
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        query_response = transmission.query(self._get_query())
        self.assertEqual(query_response, {
            "success": True,
            "search_id": self._get_query()
        })

    ###############################
    ## RESULTS
    ###############################
    @staticmethod
    def _get_query(source="unknown_source", threat_type=None):
        query = {
            "offset": 0,
            "fields": [],
            "from": 1587892612,
            "to": 1592382065,
            "source": source,
            "query": "hostName:*"
        }

        if threat_type:
            query["threat_type"] = threat_type

        return json.dumps(query)

    def test_results_missing_source(self):
        # tests ResultsConnector.create_results_connection
        query = json.dumps({
            "offset": 0,
            "fields": [],
            "from": 1587892612,
            "to": 1592382065,
            "query": "hostName:*"
        })
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(query, 0, 10)
        self.assertEqual(results_response, {'code': 'unknown', 'error': "'source'", 'success': False})

    def test_results_unknown_source(self):
        # tests ResultsConnector.create_results_connection
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        results_response = transmission.results(self._get_query(), 0, 10)
        self.assertEqual(results_response, {'code': 'unknown', 'error': "Unknown source provided source=unknown_source", 'success': False})

    ###############################
    ## STATUS
    ###############################
    def test_status(self):
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        status_response = transmission.status("search_id")
        self.assertEqual(status_response, {'progress': 100, 'status': 'COMPLETED', 'success': True})

    ###############################
    ## DELETE
    ###############################
    def test_delete(self):
        transmission = StixTransmission(MODULE, CONNECTION, CONFIG)
        status_response = transmission.delete("search_id")
        self.assertEqual(status_response, {'success': True})
