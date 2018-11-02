from stix_transmission.src.modules.synchronous_dummy import synchronous_dummy_connector
from stix_transmission.src.modules.synchronous_dummy import synchronous_dummy_results_connector
from stix_transmission.src.modules.synchronous_dummy import synchronous_dummy_ping
import unittest


class TestSynchronousDummyConnection(unittest.TestCase, object):
    def test_is_async(self):
        module = synchronous_dummy_connector
        check_async = module.Connector().is_async
        assert check_async == False

    def test_ping(self):
        ping_interface = synchronous_dummy_ping.SynchronousDummyPing()
        ping_result = ping_interface.ping()

        assert ping_result == "synchronous ping"

    def test_dummy_sync_results(self):
        results_interface = synchronous_dummy_results_connector.SynchronousDummyResultsConnector()
        options = {}
        params = {
            "config": {
                "port": 443,
                "ip": "127.0.0.1",
                "host": "localhost",
                "path": "/async_dummy/query_path"
            },
            "query": "placeholder query text"
        }

        results_response = results_interface.create_results_connection(params, options)
        response_code = results_response["response_code"]
        query_results = results_response["query_results"]

        assert response_code == 200
        assert isinstance(query_results, dict)
