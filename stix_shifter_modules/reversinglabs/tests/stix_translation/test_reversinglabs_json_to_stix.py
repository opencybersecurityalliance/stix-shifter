import json
import unittest
from functools import wraps
from stix_shifter_modules.reversinglabs.entry_point import EntryPoint

MODULE = "reversinglabs"
DATA_SOURCE = {"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
               "name": "ReversingLabs_Connector", "identity_class": "system"}
options = {'stix_validator':True}
entry_point = EntryPoint(options=options)
translation_options = {}
domain_name = "google.com"
extension_types = ['toplevel-property-extension']
extension_properties = ['x_ibm_original_threat_feed_data','threat_score', 'threat_attributes']
domain_query_pattern = "[domain-name:value='"+domain_name+"']"
hash_value = '16cda323189d8eba4248c0a2f5ad0d8f'
hash_query_pattern = "[file:hashes.MD5='"+hash_value+"']"
url_value = "https://cnn.com"
url_query_pattern = "[url:value='"+url_value+"']"
transmitQueryDataForDomain = {
    "data": [
        {
            "rl": [
                {
                    "uri_state": {
                        "domain": domain_name,
                        "sha1": "7b4a76680ca0c0f04fae3d461128a0a02d23136e",
                                "uri_type": "domain",
                                "counters": {
                                    "known": 172906,
                                    "malicious": 24350,
                                    "suspicious": 1089
                                }
                    }
                }
            ],
            "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
            "data": domain_name,
            "dataType": "domain",
            "external_reference": {
                "source_name": "Reversing_Labs_1",
                "url": ""
            }
        }
    ]
}
class TestReversingLabsResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for translate results
    """

    def __init__(self, *args, **kwargs):
        super(TestReversingLabsResultsToStix, self).__init__(*args, **kwargs)
        self.result_translator = entry_point.create_default_results_translator(
            dialect='default')
        self.extension_property_names = []

    @staticmethod
    def exists(obj, chain):
        """
        Check if the nested keys exist in the dictionary or not
        """
        _key = chain.pop(0)
        if _key in obj:
            return TestReversingLabsResultsToStix.exists(obj[_key], chain) if chain else obj[_key]

    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestReversingLabsResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    def get_extension_property_keys(self, obj):
        for k, v in obj.items():
            if isinstance(v, dict) and not "key" in v:
                self.get_extension_property_keys(v)
            else:
                self.extension_property_names.append(v["key"])
        return self.extension_property_names
    
    def check_stix_bundle_type(func):
        """
        decorator function to convert the data source query result into stix bundle
        """
        @wraps(func)
        def wrapper_func(self, *args, **kwargs):
            self.result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitQueryDataForDomain['data'],)
            self.result_bundle_domain_objects = self.result_bundle['objects']
            assert self.result_bundle['type'] == 'bundle'
            return func(self, *args, **kwargs)
        return wrapper_func 

    @check_stix_bundle_type
    def test_stix_identity_prop(self):
        """
        to test the identity stix object properties
        """
        stix_identity = TestReversingLabsResultsToStix.get_first_of_type(
            self.result_bundle_domain_objects, DATA_SOURCE['type'])
        assert 'type' in stix_identity and stix_identity['type'] == DATA_SOURCE['type']
        assert 'name' in stix_identity and stix_identity['name'] == DATA_SOURCE['name']
        assert 'identity_class' in stix_identity and stix_identity[
            'identity_class'] == DATA_SOURCE['identity_class']

    @check_stix_bundle_type
    def test_stix_extension_prop(self):
        """
        to test the extension stix object properties
        """
        sdo_type = 'extension-definition'
        stix_extension = TestReversingLabsResultsToStix.get_first_of_type(
            self.result_bundle_domain_objects, sdo_type)
        assert 'type' in stix_extension and stix_extension['type'] == sdo_type
        assert 'name' in stix_extension
        assert 'version' in stix_extension
        assert 'extension_types' in stix_extension and stix_extension[
            'extension_types'] == extension_types
        assert 'extension_properties' in stix_extension and stix_extension[
            'extension_properties'] == extension_properties

    @check_stix_bundle_type
    def test_stix_indicator_prop(self):
        """
        to test the indicator stix object properties
        """
        sdo_type = 'indicator'
        stix_indicator = TestReversingLabsResultsToStix.get_first_of_type(
            self.result_bundle_domain_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == domain_query_pattern
        assert 'valid_from' in stix_indicator
        assert 'created' in stix_indicator
        assert 'modified' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'malicious-activity'

    @check_stix_bundle_type
    def test_stix_indicator_extensions_prop(self):
        """
        to test the indicator stix object extensions properties
        """
        stix_indicator = TestReversingLabsResultsToStix.get_first_of_type(
            self.result_bundle_domain_objects, 'indicator')
        assert 'x_ibm_original_threat_feed_data' in stix_indicator
        extension_property = extension_properties[0]
        property_name = "x_ibm_original_threat_feed_data.full"
        is_exist = TestReversingLabsResultsToStix.exists(
            stix_indicator, property_name.split("."))
        assert is_exist is not None
        assert stix_indicator[extension_property]["full"][0]
        extension_property_value = {'domain': 'google.com', 'sha1': '7b4a76680ca0c0f04fae3d461128a0a02d23136e', 'uri_type': 'domain', 
                                    'counters': {'known': 172906, 'malicious': 24350, 'suspicious': 1089}}
        assert stix_indicator[extension_property]["full"][0]['uri_state'] == extension_property_value
    
    def test_indicator_hash_query_pattern(self):
        """
        to test the indicator stix object extensions properties with hash query pattern
        """
        transmitData = {
                    "data": [
                        {
                            "rl": [
                                {
                                    "malware_presence": {
                                        "status": "MALICIOUS",
                                        "scanner_count": 30,
                                        "classification": {
                                            "platform": "Win32",
                                            "type": "Trojan",
                                            "is_generic": False,
                                            "family_name": "Carberp"
                                        },
                                        "scanner_percent": 96.66666412353516,
                                        "scanner_match": 29,
                                        "threat_name": "Win32.Trojan.Carberp",
                                        "reason": "antivirus",
                                        "query_hash": {
                                            "md5": hash_value
                                        },
                                        "first_seen": "2016-08-17T18:22:06",
                                        "threat_level": 5,
                                        "trust_factor": 5,
                                        "last_seen": "2021-08-08T12:55:19"
                                    }
                                }
                            ],
                            "data": hash_value,
                            "dataType": "hash",
                            "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
                        }
                    ]
                }
        sdo_type = 'indicator'
        result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitData['data'])
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        stix_indicator = TestReversingLabsResultsToStix.get_first_of_type(result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == hash_query_pattern

    def test_indicator_url_query_pattern(self):
        """
        to test the indicator stix object extensions properties with hash query pattern
        """
        transmitData = {
            "data": [
                {
                    "rl": [
                         {
                            "requested_url": "https://cnn.com",
                            "classification": "known",
                            "analysis": {
                                "first_analysis": "2018-12-05T23:49:53",
                                "analysis_count": 24,
                                "last_analysis": {
                                    "analysis_id": "1644515525857b58",
                                    "analysis_time": "2022-02-10T17:57:00",
                                    "final_url": "https://cnn.com/",
                                    "http_response_code": 200,
                                    "availability_status": "online",
                                    "domain": "cnn.com",
                                    "serving_ip_address": "151.101.209.67"
                                },
                                "statistics": {
                                    "unknown": 0,
                                    "malicious": 0,
                                    "known": 65,
                                    "suspicious": 0,
                                    "total": 65
                                },
                                "analysis_history": [
                                        {
                                            "analysis_id": "1644515525857b58",
                                            "analysis_time": "2022-02-10T17:57:00",
                                            "final_url": "https://cnn.com/",
                                            "http_response_code": 200,
                                            "availability_status": "online",
                                            "domain": "cnn.com",
                                            "serving_ip_address": "151.101.209.67"
                                        },
                                        {
                                            "analysis_id": "164441103402a49c",
                                            "analysis_time": "2022-02-09T13:50:15",
                                            "final_url": "https://cnn.com/",
                                            "http_response_code": 200,
                                            "availability_status": "online",
                                            "domain": "cnn.com",
                                            "serving_ip_address": "199.232.37.67"
                                        },
                                        {
                                            "analysis_id": "16440412349681b4",
                                            "analysis_time": "2022-02-05T06:11:36",
                                            "final_url": "https://cnn.com/",
                                            "http_response_code": 200,
                                            "availability_status": "online",
                                            "domain": "cnn.com",
                                            "serving_ip_address": "151.101.209.67"
                                        },
                                        {
                                            "analysis_id": "16420539873081b4",
                                            "analysis_time": "2022-01-13T06:10:33",
                                            "final_url": "https://cnn.com/",
                                            "http_response_code": 200,
                                            "availability_status": "online",
                                            "domain": "cnn.com",
                                            "serving_ip_address": "151.101.209.67"
                                        },
                                        {
                                            "analysis_id": "1642009825797b58",
                                            "analysis_time": "2022-01-12T17:55:15",
                                            "final_url": "https://cnn.com/",
                                            "http_response_code": 200,
                                            "availability_status": "online",
                                            "domain": "cnn.com",
                                            "serving_ip_address": "151.101.209.67"
                                        },
                                        {
                                            "analysis_id": "1641966623047b58",
                                            "analysis_time": "2022-01-12T05:54:41",
                                            "final_url": "https://cnn.com/",
                                            "http_response_code": 200,
                                            "availability_status": "online",
                                            "domain": "cnn.com",
                                            "serving_ip_address": "151.101.209.67"
                                        },
                                        {
                                            "analysis_id": "16419659611903d5",
                                            "analysis_time": "2022-01-12T05:43:31",
                                            "final_url": "https://cnn.com/",
                                            "http_response_code": 200,
                                            "availability_status": "online",
                                            "domain": "cnn.com",
                                            "serving_ip_address": "199.232.37.67"
                                        },
                                        {
                                            "analysis_id": "16419371406303d5",
                                            "analysis_time": "2022-01-11T21:43:27",
                                            "final_url": "https://cnn.com/",
                                            "http_response_code": 200,
                                            "availability_status": "online",
                                            "domain": "cnn.com",
                                            "serving_ip_address": "199.232.37.67"
                                        },
                                        {
                                            "analysis_id": "16419226906703d5",
                                            "analysis_time": "2022-01-11T17:42:47",
                                            "final_url": "https://cnn.com/",
                                            "http_response_code": 200,
                                            "availability_status": "online",
                                            "domain": "cnn.com",
                                            "serving_ip_address": "199.232.37.67"
                                        },
                                        {
                                            "analysis_id": "16415355516381b4",
                                            "analysis_time": "2022-01-07T06:10:35",
                                            "final_url": "https://cnn.com/",
                                            "http_response_code": 200,
                                            "availability_status": "online",
                                            "domain": "cnn.com",
                                            "serving_ip_address": "151.101.209.67"
                                        }
                                    ]
                            }
                        }
                    ],
                    "data": url_value,
                    "dataType": "url",
                    "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409"
                }
            ]
        }
        sdo_type = 'indicator'
        result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitData['data'])
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        stix_indicator = TestReversingLabsResultsToStix.get_first_of_type(result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == url_query_pattern

    def test_domain_query_pattern(self):
        """
        to test the indicator stix object extensions properties with domain query pattern
        """
        transmitData = {
                    "data": [
                        {
                            "rl": [
                                {
                                    "uri_state": {
                                        "domain": "cin7.com",
                                        "sha1": "a516aaefb20f6f26ad8299735195137077728163",
                                        "uri_type": "domain",
                                        "counters": {
                                            "known": 553,
                                            "malicious": 0,
                                            "suspicious": 0
                                        }
                                    }
                                }
                            ],
                            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae",
                            "data": "cin7.com",
                            "dataType": "domain"
                        }
                    ]
                }
        sdo_type = 'indicator'
        result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitData['data'])
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        stix_indicator = TestReversingLabsResultsToStix.get_first_of_type(result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == "[domain-name:value='cin7.com']"
    
    def test_ip_query_pattern(self):
        """
        to test the indicator stix object extensions properties with domain query pattern
        """
        transmitData = {
                    "data": [
                        {
                            "rl": [
                                {
                                    "message": "IOC not found"
                                }
                            ],
                            "data": "194.147.78.155",
                            "dataType": "ip",
                            "namespace": "9d4bedaf-d351-4f50-930f-f8eb121e5bae"
                        }
                    ]
                }
        sdo_type = 'indicator'
        result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitData['data'])
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        stix_indicator = TestReversingLabsResultsToStix.get_first_of_type(result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == "[ipv4-addr:value='194.147.78.155']"
        assert 'x_ibm_original_threat_feed_data' in stix_indicator and stix_indicator['x_ibm_original_threat_feed_data']['full'][0] == {'message': 'IOC not found'}

