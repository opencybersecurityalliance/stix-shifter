from stix_shifter.src.modules.csa import csa_translator
# from stix_shifter.src.modules.qradar import qradar_data_mapping
from stix_shifter.src.modules.base import base_translator
import unittest
import random

class TestStixToCsaNfMongo(unittest.TestCase, object):

    def test_ipv4_query(self):
        interface = csa_translator.Translator()
        input_arguments = "[ipv4-addr:value = '192.168.122.83' or ipv4-addr:value = '192.168.122.84']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        # match = {
        #     "$or" : [
        #         {
        #             "$and" : [
        #             {"Network.A" : {"$or" : ["192.168.122.83", "192.168.122.84"]}},
        #             {"Network.Protocol" : "IPV4"}
        #         ]
        #         },
        #         {"Network.B" : {"$or" : ["192.168.122.83", "192.168.122.84"]}}
        #     ]
        # }
        match = {
            "$or" : [
                {"Network.A" : {"$or" : ["192.168.122.83", "192.168.122.84"]}},
                {"Network.B" : {"$or" : ["192.168.122.83", "192.168.122.84"]}}
            ]
        }
        match = {
            '$or': [
                {'$or': [
                    {'Network.A': {'$eq': '192.168.122.84'}},
                    {'Network.B': {'$eq': '192.168.122.84'}}
                    ]
                },
                {'$or': [
                    {'Network.A': {'$eq': '192.168.122.83'}},
                    {'Network.B': {'$eq': '192.168.122.83'}}
                    ]
                }
            ]
        }
        print(query)
        assert query == match
    
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
        interface = csa_translator.Translator()
        input_arguments = "[mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        match = {
                '$or': [
                    {'Link.A': {'$eq': '00-00-5E-00-53-00'}},
                    {'Link.B': {'$eq': '00-00-5E-00-53-00'}}
                    ]
        }
        assert query == match
    
    def test_domain_query(self):
        interface = qradar_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + \
            " FROM events WHERE domainname = 'example.com'"
    
    def test_query_from_multiple_observation_expressions_joined_by_and(self):
        interface = csa_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com'] and [mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        # Expect the STIX and to convert to an AQL OR.
        match = {
            '$and': [
                    {'Network.A_Name': {'$eq': 'example.com'}},
                {'$or': [
                    {'Link.A': {'$eq': '00-00-5E-00-53-00'}},
                    {'Link.B': {'$eq': '00-00-5E-00-53-00'}}
                    ]
                }
            ]
        }
        print('Query',query)
        assert query == match

    def test_query_from_multiple_comparison_expressions_joined_by_and(self):
        interface = csa_translator.Translator()
        input_arguments = "[domain-name:value = 'example.com' and mac-addr:value = '00-00-5E-00-53-00']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        match = {
            '$and': [
                {'$or': [
                    {'Link.A': {'$eq': '00-00-5E-00-53-00'}},
                    {'Link.B': {'$eq': '00-00-5E-00-53-00'}}
                    ]
                },
                    {'Network.A_Name': {'$eq': 'example.com'}}
                
            ]
        }
        print('Query',query)
        print('Match',match)
        assert query == match
    
    def test_file_query(self):
        # TODO: Add support for file hashes. Unsure at this point how QRadar queries them
        interface = qradar_translator.Translator()
        input_arguments = "[file:name = 'some_file.exe']"
        options = {}
        query = interface.transform_query(input_arguments, options)
        assert query == selections + " FROM events WHERE filename = 'some_file.exe'"

    def test_port_queries(self):
        interface = csa_translator.Translator()
        input_arguments = "[network-traffic:src_port = 12345 or network-traffic:dst_port = 23456]"
        options = {}
        query = interface.transform_query(input_arguments, options)
        match = {
            '$or': [
                {'Transport.B': {'$eq': 23456}},
                {'Transport.A': {'$eq': 12345}}
        ]}
        print('Query',query)
        print('Match',match)
        assert query == match
    
    def test_unmapped_attribute(self):
        data_mapping_exception = csa_translator.DataMappingException
        interface = csa_translator.Translator()
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
