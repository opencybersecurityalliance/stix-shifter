from stix_shifter_modules.proofpoint.entry_point import EntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode
import unittest
import datetime
import re


translation = stix_translation.StixTranslation()

def _test_query_assertions(translated_query, test_query):
    assert translated_query['queries'] == test_query

def _remove_timestamp_from_query(queries):
    pattern = r'\s*AND\s*\(\@timestamp:\["\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z"\s*TO\s*"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z"\]\)'
    if isinstance(queries, list):
        return [re.sub(pattern, "", query) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, "", queries)


class TestAsyncDummyConnection(unittest.TestCase, object):

    def connection(self):
        return {
            "host": "hostbla",
            "port": 8080,
        }

    def configuration(self):
        return {
            "auth": {
                "username": "u",
                "password": "p"
            }
        }

    def test_dummy_async_query(self):
        entry_point = EntryPoint(self.connection(), self.configuration())
        query = "placeholder query text"
        query_response = entry_point.create_query_connection(query)

        assert query_response['search_id'] == "uuid_1234567890"

    def test_dummy_async_status(self):
        entry_point = EntryPoint(self.connection(), self.configuration())
        query_id = "uuid_1234567890"
        status_response = entry_point.create_status_connection(query_id)

        success = status_response["success"]
        assert success
        status = status_response["status"]
        assert status == Status.COMPLETED.value

    def test_dummy_async_results(self):
        entry_point = EntryPoint(self.connection(), self.configuration())
        # query_id = "uuid_1234567890"
        query_id = 'all?format=syslog&sinceSeconds=3600'
        results_response = entry_point.create_results_connection(query_id, 1, 1)
        print('results_response :', results_response)

        success = results_response["success"]
        assert success
        data = results_response["data"]
        # assert data == "Results from search"

    def test_is_async(self):
        entry_point = EntryPoint(self.connection(), self.configuration())
        check_async = entry_point.is_async()
        assert check_async

    def test_ping(self):
        entry_point = EntryPoint(self.connection(), self.configuration())
        ping_result = entry_point.ping_connection()
        assert ping_result["success"] is True

class TestStixtoQuery(unittest.TestCase, object):

    def test_query(self):
        stix_pattern = "[threatStatus:value = 'active' OR threatStatus:value = 'positive' OR threatStatus:value = 'falsepositive'] START t'2021-09-15T16:13:00.00Z' STOP t'2021-09-15T17:13:00.00Z'"
        stix_pattern = "[threatStatus:value = 'active'] START t'2021-08-22T07:24:00.000Z' STOP t'2022-08-22T08:20:00.000Z'"
        translated_query = translation.translate('proofpoint', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['hreatStatus=active&interval=2021-08-22T07:24:00.000Z/2022-08-22T08:20:00.000Z']
        _test_query_assertions(translated_query, test_query)
