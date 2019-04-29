from stix_shifter.stix_translation import stix_translation
from stix_shifter.stix_translation.src.modules.qradar import qradar_data_mapping
from stix_shifter.utils.error_response import ErrorCode
import unittest
import random
import json
import copy
from freezegun import freeze_time

options_file = open('tests/stix_translation/qradar_stix_to_aql/options.json').read()
selections_file = open('stix_shifter/stix_translation/src/modules/qradar/json/aql_event_fields.json').read()
protocols_file = open('stix_shifter/stix_translation/src/modules/qradar/json/network_protocol_map.json').read()
OPTIONS = json.loads(options_file)
DEFAULT_SELECTIONS = json.loads(selections_file)
DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5
DEFAULT_START_TIME = 1548926700000
DEFAULT_END_TIME = 1548927000000
PROTOCOLS = json.loads(protocols_file)


freeze_time("2019-01-31 09:30:00").start()
selections = "SELECT {}".format(", ".join(DEFAULT_SELECTIONS['default']))
custom_selections = "SELECT {}".format(", ".join(OPTIONS['select_fields']))
from_statement = " FROM events "


default_limit = "limit {}".format(DEFAULT_LIMIT)
default_time = "last {} minutes".format(DEFAULT_TIMERANGE)

translation = stix_translation.StixTranslation()


def _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix):
    assert query['queries'] == [selections + from_statement + where_statement]
    assert query['parsed_stix'] == parsed_stix
    assert query['start_time'] == DEFAULT_START_TIME
    assert query['end_time'] == DEFAULT_END_TIME


def _translate_query(stix_pattern):
    return translation.translate('qradar', 'query', '{}', stix_pattern)


