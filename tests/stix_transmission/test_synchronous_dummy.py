from stix_shifter_modules.synchronous_dummy.entry_point import EntryPoint
import unittest

CONNECTION = {"host": "hostbla",  "port": "8080",  "path": "/"}


class TestSynchronousDummyConnection(unittest.TestCase, object):
    def test_is_async(self):
        entry_point = EntryPoint()
        check_async = entry_point.is_async()
        assert check_async == False

    def test_ping(self):
        entry_point = EntryPoint(CONNECTION, None)
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True

    def test_dummy_sync_results(self):
        entry_point = EntryPoint(CONNECTION, None)
        results_response = entry_point.create_results_connection("some query", 1, 1)
        response_code = results_response["success"]
        query_results = results_response["data"]

        assert response_code is True
        assert query_results == "Results from search"
