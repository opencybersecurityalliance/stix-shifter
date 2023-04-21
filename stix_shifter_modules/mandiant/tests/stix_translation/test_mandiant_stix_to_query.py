import unittest
from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()
MODULE = 'mandiant'

def _test_query_assertions(query, queries):
    assert isinstance(query, dict) is True
    assert 'queries' in query
    assert query['queries'] == [queries]


class TestStixToQuery(unittest.TestCase, object):

    @staticmethod
    def get_query_translation_result(stix_pattern, options={}):
        return translation.translate(MODULE, 'query', MODULE, stix_pattern, options)

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value='194.147.78.155']"
        query = TestStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '194.147.78.155', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)
    
    def test_ipv6_query(self):
        stix_pattern = "[ipv6-addr:value = '3001:0:0:0:0:0:0:2']"
        query = TestStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '3001:0:0:0:0:0:0:2', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)
    
    def test_url_query(self):
        stix_pattern = "[url:value='https://test.com']"
        query = TestStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'https://test.com', 'dataType': 'url'}"
        _test_query_assertions(query, queries)
    
    def test_file_hash_query(self):
        stix_pattern = "[file:hashes.'SHA-1'='D5DD920BE5BCFEB904E95DA4B6D0CCCA0727D692']"
        query = TestStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'D5DD920BE5BCFEB904E95DA4B6D0CCCA0727D692', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)
    
    def test_file_hash_md5_query(self):
        stix_pattern = "[file:hashes.'MD5'='16cda323189d8eba4248c0a2f5ad0d8f']"
        query = TestStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '16cda323189d8eba4248c0a2f5ad0d8f', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)    

    def test_file_hash_sha256_query(self):
        stix_pattern = "[file:hashes.'SHA-256' = 'd7fc5162511d42d22462ad5b4c716b73903a677806119f9ad0314763ccd719ca']"
        query = TestStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'd7fc5162511d42d22462ad5b4c716b73903a677806119f9ad0314763ccd719ca', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)
    
    def test_domain_query(self):
        stix_pattern = "[domain-name:value='test.com']"
        query = TestStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'test.com', 'dataType': 'domain'}"
        _test_query_assertions(query, queries)