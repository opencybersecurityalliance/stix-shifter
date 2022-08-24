from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode

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

default_time_range_spl = '-' + str(DEFAULT_TIMERANGE) + 'minutes'

translation = stix_translation.StixTranslation()

fields = ", ".join([
    "src_ip",
    "src_port",
    "src_mac",
    "src_ipv6",
    "dest_ip",
    "dest_port",
    "dest_mac",
    "dest_ipv6",
    "file_hash",
    "user",
    "url",
    "protocol",
    "host",
    "source",
    "DeviceType",
    "Direction",
    "severity",
    "EventID",
    "EventName",
    "ss_name",
    "TacticId",
    "Tactic",
    "TechniqueId",
    "Technique",
    "process",
    "process_id",
    "process_name",
    "process_exec",
    "process_path",
    "process_hash",
    "parent_process",
    "parent_process_id",
    "parent_process_name",
    "parent_process_exec",
    "description",
    "result",
    "signature",
    "signature_id",
    "query",
    "answer"
])


def _test_query_assertions(query, queries):
    assert query['queries'] == [queries]


class TestStixToSpl(unittest.TestCase, object):

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (((src_ip = "192.168.122.84") OR (dest_ip = "192.168.122.84")) OR ((src_ip = "192.168.122.83") OR (dest_ip = "192.168.122.83"))) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_ipv6_query(self):
        stix_pattern = "[ipv6-addr:value = 'fe80::8c3b:a720:dc5c:2abf%19']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((src_ipv6 = "fe80::8c3b:a720:dc5c:2abf%19") OR (dest_ipv6 = "fe80::8c3b:a720:dc5c:2abf%19")) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_url_query(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (url = "http://www.testaddress.com") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_not_equal_operator(self):
        stix_pattern = "[url:value != 'http://www.testaddress.com']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (url != "http://www.testaddress.com") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_NOT_operator(self):
        stix_pattern = "[url:value NOT = 'http://www.testaddress.com']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (NOT (url = "http://www.testaddress.com")) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_mac_address_query(self):
        stix_pattern = "[mac-addr:value = '00-00-5E-00-53-00']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((src_mac = "00-00-5E-00-53-00") OR (dest_mac = "00-00-5E-00-53-00")) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_domain_query(self):
        stix_pattern = "[domain-name:value = 'example.com']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((host = "example.com") OR (url = "example.com")) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_query_from_multiple_observation_expressions_joined_by_AND(self):
        stix_pattern = "[domain-name:value = 'example.com'] AND [mac-addr:value = '00-00-5E-00-53-00']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        # Expect the STIX AND to convert to an SPL OR.
        queries = f'search ((host = "example.com") OR (url = "example.com")) OR ((src_mac = "00-00-5E-00-53-00") OR (dest_mac = "00-00-5E-00-53-00")) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_query_from_multiple_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[domain-name:value = 'example.com' AND mac-addr:value = '00-00-5E-00-53-00']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        # Expect the STIX AND to convert to an AQL AND.
        queries = f'search (((src_mac = "00-00-5E-00-53-00") OR (dest_mac = "00-00-5E-00-53-00")) AND ((host = "example.com") OR (url = "example.com"))) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_file_query(self):
        stix_pattern = "[file:name = 'some_file.exe']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (file_name = "some_file.exe") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_file_hash_query(self):
        stix_pattern = "[file:hashes.'SHA-1' = '5e5a7065f1b551eb3632fb189ce1baefd23158aa']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (file_hash = \"5e5a7065f1b551eb3632fb189ce1baefd23158aa\") earliest=\"-5minutes\" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_risk_finding(self):
        stix_pattern = "[x-ibm-finding:name = 'sample_alert']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search index=_audit ss_name="sample_alert" action=alert_fired earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_dst_ref_queries(self):
        stix_pattern = "[network-traffic:dst_ref.value = '192.168.122.83']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (dest = "192.168.122.83") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_port_queries(self):
        stix_pattern = "[network-traffic:src_port = 12345 OR network-traffic:dst_port = 23456]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((dest_port = 23456) OR (src_port = 12345)) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_unmapped_attribute_handling_with_OR(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com' OR unmapped:attribute = 'something']"
        translated_query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (url = "http://www.testaddress.com") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(translated_query, queries)

    def test_unmapped_attribute_handling_with_AND(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com' AND unmapped:attribute = 'something']"
        result = translation.translate('splunk', 'query', '{}', stix_pattern)
        assert result['success'] == False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert "data mapping error : Unable to map the following STIX objects and properties: " \
            "['unmapped:attribute'] to data source fields" in result['error']

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('splunk', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
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
        queries = 'search (protocol = "' + key + '") earliest="{}" | head {} | fields {}'.format(default_time_range_spl,
                                                                                                 DEFAULT_LIMIT, fields)
        _test_query_assertions(query, queries)

    def test_network_traffic_start_stop(self):
        stix_pattern = "[network-traffic:start = '2018-06-14T08:36:24.000Z' OR network-traffic:end = '2018-06-14T08:36:24.000Z']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((latest = "2018-06-14T08:36:24.000Z") OR (earliest = "2018-06-14T08:36:24.000Z")) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_start_stop_qualifiers(self):
        stix_pattern = "[network-traffic:src_port = 37020] START t'2016-06-01T01:30:00.000Z' STOP t'2016-06-01T02:20:00.000Z' OR [ipv4-addr:value = '192.168.122.83'] START t'2016-06-01T03:55:00.000Z' STOP t'2016-06-01T04:30:00.000Z'"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (src_port = 37020) earliest="06/01/2016:01:30:00" latest="06/01/2016:02:20:00" OR ((src_ip = "192.168.122.83") OR (dest_ip = "192.168.122.83")) earliest="06/01/2016:03:55:00" latest="06/01/2016:04:30:00" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_start_stop_qualifiers_one_time(self):
        stix_pattern = "[network-traffic:src_port = 37020] START t'2016-06-01T01:30:00.000Z' STOP t'2016-06-01T02:20:00.000Z'"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (src_port = 37020) earliest="06/01/2016:01:30:00" latest="06/01/2016:02:20:00" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_start_stop_qualifiers_seconds(self):
        stix_pattern = "[network-traffic:src_port = 37020] START t'2016-06-01T01:30:00Z' STOP t'2016-06-01T02:20:00Z'"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (src_port = 37020) earliest="06/01/2016:01:30:00" latest="06/01/2016:02:20:00" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_issubset_operator(self):
        stix_pattern = "[ipv4-addr:value ISSUBSET '198.51.100.0/24']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((src_ip = "198.51.100.0/24") OR (dest_ip = "198.51.100.0/24")) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_custom_time_limit_and_result_count(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83']"
        options = {"time_range": 25, "result_limit": 5000}
        query = translation.translate('splunk', 'query', '{}', stix_pattern, options)
        queries = f'search ((src_ip = "192.168.122.83") OR (dest_ip = "192.168.122.83")) earliest="-25minutes" | head 5000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_custom_index(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83']"
        options = {"index": "my_index"}
        query = translation.translate('splunk', 'query', '{}', stix_pattern, options)
        queries = f'search index=my_index ((src_ip = "192.168.122.83") OR (dest_ip = "192.168.122.83")) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_custom_mapping(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' AND mac-addr:value = '00-00-5E-00-53-00']"

        options = {
            "time_range": 15,
            "result_limit": 1000,
            "mapping": {
                "from_stix_map": {
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
        }

        query = translation.translate('splunk', 'query', '{}', stix_pattern, options)
        queries = f'search ((mac = "00-00-5E-00-53-00") AND ((src_ip = "192.168.122.83") OR (dest_ip = "192.168.122.83"))) earliest="-15minutes" | head 1000 | fields src_ip, src_port'
        _test_query_assertions(query, queries)

    def test_free_search(self):
        stix_pattern = "[x-readable-payload:value = 'malware']"
        options = {"time_range": 25, "result_limit": 5000}
        query = translation.translate('splunk', 'query', '{}', stix_pattern, options)
        queries = f'search _raw=*malware* earliest="-25minutes" | head 5000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_event_query(self):
        stix_pattern = "[x-oca-event:code = 1]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (signature_id = 1) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_x_oca_asset_by_hostname(self):
        stix_pattern = "[x-oca-asset:hostname = 'omer']"
        result_query = translation.translate('splunk', 'query', '{}', stix_pattern)
        expected_query = f'search (host = "omer") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(result_query, expected_query)

    def test_x_oca_event(self):
        stix_pattern = "[(x-oca-event:action = 'DNS Query' OR x-oca-event:code = 22) AND (x-oca-event:module = 'XmlWinEventLog:Microsoft-Windows-Sysmon/Operational')]"
        result_query = translation.translate('splunk', 'query', '{}', stix_pattern)
        expected_queries = f'search ((source = "XmlWinEventLog:Microsoft-Windows-Sysmon/Operational") AND ((signature_id = 22) OR (signature = "DNS Query"))) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(result_query, expected_queries)

    def test_x_oca_event_missing_vals(self):
        stix_pattern = "[(x-oca-event:action = '' OR x-oca-event:code = '') AND (x-oca-event:module = '')]"
        result_query = translation.translate('splunk', 'query', '{}', stix_pattern)
        print(result_query)
        expected_queries = f'search ((source = "") AND ((signature_id = "") OR (signature = ""))) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(result_query, expected_queries)

    def test_proc_command_line_query(self):
        stix_pattern = "[process:command_line = 'wmic.exe process call create calc']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (process = "wmic.exe process call create calc") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_proc_name_query(self):
        stix_pattern = "[process:name = 'wmic.exe']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (process_name = "wmic.exe") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_ipv4_query_in_operator(self):
        stix_pattern = "[ipv4-addr:value IN ('192.168.122.83', '192.168.122.84')]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((src_ip IN ("192.168.122.83", "192.168.122.84")) OR (dest_ip IN ("192.168.122.83", "192.168.122.84"))) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)


if __name__ == '__main__':
    unittest.main()
