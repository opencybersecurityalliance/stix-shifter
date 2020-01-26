from stix_shifter.stix_translation import stix_translation
from stix_shifter.utils.error_response import ErrorCode
import unittest
import datetime
import re

DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5


translation = stix_translation.StixTranslation()


def _test_query_assertions(translated_query, test_query):
    assert translated_query['queries'] == test_query


def _start_and_stop_time():
    stop_time = datetime.datetime.utcnow()
    go_back_in_minutes = datetime.timedelta(minutes=DEFAULT_TIMERANGE)
    start_time = stop_time - go_back_in_minutes
    # converting from UTC timestamp 2019-04-13 23:13:06.130401 to
    # string format 2019-04-13 23:13:06.130Z
    converted_starttime = start_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    converted_stoptime = stop_time.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return converted_starttime, converted_stoptime


def _remove_timestamp_from_query(queries):
    pattern = r'\s*AND\s*\(\@timestamp:\["\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z"\s*TO\s*"\d{4}(-\d{2}){2}T\d{2}(:\d{2}){2}(\.\d+)?Z"\]\)'
    if isinstance(queries, list):
        return [re.sub(pattern, "", query) for query in queries]
    elif isinstance(queries, str):
        return re.sub(pattern, "", queries)


class TestStixtoQuery(unittest.TestCase, object):

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(source.ip : "192.168.122.84" OR destination.ip : "192.168.122.84" OR client.ip : "192.168.122.84" OR server.ip : "192.168.122.84") OR (source.ip : "192.168.122.83" OR destination.ip : "192.168.122.83" OR client.ip : "192.168.122.83" OR server.ip : "192.168.122.83")']
        _test_query_assertions(translated_query, test_query)

    def test_ipv6_query(self):
        stix_pattern = "[ipv6-addr:value = '3001:0:0:0:0:0:0:2']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(source.ip : "3001:0:0:0:0:0:0:2" OR destination.ip : "3001:0:0:0:0:0:0:2" OR client.ip : "3001:0:0:0:0:0:0:2" OR server.ip : "3001:0:0:0:0:0:0:2")']
        _test_query_assertions(translated_query, test_query)

    def test_url_query(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['url.original : "http://www.testaddress.com"']
        _test_query_assertions(translated_query, test_query)

    def test_mac_address_query(self):
        stix_pattern = "[mac-addr:value = '00-00-5E-00-53-00']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(source.mac : "00-00-5E-00-53-00" OR destination.mac : "00-00-5E-00-53-00" OR client.mac : "00-00-5E-00-53-00" OR server.mac : "00-00-5E-00-53-00")']
        _test_query_assertions(translated_query, test_query)

    def test_query_from_multiple_observation_expressions_joined_by_AND(self):
        stix_pattern = "[url:value = 'www.example.com'] AND [mac-addr:value = '00-00-5E-00-53-00']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(url.original : "www.example.com") OR ((source.mac : "00-00-5E-00-53-00" OR destination.mac : "00-00-5E-00-53-00" OR client.mac : "00-00-5E-00-53-00" OR server.mac : "00-00-5E-00-53-00"))']
        _test_query_assertions(translated_query, test_query)

    def test_query_from_multiple_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[(url:value = 'www.example.com' OR url:value = 'www.test.com') AND mac-addr:value = '00-00-5E-00-53-00']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(source.mac : "00-00-5E-00-53-00" OR destination.mac : "00-00-5E-00-53-00" OR client.mac : "00-00-5E-00-53-00" OR server.mac : "00-00-5E-00-53-00") AND (url.original : "www.test.com" OR url.original : "www.example.com")']
        _test_query_assertions(translated_query, test_query)

    def test_file_query(self):
        stix_pattern = "[file:name = 'some_file.exe']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['process.name : "some_file.exe"']
        _test_query_assertions(translated_query, test_query)

    def test_complex_query(self):
        stix_pattern = "[network-traffic:protocols[*] LIKE 'ipv_' AND network-traffic:src_port>443] START t'2019-04-11T08:42:39.297Z' STOP t'2019-04-11T08:43:39.297Z' OR [user-account:user_id = '_' AND artifact:payload_bin LIKE '%'] START t'2019-04-11T14:35:44.011Z' STOP t'2019-04-21T16:35:44.011Z' AND [process:pid<700 OR url:value LIKE '%' AND process:creator_user_ref.user_id IN ('root','admin')] START t'2019-04-11T14:35:44.011Z' STOP t'2019-04-17T14:35:44.011Z'"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        test_query = ['(source.port:>443 OR client.port:>443) AND (network.transport : ipv? OR network.type : ipv? OR network.protocol : ipv?) AND (@timestamp:["2019-04-11T08:42:39.297Z" TO "2019-04-11T08:43:39.297Z"])',
                      'event.original : * AND user.name : "_" AND (@timestamp:["2019-04-11T14:35:44.011Z" TO "2019-04-21T16:35:44.011Z"])', '(user.name : ("root" OR "admin") AND url.original : *) OR process.pid:<700 AND (@timestamp:["2019-04-11T14:35:44.011Z" TO "2019-04-17T14:35:44.011Z"])']
        assert translated_query['queries'] == test_query

    def test_file_not_equal_query(self):
        stix_pattern = "[file:name != 'some_file.exe']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(NOT process.name : "some_file.exe" AND process.name:*)']
        _test_query_assertions(translated_query, test_query)

    def test_port_queries(self):
        stix_pattern = "[network-traffic:src_port = 12345 OR network-traffic:dst_port = 23456]"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(destination.port : "23456" OR server.port : "23456") OR (source.port : "12345" OR client.port : "12345")']
        _test_query_assertions(translated_query, test_query)

    def test_port_queries_lessthan_greaterthan(self):
        stix_pattern = "[network-traffic:src_port > 12345 AND network-traffic:dst_port < 23456]"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(destination.port:<23456 OR server.port:<23456) AND (source.port:>12345 OR client.port:>12345)']
        _test_query_assertions(translated_query, test_query)

    def test_port_queries_src_ref_equal(self):
        stix_pattern = "[network-traffic:src_ref.value = '127.0.0.1']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(source.ip : "127.0.0.1" OR client.ip : "127.0.0.1")']
        _test_query_assertions(translated_query, test_query)

    def test_port_queries_src_ref_notequal(self):
        stix_pattern = "[network-traffic:src_ref.value != '127.0.0.1']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['((NOT source.ip : "127.0.0.1" AND source.ip:*) OR (NOT client.ip : "127.0.0.1" AND client.ip:*))']
        _test_query_assertions(translated_query, test_query)

    def test_port_queries_greaterthanorequal(self):
        stix_pattern = "[network-traffic:src_port >=443]"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(source.port:>=443 OR client.port:>=443)']
        _test_query_assertions(translated_query, test_query)

    def test_port_queries_lessthanorequal(self):
        stix_pattern = "[network-traffic:src_port <=443]"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(source.port:<=443 OR client.port:<=443)']
        _test_query_assertions(translated_query, test_query)

    def test_network_traffic_in_operator(self):
        stix_pattern = "[network-traffic:protocols[*] IN ('tcp','dns')]"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(network.transport : ("tcp" OR "dns") OR network.type : ("tcp" OR "dns") OR network.protocol : ("tcp" OR "dns"))']
        assert translated_query['queries'] == test_query

    def test_network_traffic_queries(self):
        stix_pattern = "[network-traffic:src_port = 12345 OR network-traffic:protocols[*] LIKE '_n%']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(network.transport : ?n* OR network.type : ?n* OR network.protocol : ?n*) OR (source.port : "12345" OR client.port : "12345")']
        _test_query_assertions(translated_query, test_query)

    def test_unmapped_attribute_handling_with_OR(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com' OR unmapped:attribute = 'something']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['url.original : "http://www.testaddress.com"']
        _test_query_assertions(translated_query, test_query)

    def test_unmapped_attribute_handling_with_AND(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com' AND unmapped:attribute = 'something']"
        result = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        assert result['success'] == False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert 'Unable to map the following STIX objects and properties' in result['error']

    def test_user_account_query(self):
        stix_pattern = "[user-account:user_id = 'root']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['user.name : "root"']
        _test_query_assertions(translated_query, test_query)

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('elastic_ecs', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert result['success'] == False
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_process_created_greaterthan(self):
        stix_pattern = "[process:created>'2019-04-10T11:34:05.500Z']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(process.start:["2019-04-10T11:34:06.000Z" TO *])']
        _test_query_assertions(translated_query, test_query)

    def test_process_created_lessthan(self):
        stix_pattern = "[process:created<'2019-04-10T11:34:05.500Z']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(process.start:[* TO "2019-04-10T11:34:04.000Z"])']
        _test_query_assertions(translated_query, test_query)

    def test_process_created_greaterthan_orequal(self):
        stix_pattern = "[process:created>='2019-04-10T11:34:05.500Z']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(process.start:["2019-04-10T11:34:05.500Z" TO *])']
        _test_query_assertions(translated_query, test_query)

    def test_process_created_lessthan_orequal(self):
        stix_pattern = "[process:created<='2019-04-10T11:34:05.500Z']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['(process.start:[* TO "2019-04-10T11:34:05.500Z"])']
        _test_query_assertions(translated_query, test_query)

    def test_process_created_equal(self):
        stix_pattern = "[process:created='2019-04-10T11:34:05.500Z']"
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['process.start : "2019-04-10T11:34:05.500Z"']
        _test_query_assertions(translated_query, test_query)

    def test_combined_observations_with_one_qualifier(self):
        start_time = "t'2019-04-01T01:30:00.123Z'"
        stop_time = "t'2019-04-01T02:20:00.123Z'"
        stix_pattern = "([network-traffic:src_port = 37020 AND user-account:user_id = 'root'] OR [ipv4-addr:value = '192.168.122.83']) START {} STOP {}".format(start_time, stop_time)
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'][-1] = _remove_timestamp_from_query(translated_query['queries'][-1])
        test_query = ['(source.ip : "192.168.122.83" OR destination.ip : "192.168.122.83" OR client.ip : "192.168.122.83" OR server.ip : "192.168.122.83") AND (@timestamp:["2019-04-01T01:30:00.123Z" TO "2019-04-01T02:20:00.123Z"])',
                      'user.name : "root" AND (source.port : "37020" OR client.port : "37020")']
        assert len(translated_query['queries']) == 2
        _test_query_assertions(translated_query, test_query)

    def test_start_stop_qualifiers_with_two_observations(self):
        start_time_01 = "t'2019-04-01T01:30:00.123Z'"
        stop_time_01 = "t'2019-04-01T02:20:00.123Z'"
        start_time_02 = "t'2019-04-01T03:55:00.123Z'"
        stop_time_02 = "t'2019-04-01T04:30:24.743Z'"
        stix_pattern = "[network-traffic:src_port = 37020 AND user-account:user_id = 'root'] START {} STOP {} OR [ipv4-addr:value = '192.168.122.83'] START {} STOP {}".format(start_time_01, stop_time_01, start_time_02, stop_time_02)
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        test_query = ['user.name : "root" AND (source.port : "37020" OR client.port : "37020") AND (@timestamp:["2019-04-01T01:30:00.123Z" TO "2019-04-01T02:20:00.123Z"])',
                      '(source.ip : "192.168.122.83" OR destination.ip : "192.168.122.83" OR client.ip : "192.168.122.83" OR server.ip : "192.168.122.83") AND (@timestamp:["2019-04-01T03:55:00.123Z" TO "2019-04-01T04:30:24.743Z"])']
        assert len(translated_query['queries']) == 2
        _test_query_assertions(translated_query, test_query)

    def test_start_stop_qualifiers_with_three_observations(self):
        start_time_01 = "t'2019-04-01T00:00:00.123Z'"
        stop_time_01 = "t'2019-04-01T01:11:11.456Z'"
        start_time_02 = "t'2019-04-07T02:22:22.789Z'"
        stop_time_02 = "t'2019-04-07T03:33:33.012Z'"
        stix_pattern = "[network-traffic:src_port = 37020 AND network-traffic:dst_port = 635] START {} STOP {} OR [url:value = 'www.example.com'] OR [ipv4-addr:value = '333.333.333.0'] START {} STOP {}".format(
            start_time_01, stop_time_01, start_time_02, stop_time_02)
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'][-1] = _remove_timestamp_from_query(translated_query['queries'][-1])
        test_query = ['(destination.port : "635" OR server.port : "635") AND (source.port : "37020" OR client.port : "37020") AND (@timestamp:["2019-04-01T00:00:00.123Z" TO "2019-04-01T01:11:11.456Z"])',
                      '(source.ip : "333.333.333.0" OR destination.ip : "333.333.333.0" OR client.ip : "333.333.333.0" OR server.ip : "333.333.333.0") AND (@timestamp:["2019-04-07T02:22:22.789Z" TO "2019-04-07T03:33:33.012Z"])', 'url.original : "www.example.com"']
        assert len(translated_query['queries']) == 3
        _test_query_assertions(translated_query, test_query)

    def test_match_operator(self):
        stix_pattern = "[artifact:payload_bin MATCHES '1*']"  # Elastic search does not support PCRE
        translated_query = translation.translate('elastic_ecs', 'query', '{}', stix_pattern)
        translated_query['queries'] = _remove_timestamp_from_query(translated_query['queries'])
        test_query = ['event.original : 1*']
        _test_query_assertions(translated_query, test_query)
