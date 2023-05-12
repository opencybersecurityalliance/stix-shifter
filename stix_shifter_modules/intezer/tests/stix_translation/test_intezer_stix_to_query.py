import unittest
from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()
MODULE = 'intezer'

def _test_query_assertions(query, queries):
    assert isinstance(query, dict) is True
    assert 'queries' in query
    assert query['queries'] == [queries]

class TestIntezerStixToQuery(unittest.TestCase, object):

    @staticmethod
    def get_query_translation_result(stix_pattern, options={}):
        return translation.translate(MODULE, 'query', MODULE, stix_pattern, options)
    
    def test_file_hash_query(self):
        stix_pattern = "[file:hashes.'SHA-1'='D5DD920BE5BCFEB904E95DA4B6D0CCCA0727D692']"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'D5DD920BE5BCFEB904E95DA4B6D0CCCA0727D692', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)
    
    def test_multi_expression_query(self):
        stix_pattern = "[file:hashes.'SHA-1'='D5DD920BE5BCFEB904E95DA4B6D0CCCA0727D692' OR file:hashes.'MD5'='f5ae03de0ad60f5b17b82f2cd68402fe']"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'D5DD920BE5BCFEB904E95DA4B6D0CCCA0727D692', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)
    
    def test_multi_observation_expression_query(self):
        stix_pattern = "([file:hashes.'SHA-1'='D5DD920BE5BCFEB904E95DA4B6D0CCCA0727D692'] OR [file:hashes.'MD5'='f5ae03de0ad60f5b17b82f2cd68402fe'])"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'f5ae03de0ad60f5b17b82f2cd68402fe', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)
    
    def test_hash_time_interval_query(self):
        """
        Test file hash time interval operation
        """
        stix_pattern = "[file:hashes.'MD5' = 'f5ae03de0ad60f5b17b82f2cd68402fe'] START t'2020-09-30T23:00:00.000Z' STOP t'2020-11-04T00:00:00.000Z''"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'f5ae03de0ad60f5b17b82f2cd68402fe', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)
    
    def test_oper_issuperset(self):
        """
        Test Unsupportted operator
        """
        stix_pattern = "([file:hashes.'MD5' ISSUPERSET 'f5ae03de0ad60f5b17b82f2cd68402fe'] START t'2020-10-01T08:43:10.003Z' STOP " \
                       "t'2020-10-30T10:43:10.003Z')"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        assert query['success'] is False
        assert query['code'] == 'mapping_error'

    def test_like_comp_exp(self):
        """
        Test with LIKE operator
        """
        stix_pattern = "[file:hashes.'MD5' LIKE 'f5ae03de0ad60f5b17b82f2cd68402fe'] START t'2020-10-01T08:43:10.003Z' " \
                       "STOP t'2020-10-30T10:43:10.003Z'"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '%f5ae03de0ad60f5b17b82f2cd68402fe%', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)
    
    def test_matches_comp_exp(self):
        """
        Test with MATCHES operator
        :return:
        """
        stix_pattern = "[file:hashes.'MD5' MATCHES '\\\\d+'] START t'2020-10-01T08:43:10.003Z' STOP " \
                       "t'2020-10-30T10:43:10.003Z'"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '.*\\\\\\\\d+.*', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)
    
    def test_not_comp_exp(self):
        """
        Test with NOT operator
        :return:
        """
        stix_pattern = "[file:hashes.'MD5' NOT = 'f5ae03de0ad60f5b17b82f2cd68402fe'] START t'2020-05-01T08:43:10.003Z' " \
                       "STOP t'2020-10-30T10:43:10.003Z'"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'f5ae03de0ad60f5b17b82f2cd68402fe', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        """
        Test with IN operator
        """
        stix_pattern = "[file:hashes.'MD5' IN ('f5ae03de0ad60f5b17b82f2cd68402fe','f5ae03de0ad60f5b17b82f2cd68402fe')]"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '(f5ae03de0ad60f5b17b82f2cd68402fe OR f5ae03de0ad60f5b17b82f2cd68402fe)', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)
    
    def test_file_hash_md5_query(self):
        stix_pattern = "[file:hashes.'MD5'='16cda323189d8eba4248c0a2f5ad0d8f']"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '16cda323189d8eba4248c0a2f5ad0d8f', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)    

    def test_file_hash_sha256_query(self):
        stix_pattern = "[file:hashes.'SHA-256' = 'd7fc5162511d42d22462ad5b4c716b73903a677806119f9ad0314763ccd719ca']"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'd7fc5162511d42d22462ad5b4c716b73903a677806119f9ad0314763ccd719ca', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)
    
    def test_url_query(self):
        stix_pattern = "[url:value='https://test.com']"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'https://test.com', 'dataType': 'url'}"
        _test_query_assertions(query, queries)
    
    def test_domain_query(self):
        stix_pattern = "[domain-name:value='test.com']"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'test.com', 'dataType': 'domain'}"
        _test_query_assertions(query, queries)

    def test_hash_time_interval_query(self):
        stix_pattern = "[file:hashes.'MD5' = 'f5ae03de0ad60f5b17b82f2cd68402fe'] START t'2020-09-30T23:00:00.000Z' STOP t'2020-11-04T00:00:00.000Z''"
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'f5ae03de0ad60f5b17b82f2cd68402fe', 'dataType': 'hash'}"
        _test_query_assertions(query, queries)        
    
    def test_NOT_and_not_equals_operators(self):
        search_string1 = "www.example.com"
        search_string2 = "www.example.ca"
        stix_pattern = "[url:value != '{}' OR url:value NOT = '{}']".format(search_string1, search_string2)
        query = TestIntezerStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': 'www.example.com', 'dataType': 'url'}"
        _test_query_assertions(query, queries)        