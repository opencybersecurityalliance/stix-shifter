from stix_shifter.src.modules.qradar import qradar_translator
from stix_shifter.src.modules.qradar import qradar_data_mapping
from stix_shifter.src.modules.base import base_translator
import unittest
import random

selections = "SELECT QIDNAME(qid) as qidname, qid as qid, CATEGORYNAME(category) as categoryname, \
category as categoryid, CATEGORYNAME(highlevelcategory) as high_level_category_name, \
highlevelcategory as high_level_category_id, logsourceid as logsourceid, LOGSOURCETYPENAME(logsourceid) as logsourcename, starttime as starttime, \
endtime as endtime, devicetime as devicetime, sourceip as sourceip, sourceport as sourceport, sourcemac as sourcemac, \
destinationip as destinationip, destinationport as destinationport, destinationmac as destinationmac, \
username as username, eventdirection as direction, identityip as identityip, identityhostname as identity_host_name, \
eventcount as eventcount, PROTOCOLNAME(protocolid) as protocol, UTF8(payload) as payload, URL as url, magnitude as magnitude"

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


class TestStixToAql(unittest.TestCase, object):

    def test_ipv4_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[ipv4-addr:value = '192.168.122.83' or ipv4-addr:value = '192.168.122.84']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE (sourceip = '192.168.122.84' OR destinationip = '192.168.122.84' OR identityip = '192.168.122.84') OR (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83' OR identityip = '192.168.122.83')"

    def test_ipv6_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[ipv6-addr:value = '192.168.122.83']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE (sourceip = '192.168.122.83' OR destinationip = '192.168.122.83' OR identityip = '192.168.122.83')"

    def test_url_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[url:value = 'http://www.testaddress.com']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE url = 'http://www.testaddress.com'"

    def test_mac_address_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE (sourcemac = '00-00-5E-00-53-00' OR destinationmac = '00-00-5E-00-53-00')"

    def test_domain_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE domainname = 'example.com'"

    def test_query_from_multiple_observation_expressions_joined_by_and(self):
        interface = qradar_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com'] and [mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        # Expect the STIX and to convert to an AQL OR.
        assert query == selections + \
            " FROM events WHERE domainname = 'example.com' OR (sourcemac = '00-00-5E-00-53-00' OR destinationmac = '00-00-5E-00-53-00')"

    def test_query_from_multiple_comparison_expressions_joined_by_and(self):
        interface = qradar_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com' and mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        # Expect the STIX and to convert to an AQL AND.
        assert query == selections + \
            " FROM events WHERE (sourcemac = '00-00-5E-00-53-00' OR destinationmac = '00-00-5E-00-53-00') AND domainname = 'example.com'"

    def test_file_query(self):
        # TODO: Add support for file hashes. Unsure at this point how QRadar queries them
        interface = qradar_translator.Translator()
        input_arguments = "[file:name = 'some_file.exe']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + " FROM events WHERE filename = 'some_file.exe'"

    def test_port_queries(self):
        interface = qradar_translator.Translator()
        input_arguments = "[network-traffic:src_port = 12345 or network-traffic:dst_port = 23456]"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE destinationport = '23456' OR sourceport = '12345'"

    def test_unmapped_attribute(self):
        data_mapping_exception = qradar_data_mapping.DataMappingException
        interface = qradar_translator.Translator()
        input_arguments = "[network-traffic:some_invalid_attribute = 'whatever']"
        options = {}
        self.assertRaises(data_mapping_exception,
                          lambda: interface.transform_query(input_arguments, options))

    def test_user_account_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[user-account:user_id = 'root']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE username = 'root'"

    def test_invalid_stix_pattern(self):
        stix_validation_exception = base_translator.StixValidationException
        interface = qradar_translator.Translator()
        input_arguments = "[not_a_valid_pattern]"
        options = {}
        self.assertRaises(stix_validation_exception,
                          lambda: interface.transform_query(input_arguments, options))

    def test_network_traffic_protocols(self):
        interface = qradar_translator.Translator()
        for key, value in protocols.items():
            # Test for both upper and lower case protocols in the STIX pattern
            if random.randint(0, 1) == 0:
                key = key.upper()
            input_arguments = "[network-traffic:protocols[*] = '" + key + "']"
            options = {}
            query = interface.transform_query(input_arguments, options)
            assert query == selections + " FROM events WHERE protocolid = '" + value + "'"

    def test_network_traffic_start_stop(self):
        interface = qradar_translator.Translator()
        input_arguments = "[network-traffic:'start' = '2018-06-14T08:36:24.000Z' or network-traffic:end = '2018-06-14T08:36:24.000Z']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE endtime = '1528965384' OR starttime = '1528965384'"

    def test_artifact_queries(self):
        interface = qradar_translator.Translator()
        input_arguments = "[artifact:payload_bin matches 'some text']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE payload MATCHES '.*some text.*'"

    def test_start_stop_qualifiers(self):
        interface = qradar_translator.Translator()
        input_arguments = "[user-account:user_id = 'root'] START '2016-06-01T01:30:00Z' STOP '2016-07-01T02:30:00Z'"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE username = 'root' START '2016-06-01 01:30' STOP '2016-06-01 02:30'"
