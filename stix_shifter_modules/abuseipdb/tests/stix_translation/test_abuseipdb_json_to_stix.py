import json
import unittest
from functools import wraps
from stix_shifter_modules.abuseipdb.entry_point import EntryPoint

MODULE = "abuseipdb"
DATA_SOURCE = {"type": "identity", "id": "identity--000810fd-722d-52a0-bb9e-cd852e6ba394", "name": "AbuseIPDB_Connector",
               "identity_class": "system"}
options = {'stix_validator':True}
entry_point = EntryPoint(options=options)
ip_value = "194.147.78.155"
extension_types = ["toplevel-property-extension"]
extension_properties = ["x_ibm_original_threat_feed_data","threat_score","threat_attributes"]
query_pattern = "[ipv4-addr:value='"+ip_value+"']"
transmitQueryData = {
            "data": [
                {
                    "code": 200,
                    "success": True,
                    "report": [{
                            "ipAddress": "194.147.78.155",
                            "isPublic": True,
                            "ipVersion": 4,
                            "isWhitelisted": '',
                            "abuseConfidenceScore": 0,
                            "countryCode": "RU",
                            "usageType": "Data Center/Web Hosting/Transit",
                            "isp": "LIR LLC",
                            "domain": "lir.am",
                            "hostnames": [
                                "free.ds"
                            ],
                            "totalReports": 0,
                            "numDistinctUsers": 0,
                            "lastReportedAt": ''
                    }],
                    "data": ip_value,
                    "dataType": "ip",
                    "namespace": "8bf42ea1-e30d-41a2-a3ee-1aec759cf409",
                    "external_reference": {
                        "source_name": "AbuseIPDP_1_0",
                        "url": "https://www.abuseipdb.com/check/194.147.78.155"
                    }
                }
            ]
        }

class TestAbuseipdbResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for translate results
    """

    def __init__(self,*args, **kwargs):
        super(TestAbuseipdbResultsToStix, self).__init__(*args, **kwargs)
        self.result_translator = entry_point.create_default_results_translator(dialect='default')
        self.result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=transmitQueryData['data'])
        self.result_bundle_objects = self.result_bundle['objects']
        self.extension_property_names = []
    
    @staticmethod
    def exists(obj, chain):
        """
        Check if the nested keys exist in the dictionary or not
        """
        _key = chain.pop(0)
        if _key in obj:
            return TestAbuseipdbResultsToStix.exists(obj[_key], chain) if chain else obj[_key]
    
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestAbuseipdbResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)
            
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
            assert self.result_bundle['type'] == 'bundle'
            return func(self, *args, **kwargs)
        return wrapper_func

    @check_stix_bundle_type
    def test_stix_identity_prop(self):
        """
        to test the identity stix object properties
        """
        stix_identity = TestAbuseipdbResultsToStix.get_first_of_type(self.result_bundle_objects, DATA_SOURCE['type'])
        assert 'type' in stix_identity and stix_identity['type'] == DATA_SOURCE['type']
        assert 'name' in stix_identity and stix_identity['name'] == DATA_SOURCE['name']
        assert 'identity_class' in stix_identity and stix_identity['identity_class'] == DATA_SOURCE['identity_class']
    
    @check_stix_bundle_type
    def test_stix_extension_prop(self):
        """
        to test the extension stix object properties
        """
        sdo_type = 'extension-definition'
        stix_extension = TestAbuseipdbResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
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
        stix_indicator = TestAbuseipdbResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == query_pattern
        assert 'valid_from' in stix_indicator
        assert 'created' in stix_indicator
        assert 'modified' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'benign'
        assert 'external_references' in stix_indicator and len(stix_indicator['external_references']) > 0
        assert 'url' in stix_indicator['external_references'][0]
        assert stix_indicator['external_references'][0]['url'] == 'https://www.abuseipdb.com/check/194.147.78.155'
        assert 'threat_score' in stix_indicator
        assert 'threat_attributes' in stix_indicator
    
    @check_stix_bundle_type
    def test_stix_indicator_extensions_prop(self):
        """
        to test the indicator stix object extensions properties
        """
        stix_indicator = TestAbuseipdbResultsToStix.get_first_of_type(
            self.result_bundle_objects, 'indicator')

        assert 'x_ibm_original_threat_feed_data' in stix_indicator
        extension_property = extension_properties[0]
        property_name1 = "x_ibm_original_threat_feed_data.full"
        is_exist = TestAbuseipdbResultsToStix.exists(
            stix_indicator, property_name1.split("."))
        assert is_exist is not None
        assert stix_indicator[extension_property]["full"][0]
        property_name2 = "threat_attributes"
        is_exist1 = TestAbuseipdbResultsToStix.exists(
            stix_indicator, property_name2.split("."))
        assert is_exist1 is not None
        assert stix_indicator['threat_attributes']

