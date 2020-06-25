from stix_shifter_modules.db2.entry_point import EntryPoint
import unittest


connection = {
    "host": "locahost", 
    "port": "3306"
}

config =  {
    "auth": {
        "mysql_username": "admin","mysql_password": "admin", 
        "mysql_hostname": "localhost", 
        "mysql_database": "port" 
    }  
}

class Testdb2Connection(unittest.TestCase, object):
    def test_query(self):
        entry_point = EntryPoint(connection, config)
        query = "SELECT * FROM INSERT_TABLE"
        query_response = entry_point.create_query_connection(query)
        response_code = query_response["success"]
        response_search = query_response["search_id"]

        assert response_code is True
        assert response_search == query

    def test_is_async(self):
        entry_point = EntryPoint()
        check_async = entry_point.is_async()
        assert check_async == False

    def test_ping(self):
        entry_point = EntryPoint(connection, config)
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True

    def test_mysql_results(self):
        entry_point = EntryPoint(connection, config)
        query = "SELECT * FROM INSERT_TABLE WHERE INSERT_COLUMN='INSERT_VALUE'"
        results_response = entry_point.create_results_connection(query, 1, 1)
        response_code = results_response["success"]
        query_results = results_response["data"]
        res = query_results[0]
        expected_result = "INSERT_EXPECTED_RESULT"
        assert response_code is True
        assert res["INSERT_COLUMN"] == expected_result # Change query results to output from query_results.
