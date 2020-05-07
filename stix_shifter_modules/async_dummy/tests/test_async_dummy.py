from stix_shifter_modules.async_dummy.entry_point import EntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
import unittest


class TestAsyncDummyConnection(unittest.TestCase, object):
    def test_dummy_async_query(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }
        entry_point = EntryPoint(connection, None)
        query = "placeholder query text"
        query_response = entry_point.create_query_connection(query)

        assert query_response['search_id'] == "uuid_1234567890"

    def test_dummy_async_status(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }
        entry_point = EntryPoint(connection, None)
        query_id = "uuid_1234567890"
        status_response = entry_point.create_status_connection(query_id)

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
        entry_point = EntryPoint(connection, None)
        query_id = "uuid_1234567890"
        results_response = entry_point.create_results_connection(query_id, 1, 1)

        success = results_response["success"]
        assert success == True
        data = results_response["data"]
        assert data == "Results from search"

    def test_is_async(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }
        entry_point = EntryPoint(connection, None)
        check_async = entry_point.is_async()
        assert check_async

    def test_ping(self):
        connection = {
            "host": "hostbla",
            "port": "8080",
            "path": "/"
        }

        entry_point = EntryPoint(connection, None)
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True
