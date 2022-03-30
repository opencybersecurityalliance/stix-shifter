from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode
import unittest
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
    
    def test_query_from_multiple_observation_expressions(self):
        stix_pattern = "[x-proofpoint:threatstatus = 'active'] AND [x-proofpoint:threatstatus = 'cleared'] START t'2021-09-29T06:00:00.00Z' STOP t'2021-09-29T06:30:00.00Z'"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["threatStatus=active&threatStatus=cleared&interval=2021-09-29T06:00:00.00Z/2021-09-29T06:30:00.00Z"]
        _test_query_assertions(query, queries)

    def test_query_unmapped_attribute_combined_comparison(self):
        stix_pattern = "[x-proofpoint:threatstatus = 'active' AND x-proofpoint:threatstatus = 'cleared' AND unmapped:attribute = 'something']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        assert query['success'] == False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == query['code']
        assert "data mapping error : Unable to map the following STIX objects and properties: ['unmapped:attribute'] to data source fields" in query['error']

    def test_query_unmapped_attribute(self):
        stix_pattern = "[ipv4-addr:value = '127.0.0.1'] START t'2021-09-29T06:00:00.00Z' STOP t'2021-09-29T06:30:00.00Z'"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["interval=2021-09-29T06:00:00.00Z/2021-09-29T06:30:00.00Z"]
        _test_query_assertions(query, queries)

    def test_query_unmapped_attribute_combined_observation(self):
        stix_pattern = "[ipv4-addr:value = '127.0.0.1'] OR [x-proofpoint:threatstatus ='active'] START t'2021-09-29T06:00:00.00Z' STOP t'2021-09-29T06:30:00.00Z'"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ["threatStatus=active&interval=2021-09-29T06:00:00.00Z/2021-09-29T06:30:00.00Z"]
        _test_query_assertions(query, queries)