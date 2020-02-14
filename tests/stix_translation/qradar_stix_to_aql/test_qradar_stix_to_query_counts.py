from stix_shifter.stix_translation import stix_translation
import unittest

translation = stix_translation.StixTranslation()


def _translate_query(stix_pattern):
    return translation.translate('qradar', 'query', '{}', stix_pattern)


class TestStixToQueryCounts(unittest.TestCase, object):

    def test_query_count_for_events_and_flows(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84']"
        query = _translate_query(stix_pattern)
        assert len(query['queries']) == 2

    def test_query_count_for_events_and_flows_with_multi_start_stop(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83'] START t'2019-01-28T12:24:01.009Z' STOP t'2019-01-28T12:54:01.009Z' OR [ipv4-addr:value = '192.168.122.84'] START t'2019-01-29T12:24:01.009Z' STOP t'2019-01-29T12:54:01.009Z'"
        query = _translate_query(stix_pattern)
        assert len(query['queries']) == 4

    def test_query_count_for_events(self):
        stix_pattern = "[user-account:user_id = 'some user']"
        query = _translate_query(stix_pattern)
        assert len(query['queries']) == 1

    def test_query_count_for_flows(self):
        stix_pattern = "[network-traffic:src_byte_count = 1280]"
        query = _translate_query(stix_pattern)
        assert len(query['queries']) == 1