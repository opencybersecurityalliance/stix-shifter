'''
STIX to CSQL query adaptor test cases
'''
from stix_shifter.stix_translation import stix_translation
from stix_shifter.utils.error_response import ErrorCode
import unittest
import json
import random

selections = "SELECT Network.A as sourceip, Transport.A as sourceport, \
Link.A as sourcemac, Network.B as destinationip, Transport.B as destinationport, \
Link.B as destinationmac, Transport.Protocol as protocol, Start as starttime, \
Last as endtime"

at_selections = "SELECT initiator.id as initiator_id, initiator.name as initiator_name, \
initiator.credential.type as initiator_credential_type, \
initiator.host.address as initiator_host_address, ALCH_ACCOUNT_ID as \
alch_account_id, ALCH_TENANT_ID as alch_tenant_id, eventTime as eventTime, \
action as action, target.id as target_id, target.name as target_name, \
target.host.address as target_host_address, event_uuid as event_uuid, \
observer.host.address as observer_host_addres, observer.name as \
observer_name, observer.host.address as observer_host_address, api.name \
as api_name"

at_from_statement = " FROM cos://us-geo/at-hourly-dumps STORED AS JSON "

from_statement = " FROM cos://us-geo/nf-hourly-dumps STORED AS JSON "

num_rows = 1024

protocols_file = open('stix_shifter/stix_translation/src/modules/csa/json/network_protocol_map.json').read()
PROTOCOLS = json.loads(protocols_file)


translation = stix_translation.StixTranslation()


def _translate_query(stix_pattern, dialect):
    return translation.translate("csa:{}".format(dialect), 'query', '{}', stix_pattern)


def _test_query_assertions(query, selections, from_statement, where_statement):
    assert query['queries'] == [selections + from_statement + where_statement + ' PARTITIONED EVERY {num_rows} ROWS'.format(num_rows=num_rows)]


