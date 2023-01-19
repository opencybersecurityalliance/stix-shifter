import unittest
from stix_shifter.stix_translation import stix_translation
from freezegun import freeze_time


translation = stix_translation.StixTranslation()

def _test_query_assertions(query, expected_query):
    assert query['queries'] == [expected_query]

def _translate_query(stix_pattern):
    return translation.translate('stix_bundle', 'query', '{}', stix_pattern)

class TestQueryTranslator(unittest.TestCase, object):

    @freeze_time("2023-01-18 01:30:00")
    def test_pattern_without_timestamps(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83']"
        query = _translate_query(stix_pattern)
        expected_query = "[ipv4-addr:value = '192.168.122.83'] START t'2023-01-18T01:25:00.000Z' STOP t'2023-01-18T01:30:00.000Z'"
        _test_query_assertions(query, expected_query)

    def test_pattern_with_timestamps(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83'] START t'2019-03-28T12:24:01.009Z' STOP t'2019-03-28T12:54:01.009Z'"
        query = _translate_query(stix_pattern)
        expected_query = "[ipv4-addr:value = '192.168.122.83'] START t'2019-03-28T12:24:01.009Z' STOP t'2019-03-28T12:54:01.009Z'"
        _test_query_assertions(query, expected_query)

