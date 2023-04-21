import json
import unittest
from functools import wraps
from stix_shifter_modules.maxmind.entry_point import EntryPoint

MODULE = "maxmind"
DATA_SOURCE = {"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3", "name": "MaxMind_Connector", "identity_class": "system"}
options = {'stix_validator':True}
entry_point = EntryPoint(options=options)
translation_options = {}
ip_value = "34.102.136.180"
extension_types = ['toplevel-property-extension']
extension_properties = ['x_ibm_original_threat_feed_data', 'threat_score', 'threat_attributes']
query_pattern = "[ipv4-addr:value='"+ip_value+"']"
hash_value = '16cda323189d8eba4248c0a2f5ad0d8f'
hash_query_pattern = "[file:hashes.MD5='"+hash_value+"']"
url_value = "https://safaricom.co.ke"
url_query_pattern = "[url:value='"+url_value+"']"
domain_name = "telkom.co.id"
domain_query_pattern = "[domain-name:value='"+domain_name+"']"
transmitQueryData = {
    "data": [
        {
            "code": 200,
            "data": "34.102.136.180",
            "report": {
                "success": "True",
                "full": {
                    "city": {
                        "confidence": 50,
                        "geoname_id": 4393217,
                        "names": {
                            "ja": "カンザスシティ",
                            "pt-BR": "Kansas City",
                            "ru": "Канзас-Сити",
                            "de": "Kansas City",
                            "en": "Kansas City",
                            "es": "Kansas City",
                            "fr": "Kansas City"
                        },
                        "name": "Kansas City"
                    },
                    "continent": {
                        "code": "NA",
                        "geoname_id": 6255149,
                        "names": {
                            "en": "North America",
                            "es": "Norteamérica",
                            "fr": "Amérique du Nord",
                            "ja": "北アメリカ",
                            "pt-BR": "América do Norte",
                            "ru": "Северная Америка",
                            "zh-CN": "北美洲",
                            "de": "Nordamerika"
                        },
                        "name": "North America"
                    },
                    "country": {
                        "confidence": 99,
                        "iso_code": "US",
                        "geoname_id": 6252001,
                        "names": {
                            "ru": "США",
                            "zh-CN": "美国",
                            "de": "Vereinigte Staaten",
                            "en": "United States",
                            "es": "Estados Unidos",
                            "fr": "États Unis",
                            "ja": "アメリカ",
                            "pt-BR": "EUA"
                        },
                        "name": "United States"
                    },
                    "location": {
                        "accuracy_radius": 20,
                        "latitude": 39.1027,
                        "longitude": -94.5778,
                        "metro_code": 616,
                        "time_zone": "America/Chicago"
                    },
                    "maxmind": {
                        "queries_remaining": 26181
                    },
                    "postal": {
                        "confidence": 20,
                        "code": "64184"
                    },
                    "registered_country": {
                        "iso_code": "US",
                        "geoname_id": 6252001,
                        "names": {
                            "zh-CN": "美国",
                            "de": "Vereinigte Staaten",
                            "en": "United States",
                            "es": "Estados Unidos",
                            "fr": "États Unis",
                            "ja": "アメリカ",
                            "pt-BR": "EUA",
                            "ru": "США"
                        }
                    },
                    "subdivisions": [
                        {
                            "confidence": 80,
                            "iso_code": "MO",
                            "geoname_id": 4398678,
                            "names": {
                                "en": "Missouri",
                                "es": "Missouri",
                                "fr": "Missouri",
                                "ja": "ミズーリ州",
                                "pt-BR": "Missúri",
                                "ru": "Миссури",
                                "zh-CN": "密苏里州"
                            }
                        }
                    ],
                    "traits": {
                        "is_anonymous": "True",
                        "is_hosting_provider": "True",
                        "user_count": 5,
                        "user_type": "hosting",
                        "autonomous_system_number": 396982,
                        "autonomous_system_organization": "GOOGLE-CLOUD-PLATFORM",
                        "domain": "googleusercontent.com",
                        "isp": "Google Cloud",
                        "organization": "Google Cloud",
                        "ip_address": "34.102.136.180",
                        "network": "34.102.136.180/32"
                    }
                }
            },
            "dataType": "ip",
            "external_reference": {
                        "source_name": "MaxMind GeoIP",
                        "url": "N/A"
            },
            "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409"
        }
    ]
}

class TestMaxmindResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for alienvault_otx translate results
    """

    def __init__(self,*args, **kwargs):
        super(TestMaxmindResultsToStix, self).__init__(*args, **kwargs)
        self.result_translator = entry_point.create_default_results_translator(dialect='default')
        self.extension_property_names = []
    
    @staticmethod
    def exists(obj, chain):
        """
        Check if the nested keys exist in the dictionary or not
        """
        _key = chain.pop(0)
        if _key in obj:
            return TestMaxmindResultsToStix.exists(obj[_key], chain) if chain else obj[_key]
    
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestMaxmindResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)
            
    def get_extension_property_keys(self, obj):
        for k, v in obj.items():
            if isinstance(v,dict) and not "key" in v:
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
            self.result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitQueryData['data'])
            self.result_bundle_objects = self.result_bundle['objects']
            assert self.result_bundle['type'] == 'bundle'
            return func(self, *args, **kwargs)
        return wrapper_func

    @check_stix_bundle_type
    def test_stix_identity_prop(self):
        """
        to test the identity stix object properties
        """
        stix_identity = TestMaxmindResultsToStix.get_first_of_type(self.result_bundle_objects, DATA_SOURCE['type'])
        assert 'type' in stix_identity and stix_identity['type'] == DATA_SOURCE['type']
        assert 'name' in stix_identity and stix_identity['name'] == DATA_SOURCE['name']
        assert 'identity_class' in stix_identity and stix_identity['identity_class'] == DATA_SOURCE['identity_class']
    
    @check_stix_bundle_type
    def test_stix_extension_prop(self):
        """
        to test the extension stix object properties
        """
        sdo_type = 'extension-definition'
        stix_extension = TestMaxmindResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
        assert 'type' in stix_extension and stix_extension['type'] == sdo_type
        assert 'name' in stix_extension
        assert 'version' in stix_extension
        assert 'extension_types' in stix_extension and stix_extension['extension_types'] == extension_types
        assert 'extension_properties' in stix_extension and stix_extension['extension_properties'] == extension_properties
    
    @check_stix_bundle_type
    def test_stix_indicator_prop(self):
        """
        to test the indicator stix object properties
        """
        sdo_type = 'indicator'
        stix_indicator = TestMaxmindResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == query_pattern
        assert 'valid_from' in stix_indicator
        assert 'created' in stix_indicator
        assert 'modified' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'unknown'
    @check_stix_bundle_type
    def test_stix_indicator_extensions_prop(self):
        """
        to test the indicator stix object extensions properties
        """
        stix_indicator = TestMaxmindResultsToStix.get_first_of_type(self.result_bundle_objects, 'indicator')
        assert 'x_ibm_original_threat_feed_data' in stix_indicator
        extension_property = extension_properties[0]
        property_name = "x_ibm_original_threat_feed_data.full"
        is_exist = TestMaxmindResultsToStix.exists(stix_indicator, property_name.split("."))
        assert is_exist is not None
        assert stix_indicator[extension_property]["full"][0]
