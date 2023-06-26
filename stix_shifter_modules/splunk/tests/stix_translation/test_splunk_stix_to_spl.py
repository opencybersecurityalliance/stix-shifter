import unittest
import random
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode


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
    "dest_ip",
    "dest_port",
    "dest_mac",
    "file_hash",
    "user",
    "url",
    "protocol",
    "host",
    "source",
    "severity",
    "process",
    "process_id",
    "process_name",
    "process_exec",
    "process_path",
    "process_hash",
    "process_guid",
    "parent_process",
    "parent_process_id",
    "parent_process_name",
    "parent_process_exec",
    "description",
    "signature",
    "signature_id",
    "query",
    "answer",
    "transport",
    "bytes_in",
    "bytes_out",
    "packets_in",
    "packets_out",
    "direction",
    "name",
    "message_type",
    "query_count",
    "query_type",
    "record_type",
    "reply_code",
    "reply_code_id",
    "vendor_product",
    "duration",
    "transaction_id",
    "action",
    "file_access_time",
    "file_acl",
    "registry_hive",
    "registry_path",
    "registry_key_name",
    "registry_value_data",
    "registry_value_name",
    "registry_value_text",
    "registry_value_type",
    "status",
    "ssl_version",
    "ssl_serial",
    "ssl_issuer",
    "ssl_subject",
    "ssl_signature_algorithm",
    "ssl_publickey_algorithm",
    "ssl_start_time",
    "ssl_end_time",
    "ssl_is_valid",
    "ssl_issuer_common_name",
    "ssl_subject_common_name",
    "ssl_name",
    "ssl_publickey",
    "ssl_issuer_email",
    "ssl_subject_email",
    "ssl_issuer_email_domain",
    "ssl_subject_email_domain",
    "ssl_issuer_organization",
    "ssl_subject_organization",
    "recipient",
    "subject",
    "file_hash",
    "file_name",
    "file_size",
    "recipient_domain",
    "src_user_domain",
    "internal_message_id",
    "message_id",
    "message_info",
    "app",
    "authentication_method",
    "authentication_service",
    "dest",
    "src",
    "src_user",
    "user_name",
    "user_id",
    "user_type",
    "user_agent",
    "http_method",
    "http_referrer",
    "http_user_agent",
    "uri_path",
    "uri_query",
    "os",
    "dvc",
    "id",
    "msft",
    "cve",
    "cvss",
    "mskb",
    "type",
    "eventtype",
    "event_id",
    "mitre_technique_id",
    "mem_used",
    "original_file_name",
    "file_create_time",
    "file_modify_time"
])


def _test_query_assertions(query, queries):
    assert query['queries'] == [queries]


