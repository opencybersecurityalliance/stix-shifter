import unittest
from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()
MODULE = 'dshield'

def _test_query_assertions(query, queries):
    assert isinstance(query, dict) is True
    assert 'queries' in query
    assert query['queries'] == [queries]


class TestDshieldStixToQuery(unittest.TestCase, object):

    @staticmethod
    def get_query_translation_result(stix_pattern, options={}):
        return translation.translate(MODULE, 'query', MODULE, stix_pattern, options)

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value='194.147.78.155']"
        query = TestDshieldStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '194.147.78.155', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)
    
    def test_ipv6_query(self):
        stix_pattern = "[ipv6-addr:value = '3001:0:0:0:0:0:0:2']"
        query = TestDshieldStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '3001:0:0:0:0:0:0:2', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)

    def test_multi_ipv4_expression_query(self):
        stix_pattern = "([ipv4-addr:value = '194.147.78.155'] OR [ipv4-addr:value = '198.51.100.10'])"
        query = TestDshieldStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '198.51.100.10', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)    
    
    def test_NOT_and_not_equals_operators(self):
        search_string1 = "194.147.78.155"
        search_string2 = "198.51.100.10"
        stix_pattern = "[ipv4-addr:value != '{}' OR ipv4-addr:value NOT = '{}']".format(search_string1, search_string2)
        query = TestDshieldStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '194.147.78.155', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)

    def test_multi_expression_query(self):
        stix_pattern = "[ipv6-addr:value = '3001:0:0:0:0:0:0:2' OR ipv4-addr:value='194.147.78.155']"
        query = TestDshieldStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '3001:0:0:0:0:0:0:2', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)    

    def test_not_comp_exp(self):
        """
        Test with NOT operator
        :return:
        """
        stix_pattern = "[ipv4-addr:value NOT = '172.31.60.104'] START t'2020-05-01T08:43:10.003Z' " \
                       "STOP t'2020-10-30T10:43:10.003Z'"
        query = TestDshieldStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '172.31.60.104', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)

    def test_in_comp_exp(self):
        """
        Test with IN operator
        """
        stix_pattern = "[ipv4-addr:value IN ('172.31.60.104','94.147.78.155')]"
        query = TestDshieldStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '(172.31.60.104 OR 94.147.78.155)', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)

    def test_one_obser_is_super_set_operator_network(self):
        """
        to test single observation with an un-supported operator
        """
        stix_pattern = "[ipv4-addr:value ISSUPERSET '172.217.0.0/24'] " \
                       "START t'2019-04-10T08:43:10.003Z' STOP t'2019-04-23T10:43:10.003Z'"
        query = TestDshieldStixToQuery.get_query_translation_result(stix_pattern)
        assert query['success'] is False
        assert query['code'] == 'mapping_error'

    def test_like_comp_exp(self):
        """
        Test with LIKE operator
        """
        stix_pattern = "[ipv4-addr:value LIKE '172.31.60.104'] START t'2020-10-01T08:43:10.003Z' " \
                       "STOP t'2020-10-30T10:43:10.003Z'"
        query = TestDshieldStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '%172.31.60.104%', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)
    
    def test_matches_comp_exp(self):
        """
        Test with MATCHES operator
        :return:
        """
        stix_pattern = "[ipv4-addr:value MATCHES '\\\\d+'] START t'2020-10-01T08:43:10.003Z' STOP " \
                       "t'2020-10-30T10:43:10.003Z'"
        query = TestDshieldStixToQuery.get_query_translation_result(stix_pattern)
        queries = "{'data': '.*\\\\\\\\d+.*', 'dataType': 'ip'}"
        _test_query_assertions(query, queries)    