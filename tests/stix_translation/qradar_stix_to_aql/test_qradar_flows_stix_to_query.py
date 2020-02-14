from stix_shifter.stix_translation import stix_translation
import unittest
import random
import json

options_file = open('tests/stix_translation/qradar_stix_to_aql/options.json').read()
selections_file = open('stix_shifter/stix_translation/src/modules/qradar/json/aql_flow_fields.json').read()
protocols_file = open('stix_shifter/stix_translation/src/modules/qradar/json/network_protocol_map.json').read()
OPTIONS = json.loads(options_file)
DEFAULT_SELECTIONS = json.loads(selections_file)
DEFAULT_LIMIT = 10000
DEFAULT_TIMERANGE = 5
PROTOCOLS = json.loads(protocols_file)
MAPPING_ERROR = "Unable to map the following STIX objects and properties to data source fields:"


selections = "SELECT {}".format(", ".join(DEFAULT_SELECTIONS['default']))
custom_selections = "SELECT {}".format(", ".join(OPTIONS['select_fields']))
from_statement = " FROM flows "


default_limit = "limit {}".format(DEFAULT_LIMIT)
default_time = "last {} minutes".format(DEFAULT_TIMERANGE)

translation = stix_translation.StixTranslation()


def _test_query_assertions(query, selections, from_statement, where_statement):
    assert query['queries'] == [selections + from_statement + where_statement]


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
