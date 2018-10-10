from stix_shifter.src.modules.splunk import splunk_translator
from stix_shifter.src.exceptions import DataMappingException
import unittest
import random

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

class TestStixToSpl(unittest.TestCase, object):

    def test_ipv4_query(self):
        interface = splunk_translator.Translator()
        input_arguments = "[ipv4-addr:value = '192.168.122.83' or ipv4-addr:value = '192.168.122.84']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        spl = '(((tag="flow" AND src_ip = "192.168.122.84") OR (tag="flow" AND dest_ip = "192.168.122.84")) OR ((tag="flow" AND src_ip = "192.168.122.83") OR (tag="flow" AND dest_ip = "192.168.122.83")))'
        assert query == spl

    def test_ipv6_query(self):
        interface = splunk_translator.Translator()
        input_arguments = "[ipv6-addr:value = 'fe80::8c3b:a720:dc5c:2abf%19']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        spl = '((tag="flow" AND src_ip = "fe80::8c3b:a720:dc5c:2abf%19") OR (tag="flow" AND dest_ip = "fe80::8c3b:a720:dc5c:2abf%19"))'
        assert query == spl

    def test_url_query(self):
        interface = splunk_translator.Translator()
        input_arguments = "[url:value = 'http://www.testaddress.com']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        spl = '(tag="web" AND url = "http://www.testaddress.com")'
        assert query == spl

    def test_mac_address_query(self):
        interface = splunk_translator.Translator()
        input_arguments = "[mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        spl = '(tag="flow" AND mac = "00-00-5E-00-53-00")'
        assert query == spl

    def test_domain_query(self):
        interface = splunk_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        spl = '(tag="flow" AND dest_fqdn = "example.com")'
        assert query == spl

    def test_query_from_multiple_observation_expressions_joined_by_and(self):
        interface = splunk_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com'] and [mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        # Expect the STIX and to convert to an SPL OR.
        spl = '(tag="flow" AND dest_fqdn = "example.com") OR (tag="flow" AND mac = "00-00-5E-00-53-00")'
        assert query == spl

    def test_query_from_multiple_comparison_expressions_joined_by_and(self):
        interface = splunk_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com' and mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        # Expect the STIX and to convert to an AQL AND.
        spl = '((tag="flow" AND mac = "00-00-5E-00-53-00") AND (tag="flow" AND dest_fqdn = "example.com"))'
        assert query == spl

    def test_file_query(self):
        interface = splunk_translator.Translator()
        input_arguments = "[file:name = 'some_file.exe']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        spl = '(tag="endpoint" AND file_name = "some_file.exe")'
        assert query == spl

    def test_port_queries(self):
        interface = splunk_translator.Translator()
        input_arguments = "[network-traffic:src_port = 12345 or network-traffic:dst_port = 23456]"
        options = {}
        query = interface.transform_query(input_arguments, options)
        spl = '((tag="network" AND dest_port = 23456) OR (tag="network" AND src_port = 12345))'
        assert query == spl

    def test_unmapped_attribute(self):
        data_mapping_exception = DataMappingException
        interface = splunk_translator.Translator()
        input_arguments = "[network-traffic:some_invalid_attribute = 'whatever']"
        options = {}
        self.assertRaises(data_mapping_exception,
                           lambda: interface.transform_query(input_arguments, options))

    def test_invalid_stix_pattern(self):
        interface = splunk_translator.Translator()
        input_arguments = "[not_a_valid_pattern]"
        options = {}
        self.assertRaises(Exception,
                          lambda: interface.transform_query(input_arguments, options))

    def test_network_traffic_protocols(self):
        interface = splunk_translator.Translator()
        for key, value in protocols.items():
            # Test for both upper and lower case protocols in the STIX pattern
            if random.randint(0, 1) == 0:
                key = key.upper()
            input_arguments = "[network-traffic:protocols[*] = '" + key + "']"
            options = {}
            query = interface.transform_query(input_arguments, options)
        spl = '(tag="network" AND protocol = "'+key+'")'
        assert query == spl

    def test_network_traffic_start_stop(self):
        interface = splunk_translator.Translator()
        input_arguments = "[network-traffic:'start' = '2018-06-14T08:36:24.000Z' or network-traffic:end = '2018-06-14T08:36:24.000Z']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        spl = '((tag="network" AND latest = "2018-06-14T08:36:24.000Z") OR (tag="network" AND earliest = "2018-06-14T08:36:24.000Z"))'
        assert query == spl

    def test_start_stop_qualifiers(self):
        interface = splunk_translator.Translator()
        input_arguments = "[network-traffic:src_port = 37020] START '2016-06-01T01:30:00Z' STOP '2016-06-01T02:20:00Z' OR [ipv4-addr:value = '192.168.122.83'] START '2016-06-01T03:55:00Z' STOP '2016-06-01T04:30:00Z'"
        options = {}
        query = interface.transform_query(input_arguments, options)
        spl = '(tag="network" AND src_port = 37020) earliest="06/01/2016:01:30:00" latest="06/01/2016:02:20:00" OR ((tag="flow" AND src_ip = "192.168.122.83") OR (tag="flow" AND dest_ip = "192.168.122.83")) earliest="06/01/2016:03:55:00" latest="06/01/2016:04:30:00"'
        assert query == spl

    def test_issuperset_operator(self):
        interface = splunk_translator.Translator()
        input_arguments = "[ipv4-addr:value ISSUPERSET '198.51.100.0/24']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        spl = '((tag="flow" AND src_ip = "198.51.100.0/24") OR (tag="flow" AND dest_ip = "198.51.100.0/24"))'
        assert query == spl
    
    def test_issubset_operator(self):
        interface = splunk_translator.Translator()
        input_arguments = "[ipv4-addr:value ISSUBSET '198.51.100.0/24']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        spl = '((tag="flow" AND src_ip = "198.51.100.0/24") OR (tag="flow" AND dest_ip = "198.51.100.0/24"))'
        assert query == spl