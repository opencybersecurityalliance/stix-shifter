from stix_shifter_modules.proofpoint.entry_point import EntryPoint
from stix_shifter_utils.modules.base.stix_transmission.base_status_connector import Status
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode
import unittest
import datetime
import re


MODULE = "proofpoint"
translation = stix_translation.StixTranslation()

def _test_query_assertions(translated_query, test_query):
    assert translated_query['queries'] == test_query

def _remove_timestamp_from_query(queries):
    pattern = r'\s*AND\s*\(\@timestamp:\["\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z"\s*TO\s*"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z"\]\)'
    if isinstance(queries, list):
        return [re.sub(pattern, "", query) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, "", queries)


class TestProofpointConnection(unittest.TestCase, object):

    def connection(self):
        return {
            "host": "tap-api-v2.proofpoint.com/v2/siem",
            "port": 8080,
        }

    def configuration(self):
        return {
            "auth": {
                "principal": "96dbfb1e-e6bf-f298-3080-3cab5b1cfe19",
                "secret": "1ee4776401dc372e608cb9ae4810cec5420c2689ff38befa1ac46bd17da20904"
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

class TestStixtoQuery(unittest.TestCase, object):

    def test_url_params_query(self):
        stix_pattern = "[x-proofpoint:threatstatus = 'active'] START t'2021-09-29T06:00:00.00Z' STOP t'2021-09-29T06:30:00.00Z'"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["threatStatus=active&interval=2021-09-29T06:00:00.00Z/2021-09-29T06:30:00.00Z"]
        _test_query_assertions(query, queries)

    def test_default_timerange_query(self):
        stix_pattern = "[x-proofpoint:threatstatus = 'active']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["threatStatus=active&interval=2021-09-29T06:00:00.00Z/2021-09-29T06:30:00.00Z"]
        assert "threatStatus=active" in queries[0]
        assert "interval" in queries[0]

    def test_query_from_multiple_comparison_expressions(self):
        stix_pattern = "[x-proofpoint:threatstatus = 'active' AND x-proofpoint:threatstatus = 'cleared'] START t'2021-09-29T06:00:00.00Z' STOP t'2021-09-29T06:30:00.00Z'"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["threatStatus=cleared&threatStatus=active&interval=2021-09-29T06:00:00.00Z/2021-09-29T06:30:00.00Z"]
        _test_query_assertions(query, queries)

    def test_query_unmapped_attribute(self):
        stix_pattern = "[x-proofpoint:threatstatus = 'active' AND x-proofpoint:threatstatus = 'cleared' AND unmapped:attribute = 'something']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        assert query['success'] == False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == query['code']
        assert 'Unable to map the following STIX objects and properties to data source fields' in query['error']
