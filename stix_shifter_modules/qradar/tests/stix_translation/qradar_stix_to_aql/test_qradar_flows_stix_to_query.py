from stix_shifter.stix_translation import stix_translation
import unittest
import random
import json

options_file = open('stix_shifter_modules/qradar/tests/stix_translation/qradar_stix_to_aql/options.json').read()
selections_file = open('stix_shifter_modules/qradar/stix_translation/json/aql_flows_fields.json').read()
protocols_file = open('stix_shifter_modules/qradar/stix_translation/json/network_protocol_map.json').read()
OPTIONS = json.loads(options_file)
DEFAULT_SELECTIONS = json.loads(selections_file)
DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5
PROTOCOLS = json.loads(protocols_file)
MAPPING_ERROR = "Unable to map the following STIX objects and properties to data source fields:"


selections = "SELECT {}".format(", ".join(DEFAULT_SELECTIONS['default']))
from_statement = " FROM flows "


default_limit = "limit {}".format(DEFAULT_LIMIT)
default_time = "last {} minutes".format(DEFAULT_TIMERANGE)

translation = stix_translation.StixTranslation()


def _test_query_assertions(query, selections, from_statement, where_statement):
    assert query['queries'] == [selections + from_statement + where_statement], "Actual Query:\n%s\n\nExpected Query:\n%s" % (query['queries'], [selections + from_statement + where_statement])


def _translate_query(stix_pattern):
    return translation.translate('qradar:flows', 'query', '{}', stix_pattern)


