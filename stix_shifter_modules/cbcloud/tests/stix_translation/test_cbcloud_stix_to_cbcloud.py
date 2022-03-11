from stix_shifter.stix_translation import stix_translation
import unittest
import json

translation = stix_translation.StixTranslation()
MODULE = "cbcloud"

class TestQueryTranslator(unittest.TestCase):

    def _test_query_assertions(self, query, queries):
        assert query['queries'] == queries


    def test_file_query(self):
        test_options = {"time_range": None} 
        stix_pattern = "[file:name = 'some_file.exe']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern, options=test_options)
        queries = ['(process_name:some_file.exe) AND -enriched:True']
        self._test_query_assertions(query, queries)

    def test_file_hash_query(self):
        test_options = {"time_range": None} 
        stix_pattern = "[file:hashes.MD5 = '5746bd7e255dd6a8afa06f7c42c1ba41']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern, options=test_options)
        queries = ['(process_hash:5746bd7e255dd6a8afa06f7c42c1ba41) AND -enriched:True']
        self._test_query_assertions(query, queries)
    
    def test_multiple_comparison_expression(self):
        test_options = {"time_range": None} 
        stix_pattern = "[file:hashes.MD5 = '2f50b945d2a6554c1031a744764a0fe2' OR file:name = 'scanhost.exe']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern, options=test_options)
        queries = ['(process_hash:2f50b945d2a6554c1031a744764a0fe2 OR process_name:scanhost.exe) AND -enriched:True']
        self._test_query_assertions(query, queries)
    
    def test_multiple_observation_expression(self):
        test_options = {"time_range": None} 
        stix_pattern = "[file:hashes.MD5 = '2f50b945d2a6554c1031a744764a0fe2'] OR [file:name = 'scanhost.exe']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern, options=test_options)
        queries = ['((process_hash:2f50b945d2a6554c1031a744764a0fe2) OR (process_name:scanhost.exe)) AND -enriched:True']
        self._test_query_assertions(query, queries)
    
    def test_simple_query_with_start_stop_qualifier(self):
        stix_pattern = "[process:name = 'svchost.exe'] START t'2021-01-04T00:00:00.000Z' STOP t'2021-01-04T01:00:00.000Z'"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ['((process_name:svchost.exe) AND device_timestamp:[2021-01-04T00:00:00.000Z TO 2021-01-04T01:00:00.000Z]) AND -enriched:True']
        self._test_query_assertions(query, queries)

    def test_multiple_grouped_observation_expression(self):
        stix_pattern = "([file:hashes.MD5 = '2f50b945d2a6554c1031a744764a0fe2'] OR [file:name = 'scanhost.exe'])  START t'2020-11-01T23:51:59.637Z' STOP t'2020-11-15T23:51:59.637Z'"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern)
        queries = ['(((process_hash:2f50b945d2a6554c1031a744764a0fe2) AND device_timestamp:[2020-11-01T23:51:59.637Z TO 2020-11-15T23:51:59.637Z]) OR ((process_name:scanhost.exe) AND device_timestamp:[2020-11-01T23:51:59.637Z TO 2020-11-15T23:51:59.637Z])) AND -enriched:True']
        self._test_query_assertions(query, queries)
    
    def test_unmapped_attribute_failure(self):
        test_options = {"time_range": None} 
        stix_pattern = "[obj_unmp:unmapped = '5746bd7e255dd6a8afa06f7c42c1ba41']"
        query = translation.translate(MODULE, 'query', '{}', stix_pattern, options=test_options)

        assert query['success'] == False
        assert query['code'] == "mapping_error"
        assert query['connector'] == 'cbcloud'
        assert query['error'] == "cbcloud connector error => data mapping error : Unable to map the following STIX objects and properties: ['obj_unmp:unmapped'] to data source fields"

    def test_unmapped_attribute_handling(self):
        test_options = {"time_range": None} 
        stix_pattern = "[file:hashes.MD5 = '2f50b945d2a6554c1031a744764a0fe2' OR obj_unmp:unmapped = 'scanhost.exe']"
        
        query = translation.translate(MODULE, 'query', '{}', stix_pattern, options=test_options)
        queries = ['(process_hash:2f50b945d2a6554c1031a744764a0fe2) AND -enriched:True']
        self._test_query_assertions(query, queries)
    
    def test_in_operator(self):
        test_options = {"time_range": None} 
        stix_pattern = "[ipv4-addr:value IN ('127.0.0.1', '127.0.0.2')]"
        
        query = translation.translate(MODULE, 'query', '{}', stix_pattern, options=test_options)
        queries = ['((netconn_ipv4:127.0.0.1 OR netconn_local_ipv4:127.0.0.1 OR netconn_ipv4:127.0.0.2 OR netconn_local_ipv4:127.0.0.2)) AND -enriched:True']
        self._test_query_assertions(query, queries)