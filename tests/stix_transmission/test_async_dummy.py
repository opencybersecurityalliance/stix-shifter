from stix_shifter.stix_transmission.src.modules.async_dummy import async_dummy_connector
from stix_shifter.stix_transmission.src.modules.base.base_status_connector import Status
import unittest


class TestAsyncDummyConnection(unittest.TestCase, object):
    def test_dummy_async_query(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }
        interface = async_dummy_connector.Connector(connection, None)
        query = "placeholder query text"
        query_response = interface.create_query_connection(query)

        assert query_response['query_id'] == "uuid_1234567890"
        assert query_response['code'] == 200

    def test_dummy_async_status(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }
        interface = async_dummy_connector.Connector(connection, None)
        query_id = "uuid_1234567890"
        status_response = interface.create_status_connection(query_id)

        success = status_response["success"]
        assert success == True
        status = status_response["status"]
        assert status == Status.COMPLETED.value

    def test_dummy_async_results(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }
        interface = async_dummy_connector.Connector(connection, None)
        query_id = "uuid_1234567890"
        results_response = interface.create_results_connection(query_id, 1, 1)

        success = results_response["success"]
        assert success == True
        data = results_response["data"]
        assert data == "Results for search"

    def test_is_async(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }
        check_async = async_dummy_connector.Connector(connection, None).is_async
        assert check_async

    def test_ping(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }

        interface = async_dummy_connector.Connector(connection, None)
        ping_result = interface.ping()
        assert ping_result == "async ping"
