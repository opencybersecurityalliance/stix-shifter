from stix_shifter.stix_translation import stix_translation
from stix_shifter.stix_translation.src.exceptions import DataMappingException
from stix_shifter.stix_translation.src.modules.splunk import stix_to_splunk
from stix_shifter.utils.error_response import ErrorCode

import unittest
import random

DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5

protocols = {
    "tcp": "6",
    "udp": "17",
    "icmp": "1",
    "idpr-cmtp": "38",
    "ipv6": "40",
    "rsvp": "46",
    "gre": "47",
    "esp": "50",
    "ah": "51",
    "narp": "54",
    "ospfigp": "89",
    "ipip": "94",
    "any": "99",
    "sctp": "132"
}

default_timerange_spl = '-' + str(DEFAULT_TIMERANGE) + 'minutes'

translation = stix_translation.StixTranslation()


def _test_query_assertions(query, queries, parsed_stix):
    assert query['queries'] == queries
    assert query['parsed_stix'] == parsed_stix


class TestStixToSpl(unittest.TestCase, object):

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search (((src_ip = "192.168.122.84") OR (dest_ip = "192.168.122.84")) OR ((src_ip = "192.168.122.83") OR (dest_ip = "192.168.122.83"))) earliest="-5minutes" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.84'}, {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_ipv6_query(self):
        stix_pattern = "[ipv6-addr:value = 'fe80::8c3b:a720:dc5c:2abf%19']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search ((src_ipv6 = "fe80::8c3b:a720:dc5c:2abf%19") OR (dest_ipv6 = "fe80::8c3b:a720:dc5c:2abf%19")) earliest="-5minutes" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'ipv6-addr:value', 'comparison_operator': '=', 'value': 'fe80::8c3b:a720:dc5c:2abf%19'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_url_query(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        parsed_stix = [{'attribute': 'url:value', 'comparison_operator': '=', 'value': 'http://www.testaddress.com'}]
        queries = 'search (url = "http://www.testaddress.com") earliest="-5minutes" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        _test_query_assertions(query, queries, parsed_stix)

    def test_mac_address_query(self):
        stix_pattern = "[mac-addr:value = '00-00-5E-00-53-00']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search ((src_mac = "00-00-5E-00-53-00") OR (dest_mac = "00-00-5E-00-53-00")) earliest="-5minutes" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_domain_query(self):
        stix_pattern = "[domain-name:value = 'example.com']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search (url = "example.com") earliest="-5minutes" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'domain-name:value', 'comparison_operator': '=', 'value': 'example.com'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_query_from_multiple_observation_expressions_joined_by_AND(self):
        stix_pattern = "[domain-name:value = 'example.com'] AND [mac-addr:value = '00-00-5E-00-53-00']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        # Expect the STIX AND to convert to an SPL OR.
        queries = 'search (url = "example.com") OR ((src_mac = "00-00-5E-00-53-00") OR (dest_mac = "00-00-5E-00-53-00")) earliest="-5minutes" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'domain-name:value', 'comparison_operator': '=', 'value': 'example.com'}, {'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_query_from_multiple_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[domain-name:value = 'example.com' AND mac-addr:value = '00-00-5E-00-53-00']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        # Expect the STIX AND to convert to an AQL AND.
        queries = 'search (((src_mac = "00-00-5E-00-53-00") OR (dest_mac = "00-00-5E-00-53-00")) AND (url = "example.com")) earliest="-5minutes" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}, {'attribute': 'domain-name:value', 'comparison_operator': '=', 'value': 'example.com'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_file_query(self):
        stix_pattern = "[file:name = 'some_file.exe']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search (file_name = "some_file.exe") earliest="-5minutes" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'file:name', 'comparison_operator': '=', 'value': 'some_file.exe'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_port_queries(self):
        stix_pattern = "[network-traffic:src_port = 12345 OR network-traffic:dst_port = 23456]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search ((dest_port = 23456) OR (src_port = 12345)) earliest="-5minutes" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'network-traffic:dst_port', 'comparison_operator': '=', 'value': 23456}, {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 12345}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_unmapped_attribute(self):
        stix_pattern = "[network-traffic:some_invalid_attribute = 'whatever']"
        result = translation.translate('splunk', 'query', '{}', stix_pattern)
        assert False == result['success']
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert result['error'].startswith('data mapping error : Unable to map property')

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('splunk', 'query', '{}', stix_pattern)
        assert False == result['success']
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_network_traffic_protocols(self):
        for key, value in protocols.items():
            # Test for both upper and lower case protocols in the STIX pattern
            if random.randint(0, 1) == 0:
                key = key.upper()
            stix_pattern = "[network-traffic:protocols[*] = '" + key + "']"
            query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search (protocol = "'+key+'") earliest="{}" | head {} | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'.format(default_timerange_spl, DEFAULT_LIMIT)
        parsed_stix = [{'attribute': 'network-traffic:protocols[*]', 'comparison_operator': '=', 'value': key}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_network_traffic_start_stop(self):
        stix_pattern = "[network-traffic:'start' = '2018-06-14T08:36:24.000Z' OR network-traffic:end = '2018-06-14T08:36:24.000Z']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search ((latest = "2018-06-14T08:36:24.000Z") OR (earliest = "2018-06-14T08:36:24.000Z")) earliest="-5minutes" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'network-traffic:end', 'comparison_operator': '=', 'value': '2018-06-14T08:36:24.000Z'}, {'attribute': 'network-traffic:start', 'comparison_operator': '=', 'value': '2018-06-14T08:36:24.000Z'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_start_stop_qualifiers(self):
        stix_pattern = "[network-traffic:src_port = 37020] START t'2016-06-01T01:30:00.000Z' STOP t'2016-06-01T02:20:00.000Z' OR [ipv4-addr:value = '192.168.122.83'] START t'2016-06-01T03:55:00.000Z' STOP t'2016-06-01T04:30:00.000Z'"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search (src_port = 37020) earliest="06/01/2016:01:30:00" latest="06/01/2016:02:20:00" OR ((src_ip = "192.168.122.83") OR (dest_ip = "192.168.122.83")) earliest="06/01/2016:03:55:00" latest="06/01/2016:04:30:00" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 37020}, {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_start_stop_qualifiers_one_time(self):
        stix_pattern = "[network-traffic:src_port = 37020] START t'2016-06-01T01:30:00.000Z' STOP t'2016-06-01T02:20:00.000Z'"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search (src_port = 37020) earliest="06/01/2016:01:30:00" latest="06/01/2016:02:20:00" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 37020}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_issubset_operator(self):
        stix_pattern = "[ipv4-addr:value ISSUBSET '198.51.100.0/24']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search ((src_ip = "198.51.100.0/24") OR (dest_ip = "198.51.100.0/24")) earliest="-5minutes" | head 10000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'ipv4-addr:value', 'comparison_operator': 'ISSUBSET', 'value': '198.51.100.0/24'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_custom_time_limit_and_result_count(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83']"

        timerange = 25
        result_limit = 5000
        options = {"timerange": timerange, "result_limit": result_limit}

        query = translation.translate('splunk', 'query', '{}', stix_pattern, options)
        queries = 'search ((src_ip = "192.168.122.83") OR (dest_ip = "192.168.122.83")) earliest="-25minutes" | head 5000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_custom_mapping(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' AND mac-addr:value = '00-00-5E-00-53-00']"

        timerange = 15
        result_limit = 1000

        options = {
            "timerange": timerange,
            "result_limit": result_limit,
            "mapping": {
                "mac-addr": {
                    "cim_type": "flow",
                    "fields": {
                        "value": "mac"
                    }
                },
                "ipv4-addr": {
                    "cim_type": "flow",
                    "fields": {
                        "value": ["src_ip", "dest_ip"]
                    }
                }
            },
            "select_fields": {
                "default":
                    [
                        "src_ip",
                        "src_port",
                    ]
            }
        }

        query = translation.translate('splunk', 'query', '{}', stix_pattern, options)
        queries = 'search ((mac = "00-00-5E-00-53-00") AND ((src_ip = "192.168.122.83") OR (dest_ip = "192.168.122.83"))) earliest="-15minutes" | head 1000 | fields src_ip, src_port'
        parsed_stix = [{'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}, {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        _test_query_assertions(query, queries, parsed_stix)

    def test_free_search(self):
        stix_pattern = "[x-readable-payload:value = 'malware']"

        timerange = 25
        result_limit = 5000
        options = {"timerange": timerange, "result_limit": result_limit}

        query = translation.translate('splunk', 'query', '{}', stix_pattern, options)
        queries = 'search _raw=*malware* earliest="-25minutes" | head 5000 | fields src_ip, src_port, src_mac, src_ipv6, dest_ip, dest_port, dest_mac, dest_ipv6, file_hash, user, url, protocol'
        parsed_stix = [{'attribute': 'x-readable-payload:value', 'comparison_operator': '=', 'value': 'malware'}]
        _test_query_assertions(query, queries, parsed_stix)
