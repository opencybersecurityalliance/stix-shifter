from stix_shifter.stix_transmission.src.modules.synchronous_dummy import synchronous_dummy_connector
import unittest

CONNECTION = {"host": "hostbla",  "port": "8080",  "path": "/"}


class TestSynchronousDummyConnection(unittest.TestCase, object):
    def test_is_async(self):
        module = synchronous_dummy_connector
        check_async = module.Connector(CONNECTION, None).is_async
        assert check_async == False

    def test_ping(self):
        interface = synchronous_dummy_connector.Connector(CONNECTION, None)
        ping_result = interface.ping()
        assert ping_result["success"] is True

    def test_dummy_sync_results(self):
        interface = synchronous_dummy_connector.Connector(CONNECTION, None)
        results_response = interface.create_results_connection("some query", 1, 1)
        response_code = results_response["success"]
        query_results = results_response["data"]

        assert response_code is True
        assert query_results == "Results from search"