class TestStixToAql(unittest.TestCase, object):

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84/10']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (INCIDR('192.168.122.84/10',sourceip) OR INCIDR('192.168.122.84/10',destinationip) OR INCIDR('192.168.122.84/10',identityip)) OR (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83' OR identityip = '192.168.122.83') {} {}".format(
            default_limit, default_time)
        parsed_stix = [{'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.84/10'}, {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_ipv6_query(self):
        stix_pattern = "[ipv6-addr:value = '3001:0:0:0:0:0:0:2']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (sourceip = '3001:0:0:0:0:0:0:2' OR destinationip = '3001:0:0:0:0:0:0:2') {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'ipv6-addr:value', 'comparison_operator': '=', 'value': '3001:0:0:0:0:0:0:2'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_url_query(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE url = 'http://www.testaddress.com' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'url:value', 'comparison_operator': '=', 'value': 'http://www.testaddress.com'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_mac_address_query(self):
        stix_pattern = "[mac-addr:value = '00-00-5E-00-53-00']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (sourcemac = '00-00-5E-00-53-00' OR destinationmac = '00-00-5E-00-53-00') {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_query_from_multiple_observation_expressions_joined_by_AND(self):
        stix_pattern = "[url:value = 'www.example.com'] AND [mac-addr:value = '00-00-5E-00-53-00']"
        query = _translate_query(stix_pattern)
        # Expect the STIX and to convert to an AQL OR.
        where_statement = "WHERE (url = 'www.example.com') OR ((sourcemac = '00-00-5E-00-53-00' OR destinationmac = '00-00-5E-00-53-00')) {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'url:value', 'comparison_operator': '=', 'value': 'www.example.com'}, {'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_query_from_multiple_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[(url:value = 'www.example.com' OR url:value = 'www.test.com') AND mac-addr:value = '00-00-5E-00-53-00']"
        query = _translate_query(stix_pattern)
        # Expect the STIX and to convert to an AQL AND.
        where_statement = "WHERE (sourcemac = '00-00-5E-00-53-00' OR destinationmac = '00-00-5E-00-53-00') AND (url = 'www.test.com' OR url = 'www.example.com') {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'},
                       {'attribute': 'url:value', 'comparison_operator': '=', 'value': 'www.test.com'},
                       {'attribute': 'url:value', 'comparison_operator': '=', 'value': 'www.example.com'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_file_query(self):
        # TODO: Add support for file hashes. Unsure at this point how QRadar queries them
        stix_pattern = "[file:name = 'some_file.exe']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE filename = 'some_file.exe' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'file:name', 'comparison_operator': '=', 'value': 'some_file.exe'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_port_queries(self):
        stix_pattern = "[network-traffic:src_port = 12345 OR network-traffic:dst_port = 23456]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE destinationport = '23456' OR sourceport = '12345' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'network-traffic:dst_port', 'comparison_operator': '=', 'value': 23456}, {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 12345}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_unmapped_attribute_with_AND(self):
        stix_pattern = "[network-traffic:some_invalid_attribute = 'whatever' AND file:name = 'some_file.exe']"
        result = translation.translate('qradar', 'query', '{}', stix_pattern)
        assert result['success'] == False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert 'Unable to map property' in result['error']

    def test_pattern_with_one_observation_exp_with_one_unmapped_attribute(self):
        stix_pattern = "[network-traffic:some_invalid_attribute = 'whatever']"
        result = translation.translate('qradar', 'query', '{}', stix_pattern)
        assert result['success'] == False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert 'Unable to map property' in result['error']

    def test_unmapped_attribute_with_OR(self):
        stix_pattern = "[network-traffic:some_invalid_attribute = 'whatever' OR file:name = 'some_file.exe']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE filename = 'some_file.exe' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'file:name', 'comparison_operator': '=', 'value': 'some_file.exe'},
                       {'attribute': 'network-traffic:some_invalid_attribute', 'comparison_operator': '=', 'value': 'whatever'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_pattern_with_two_observation_exps_one_with_unmapped_attribute(self):
        stix_pattern = "[network-traffic:some_invalid_attribute = 'whatever'] OR [file:name = 'some_file.exe' AND url:value = 'www.example.com']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE url = 'www.example.com' AND filename = 'some_file.exe' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'network-traffic:some_invalid_attribute', 'comparison_operator': '=', 'value': 'whatever'},
                       {'attribute': 'url:value', 'comparison_operator': '=', 'value': 'www.example.com'},
                       {'attribute': 'file:name', 'comparison_operator': '=', 'value': 'some_file.exe'}]
        for parsing in parsed_stix:
            assert parsing in query['parsed_stix']
        assert query['queries'] == [selections + from_statement + where_statement]

    def test_pattern_with_three_observation_exps_one_with_unmapped_attribute(self):
        stix_pattern = "[file:name = 'some_file.exe' AND network-traffic:some_invalid_attribute = 'whatever'] OR [url:value = 'www.example.com'] AND [mac-addr:value = '00-00-5E-00-53-00']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (url = 'www.example.com') OR ((sourcemac = '00-00-5E-00-53-00' OR destinationmac = '00-00-5E-00-53-00')) {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'network-traffic:some_invalid_attribute', 'comparison_operator': '=', 'value': 'whatever'},
                       {'attribute': 'url:value', 'comparison_operator': '=', 'value': 'www.example.com'},
                       {'attribute': 'file:name', 'comparison_operator': '=', 'value': 'some_file.exe'},
                       {'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}]
        for parsing in parsed_stix:
            assert parsing in query['parsed_stix']
        assert query['queries'] == [selections + from_statement + where_statement]

    def test_user_account_query(self):
        stix_pattern = "[user-account:user_id = 'root']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE username = 'root' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'user-account:user_id', 'comparison_operator': '=', 'value': 'root'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('qradar', 'query', '{}', stix_pattern)
        assert result['success'] == False
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_network_traffic_protocols(self):
        for key, value in PROTOCOLS.items():
            # Test for both upper and lower case protocols in the STIX pattern
            if random.randint(0, 1) == 0:
                key = key.upper()
            stix_pattern = "[network-traffic:protocols[*] = '" + key + "']"
            query = _translate_query(stix_pattern)
        where_statement = "WHERE protocolid = '{}' {} {}".format(value, default_limit, default_time)
        parsed_stix = [{'attribute': 'network-traffic:protocols[*]', 'comparison_operator': '=', 'value': key}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_network_traffic_start_stop(self):
        stix_pattern = "[network-traffic:'start' = '2018-06-14T08:36:24.000Z' OR network-traffic:end = '2018-06-14T08:36:24.567Z']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE endtime = '1528965384567' OR starttime = '1528965384000' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'network-traffic:end', 'comparison_operator': '=', 'value': '2018-06-14T08:36:24.567Z'}, {'attribute': 'network-traffic:start', 'comparison_operator': '=', 'value': '2018-06-14T08:36:24.000Z'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_start_stop_qualifiers_with_one_observation(self):
        start_time_01 = "t'2016-06-01T01:30:00.123Z'"
        stop_time_01 = "t'2016-06-01T02:20:00.123Z'"
        unix_start_time_01 = 1464744600123
        unix_stop_time_01 = 1464747600123
        stix_pattern = "[network-traffic:src_port = 37020 AND user-account:user_id = 'root' OR network-traffic:some_invalid_attribute = 'whatever'] START {} STOP {}".format(start_time_01, stop_time_01)
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (username = 'root' AND sourceport = '37020') {} START {} STOP {}".format(default_limit, unix_start_time_01, unix_stop_time_01)
        parsed_stix = [{'attribute': 'user-account:user_id', 'comparison_operator': '=', 'value': 'root'},
                       {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 37020},
                       {'attribute': 'network-traffic:some_invalid_attribute', 'comparison_operator': '=', 'value': 'whatever'}]
        assert len(query['queries']) == 1
        assert query['queries'] == [selections + from_statement + where_statement]
        for parsing in parsed_stix:
            assert parsing in query['parsed_stix']
        assert query['start_time'] == unix_start_time_01
        assert query['end_time'] == unix_stop_time_01

    def test_start_stop_qualifiers_with_two_observations(self):
        start_time_01 = "t'2016-06-01T01:30:00.123Z'"
        stop_time_01 = "t'2016-06-01T02:20:00.123Z'"
        start_time_02 = "t'2016-06-01T03:55:00.123Z'"
        stop_time_02 = "t'2016-06-01T04:30:24.743Z'"
        unix_start_time_01 = 1464744600123
        unix_stop_time_01 = 1464747600123
        unix_start_time_02 = 1464753300123
        unix_stop_time_02 = 1464755424743
        stix_pattern = "[network-traffic:src_port = 37020 AND user-account:user_id = 'root'] START {} STOP {} OR [ipv4-addr:value = '192.168.122.83'] START {} STOP {}".format(start_time_01, stop_time_01, start_time_02, stop_time_02)
        query = _translate_query(stix_pattern)
        where_statement_01 = "WHERE username = 'root' AND sourceport = '37020' {} START {} STOP {}".format(default_limit, unix_start_time_01, unix_stop_time_01)
        where_statement_02 = "WHERE (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83' OR identityip = '192.168.122.83') {} START {} STOP {}".format(default_limit, unix_start_time_02, unix_stop_time_02)
        parsed_stix = [{'attribute': 'user-account:user_id', 'comparison_operator': '=', 'value': 'root'},
                       {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 37020},
                       {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        assert len(query['queries']) == 2
        assert query['queries'] == [selections + from_statement + where_statement_01, selections + from_statement + where_statement_02]
        assert query['parsed_stix'] == parsed_stix
        # The biggest time window should be returned
        assert query['start_time'] == unix_start_time_01
        assert query['end_time'] == unix_stop_time_02

    def test_start_stop_qualifiers_with_three_observations(self):
        start_time_01 = "t'2016-06-01T00:00:00.123Z'"
        stop_time_01 = "t'2016-06-01T01:11:11.456Z'"
        start_time_02 = "t'2016-06-07T02:22:22.789Z'"
        stop_time_02 = "t'2016-06-07T03:33:33.012Z'"
        unix_start_time_01 = 1464739200123
        unix_stop_time_01 = 1464743471456
        unix_start_time_02 = 1465266142789
        unix_stop_time_02 = 1465270413012
        stix_pattern = "[network-traffic:src_port = 37020 AND network-traffic:dst_port = 635] START {} STOP {} OR [url:value = 'www.example.com'] OR [ipv4-addr:value = '333.333.333.0' OR network-traffic:some_invalid_attribute = 'whatever'] START {} STOP {}".format(
            start_time_01, stop_time_01, start_time_02, stop_time_02)
        query = _translate_query(stix_pattern)
        where_statement_01 = "WHERE destinationport = '635' AND sourceport = '37020' {} START {} STOP {}".format(default_limit, unix_start_time_01, unix_stop_time_01)
        where_statement_02 = "WHERE (sourceip = '333.333.333.0' OR destinationip = '333.333.333.0' OR identityip = '333.333.333.0') {} START {} STOP {}".format(default_limit, unix_start_time_02, unix_stop_time_02)
        where_statement_03 = "WHERE url = 'www.example.com' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'network-traffic:dst_port', 'comparison_operator': '=', 'value': 635},
                       {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 37020},
                       {'attribute': 'url:value', 'comparison_operator': '=', 'value': 'www.example.com'},
                       {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '333.333.333.0'},
                       {'attribute': 'network-traffic:some_invalid_attribute', 'comparison_operator': '=', 'value': 'whatever'}]
        assert len(query['queries']) == 3
        assert query['queries'] == [selections + from_statement + where_statement_01, selections + from_statement + where_statement_02, selections + from_statement + where_statement_03]
        for parsing in parsed_stix:
            assert parsing in query['parsed_stix']
        # The biggest time window should be returned
        assert query['start_time'] == unix_start_time_01
        assert query['end_time'] == unix_stop_time_02

    def test_start_stop_qualifiers_with_missing_or_partial_milliseconds(self):
        # missing milliseconds
        start_time_01 = "t'2016-06-01T01:30:00Z'"
        stop_time_01 = "t'2016-06-01T02:20:00Z'"
        # one-digit millisecond
        start_time_02 = "t'2016-06-01T03:55:00.1Z'"
        # four-digit millisecond
        stop_time_02 = "t'2016-06-01T04:30:24.1243Z'"
        unix_start_time_01 = 1464744600000
        unix_stop_time_01 = 1464747600000
        unix_start_time_02 = 1464753300100
        unix_stop_time_02 = 1464755424124
        stix_pattern = "[user-account:user_id = 'root'] START {} STOP {} OR [ipv4-addr:value = '192.168.122.83'] START {} STOP {}".format(start_time_01, stop_time_01, start_time_02, stop_time_02)
        query = _translate_query(stix_pattern)
        where_statement_01 = "WHERE username = 'root' {} START {} STOP {}".format(default_limit, unix_start_time_01, unix_stop_time_01)
        where_statement_02 = "WHERE (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83' OR identityip = '192.168.122.83') {} START {} STOP {}".format(default_limit, unix_start_time_02, unix_stop_time_02)
        parsed_stix = [{'attribute': 'user-account:user_id', 'comparison_operator': '=', 'value': 'root'},
                       {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        assert len(query['queries']) == 2
        assert query['queries'] == [selections + from_statement + where_statement_01, selections + from_statement + where_statement_02]
        assert query['parsed_stix'] == parsed_stix
        # The biggest time window should be returned
        assert query['start_time'] == unix_start_time_01
        assert query['end_time'] == unix_stop_time_02

    def test_set_operators(self):
        stix_pattern = "[ipv4-addr:value ISSUBSET '198.51.100.0/24']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (INCIDR('198.51.100.0/24',sourceip) OR INCIDR('198.51.100.0/24',destinationip) OR INCIDR('198.51.100.0/24',identityip)) {} {}".format(default_limit, default_time)
        parsed_stix = [{'value': '198.51.100.0/24', 'comparison_operator': 'ISSUBSET', 'attribute': 'ipv4-addr:value'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    # def test_custom_time_limit_and_result_count_and_mappings(self):
    #     stix_pattern = "[ipv4-addr:value = '192.168.122.83']"
    #     custom_options = copy.deepcopy(OPTIONS)
    #     query = translation.translate('qradar', 'query', '{}', stix_pattern, custom_options)
    #     where_statement = "WHERE (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83' OR identityip = '192.168.122.83') limit {} last {} minutes".format(custom_options['result_limit'], custom_options['timerange'])
    #     parsed_stix = [{'value': '192.168.122.83', 'comparison_operator': '=', 'attribute': 'ipv4-addr:value'}]
    #     assert query == {'queries': [custom_selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_domainname_query(self):
        stix_pattern = "[domain-name:value = 'example.com']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE domainname LIKE '%example.com%' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'domain-name:value', 'comparison_operator': '=', 'value': 'example.com'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_generic_filehash_query(self):
        stix_pattern = "[file:hashes.'SHA-256' = 'sha256hash']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE filehash = 'sha256hash' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'file:hashes.SHA-256', 'comparison_operator': '=', 'value': 'sha256hash'}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    # def test_sha256_filehash_query(self):
    #     stix_pattern = "[file:hashes.'SHA-256' = 'sha256hash']"
    #     query = translation.translate('qradar', 'query', '{}', stix_pattern, OPTIONS)
    #     where_statement = "WHERE (sha256hash = 'sha256hash' OR filehash = 'sha256hash') limit {} last {} minutes".format(OPTIONS['result_limit'], OPTIONS['timerange'])
    #     parsed_stix = [{'attribute': 'file:hashes.SHA-256', 'comparison_operator': '=', 'value': 'sha256hash'}]
    #     assert query == {'queries': [custom_selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    # def test_multi_filehash_query(self):
    #     stix_pattern = "[file:hashes.'SHA-256' = 'sha256hash'] OR [file:hashes.'MD5' = 'md5hash']"
    #     query = translation.translate('qradar', 'query', '{}', stix_pattern, OPTIONS)
    #     where_statement = "WHERE ((sha256hash = 'sha256hash' OR filehash = 'sha256hash')) OR ((md5hash = 'md5hash' OR filehash = 'md5hash')) limit {} last {} minutes".format(OPTIONS['result_limit'], OPTIONS['timerange'])
    #     parsed_stix = [{'attribute': 'file:hashes.SHA-256', 'comparison_operator': '=', 'value': 'sha256hash'}, {'attribute': 'file:hashes.MD5', 'comparison_operator': '=', 'value': 'md5hash'}]
    #     assert query == {'queries': [custom_selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_source_and_destination_references(self):
        where_statements = [
            [
                "WHERE sourceip = '192.0.2.0' {} {}".format(default_limit, default_time),
                "WHERE sourcemac = '00-00-5E-00-53-00' {} {}".format(default_limit, default_time),
                "WHERE INCIDR('192.0.2.0/25',sourceip) {} {}".format(default_limit, default_time),
                "WHERE sourceip = '3001:0:0:0:0:0:0:2' {} {}".format(default_limit, default_time)
            ],
            [
                "WHERE destinationip = '192.0.2.0' {} {}".format(default_limit, default_time),
                "WHERE destinationmac = '00-00-5E-00-53-00' {} {}".format(default_limit, default_time),
                "WHERE INCIDR('192.0.2.0/25',destinationip) {} {}".format(default_limit, default_time),
                "WHERE destinationip = '3001:0:0:0:0:0:0:2' {} {}".format(default_limit, default_time)
            ]
        ]
        for ref_index, reference in enumerate(["network-traffic:src_ref.value", "network-traffic:dst_ref.value"]):
            for dat_index, datum in enumerate(["'192.0.2.0'", "'00-00-5E-00-53-00'", "'192.0.2.0/25'", "'3001:0:0:0:0:0:0:2'"]):
                stix_pattern = "[{} = {}]".format(reference, datum)
                query = _translate_query(stix_pattern)
                where_statement = where_statements[ref_index][dat_index]
                parsed_stix = [{'attribute': reference, 'comparison_operator': '=', 'value': datum.strip("'")}]
                _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_nested_parenthesis_in_pattern(self):
        stix_pattern = "[(ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '100.100.122.90') AND network-traffic:src_port = 37020] OR [user-account:user_id = 'root'] AND [url:value = 'www.example.com']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (sourceport = '37020' AND ((sourceip = '100.100.122.90' OR destinationip = '100.100.122.90' OR identityip = '100.100.122.90') OR (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83' OR identityip = '192.168.122.83'))) OR ((username = 'root') OR (url = 'www.example.com')) {} {}".format(default_limit, default_time)
        parsed_stix = [
            {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 37020},
            {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '100.100.122.90'},
            {'attribute': 'user-account:user_id', 'comparison_operator': '=', 'value': 'root'},
            {'attribute': 'url:value', 'comparison_operator': '=', 'value': 'www.example.com'},
            {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}
        ]
        for parsing in parsed_stix:
            assert parsing in query['parsed_stix']
        assert query['queries'] == [selections + from_statement + where_statement]

    def test_LIKE_operator(self):
        search_string = 'example.com'
        stix_pattern = "[url:value LIKE '{}']".format(search_string)
        query = _translate_query(stix_pattern)
        where_statement = "WHERE url LIKE '%{}%' {} {}".format(search_string, default_limit, default_time)
        parsed_stix = [{'attribute': 'url:value', 'comparison_operator': 'LIKE', 'value': search_string}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_payload_string_matching_with_LIKE(self):
        search_string = 'search term'
        stix_pattern = "[x-readable-payload:value LIKE '{}']".format(search_string)
        query = _translate_query(stix_pattern)
        where_statement = "WHERE TEXT SEARCH '{}' {} {}".format(search_string, default_limit, default_time)
        parsed_stix = [{'attribute': 'x-readable-payload:value', 'comparison_operator': 'LIKE', 'value': search_string}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_payload_string_matching_with_MATCH(self):
        search_string = '^.*https://wally.fireeye.com.*$'
        stix_pattern = "[x-readable-payload:value MATCHES '{}']".format(search_string)
        query = _translate_query(stix_pattern)
        where_statement = "WHERE utf8_payload MATCHES '{}' {} {}".format(search_string, default_limit, default_time)
        parsed_stix = [{'attribute': 'x-readable-payload:value', 'comparison_operator': 'MATCHES', 'value': search_string}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)

    def test_backslash_escaping(self):
        # Stix pattern requires backslash to be double escaped to pass pattern validation.
        # Not sure yet how we will make this work for an AQL query.
        # See https://github.com/oasis-open/cti-stix2-json-schemas/issues/51
        search_string = '^.*http://graphics8\\\.nytimes\\\.com/bcvideo.*$'
        stix_pattern = "[x-readable-payload:value MATCHES '{}']".format(search_string)
        query = _translate_query(stix_pattern)
        translated_value = '^.*http://graphics8\\.nytimes\\.com/bcvideo.*$'
        where_statement = "WHERE utf8_payload MATCHES '{}' {} {}".format(translated_value, default_limit, default_time)
        parsed_stix = [{'attribute': 'x-readable-payload:value', 'comparison_operator': 'MATCHES', 'value': translated_value}]
        _test_query_assertions(query, selections, from_statement, where_statement, parsed_stix)
