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
        query_interface = async_dummy_connector.Connector(connection, None)

        query = "placeholder query text"

        query_response = query_interface.create_query_connection(query)
        query_id = query_response['query_id']

        assert query_id == "uuid_1234567890"

    def test_dummy_async_status(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }
        status_interface = async_dummy_connector.Connector(connection, None)

        query_id = "uuid_1234567890"

        status_response = status_interface.create_status_connection(query_id)
        status = status_response["status"]
        assert status == Status.COMPLETED.value

    def test_dummy_async_results_error(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }
        results_interface = async_dummy_connector.Connector(connection, None)

        query_id = "uuid_should_error"
        offset = 0
        length = 1
        results_response = results_interface.create_results_connection(query_id, offset, length)

        success = results_response["success"]
        assert success is not True
        query_results = results_response["error"]
        assert query_results == "Error: query results not found"

    def test_dummy_async_results_running(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }
        results_interface = async_dummy_connector.Connector(connection, None)

        query_id = "uuid_not_done"
        offset = 0
        length = 1
        results_response = results_interface.create_results_connection(query_id, offset, length)

        query_results = results_response["error"]
        success = results_response["success"]
        assert success is not True
        assert query_results == "Query is not finished processing"

    def test_dummy_async_results_success(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }
        results_interface = async_dummy_connector.Connector(connection, None)

        query_id = "uuid_1234567890"
        offset = 0
        length = 1

        results_response = results_interface.create_results_connection(query_id, offset, length)
        query_results = results_response["data"]

        success = results_response["success"]
        assert success
        assert query_results

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
