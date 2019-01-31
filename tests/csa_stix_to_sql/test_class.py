'''
STIX to CSQL query adaptor test cases
'''
from stix_shifter.stix_translation import stix_translation
from stix_shifter.stix_translation.src.modules.csa import csa_translator
from stix_shifter.stix_translation.src.modules.csa import cloudsql_data_mapping
from stix_shifter.stix_translation.src.modules.base import base_translator
import unittest
import random

selections = "SELECT Network.A as sourceip, Transport.A as sourceport, \
Link.A as sourcemac, Network.B as destinationip, Transport.B as destinationport, \
Link.B as destinationmac, Transport.Protocol as protocol, Start as starttime, \
Last as endtime"

at_selections = "SELECT initiator.id as initiator_id, initiator.name as initiator_name, \
initiator.credential.type as initiator_credential_type, ALCH_ACCOUNT_ID as alch_account_id, \
ALCH_TENANT_ID as alch_tenant_id, eventTime as eventTime, action as action, \
target.id as target_id, target.name as target_name, event_uuid as event_uuid"

at_from_statement = " FROM cos://us-geo/at-hourly-dumps STORED AS JSON "

from_statement = " FROM cos://us-geo/nf-hourly-dumps STORED AS JSON "


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

translation = stix_translation.StixTranslation()


class TestStixToSql(unittest.TestCase, object):

    def test_ipv4_query(self):
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[ipv4-addr:value = '192.168.122.83' OR ipv4-addr:value = '192.168.122.84']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE (Network.A = '192.168.122.84' OR Network.B = '192.168.122.84') OR (Network.A = '192.168.122.83' OR Network.B = '192.168.122.83')"
        parsed_stix = [{'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.84'}, {'attribute': 'ipv4-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_ipv4_in_query(self):
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[ipv4-addr:value IN ('192.168.122.83', '192.168.122.84')]"
        options = {}
        query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE (Network.A IN (192.168.122.83 OR 192.168.122.84) OR Network.B IN (192.168.122.83 OR 192.168.122.84))"
#        parsed_stix = [{'attribute': 'ipv4-addr:value', 'comparison_operator': 'IN', 'value': '192.168.122.84'}, {'attribute': 'ipv4-addr:value', 'comparison_operator': 'IN', 'value': '192.168.122.83'}]
        print(query)
        assert query['sql_queries'] == [selections + from_statement + where_statement]

    def test_ipv6_query(self):
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[ipv6-addr:value = '192.168.122.83']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE (Network.A = '192.168.122.83' OR Network.B = '192.168.122.83')"
        parsed_stix = [{'attribute': 'ipv6-addr:value', 'comparison_operator': '=', 'value': '192.168.122.83'}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_url_query(self):
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[url:value = 'http://www.testaddress.com']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE url = 'http://www.testaddress.com'"
        parsed_stix = [{'attribute': 'url:value', 'comparison_operator': '=', 'value': 'http://www.testaddress.com'}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_mac_address_query(self):
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE (Link.A = '00-00-5E-00-53-00' OR Link.B = '00-00-5E-00-53-00')"
        parsed_stix = [{'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_domain_query(self):
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[domain-name:value = 'example.com']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE domainname = 'example.com'"
        parsed_stix = [{'attribute': 'domain-name:value', 'comparison_operator': '=', 'value': 'example.com'}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_query_from_multiple_observation_expressions_joined_by_and(self):
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[domain-name:value = 'example.com'] AND [mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        # Expect the STIX AND to convert to an AQL OR.
        where_statement = "WHERE domainname = 'example.com' OR (Link.A = '00-00-5E-00-53-00' OR Link.B = '00-00-5E-00-53-00')"
        parsed_stix = [{'attribute': 'domain-name:value', 'comparison_operator': '=', 'value': 'example.com'}, {'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_query_from_multiple_comparison_expressions_joined_by_and(self):
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[domain-name:value = 'example.com' AND mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        # Expect the STIX AND to convert to an AQL AND.
        where_statement = "WHERE (Link.A = '00-00-5E-00-53-00' OR Link.B = '00-00-5E-00-53-00') AND domainname = 'example.com'"
        parsed_stix = [{'attribute': 'mac-addr:value', 'comparison_operator': '=', 'value': '00-00-5E-00-53-00'}, {'attribute': 'domain-name:value', 'comparison_operator': '=', 'value': 'example.com'}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_file_query(self):
        # TODO: Add support for file hashes. Unsure at this point how QRadar queries them
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[file:name = 'some_file.exe']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE filename = 'some_file.exe'"
        parsed_stix = [{'attribute': 'file:name', 'comparison_operator': '=', 'value': 'some_file.exe'}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_port_queries(self):
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[network-traffic:src_port = 12345 OR network-traffic:dst_port = 23456]"
        options = {}
        query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE Transport.B = '23456' OR Transport.A = '12345'"
        parsed_stix = [{'attribute': 'network-traffic:dst_port', 'comparison_operator': '=', 'value': 23456}, {'attribute': 'network-traffic:src_port', 'comparison_operator': '=', 'value': 12345}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_unmapped_attribute(self):
        data_mapping_exception = cloudsql_data_mapping.DataMappingException
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[network-traffic:some_invalid_attribute = 'whatever']"
        options = {}
        self.assertRaises(data_mapping_exception,
                          lambda: interface.transform_query(input_arguments, options))

    def test_user_account_query(self):
        interface = csa_translator.Translator(dialect='at')
        input_arguments = "[user-account:user_id = 'root']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE initiator.id = 'root'"
        parsed_stix = [{'attribute': 'user-account:user_id', 'comparison_operator': '=', 'value': 'root'}]
        assert query == {'sql_queries': [at_selections + at_from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_invalid_stix_pattern(self):
        stix_validation_exception = stix_translation.StixValidationException
        stix_pattern = "[not_a_valid_pattern]"
        self.assertRaises(stix_validation_exception,
                          lambda: translation.translate('csa', 'query', '{}', stix_pattern))

    def test_network_traffic_protocols(self):
        interface = csa_translator.Translator(dialect='nf')
        for key, value in protocols.items():
            # Test for both upper AND lower case protocols in the STIX pattern
            if random.randint(0, 1) == 0:
                key = key.upper()
            input_arguments = "[network-traffic:protocols[*] = '" + key + "']"
            options = {}
            query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE Transport.Protocol = '" + value + "'"
        parsed_stix = [{'attribute': 'network-traffic:protocols[*]', 'comparison_operator': '=', 'value': key}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_network_traffic_start_stop(self):
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[network-traffic:'start' = '2018-06-14T08:36:24.000Z' OR network-traffic:end = '2018-06-14T08:36:24.000Z']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE Last = '1528965384' OR Start = '1528965384'"
        parsed_stix = [{'attribute': 'network-traffic:end', 'comparison_operator': '=', 'value': '2018-06-14T08:36:24.000Z'}, {'attribute': 'network-traffic:start', 'comparison_operator': '=', 'value': '2018-06-14T08:36:24.000Z'}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

    def test_artifact_queries(self):
        interface = csa_translator.Translator(dialect='nf')
        input_arguments = "[artifact:payload_bin MATCHES 'some text']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        where_statement = "WHERE payload MATCHES '.*some text.*'"
        parsed_stix = [{'attribute': 'artifact:payload_bin', 'comparison_operator': 'MATCHES', 'value': 'some text'}]
        assert query == {'sql_queries': [selections + from_statement + where_statement], 'parsed_stix': parsed_stix}

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
