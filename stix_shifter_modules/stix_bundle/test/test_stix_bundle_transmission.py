import unittest
import json

from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_modules.stix_bundle.entry_point import EntryPoint
from stix_shifter.stix_transmission.stix_transmission import run_in_thread

class TestSTIXBundleConnector(unittest.TestCase, object):
    configuration = {
        "auth": {
            "username": "",
            "password": ""
        }
    }

    connection = {
        'url': 'https://raw.githubusercontent.com/opencybersecurityalliance/stix-shifter/develop/data/cybox/qradar/qradar_observed_2000.json'
    }

    def test_ping(self):
        entry_point = EntryPoint(self.connection, self.configuration)
        ping_result = run_in_thread(entry_point.ping_connection)
        assert ping_result["success"] is True
        assert False

    def test_ping_failure(self):
        connection = {
            'url': 'https://invalid_host.com/org/master/data/bundle.json'
        }
        entry_point = EntryPoint(connection, self.configuration)
        ping_result = run_in_thread(entry_point.ping_connection)

        assert ping_result["success"] is False
        assert ping_result["code"] == 'service_unavailable'

    def test_query(self):
        query = "[ipv4-addr:value = '9.28.234.169'] START t'2020-09-30T16:24:59.988Z' STOP t'2020-09-30T16:25:59.988Z'"
        transmission = stix_transmission.StixTransmission("stix_bundle", self.connection, self.configuration)
        query_response = transmission.query(query)
        self.assertTrue(query_response["success"])
        self.assertEqual(query_response["search_id"], query)
    
    
    def test_status(self):
        transmission = stix_transmission.StixTransmission("stix_bundle", self.connection, self.configuration)
        status_response = transmission.status("search_id")
        self.assertTrue(status_response["success"])
        self.assertEqual(status_response["status"], "COMPLETED")
        self.assertEqual(status_response["progress"], 100)
    
    def test_results(self):
        result_file = open('stix_shifter_modules/stix_bundle/test/qradar_observed_2000.json', 'r').read()
        data = json.loads(result_file)
        result_bundle_objects = data['objects']
        observed_data = result_bundle_objects[1]

        transmission = stix_transmission.StixTransmission('stix_bundle', self.connection, self.configuration)
        results_response = transmission.results("[ipv4-addr:value = '9.28.234.169'] START t'2020-09-30T16:24:59.988Z' STOP t'2020-09-30T16:25:59.988Z'", 0, 1)
        assert results_response["success"] is True
        assert results_response["data"] == [observed_data]