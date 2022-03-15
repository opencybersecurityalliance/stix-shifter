import unittest
from stix_shifter_modules.sumologic.stix_translation import query_constructor

from stix_shifter.stix_translation import stix_translation

translation = stix_translation.StixTranslation()


def _test_query_assertions(query, queries):
    assert query['queries'] == [queries]


class TestStixToQuery(unittest.TestCase, object):
    def test_artifact_payload_query(self):
        stix_pattern = "[artifact:payload_bin = 'Sep 26 05:29:06 sumologic NetworkManager[677]: <info>" \
                       "  [1632614346.1076] dhcp4 (eth0)']"
        query = translation.translate('sumologic', 'query', 'sumologic', stix_pattern, options={"result_limit": 100})
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"_raw = \\\"Sep 26 05:29:06 sumologic NetworkManager[677]: <info>  [1632614346.1076] " \
                  "dhcp4 (eth0)\\\"\", \"fromTime\": \"%s\", \"toTime\": \"%s\"}" % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_domain_and_userid_query(self):
        stix_pattern = "[domain-name:value = 'sumologic.domain_name.com' AND user-account:user_id = '12345678'] " \
                       "START t'2021-09-01T00:00:00.000Z' STOP t'2021-09-26T10:16:00.000Z'"
        query = translation.translate('sumologic', 'query', 'sumologic', stix_pattern, options={"result_limit": 100})
        queries = "{\"query\": \"id = \\\"12345678\\\" AND _sourcehost = \\\"sumologic.domain_name.com\\\"\", " \
                  "\"fromTime\": \"20210901T000000\", \"toTime\": \"20210926T101600\"}"
        _test_query_assertions(query, queries)

    def test_domain_and_userid_query_no_timestamp(self):
        stix_pattern = "[domain-name:value = 'sumologic.domain_name.com' AND user-account:user_id = '12345678']"
        query = translation.translate('sumologic', 'query', 'sumologic', stix_pattern, options={"result_limit": 100})
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"id = \\\"12345678\\\" AND _sourcehost = \\\"sumologic.domain_name.com\\\"\", " \
                  "\"fromTime\": \"%s\", \"toTime\": \"%s\"}" % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_event_count_query(self):
        stix_pattern = "[x-ibm-finding:event_count = '21'] START t'2021-01-28T12:24:01.009Z' " \
                       "STOP t'2021-07-25T12:54:01.009Z'"
        query = translation.translate('sumologic', 'query', 'sumologic', stix_pattern)
        queries = "{\"query\": \"_messagecount = \\\"21\\\"\", \"fromTime\": \"20210128T122401\", " \
                  "\"toTime\": \"20210725T125401\"}"
        _test_query_assertions(query, queries)

    def test_time_observed_query(self):
        stix_pattern = "[x-ibm-finding:time_observed = '2021-09-23T11:34:07.255Z']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"_messagetime = \\\"2021-09-23T11:34:07.255Z\\\"\", \"fromTime\": \"%s\", " \
                  "\"toTime\": \"%s\"}" % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_src_device_query(self):
        stix_pattern = "[x-ibm-finding:src_device = 'sumologic.domain.com']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"_collector = \\\"sumologic.domain.com\\\"\", \"fromTime\": \"%s\", " \
                  "\"toTime\": \"%s\"}" % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_event_code_query(self):
        stix_pattern = "[x-oca-event:code = '12345678']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"_messageid = \\\"12345678\\\"\", \"fromTime\": \"%s\", " \
                  "\"toTime\": \"%s\"}" % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_event_agent_query(self):
        stix_pattern = "[x-oca-event:agent='sumologic.domain.com']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"_collector = \\\"sumologic.domain.com\\\"\", \"fromTime\": \"%s\", " \
                  "\"toTime\": \"%s\"}" \
                  % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_event_module_query(self):
        stix_pattern = "[x-oca-event:module = 'Linux System_3']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"_source = \\\"Linux System_3\\\"\", \"fromTime\": \"%s\", " \
                  "\"toTime\": \"%s\"}" % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_event_provider_query(self):
        stix_pattern = "[x-oca-event:provider = 'linux/system']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"_sourcecategory = \\\"linux/system\\\"\", \"fromTime\": \"%s\", \"toTime\": \"%s\"}" \
                  % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_custom_collector_id_query(self):
        stix_pattern = "[x-sumologic-source:collectorid = '12345678']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"_collectorid = \\\"12345678\\\"\", \"fromTime\": \"%s\", \"toTime\": \"%s\"}" \
                  % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_custom_sourcename_query(self):
        stix_pattern = "[x-sumologic-source:sourcename = '/var/log/messages']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"_sourcename = \\\"/var/log/messages\\\"\", \"fromTime\": \"%s\", \"toTime\": \"%s\"}" \
                  % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_user_id_query(self):
        stix_pattern = "[user-account:user_id = '12345678']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"id = \\\"12345678\\\"\", \"fromTime\": \"%s\", \"toTime\": \"%s\"}" \
                  % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_user_account_login_query(self):
        stix_pattern = "[user-account:account_login = 'abc@domain.com']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"email = \\\"abc@domain.com\\\"\", \"fromTime\": \"%s\", \"toTime\": \"%s\"}" \
                  % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_user_display_name_query(self):
        stix_pattern = "[user-account:display_name = 'abc def']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"displayName = \\\"abc def\\\"\", \"fromTime\": \"%s\", \"toTime\": \"%s\"}" \
                  % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_user_account_created_query(self):
        stix_pattern = "[user-account:account_created = '2021-09-23T11:34:07.255Z']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"createdAt = \\\"2021-09-23T11:34:07.255Z\\\"\", \"fromTime\": \"%s\", " \
                  "\"toTime\": \"%s\"}" % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_in_operator(self):
        stix_pattern = "[user-account:display_name IN ('abc', 'def')]"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"displayName = \\\"abc\\\" OR displayName = \\\"def\\\"\", " \
                  "\"fromTime\": \"%s\", \"toTime\": \"%s\"}" \
                  % (from_time, to_time)
        _test_query_assertions(query, queries)

    def test_user_account_last_login_query(self):
        stix_pattern = "[user-account:account_last_login = '2021-10-04T13:51:09.958Z']"
        query = translation.translate('sumologic', 'query', '{}', stix_pattern)
        _, from_time, to_time = query_constructor.convert_timestamp(query)
        queries = "{\"query\": \"lastLoginTimestamp = \\\"2021-10-04T13:51:09.958Z\\\"\", \"fromTime\": \"%s\", " \
                  "\"toTime\": \"%s\"}" % (from_time, to_time)
        _test_query_assertions(query, queries)
