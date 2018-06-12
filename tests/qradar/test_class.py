from stix_shifter.src.modules.qradar import qradar_translator
from stix_shifter.src.modules.qradar import qradar_data_mapping
import unittest

selections = "SELECT QIDNAME(qid) as qidname, qid as qid, CATEGORYNAME(category) as categoryname, \
category as categoryid, CATEGORYNAME(highlevelcategory) as high_level_category_name, \
highlevelcategory as high_level_category_id, LOGSOURCETYPENAME(logsourceid) as logsourcename, starttime as starttime, \
endtime as endtime, devicetime as devicetime, sourceip as sourceip, sourceport as sourceport, sourcemac as sourcemac, \
destinationip as destinationip, destinationport as destinationport, destinationmac as destinationmac, \
username as username, eventdirection as direction, identityip as identityip, identityhostname as identity_host_name, \
eventcount as eventcount, PROTOCOLNAME(protocolid) as protocol"


class TestStixToAql(unittest.TestCase, object):

    def test_ipv4_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[ipv4-addr:value = '192.168.122.83' or ipv4-addr:value = '192.168.122.84']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE (sourceip='192.168.122.84' OR destinationip='192.168.122.84' OR identityip='192.168.122.84') OR (sourceip='192.168.122.83' OR destinationip='192.168.122.83' OR identityip='192.168.122.83')"

    def test_ipv6_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[ipv6-addr:value = '192.168.122.83']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE (sourceip='192.168.122.83' OR destinationip='192.168.122.83' OR identityip='192.168.122.83')"

    def test_url_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[url:value = 'http://www.testaddress.com']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE url='http://www.testaddress.com'"

    def test_mac_address_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE (sourcemac='00-00-5E-00-53-00' OR destinationmac='00-00-5E-00-53-00')"

    def test_domain_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE domainname='example.com'"

    def test_query_from_multiple_observation_expressions_joined_by_and(self):
        interface = qradar_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com'] and [mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        # Expect the STIX and to convert to an AQL OR.
        assert query == selections + \
            " FROM events WHERE domainname='example.com' OR (sourcemac='00-00-5E-00-53-00' OR destinationmac='00-00-5E-00-53-00')"

    def test_query_from_multiple_comparison_expressions_joined_by_and(self):
        interface = qradar_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com' and mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        # Expect the STIX and to convert to an AQL AND.
        assert query == selections + \
            " FROM events WHERE (sourcemac='00-00-5E-00-53-00' OR destinationmac='00-00-5E-00-53-00') AND domainname='example.com'"

    def test_file_query(self):
        # TODO: Add support for file hashes. Unsure at this point how QRadar queries them
        interface = qradar_translator.Translator()
        input_arguments = "[file:name = 'some_file.exe']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + " FROM events WHERE filename='some_file.exe'"

    def test_port_queries(self):
        interface = qradar_translator.Translator()
        input_arguments = "[network-traffic:src_port = 12345 or network-traffic:dst_port = 23456]"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE destinationport='23456' OR sourceport='12345'"

    def test_unmapped_attribute(self):
        data_mapping_exception = qradar_data_mapping.DataMappingException
        interface = qradar_translator.Translator()
        input_arguments = "[network-traffic:some_invalid_attribute = 'whatever']"
        options = {}
        self.assertRaises(data_mapping_exception,
                          lambda: interface.transform_query(input_arguments, options))
