from stix_shifter_modules.proofpoint.entry_point import EntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
import unittest


class TestProofpointConnection(unittest.TestCase, object):

    def connection(self):
        return {
            "host": "host",
            "port": 8080,
        }

    def configuration(self):
        return {
            "auth": {
                "principal": "principal",
                "secret": "secret"
            }
        }

    def test_proofpoint_query(self):
        entry_point = EntryPoint(self.connection(), self.configuration())
        query = "placeholder query text"
        query_response = entry_point.create_query_connection(query)

        assert query_response['search_id'] == query

    def test_proofpoint_status(self):
        entry_point = EntryPoint(self.connection(), self.configuration())
        query_id = "placeholder query text"
        status_response = entry_point.create_status_connection(query_id)

        success = status_response["success"]
        assert success
        status = status_response["status"]
        assert status == Status.COMPLETED.value

    def test_proofpoint_results(self):
        entry_point = EntryPoint(self.connection(), self.configuration())
        query_id = 'sinceSeconds=3600'
        results_response = entry_point.create_results_connection(query_id, 1, 1)

        success = results_response["success"]
        assert success

    def test_ping(self):
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True