class TestStixToAql(unittest.TestCase, object):

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84/10']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (INCIDR('192.168.122.84/10',sourceip) OR INCIDR('192.168.122.84/10',destinationip)) OR (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83') {} {}".format(
            default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_ipv6_query(self):
        stix_pattern = "[ipv6-addr:value = '3001:0:0:0:0:0:0:2']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (sourcev6 = '3001:0:0:0:0:0:0:2' OR destinationv6 = '3001:0:0:0:0:0:0:2') {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_network_traffic_ports_query(self):
        stix_pattern = "[network-traffic:src_port = 123 OR network-traffic:dst_port = 456]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE destinationport = '456' OR sourceport = '123' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_network_traffic_protocols(self):
        for key, value in PROTOCOLS.items():
            # Test for both upper and lower case protocols in the STIX pattern
            if random.randint(0, 1) == 0:
                key = key.upper()
            stix_pattern = "[network-traffic:protocols[*] = '" + key + "']"
            query = _translate_query(stix_pattern)
        where_statement = "WHERE protocolid = '{}' {} {}".format(value, default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_network_traffic_start_end(self):
        stix_pattern = "[network-traffic:start = '2018-06-14T08:36:24.000Z' AND network-traffic:end = '2018-06-14T08:36:24.567Z']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE endtime = '1528965384567' AND starttime = '1528965384000' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_network_traffic_src_dst_ipv4_ref(self):
        stix_pattern = "[network-traffic:src_ref.value = '192.168.122.83' OR network-traffic:dst_ref.value = '192.168.122.84/10']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE INCIDR('192.168.122.84/10',destinationip) OR sourceip = '192.168.122.83' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_network_traffic_src_dst_ipv6_ref(self):
        stix_pattern = "[network-traffic:src_ref.value = '3001:0:0:0:0:0:0:2' OR network-traffic:dst_ref.value = '3001:2:4:7:3:0:0:1/32']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE INCIDR('3001:2:4:7:3:0:0:1/32',destinationv6) OR sourcev6 = '3001:0:0:0:0:0:0:2' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_src_dst_byte_and_packet(self):
        start_time_01 = "t'2016-06-01T01:30:00.123Z'"
        stop_time_01 = "t'2016-06-01T02:20:00.123Z'"
        unix_start_time_01 = 1464744600123
        unix_stop_time_01 = 1464747600123
        stix_pattern = "[(network-traffic:src_byte_count = 306 AND network-traffic:dst_byte_count = 604) OR (network-traffic:src_packets = 2898 AND network-traffic:dst_packets = 1)] START {} STOP {}".format(start_time_01, stop_time_01)
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (destinationpackets = '1' AND sourcepackets = '2898') OR (destinationbytes = '604' AND sourcebytes = '306') {} START {} STOP {}".format(default_limit, unix_start_time_01, unix_stop_time_01)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_text_search(self):
        stix_pattern = "[artifact:payload_bin LIKE '%Set-ItemProperty%' AND artifact:payload_bin LIKE '%New-Item%']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE TEXT SEARCH '%New-Item% AND %Set-ItemProperty%' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_combined_observation_expression_with_qualifier(self):
        stix_pattern = "([ipv4-addr:value = '192.168.1.2'] OR [network-traffic:src_port = 8080]) START t'2020-09-11T13:00:52.000Z' STOP t'2020-09-11T13:59:04.000Z'"
        query = _translate_query(stix_pattern)
        where_statement_01 = "WHERE (sourceip = '192.168.1.2' OR destinationip = '192.168.1.2') limit 10000 START 1599829252000 STOP 1599832744000"
        where_statement_02 = "WHERE sourceport = '8080' limit 10000 START 1599829252000 STOP 1599832744000"
        assert len(query['queries']) == 2
        assert query['queries'][0] == selections + from_statement + where_statement_01
        assert query['queries'][1] == selections + from_statement + where_statement_02

    def test_sha256hash_query(self):
        stix_pattern = "[file:hashes.'SHA-256' = 'abc123']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE sha256hash = 'abc123' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_sha1hash_query(self):
        stix_pattern = "[file:hashes.'SHA-1' = 'abc123']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE sha1hash = 'abc123' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_md5hash_query(self):
        stix_pattern = "[file:hashes.MD5 = 'abc123']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE md5hash = 'abc123' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_domainname_query(self):
        stix_pattern = "[domain-name:value = 'example.com']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE dnsdomainname LIKE '%example.com%' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_filename_query(self):
        stix_pattern = "[file:name = 'abc123']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE filename = 'abc123' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_filetype_query(self):
        stix_pattern = "[file:'mime-type' = 'application/json']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE contenttype = 'application/json' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_filesize_query(self):
        stix_pattern = "[file:size > 1234]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE filesize > 1234 {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_fileentropy_query(self):
        stix_pattern = "[x-qradar:file_entropy < 6.5]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE fileentropy < 6.5 {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_httpreqhost_query(self):
        stix_pattern = "[network-traffic:extensions.'http-request-ext'.request_header.Host = 'example.com' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE httphost = 'example.com' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_httpreqreferer_query(self):
        stix_pattern = "[network-traffic:extensions.'http-request-ext'.request_header.Referer = 'example.com' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE httpreferrer = 'example.com' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_httpreqserver_query(self):
        stix_pattern = "[network-traffic:extensions.'http-request-ext'.request_header.Server = 'example.com' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE httpserver = 'example.com' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_httprequseragent_query(self):
        stix_pattern = "[network-traffic:extensions.'http-request-ext'.request_header.'User-Agent' = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0)' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE httpuseragent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0)' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_httpreqcontenttype_query(self):
        stix_pattern = "[network-traffic:extensions.'http-request-ext'.request_header.'Content-Type' = 'application/json' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE contenttype = 'application/json' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_httprequestversion_query(self):
        stix_pattern = "[network-traffic:extensions.'http-request-ext'.request_version = 'HTTP/1.1' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE httpversion = 'HTTP/1.1' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_httpresponsecode_query(self):
        stix_pattern = "[x-qradar:http_response_code = 200 ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE httpresponsecode = '200' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_flowtype_query(self):
        stix_pattern = "[x-qradar:flow_type = 'Standard Flow' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE flowtype = 'Standard Flow' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_flowid_query(self):
        stix_pattern = "[network-traffic:ipfix.flowId = 1234 ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE flowid = '1234' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_ja3_query(self):
        stix_pattern = "[x-qradar:tls_ja3_hash = 'abc123' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE tlsja3hash = 'abc123' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_ja3s_query(self):
        stix_pattern = "[x-qradar:tls_ja3s_hash = 'abc123' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE tlsja3shash = 'abc123' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_suspectcontent_query(self):
        stix_pattern = "[x-qradar:suspect_content_descriptions = 'nonstandard port' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE suspectcontentdescriptions = 'nonstandard port' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_tlssni_query(self):
        stix_pattern = "[x-qradar:tls_server_name_indication = 'example.com' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE tlsservernameindication = 'example.com' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_url_query(self):
        stix_pattern = "[url:value = 'example.com' ]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE (dnsdomainname LIKE '%example.com%' OR tlsservernameindication LIKE '%example.com%' OR httphost LIKE '%example.com%') {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)
    
    def test_in_operators(self):
        stix_pattern = "[network-traffic:dst_ref.value IN ('1.1.1.1', '2.2.2.2')] OR [network-traffic:dst_port IN ('22','443')]"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE str(destinationip) IN ('1.1.1.1', '2.2.2.2') OR destinationport IN ('22', '443') {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_hasoffense_query(self):
        stix_pattern = "[x-qradar:has_offense = 'true']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE hasoffense = 'true' {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_inoffense_query(self):
        stix_pattern = "[x-qradar:INOFFENSE = '125']"
        query = _translate_query(stix_pattern)
        where_statement = "WHERE INOFFENSE('125') {} {}".format(default_limit, default_time)
        _test_query_assertions(query, selections, from_statement, where_statement)
