from stix_shifter.stix_translation import stix_translation
from stix_shifter.utils.error_response import ErrorCode

import unittest
import json

translation = stix_translation.StixTranslation()
module = "security_advisor"

def to_json(queries):
    return list(map(lambda x: x , queries))

def _test_query_assertions(query, queries):
    assert query['queries'] == queries


class TestStixToQuery(unittest.TestCase):

    def test_simple_or_query(self):
        stix_pattern = "[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = to_json( ["[url:value = 'http://5.188.86.29:7000' OR url:value = 'http://5.45.69.149:7000']"] )
        _test_query_assertions(query, queries)


    def test_simple_and_query(self):
        stix_pattern = "[url:value = 'http://5.188.86.29:7000' AND url:value = 'http://5.45.69.149:7000']"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = to_json( ["[url:value = 'http://5.188.86.29:7000' AND url:value = 'http://5.45.69.149:7000']"] )
        _test_query_assertions(query, queries)


    def test_query_time_stamps(self):
        stix_pattern = "[url:value = 'http://5.188.86.29:7000' AND url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = to_json( ["[url:value = 'http://5.188.86.29:7000' AND url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"] )
        _test_query_assertions(query, queries)

    def test_advance_query(self):
        stix_pattern = "[url:value = 'http://5.188.86.29:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z' AND [url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"
        query = translation.translate(module, 'query', '{}', stix_pattern)
        queries = to_json( ["[url:value = 'http://5.188.86.29:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z' AND [url:value = 'http://5.45.69.149:7000'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-11-20T12:24:01.009Z'"] )
        _test_query_assertions(query, queries)
