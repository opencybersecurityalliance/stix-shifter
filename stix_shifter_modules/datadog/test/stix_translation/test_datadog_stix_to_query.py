import unittest
from unittest.mock import patch

from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode

translation = stix_translation.StixTranslation()


def _test_query_assertions(query, queries):
    assert query['queries'] == [queries]


class TestStixToQuery(unittest.TestCase, object):

    @patch('time.time', return_value=12345678)
    def test_ipv4_query(self, mock_time):
        stix_pattern = "[x-datadog-event:event_id = 12345678 OR domain-name:value = 'abc.com']"
        query = translation.translate('datadog', 'query', 'datadog', stix_pattern)
        queries = ['{"host": "abc.com", "start": 9580878, "end": 12345678}',
                   '{"id": 12345678, "start": 9580878, "end": 12345678}']
        assert query['queries'] == queries

    def test_url_query(self):
        stix_pattern = "[url:value = '/event/url'] START t'2021-01-28T12:24:01.009Z' STOP t'2021-07-25T12:54:01.009Z'"
        query = translation.translate('datadog', 'query', 'datadog', stix_pattern)
        queries = ['{"url": "/event/url", "start": 1611836641009, "end": 1627217641009}',
                   '{"resource": "/event/url", "start": 1611836641009, "end": 1627217641009}']
        assert query['queries'] == queries

    @patch('time.time', return_value=12345678)
    def test_domain_name_query(self, mock_time):
        stix_pattern = "[domain-name:value = 'abc.com']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"host": "abc.com", "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_event_id_query(self, mock_time):
        stix_pattern = "[x-datadog-event:event_id = 12345678]"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"id": 12345678, "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_priority_query(self, mock_time):
        stix_pattern = "[x-datadog-event:priority = 'info']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"priority": "info", "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_title_query(self, mock_time):
        stix_pattern = "[x-datadog-event:title = 'title']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"title": "title", "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_text_query(self, mock_time):
        stix_pattern = "[x-datadog-event:text = 'text']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"text": "text", "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_device_name_query(self, mock_time):
        stix_pattern = "[x-datadog-event:device_name = 'Windows']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"device_name": "Windows", "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_source_query(self, mock_time):
        stix_pattern = "[x-datadog-event:source = 'source' AND x-datadog-event:source = 'default']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"source": "default,source", "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_monitor_id_query(self, mock_time):
        stix_pattern = "[x-datadog-event:monitor_id = '12345678']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"monitor_id": 12345678, "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_tags_query(self, mock_time):
        stix_pattern = "[x-datadog-event:tags = 'tags']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"tags": "tags", "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_is_aggregate_query(self, mock_time):
        stix_pattern = "[x-datadog-event:is_aggregate = 'true']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"unaggregated": "true", "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_alert_type_query(self, mock_time):
        stix_pattern = "[x-datadog-event:alert_type = 'alert_type']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"alert_type": "alert_type", "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_start_query(self, mock_time):
        stix_pattern = "[x-ibm-finding:start = '2021-01-28T12:24:01.009Z']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"start": 1611836641009, "end": 12345678}'
        _test_query_assertions(query, queries)

    def test_end_query(self):
        stix_pattern = "[x-ibm-finding:end = '2021-01-28T12:24:01.009Z']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"end": 1611836641009, "start": 1611833876209}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_time_observed_query(self, mock_time):
        stix_pattern = "[x-ibm-finding:time_observed = '2021-01-28T12:24:01.009Z']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"date_happened": 1611836641009, "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_query_from_multiple_observation_expressions_joined_by_AND(self, mock_time):
        stix_pattern = "[x-datadog-event:alert_type = 'alert_type'] AND [x-datadog-event:tags = 'tags']"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = ['{"alert_type": "alert_type", "start": 9580878, "end": 12345678}',
                   '{"tags": "tags", "start": 9580878, "end": 12345678}']
        assert query['queries'] == queries

    def test_query_comparator_operator_AND_with_same_field(self):
        stix_pattern = "[domain-name:value = 'abc.com'] START t'2021-01-28T12:24:01.009Z' STOP t'2021-07-25T12:54:01.009Z'"
        query = translation.translate('datadog', 'query', 'datadog', stix_pattern)
        queries = '{"host": "abc.com", "start": 1611836641009, "end": 1627217641009}'
        _test_query_assertions(query, queries)

    def test_query_comparator_operator_AND_with_different_field(self):
        stix_pattern = "[domain-name:value = 'abc.com' AND x-datadog-event:alert_type = 'alert_type'] START t'2021-01-28T12:24:01.009Z' STOP t'2021-07-25T12:54:01.009Z'"
        query = translation.translate('datadog', 'query', 'datadog', stix_pattern)
        queries = '{"alert_type": "alert_type", "host": "abc.com", "start": 1611836641009, "end": 1627217641009}'
        _test_query_assertions(query, queries)

    @patch('time.time', return_value=12345678)
    def test_IN_query(self, mock_time):
        stix_pattern = "[x-datadog-event:alert_type IN ('alert_type', 'default')]"
        query = translation.translate('datadog', 'query', '{}', stix_pattern)
        queries = '{"alert_type": ["alert_type", "default"], "start": 9580878, "end": 12345678}'
        _test_query_assertions(query, queries)

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('datadog', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert False == result['success']
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']
