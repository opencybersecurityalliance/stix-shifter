from stix_shifter import stix_shifter
from stix_shifter.src.modules.qradar import qradar_data_mapping
import unittest
import random

selections = "SELECT QIDNAME(qid) as qidname, qid as qid, CATEGORYNAME(category) as categoryname, \
category as categoryid, CATEGORYNAME(highlevelcategory) as high_level_category_name, \
highlevelcategory as high_level_category_id, logsourceid as logsourceid, LOGSOURCETYPENAME(logsourceid) as logsourcename, starttime as starttime, \
endtime as endtime, devicetime as devicetime, sourceaddress as sourceip, sourceport as sourceport, sourcemac as sourcemac, \
destinationaddress as destinationip, destinationport as destinationport, destinationmac as destinationmac, \
username as username, eventdirection as direction, identityip as identityip, identityhostname as identity_host_name, \
eventcount as eventcount, PROTOCOLNAME(protocolid) as protocol, BASE64(payload) as payload, URL as url, magnitude as magnitude, Filename as filename, URL as domainname"

from_statement = " FROM events "

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

default_limit = "limit 10000"
default_time = "last 5 minutes"

shifter = stix_shifter.StixShifter()


class TestStixToAql(unittest.TestCase, object):

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' or ipv4-addr:value = '192.168.122.84']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)

        where_statement = "WHERE (sourceip = '192.168.122.84' OR destinationip = '192.168.122.84' OR identityip = '192.168.122.84') OR (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83' OR identityip = '192.168.122.83') {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.84'}, {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_ipv6_query(self):
        stix_pattern = "[ipv6-addr:value = '3001:0:0:0:0:0:0:2']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement = "WHERE (sourceip = '3001:0:0:0:0:0:0:2' OR destinationip = '3001:0:0:0:0:0:0:2') {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'ipv6-addr:value', 'comparison_operator': '=', 'value': '3001:0:0:0:0:0:0:2'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_url_query(self):
        stix_pattern = "[url:value = 'http://www.testaddress.com']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement = "WHERE url = 'http://www.testaddress.com' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'url:value', 'comparison_operator': '=', 'value': 'http://www.testaddress.com'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_mac_address_query(self):
        stix_pattern = "[mac-addr:value = '00-00-5E-00-53-00']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement = "WHERE (sourcemac = '00-00-5E-00-53-00' OR destinationmac = '00-00-5E-00-53-00') {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_query_from_multiple_observation_expressions_joined_by_and(self):
        stix_pattern = "[url:value = 'www.example.com'] and [mac-addr:value = '00-00-5E-00-53-00']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        # Expect the STIX and to convert to an AQL OR.
        where_statement = "WHERE url = 'www.example.com' OR (sourcemac = '00-00-5E-00-53-00' OR destinationmac = '00-00-5E-00-53-00') {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'url:value', 'comparison_operator': '=', 'value': 'www.example.com'}, {'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_query_from_multiple_comparison_expressions_joined_by_and(self):
        stix_pattern = "[url:value = 'www.example.com' and mac-addr:value = '00-00-5E-00-53-00']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        # Expect the STIX and to convert to an AQL AND.
        where_statement = "WHERE (sourcemac = '00-00-5E-00-53-00' OR destinationmac = '00-00-5E-00-53-00') AND url = 'www.example.com' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}, {'attribute': 'url:value', 'comparison_operator': '=', 'value': 'www.example.com'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_file_query(self):
        # TODO: Add support for file hashes. Unsure at this point how QRadar queries them
        stix_pattern = "[file:name = 'some_file.exe']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement = "WHERE filename = 'some_file.exe' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'file:name', 'comparison_operator': '=', 'value': 'some_file.exe'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_port_queries(self):
        stix_pattern = "[network-traffic:src_port = 12345 or network-traffic:dst_port = 23456]"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement = "WHERE destinationport = '23456' OR sourceport = '12345' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'network-traffic:dst_port', 'comparison_operator': '=', 'value': 23456}, {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 12345}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_unmapped_attribute(self):
        data_mapping_exception = qradar_data_mapping.DataMappingException
        stix_pattern = "[network-traffic:some_invalid_attribute = 'whatever']"
        self.assertRaises(data_mapping_exception,
                          lambda: shifter.translate('qradar', 'query', '{}', stix_pattern))

    def test_user_account_query(self):
        stix_pattern = "[user-account:user_id = 'root']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement = "WHERE username = 'root' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'user-account:user_id', 'comparison_operator': '=', 'value': 'root'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_invalid_stix_pattern(self):
        stix_validation_exception = stix_shifter.StixValidationException
        stix_pattern = "[not_a_valid_pattern]"
        self.assertRaises(stix_validation_exception,
                          lambda: shifter.translate('qradar', 'query', '{}', stix_pattern))

    def test_network_traffic_protocols(self):
        for key, value in protocols.items():
            # Test for both upper and lower case protocols in the STIX pattern
            if random.randint(0, 1) == 0:
                key = key.upper()
            stix_pattern = "[network-traffic:protocols[*] = '" + key + "']"
            query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement = "WHERE protocolid = '{}' {} {}".format(value, default_limit, default_time)
        parsed_stix = [{'attribute': 'network-traffic:protocols[*]', 'comparison_operator': '=', 'value': key}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_network_traffic_start_stop(self):
        stix_pattern = "[network-traffic:'start' = '2018-06-14T08:36:24.000Z' or network-traffic:end = '2018-06-14T08:36:24.567Z']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement = "WHERE endtime = '1528965384567' OR starttime = '1528965384000' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'network-traffic:end', 'comparison_operator': '=', 'value': '2018-06-14T08:36:24.567Z'}, {'attribute': 'network-traffic:start', 'comparison_operator': '=', 'value': '2018-06-14T08:36:24.000Z'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_artifact_queries(self):
        stix_pattern = "[artifact:payload_bin matches 'some text']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement = "WHERE payload MATCHES '.*some text.*' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'artifact:payload_bin', 'comparison_operator': 'MATCHES', 'value': 'some text'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_start_stop_qualifiers_with_two_observations(self):
        start_time_01 = "t'2016-06-01T01:30:00.123Z'"
        stop_time_01 = "t'2016-06-01T02:20:00.123Z'"
        start_time_02 = "t'2016-06-01T03:55:00.123Z'"
        stop_time_02 = "t'2016-06-01T04:30:24.743Z'"
        epoch_start_time_01 = 1464744600123
        epoch_stop_time_01 = 1464747600123
        epoch_start_time_02 = 1464753300123
        epoch_stop_time_02 = 1464755424743
        stix_pattern = "[network-traffic:src_port = 37020 AND user-account:user_id = 'root'] START {} STOP {} OR [ipv4-addr:value = '192.168.122.83'] START {} STOP {}".format(start_time_01, stop_time_01, start_time_02, stop_time_02)
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement_01 = "WHERE username = 'root' AND sourceport = '37020' {} START {} STOP {}".format(default_limit, epoch_start_time_01, epoch_stop_time_01)
        where_statement_02 = "WHERE (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83' OR identityip = '192.168.122.83') {} START {} STOP {}".format(default_limit, epoch_start_time_02, epoch_stop_time_02)
        parsed_stix = [{'attribute': 'user-account:user_id', 'comparison_operator': '=', 'value': 'root'},
                       {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 37020},
                       {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        assert len(query['queries']) == 2
        assert query == {'queries': [selections + from_statement + where_statement_01, selections + from_statement + where_statement_02], 'parsed_stix': parsed_stix}

    def test_start_stop_qualifiers_with_three_observations(self):
        start_time_01 = "t'2016-06-01T00:00:00.123Z'"
        stop_time_01 = "t'2016-06-01T01:11:11.456Z'"
        start_time_02 = "t'2016-06-07T02:22:22.789Z'"
        stop_time_02 = "t'2016-06-07T03:33:33.012Z'"
        epoch_start_time_01 = 1464739200123
        epoch_stop_time_01 = 1464743471456
        epoch_start_time_02 = 1465266142789
        epoch_stop_time_02 = 1465270413012
        stix_pattern = "[network-traffic:src_port = 37020 AND network-traffic:dst_port = 635] START {} STOP {} OR [url:value = 'www.example.com'] OR [ipv4-addr:value = '333.333.333.0'] START {} STOP {}".format(
            start_time_01, stop_time_01, start_time_02, stop_time_02)
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement_01 = "WHERE destinationport = '635' AND sourceport = '37020' {} START {} STOP {}".format(default_limit, epoch_start_time_01, epoch_stop_time_01)
        where_statement_02 = "WHERE url = 'www.example.com' {} {}".format(default_limit, default_time)
        where_statement_03 = "WHERE (sourceip = '333.333.333.0' OR destinationip = '333.333.333.0' OR identityip = '333.333.333.0') {} START {} STOP {}".format(default_limit, epoch_start_time_02, epoch_stop_time_02)
        parsed_stix = [{'attribute': 'network-traffic:dst_port', 'comparison_operator': '=', 'value': 635},
                       {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 37020},
                       {'attribute': 'url:value', 'comparison_operator': '=', 'value': 'www.example.com'},
                       {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '333.333.333.0'}]
        assert len(query['queries']) == 3
        assert query == {'queries': [selections + from_statement + where_statement_01, selections + from_statement + where_statement_02, selections + from_statement + where_statement_03], 'parsed_stix': parsed_stix}

    def test_start_stop_qualifiers_with_missing_or_partial_milliseconds(self):
        # missing milliseconds
        start_time_01 = "t'2016-06-01T01:30:00Z'"
        stop_time_01 = "t'2016-06-01T02:20:00Z'"
        # one-digit millisecond
        start_time_02 = "t'2016-06-01T03:55:00.1Z'"
        # four-digit millisecond
        stop_time_02 = "t'2016-06-01T04:30:24.1243Z'"
        epoch_start_time_01 = 1464744600000
        epoch_stop_time_01 = 1464747600000
        epoch_start_time_02 = 1464753300000
        epoch_stop_time_02 = 1464755424000
        stix_pattern = "[user-account:user_id = 'root'] START {} STOP {} OR [ipv4-addr:value = '192.168.122.83'] START {} STOP {}".format(start_time_01, stop_time_01, start_time_02, stop_time_02)
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement_01 = "WHERE username = 'root' {} START {} STOP {}".format(default_limit, epoch_start_time_01, epoch_stop_time_01)
        where_statement_02 = "WHERE (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83' OR identityip = '192.168.122.83') {} START {} STOP {}".format(default_limit, epoch_start_time_02, epoch_stop_time_02)
        parsed_stix = [{'attribute': 'user-account:user_id', 'comparison_operator': '=', 'value': 'root'},
                       {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        assert len(query['queries']) == 2
        assert query == {'queries': [selections + from_statement + where_statement_01, selections + from_statement + where_statement_02], 'parsed_stix': parsed_stix}

    def test_set_operators(self):
        stix_pattern = "[ipv4-addr:value ISSUBSET '198.51.100.0/24']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement = "WHERE (INCIDR('198.51.100.0/24',sourceip) OR INCIDR('198.51.100.0/24',destinationip) OR INCIDR('198.51.100.0/24',identityip)) {} {}".format(default_limit, default_time)
        parsed_stix = [{'value': '198.51.100.0/24', 'comparison_operator': 'ISSUBSET', 'attribute': 'ipv4-addr:value'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_custom_qradar_fields_and_mapping(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83']"
        options = {
            "select_fields": [
                "sourceip as sourceip", "sourceport as sourceport", "destinationip as destinationip",
                "destinationport as destinationport", "username as username", "eventcount as eventcount",
                "PROTOCOLNAME(protocolid) as protocol"
            ],
            "mapping": {
                "ipv4-addr": {"fields": {"value": ["sourceip"]}},
                "ipv6-addr": {"fields": {"value": ["sourceip"]}},
                "url": {"fields": {"value": ["url"]}},
                "mac-addr": {"fields": {"value": ["sourcemac", "destinationmac"]}},
                "file": {"fields": {"name": ["filename"]}},
                "network-traffic": {"fields": {"src_port": ["sourceport"], "dst_port": ["destinationport"], "protocols[*]": ["protocolid"], "start": ["starttime"], "end": ["endtime"]}},
                "user-account": {"fields": {"user_id": ["username"]}},
                "artifact": {"fields": {"payload_bin": ["payload"]}}
            }
        }

        query = shifter.translate('qradar', 'query', '{}', stix_pattern, options)
        where_statement = "WHERE sourceip = '192.168.122.83' {} {}".format(default_limit, default_time)
        parsed_stix = [{'value': '192.168.122.83', 'comparison_operator': '=', 'attribute': 'ipv4-addr:value'}]
        custom_selections = "SELECT sourceip as sourceip, sourceport as sourceport, destinationip as destinationip, destinationport as destinationport, username as username, eventcount as eventcount, PROTOCOLNAME(protocolid) as protocol"
        assert query == {'queries': [custom_selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_custom_time_limit_and_result_count(self):
        stix_pattern = "[ipv4-addr:value = '192.168.122.83']"
        timerange = 25
        result_limit = 5000
        options = {"timerange": timerange, "result_limit": result_limit}
        query = shifter.translate('qradar', 'query', '{}', stix_pattern, options)
        where_statement = "WHERE (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83' OR identityip = '192.168.122.83') limit {} last {} minutes".format(result_limit, timerange)
        parsed_stix = [{'value': '192.168.122.83', 'comparison_operator': '=', 'attribute': 'ipv4-addr:value'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}
    
    def test_domainname_query(self):
        stix_pattern = "[domain-name:value = 'example.com']"
        query = shifter.translate('qradar', 'query', '{}', stix_pattern)
        where_statement = "WHERE domainname LIKE '%example.com%' {} {}".format(default_limit, default_time)
        parsed_stix = [{'attribute': 'domain-name:value', 'comparison_operator': '=', 'value': 'example.com'}]
        assert query == {'queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}