class TestStixToSql(unittest.TestCase, object):

    def test_ipv4_query(self):
        dialect = 'nf'
        stix_pattern = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84']"
        query = _translate_query(stix_pattern, dialect)
        where_statement = "WHERE (Network.A = '192.168.122.84' OR Network.B = '192.168.122.84') OR (Network.A = '192.168.122.83' OR Network.B = '192.168.122.83')"
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_ipv4_in_query(self):
        dialect = 'nf'
        stix_pattern = "[ipv4-addr:value IN ('192.168.122.83', '192.168.122.84')]"
        query = _translate_query(stix_pattern, dialect)
        where_statement = "WHERE (Network.A IN (192.168.122.83 OR 192.168.122.84) OR Network.B IN (192.168.122.83 OR 192.168.122.84))"
        assert query['queries'] == [selections + from_statement + where_statement + ' PARTITIONED EVERY {num_rows} ROWS'.format(num_rows=num_rows)]

    def test_ipv6_query(self):
        dialect = 'nf'
        stix_pattern = "[ipv6-addr:value = '192.168.122.83']"
        query = _translate_query(stix_pattern, dialect)
        where_statement = "WHERE (Network.A = '192.168.122.83' OR Network.B = '192.168.122.83')"
        _test_query_assertions(query, selections, from_statement, where_statement)

    # Non-mappable now throws an error. Skydive doesn't have url
    # def test_url_query(self):
    #     dialect = 'nf'
    #     stix_pattern = "[url:value = 'http://www.testaddress.com']"
    #     query = _translate_query(stix_pattern, dialect)
    #     where_statement = "WHERE url = 'http://www.testaddress.com'"
    #     _test_query_assertions(query, selections, from_statement, where_statement)

    def test_mac_address_query(self):
        dialect = 'nf'
        stix_pattern = "[mac-addr:value = '00-00-5E-00-53-00']"
        query = _translate_query(stix_pattern, dialect)
        where_statement = "WHERE (Link.A = '00-00-5E-00-53-00' OR Link.B = '00-00-5E-00-53-00')"
        _test_query_assertions(query, selections, from_statement, where_statement)

    # def test_domain_query(self):
    #     dialect = 'nf'
    #     stix_pattern = "[domain-name:value = 'example.com']"
    #     query = _translate_query(stix_pattern, dialect)
    #     where_statement = "WHERE domainname = 'example.com'"
    #     _test_query_assertions(query, selections, from_statement, where_statement)

    def test_query_from_multiple_observation_expressions_joined_by_and(self):
        dialect = 'nf'
        stix_pattern = "[domain-name:value = 'example.com'] AND [mac-addr:value = '00-00-5E-00-53-00']"
        query = _translate_query(stix_pattern, dialect)
        # Expect the STIX AND to convert to an AQL OR.
        where_statement = "WHERE domainname = 'example.com' OR (Link.A = '00-00-5E-00-53-00' OR Link.B = '00-00-5E-00-53-00')"
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_query_from_multiple_comparison_expressions_joined_by_and(self):
        dialect = 'nf'
        stix_pattern = "[domain-name:value = 'example.com' AND mac-addr:value = '00-00-5E-00-53-00']"
        query = _translate_query(stix_pattern, dialect)
        # Expect the STIX AND to convert to an AQL AND.
        where_statement = "WHERE (Link.A = '00-00-5E-00-53-00' OR Link.B = '00-00-5E-00-53-00') AND domainname = 'example.com'"
        _test_query_assertions(query, selections, from_statement, where_statement)

    # def test_file_query(self):
    #     # TODO: Add support for file hashes. Unsure at this point how QRadar queries them
    #     dialect = 'nf'
    #     stix_pattern = "[file:name = 'some_file.exe']"
    #     query = _translate_query(stix_pattern, dialect)
    #     where_statement = "WHERE filename = 'some_file.exe'"
    #     _test_query_assertions(query, selections, from_statement, where_statement)

    def test_port_queries(self):
        dialect = 'nf'
        stix_pattern = "[network-traffic:src_port = 12345 OR network-traffic:dst_port = 23456]"
        query = _translate_query(stix_pattern, dialect)
        where_statement = "WHERE Transport.B = '23456' OR Transport.A = '12345'"
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_unmapped_attribute_with_AND(self):
        stix_pattern = "[unmapped-object:some_invalid_attribute = 'whatever' AND file:name = 'some_file.exe']"
        result = translation.translate('csa:nf', 'query', '{}', stix_pattern)
        assert result['success'] == False
        assert ErrorCode.TRANSLATION_MAPPING_ERROR.value == result['code']
        assert 'Unable to map the following STIX objects and properties to data source fields' in result['error']

    def test_unmapped_attribute_with_OR(self):
        dialect = 'nf'
        stix_pattern = "[ipv4-addr:value = '1.2.3.4' OR unmapped-object:some_invalid_attribute = 'whatever']"
        query = _translate_query(stix_pattern, dialect)
        where_statement = "WHERE (Network.A = '1.2.3.4' OR Network.B = '1.2.3.4')"
        _test_query_assertions(query, selections, from_statement, where_statement)
        # assert(False)

    def test_user_account_query(self):
        dialect = 'at'
        stix_pattern = "[user-account:user_id = 'root']"
        query = _translate_query(stix_pattern, dialect)
        where_statement = "WHERE (initiator.id = 'root' OR target.id = 'root' OR observer.id = 'root')"
        _test_query_assertions(query, at_selections, at_from_statement, where_statement)

    def test_invalid_stix_pattern(self):
        dialect = 'nf'
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('csa', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert False == result['success']
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_network_traffic_protocols(self):
        dialect = 'nf'
        for key, value in PROTOCOLS.items():
            # Test for both upper AND lower case protocols in the STIX stix_pattern
            if random.randint(0, 1) == 0:
                key = key.upper()
            stix_pattern = "[network-traffic:protocols[*] = '" + key + "']"
            query = _translate_query(stix_pattern, dialect)
        where_statement = "WHERE Transport.Protocol = '" + value + "'"
        _test_query_assertions(query, selections, from_statement, where_statement)

    def test_network_traffic_start_stop(self):
        dialect = 'nf'
        stix_pattern = "[network-traffic:'start' = '2018-06-14T08:36:24.000Z' OR network-traffic:end = '2018-06-14T08:36:24.000Z']"
        query = _translate_query(stix_pattern, dialect)
        where_statement = "WHERE Last = '1528965384' OR Start = '1528965384'"
        _test_query_assertions(query, selections, from_statement, where_statement)

    # def test_artifact_queries(self):
    #     dialect = 'nf'
    #     stix_pattern = "[artifact:payload_bin MATCHES 'some text']"
    #     query = _translate_query(stix_pattern, dialect)
    #     where_statement = "WHERE payload MATCHES '.*some text.*'"
    #     _test_query_assertions(query, selections, from_statement, where_statement)

# Sample from SkyDive
#             {
#   "Start": 1531867319.982,
#   "Metric": {
#     "BAPackets": 15,
#     "BABytes": 6766,
#     "ABBytes": 1604,
#     "ABPackets": 10
#   },
#   "Last": 1531867320.174,
#   "Network": {
#     "A": "172.30.106.116",
#     "A_Name": "k8s_node",
#     "B": "75.126.81.67",
#     "Protocol": "IPV4"
#   },
#   "Transport": {
#     "A": "43748",
#     "B": "443",
#     "Protocol": "TCP"
#   }
# }