class TestStixToSpl(unittest.TestCase, object):

    def test_ipv4_query(self):
        """ test to check ipv4 stix pattern to native data source query """
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (((src_ip = "192.168.122.84") OR (dest_ip = "192.168.122.84")) OR ' \
                  f'((src_ip = "192.168.122.83") OR (dest_ip = "192.168.122.83"))) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_ipv6_query(self):
        """ test to check ipv6 stix pattern to native data source query """
        stix_pattern = "[ipv6-addr:value = 'fe80::8c3b:a720:dc5c:2abf%19']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((src_ip = "fe80::8c3b:a720:dc5c:2abf%19") ' \
                  f'OR (dest_ip = "fe80::8c3b:a720:dc5c:2abf%19")) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_network_traffic_query(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = r"[network-traffic:dst_port = 3389]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (dest_port = 3389) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_network_query_greater_than(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = r"[network-traffic:dst_port > 3389]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (dest_port > 3389) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_network_query_not_equals(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = r"[network-traffic:dst_port != 3389]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (dest_port != 3389) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_network_query_less_than(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = r"[network-traffic:dst_port < 3389]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (dest_port < 3389) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_network_query_lessthan_or_equals(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = r"[network-traffic:dst_port <= 3389]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (dest_port <= 3389) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_network_query_greaterthan_or_equals(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = r"[network-traffic:dst_port >= 3389]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (dest_port >= 3389) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_network_query_in_operator(self):
        """ test to check network traffic stix pattern to native data source query """
        stix_pattern = r"[network-traffic:dst_port IN (80,3389)]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (dest_port IN (80, 3389)) earliest=\"-5minutes\" | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_url_query(self):
        """ test to check url stix pattern to native data source query """
        stix_pattern = "[url:value = 'http://www.testaddress.com']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (url = "http://www.testaddress.com") earliest="-5minutes" | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_not_equal_operator(self):
        """ test not equal operator stix pattern to native data source query """
        stix_pattern = "[url:value != 'http://www.testaddress.com']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (url != "http://www.testaddress.com") earliest="-5minutes" | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_followedby_operator(self):
        """ test followedby operator stix pattern to native data source query """
        stix_pattern = r"[file:name MATCHES '^x.\\..*$'] FOLLOWEDBY " \
                       r"[file:name = 'y1.exe'] START t'2022-01-19T11:00:00.000Z' " \
                       r"STOP t'2023-02-28T11:00:00.003Z'"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search |eval latest=[search ((file_name = "y1.exe") ' \
                  f'OR (process_name = "y1.exe") OR (parent_process_name = "y1.exe") ' \
                  f'OR (process_exec = "y1.exe") OR (parent_process_exec = "y1.exe")) ' \
                  f'earliest="01/19/2022:11:00:00" latest="02/28/2023:11:00:00" | ' \
                  f'append [makeresults 1 | eval _time=0] | head 1 | ' \
                  f'return $_time] | where ((match(file_name, "^x.\\..*$")) ' \
                  f'OR (match(process_name, "^x.\\..*$")) ' \
                  f'OR (match(parent_process_name, "^x.\\..*$")) ' \
                  f'OR (match(process_exec, "^x.\\..*$")) ' \
                  f'OR (match(parent_process_exec, "^x.\\..*$"))) | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_NOT_operator(self):
        """ test NOT operator stix pattern to native data source query """
        stix_pattern = "[url:value NOT = 'http://www.testaddress.com']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (NOT (url = "http://www.testaddress.com")) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_mac_address_query(self):
        """ test mac address stix pattern to native data source query """
        stix_pattern = "[mac-addr:value = '00-00-5E-00-53-00']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((src_mac = "00-00-5E-00-53-00") OR (dest_mac = "00-00-5E-00-53-00")) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_domain_query(self):
        """ test domain-name stix pattern to native data source query """
        stix_pattern = "[domain-name:value = 'example.com']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((query = "example.com") ' \
                  f'OR (recipient_domain = "example.com") ' \
                  f'OR (src_user_domain = "example.com") ' \
                  f'OR (ssl_issuer_email_domain = "example.com") ' \
                  f'OR (ssl_subject_email_domain = "example.com")) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_query_from_multiple_observation_expressions_joined_by_AND(self):
        """ test multiple observation stix pattern to native data source query """
        stix_pattern = "[domain-name:value = 'example.com'] AND " \
                       "[mac-addr:value = '00-00-5E-00-53-00']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        # Expect the STIX AND to convert to an SPL OR.
        queries = f'search ((query = "example.com") ' \
                  f'OR (recipient_domain = "example.com") ' \
                  f'OR (src_user_domain = "example.com") ' \
                  f'OR (ssl_issuer_email_domain = "example.com") ' \
                  f'OR (ssl_subject_email_domain = "example.com")) ' \
                  f'OR ((src_mac = "00-00-5E-00-53-00") ' \
                  f'OR (dest_mac = "00-00-5E-00-53-00")) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_query_from_multiple_comparison_expressions_joined_by_AND(self):
        """ test multiple comparison stix pattern to native data source query """
        stix_pattern = "[domain-name:value = 'example.com' AND " \
                       "mac-addr:value = '00-00-5E-00-53-00']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        # Expect the STIX AND to convert to an AQL AND.
        queries = f'search (((src_mac = "00-00-5E-00-53-00") ' \
                  f'OR (dest_mac = "00-00-5E-00-53-00")) ' \
                  f'AND ((query = "example.com") ' \
                  f'OR (recipient_domain = "example.com") ' \
                  f'OR (src_user_domain = "example.com") ' \
                  f'OR (ssl_issuer_email_domain = "example.com") ' \
                  f'OR (ssl_subject_email_domain = "example.com"))) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_query_from_morethan_two_comparison_expressions_joined_by_and(self):
        """ test multiple more than two comparison stix pattern to native data source query """
        stix_pattern = r"[domain-name:value = 'example.com' AND " \
                       r"mac-addr:value = '00-00-5E-00-53-00' AND " \
                       r"ipv4-addr:value = '192.168.122.84']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        # Expect the STIX AND to convert to an AQL AND.
        queries = f'search (((src_ip = "192.168.122.84") OR (dest_ip = "192.168.122.84")) ' \
                  f'AND (((src_mac = "00-00-5E-00-53-00") ' \
                  f'OR (dest_mac = "00-00-5E-00-53-00")) ' \
                  f'AND ((query = "example.com") ' \
                  f'OR (recipient_domain = "example.com") ' \
                  f'OR (src_user_domain = "example.com") ' \
                  f'OR (ssl_issuer_email_domain = "example.com") ' \
                  f'OR (ssl_subject_email_domain = "example.com")))) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_multiple_observation_query(self):
        """ test multiple observation stix pattern to native data source query """
        stix_pattern = r"([file: hashes.MD5 = '0bbd4d92d3a0178463ef6e0ad46c986a' " \
                       r"AND file:name = 'log' AND x-oca-event:code = '4998'] " \
                       r"AND [file:created = 'PE'] " \
                       r"AND [ x-oca-asset:hostname = '21.6.6.1200' " \
                       r"AND network-traffic:src_port > 80 ]) " \
                       r"START t'2022-01-19T11:00:00.000Z' STOP t'2023-03-09T11:00:00.003Z'"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        # Expect the STIX AND to convert to an AQL AND.
        queries = f'search ((signature_id = "4998") AND (((file_name = "log") ' \
                  f'OR (process_name = "log") OR (parent_process_name = "log") ' \
                  f'OR (process_exec = "log") OR (parent_process_exec = "log")) ' \
                  f'AND (file_hash = "0bbd4d92d3a0178463ef6e0ad46c986a"))) ' \
                  f'OR (file_create_time = "PE") OR ((src_port > 80) ' \
                  f'AND (host = "21.6.6.1200")) earliest="01/19/2022:11:00:00" ' \
                  f'latest="03/09/2023:11:00:00" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_file_query(self):
        """ test file stix pattern to native data source query """
        stix_pattern = "[file:name = 'some_file.exe']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((file_name = "some_file.exe") ' \
                  f'OR (process_name = "some_file.exe") ' \
                  f'OR (parent_process_name = "some_file.exe") ' \
                  f'OR (process_exec = "some_file.exe") ' \
                  f'OR (parent_process_exec = "some_file.exe")) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_file_hash_query(self):
        """ test file stix pattern to native data source query """
        stix_pattern = "[file:hashes.'SHA-1' = '5e5a7065f1b551eb3632fb189ce1baefd23158aa']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (file_hash = \"5e5a7065f1b551eb3632fb189ce1baefd23158aa\") ' \
                  f'earliest=\"-5minutes\" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_dst_ref_queries(self):
        """ test network-traffic stix pattern to native data source query """
        stix_pattern = "[network-traffic:dst_ref.value = '192.168.122.83']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (dest_ip = "192.168.122.83") earliest="-5minutes" | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_port_queries(self):
        """ test network-traffic stix pattern to native data source query """
        stix_pattern = "[network-traffic:src_port = 12345 OR network-traffic:dst_port = 23456]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((dest_port = 23456) OR (src_port = 12345)) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_unmapped_attribute_handling_with_OR(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com' OR unmapped:attribute = 'something']"
        translated_query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (url = "http://www.testaddress.com") earliest="-5minutes" | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(translated_query, queries)

    def test_unmapped_attribute_handling_with_AND(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com' AND unmapped:attribute = 'something']"
        result = translation.translate('splunk', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert "data mapping error : Unable to map the following STIX objects and properties: " \
            "['unmapped:attribute'] to data source fields" in result['error']

    def test_invalid_stix_pattern(self):
        """ test invalid stix pattern to native data source query """
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('splunk', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert False is result['success']
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_network_traffic_protocols(self):
        """ test network-traffic protocol """
        for key, value in protocols.items():
            # Test for both upper and lower case protocols in the STIX pattern
            if random.randint(0, 1) == 0:
                key = key.upper()
            stix_pattern = "[network-traffic:protocols[*] = '" + key + "']"
            query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = 'search ((protocol = "' + key + '") OR (transport = "' + key + '")) earliest="{}" | head {} | fields {}'.format(default_time_range_spl,
                                                                                                 DEFAULT_LIMIT, fields)
        _test_query_assertions(query, queries)

    def test_network_traffic_start_stop(self):
        """test stix pattern with start stop qualifier to native data source query"""
        stix_pattern = "[network-traffic:dst_packets = 400 " \
                       "OR network-traffic:src_packets = 500]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((packets_out = 500) OR (packets_in = 400)) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_start_stop_qualifiers(self):
        """test stix pattern with start stop qualifier to native data source query"""
        stix_pattern = "[network-traffic:src_port = 37020] START t'2016-06-01T01:30:00.000Z' " \
                       "STOP t'2016-06-01T02:20:00.000Z' OR [ipv4-addr:value = '192.168.122.83'] " \
                       "START t'2016-06-01T03:55:00.000Z' STOP t'2016-06-01T04:30:00.000Z'"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (src_port = 37020) earliest="06/01/2016:01:30:00" ' \
                  f'latest="06/01/2016:02:20:00" OR ((src_ip = "192.168.122.83") ' \
                  f'OR (dest_ip = "192.168.122.83")) earliest="06/01/2016:03:55:00" ' \
                  f'latest="06/01/2016:04:30:00" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_start_stop_qualifiers_one_time(self):
        """test stix pattern with start stop qualifier to native data source query"""
        stix_pattern = "[network-traffic:src_port = 37020] START t'2016-06-01T01:30:00.000Z' " \
                       "STOP t'2016-06-01T02:20:00.000Z'"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (src_port = 37020) earliest="06/01/2016:01:30:00" ' \
                  f'latest="06/01/2016:02:20:00" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_start_stop_qualifiers_seconds(self):
        """test stix pattern with start stop qualifier to native data source query"""
        stix_pattern = "[network-traffic:src_port = 37020] START t'2016-06-01T01:30:00Z' " \
                       "STOP t'2016-06-01T02:20:00Z'"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (src_port = 37020) earliest="06/01/2016:01:30:00" ' \
                  f'latest="06/01/2016:02:20:00" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_issubset_operator(self):
        """test issubset operator stix pattern to native data source query"""
        stix_pattern = "[ipv4-addr:value ISSUBSET '198.51.100.0/24']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search earliest="-5minutes" | ' \
                  f'where ((cidrmatch("198.51.100.0/24", src_ip)) ' \
                  f'OR (cidrmatch("198.51.100.0/24", dest_ip))) | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_custom_time_limit_and_result_count(self):
        """test custom time limit and result count native data source query"""
        stix_pattern = "[ipv4-addr:value = '192.168.122.83']"
        options = {"time_range": 25, "result_limit": 5000}
        query = translation.translate('splunk', 'query', '{}', stix_pattern, options)
        queries = f'search ((src_ip = "192.168.122.83") OR (dest_ip = "192.168.122.83")) ' \
                  f'earliest="-25minutes" | head 5000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_custom_index(self):
        """test custom index native data source query"""
        stix_pattern = "[ipv4-addr:value = '192.168.122.83']"
        options = {"index": "my_index"}
        query = translation.translate('splunk', 'query', '{}', stix_pattern, options)
        queries = f'search index="my_index" ((src_ip = "192.168.122.83") ' \
                  f'OR (dest_ip = "192.168.122.83")) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_custom_indices(self):
        """test custom indices native data source query"""
        stix_pattern = "[ipv4-addr:value = '192.168.122.83']"
        options = {"index": "i1, i2"}
        query = translation.translate('splunk', 'query', '{}', stix_pattern, options)
        queries = f'search index="i1" OR index="i2" ((src_ip = "192.168.122.83") ' \
                  f'OR (dest_ip = "192.168.122.83")) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_custom_mapping(self):
        """test custom mapping native data source query"""
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
        queries = f'search ((mac = "00-00-5E-00-53-00") AND ((src_ip = "192.168.122.83") ' \
                  f'OR (dest_ip = "192.168.122.83"))) earliest="-15minutes" | ' \
                  f'head 1000 | fields src_ip, src_port'
        _test_query_assertions(query, queries)

    def test_free_search(self):
        """test free search native data source query"""
        stix_pattern = "[x-readable-payload:value = 'malware']"
        options = {"time_range": 25, "result_limit": 5000}
        query = translation.translate('splunk', 'query', '{}', stix_pattern, options)
        queries = f'search _raw=*malware* earliest="-25minutes" | head 5000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_event_query(self):
        """test event native data source query"""
        stix_pattern = "[x-oca-event:code = 1]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (signature_id = 1) earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_x_oca_asset_by_hostname(self):
        """test x-oca-asset native data source query"""
        stix_pattern = "[x-oca-asset:hostname = 'omer']"
        result_query = translation.translate('splunk', 'query', '{}', stix_pattern)
        expected_query = f'search (host = "omer") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(result_query, expected_query)

    def test_x_oca_event(self):
        """test x-oca-event native data source query"""
        stix_pattern = "[(x-oca-event:action = 'DNS Query' OR x-oca-event:code = 22) " \
                       "AND (x-oca-event:module = 'XmlWinEventLog:Microsoft-Windows-Sysmon/Operational')]"
        result_query = translation.translate('splunk', 'query', '{}', stix_pattern)
        expected_queries = f'search ((source = "XmlWinEventLog:Microsoft-Windows-Sysmon/Operational") ' \
                           f'AND ((signature_id = 22) OR (signature = "DNS Query"))) ' \
                           f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(result_query, expected_queries)

    def test_x_oca_event_missing_vals(self):
        """test x-oca-event native data source query"""
        stix_pattern = "[(x-oca-event:action = '' OR x-oca-event:code = '') " \
                       "AND (x-oca-event:module = '')]"
        result_query = translation.translate('splunk', 'query', '{}', stix_pattern)
        print(result_query)
        expected_queries = f'search ((source = "") AND ((signature_id = "") ' \
                           f'OR (signature = ""))) earliest="-5minutes" | ' \
                           f'head 10000 | fields {fields}'
        _test_query_assertions(result_query, expected_queries)

    def test_proc_command_line_query(self):
        """test process command line native data source query"""
        stix_pattern = "[process:command_line = 'wmic.exe process call create calc']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((process = "wmic.exe process call create calc") ' \
                  f'OR (parent_process = "wmic.exe process call create calc")) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_proc_name_query(self):
        """test process name native data source query"""
        stix_pattern = "[process:name = 'wmic.exe']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((process_name = "wmic.exe") OR ' \
                  f'(parent_process_name = "wmic.exe")) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_ipv4_query_in_operator(self):
        """test ipv4 native data source query"""
        stix_pattern = "[ipv4-addr:value IN ('192.168.122.83', '192.168.122.84')]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search ((src_ip IN ("192.168.122.83", "192.168.122.84")) ' \
                  f'OR (dest_ip IN ("192.168.122.83", "192.168.122.84"))) ' \
                  f'earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_like(self):
        """test like operator native data source query"""
        stix_pattern = "[file:name LIKE 'x_.%']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search earliest="-5minutes" | where ((like(file_name, "x_.%")) ' \
                  f'OR (like(process_name, "x_.%")) ' \
                  f'OR (like(parent_process_name, "x_.%")) ' \
                  f'OR (like(process_exec, "x_.%")) ' \
                  f'OR (like(parent_process_exec, "x_.%"))) | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_like_or_equal(self):
        """test like operator native data source query"""
        stix_pattern = "[file:name LIKE 'x_.%' OR file:name = 'y1.exe']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search earliest="-5minutes" | where (((file_name = "y1.exe") ' \
                  f'OR (process_name = "y1.exe") ' \
                  f'OR (parent_process_name = "y1.exe") ' \
                  f'OR (process_exec = "y1.exe") ' \
                  f'OR (parent_process_exec = "y1.exe")) ' \
                  f'OR ((like(file_name, "x_.%")) ' \
                  f'OR (like(process_name, "x_.%")) ' \
                  f'OR (like(parent_process_name, "x_.%")) ' \
                  f'OR (like(process_exec, "x_.%")) ' \
                  f'OR (like(parent_process_exec, "x_.%")))) | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_match(self):
        """test match operator native data source query"""
        stix_pattern = r"[file:name MATCHES '^x.\\..*$']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search earliest="-5minutes" | where ((match(file_name, "^x.\\..*$")) ' \
                  f'OR (match(process_name, "^x.\\..*$")) ' \
                  f'OR (match(parent_process_name, "^x.\\..*$")) ' \
                  f'OR (match(process_exec, "^x.\\..*$")) ' \
                  f'OR (match(parent_process_exec, "^x.\\..*$"))) | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_multiple_comparison_with_like_and_match(self):
        """test multiple comparison match and like operator native data source query"""
        stix_pattern = r"[file:name MATCHES '^x.\\..*$' OR file:name = 'y1.exe' " \
                       r"AND file:name LIKE 'x_.%' ] START t'2022-01-19T11:00:00.000Z' " \
                       r"STOP t'2023-02-28T11:00:00.003Z'"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search earliest="01/19/2022:11:00:00" latest="02/28/2023:11:00:00" | ' \
                  f'where ((((like(file_name, "x_.%")) ' \
                  f'OR (like(process_name, "x_.%")) ' \
                  f'OR (like(parent_process_name, "x_.%")) ' \
                  f'OR (like(process_exec, "x_.%")) ' \
                  f'OR (like(parent_process_exec, "x_.%"))) ' \
                  f'AND ((file_name = "y1.exe") OR (process_name = "y1.exe") ' \
                  f'OR (parent_process_name = "y1.exe") ' \
                  f'OR (process_exec = "y1.exe") ' \
                  f'OR (parent_process_exec = "y1.exe"))) ' \
                  f'OR ((match(file_name, "^x.\\..*$")) ' \
                  f'OR (match(process_name, "^x.\\..*$")) ' \
                  f'OR (match(parent_process_name, "^x.\\..*$")) ' \
                  f'OR (match(process_exec, "^x.\\..*$")) ' \
                  f'OR (match(parent_process_exec, "^x.\\..*$")))) | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_match_or_equal(self):
        """test multiple comparison match and OR operator native data source query"""
        stix_pattern = r"[file:name MATCHES '^x.\\..*$' OR file:name = 'y1.exe']"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search earliest="-5minutes" | where (((file_name = "y1.exe") ' \
                  f'OR (process_name = "y1.exe") OR (parent_process_name = "y1.exe") ' \
                  f'OR (process_exec = "y1.exe") ' \
                  f'OR (parent_process_exec = "y1.exe")) ' \
                  f'OR ((match(file_name, "^x.\\..*$")) ' \
                  f'OR (match(process_name, "^x.\\..*$")) ' \
                  f'OR (match(parent_process_name, "^x.\\..*$")) ' \
                  f'OR (match(process_exec, "^x.\\..*$")) ' \
                  f'OR (match(parent_process_exec, "^x.\\..*$")))) | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_severity_informational(self):
        """test severity native data source query"""
        stix_pattern = r"[x-ibm-finding:severity = 15]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (severity = "informational") earliest="-5minutes" | ' \
                  f'head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_severity_low(self):
        """test severity native data source query"""
        stix_pattern = r"[x-ibm-finding:severity = 25]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (severity = "low") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_severity_medium(self):
        """test severity native data source query"""
        stix_pattern = r"[x-ibm-finding:severity = 45]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (severity = "medium") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_severity_high(self):
        """test severity native data source query"""
        stix_pattern = r"[x-ibm-finding:severity = 65]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (severity = "high") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_severity_critical(self):
        """test severity native data source query"""
        stix_pattern = r"[x-ibm-finding:severity = 85]"
        query = translation.translate('splunk', 'query', '{}', stix_pattern)
        queries = f'search (severity = "critical") earliest="-5minutes" | head 10000 | fields {fields}'
        _test_query_assertions(query, queries)

    def test_out_of_range_severity(self):
        """test severity native data source query"""
        stix_pattern = r"[x-ibm-finding:severity = 105]"
        result = translation.translate('splunk', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert 'splunk connector error => wrong parameter : only 1-100 integer ' \
               'values are supported with severity field' in result['error']


if __name__ == '__main__':
    unittest.main()
