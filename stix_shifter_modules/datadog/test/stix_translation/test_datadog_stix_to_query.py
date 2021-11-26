import json
import unittest
from unittest.mock import patch

from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode

translation = stix_translation.StixTranslation()


def _test_query_assertions(query, queries):
    assert set(query['queries']) == set(queries)

class TestStixToQuery(unittest.TestCase, object):

    @patch('time.time', return_value=12345678)
    def test_ipv4_query(self, mock_time):
        stix_pattern = "[x-oca-event:code = 12345678 OR domain-name:value = 'abc.com']"
        query = translation.translate('datadog', 'query', 'datadog', stix_pattern)
        queries = ['{"query": {"host": "abc.com", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"id": 12345678, "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"id_str": "12345678", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"host": "abc.com", "start": 12345378, "end": 12345678}, "source": "processes"}',
                   '{"query": {"id": 12345678, "start": 12345378, "end": 12345678}, "source": "processes"}',
                   '{"query": {"id_str": "12345678", "start": 12345378, "end": 12345678}, "source": "processes"}']
        
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_domain_name_query(self, mock_time):
        stix_pattern = "[domain-name:value = 'abc.com']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"host": "abc.com", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"host": "abc.com", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_event_id_query(self, mock_time):
        stix_pattern = "[x-oca-event:code = 12345678]"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"id": 12345678, "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"id_str": "12345678", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"id": 12345678, "start": 12345378, "end": 12345678}, "source": "processes"}',
                   '{"query": {"id_str": "12345678", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_priority_query(self, mock_time):
        stix_pattern = "[x-datadog-event:priority = 'info']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"priority": "info", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"priority": "info", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_title_query(self, mock_time):
        stix_pattern = "[x-oca-event:outcome = 'title']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"title": "title", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"title": "title", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_text_query(self, mock_time):
        stix_pattern = "[artifact:payload_bin = 'text']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"text": "text", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"text": "text", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_device_name_query(self, mock_time):
        stix_pattern = "[x-oca-event:agent = 'Windows']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"device_name": "Windows", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"device_name": "Windows", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_source_query(self, mock_time):
        stix_pattern = "[x-oca-event:module = 'source' AND x-oca-event:module = 'default']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"source": "default,source", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"source": "default,source", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_monitor_id_query(self, mock_time):
        stix_pattern = "[x-datadog-event:monitor_id = '12345678']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"monitor_id": 12345678, "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"monitor_id": 12345678, "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_tags_query(self, mock_time):
        stix_pattern = "[x-datadog-event:tags = 'tags']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"tags": "tags", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"tags": "tags", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_is_aggregate_query(self, mock_time):
        stix_pattern = "[x-datadog-event:is_aggregate = 'true']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"unaggregated": "true", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"unaggregated": "true", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_alert_type_query(self, mock_time):
        stix_pattern = "[x-datadog-event:alert_type = 'alert_type']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"alert_type": "alert_type", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"alert_type": "alert_type", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_start_query(self, mock_time):
        stix_pattern = "[x-ibm-finding:start = '2021-01-28T12:24:01.009Z']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"start": 1611836641, "end": 12345678}, "source": "events"}',
                   '{"query": {"start": 1611836641, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    def test_end_query(self):
        stix_pattern = "[x-ibm-finding:end = '2021-01-28T12:24:01.009Z']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"end": 1611836641, "start": 1611836341}, "source": "events"}',
                   '{"query": {"end": 1611836641, "start": 1611836341}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_time_observed_query(self, mock_time):
        stix_pattern = "[x-ibm-finding:time_observed = '2021-01-28T12:24:01.009Z']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"date_happened": 1611836641, "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"date_happened": 1611836641, "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_process_cmdline_query(self, mock_time):
        stix_pattern = "[process:command_line = 'System']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"cmdline": "System", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_process_pid_query(self, mock_time):
        stix_pattern = "[process:pid = '92']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"pid": "92", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_process_creator_user_ref_query(self, mock_time):
        stix_pattern = "[process:creator_user_ref = 2]"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"user": "2", "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_query_from_multiple_observation_expressions_joined_by_AND(self, mock_time):
        stix_pattern = "[x-datadog-event:alert_type = 'alert_type'] AND [x-datadog-event:tags = 'tags']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"alert_type": "alert_type", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"tags": "tags", "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"alert_type": "alert_type", "start": 12345378, "end": 12345678}, "source": "processes"}',
                   '{"query": {"tags": "tags", "start": 12345378, "end": 12345678}, "source": "processes"}']

        _test_query_assertions(query, queries)

    def test_query_comparator_operator_AND_with_same_field(self):
        stix_pattern = "[domain-name:value = 'abc.com'] START t'2021-01-28T12:24:01.009Z' STOP t'2021-07-25T12:54:01.009Z'"
        query = translation.translate('datadog', 'query', 'datadog', stix_pattern)
        queries = ['{"query": {"host": "abc.com", "start": 1611836641, "end": 1627217641}, "source": "events"}',
                   '{"query": {"host": "abc.com", "start": 1611836641, "end": 1627217641}, "source": "processes"}']
        _test_query_assertions(query, queries)

    def test_query_comparator_operator_AND_with_different_field(self):
        stix_pattern = "[domain-name:value = 'abc.com' AND x-datadog-event:alert_type = 'alert_type'] START t'2021-01-28T12:24:01.009Z' STOP t'2021-07-25T12:54:01.009Z'"
        query = translation.translate('datadog', 'query', 'datadog', stix_pattern)
        queries = ['{"query": {"alert_type": "alert_type", "host": "abc.com", "start": 1611836641, "end": 1627217641}, "source": "events"}',
                   '{"query": {"alert_type": "alert_type", "host": "abc.com", "start": 1611836641, "end": 1627217641}, "source": "processes"}']
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_IN_query(self, mock_time):
        stix_pattern = "[x-datadog-event:alert_type IN ('alert_type', 'default')]"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"query": {"alert_type": ["alert_type", "default"], "start": 12345378, "end": 12345678}, "source": "events"}',
                   '{"query": {"alert_type": ["alert_type", "default"], "start": 12345378, "end": 12345678}, "source": "processes"}']
        _test_query_assertions(query, queries)

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('datadog', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert False == result['success']
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']
