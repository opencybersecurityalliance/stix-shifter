import unittest
from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()
MODULE = 'recorded_future'

def _test_query_assertions(query, queries):
    assert isinstance(query, dict) is True
    assert 'queries' in query
    assert query['queries'] == [queries]


class TestRecordedFutureStixToQuery(unittest.TestCase, object):

    @staticmethod
    def get_query_translation_result(stix_pattern, options={}):
        return translation.translate(MODULE, 'query', MODULE, stix_pattern, options)

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value='194.147.78.155']"
        query = TestRecordedFutureStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '194.147.78.155', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)
    
    def test_file_hash_query(self):
        stix_pattern = "[file:hashes.'SHA-1'='D5DD920BE5BCFEB904E95DA4B6D0CCCA0727D692']"
        query = TestRecordedFutureStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'D5DD920BE5BCFEB904E95DA4B6D0CCCA0727D692', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)
    
    def test_domain_query(self):
        stix_pattern = "[domain-name:value='test.com']"
        query = TestRecordedFutureStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'test.com', 'dataType': 'domain'}"
        _test_query_assertions(query, queries)

    def test_url_query(self):
        stix_pattern = "[url:value = 'http://marebust.com']"
        query = TestRecordedFutureStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'http://marebust.com', 'dataType': 'url'}"
        _test_query_assertions(query, queries)