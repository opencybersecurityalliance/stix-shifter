from stix_shifter.stix_transmission.src.modules.synchronous_dummy import synchronous_dummy_connector
import unittest


class TestSynchronousDummyConnection(unittest.TestCase, object):
    def test_is_async(self):
        module = synchronous_dummy_connector
        check_async = module.Connector().is_async
        assert check_async == False

    def test_ping(self):
        interface = synchronous_dummy_connector.Connector()
        ping_result = interface.ping()
        assert ping_result == "synchronous ping"

    def test_dummy_sync_results(self):
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

        interface = synchronous_dummy_connector.Connector()
        results_response = interface.create_results_connection(params, options)
        response_code = results_response["response_code"]
        query_results = results_response["query_results"]

        assert response_code == 200
        assert isinstance(query_results, dict)
