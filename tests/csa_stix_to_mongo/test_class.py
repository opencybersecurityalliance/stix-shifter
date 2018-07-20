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
