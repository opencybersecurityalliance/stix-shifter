import json
import unittest
from functools import wraps
from stix_shifter_modules.dshield.entry_point import EntryPoint
from stix_shifter_modules.dshield.tests.stix_translation.json.json_translation import *

MODULE = "dshield"
DATA_SOURCE = {"type": "identity", "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3","name": "DShield_Connector","identity_class": "system"}

options = {'stix_validator':True}
entry_point = EntryPoint(options=options)
translation_options = {}

extension_types = ["toplevel-property-extension"] 
extension_properties = ["x_ibm_original_threat_feed_data", "threat_score", "threat_attributes"]

class TestDshieldResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for translate results
    """

    def __init__(self,*args, **kwargs):
        super(TestDshieldResultsToStix, self).__init__(*args, **kwargs)
        self.result_translator = entry_point.create_default_results_translator(dialect='default')
        self.result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=dshield_test_transmitQueryData_ip_benign['data'])
        self.result_bundle_objects = self.result_bundle['objects']
        self.result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=dshield_test_transmitQueryData_ip_unkown['data'])
        self.result_bundle_objects_none = self.result_bundle['objects']
        self.result_bundle = self.result_translator.translate_results(data_source=DATA_SOURCE, data=dshield_test_transmitQueryData_ip_anoma['data'])
        self.result_bundle_objects_anoma = self.result_bundle['objects']
        self.extension_property_names = []
    
    @staticmethod
    def exists(obj, chain):
        """
        Check if the nested keys exist in the dictionary or not
        """
        _key = chain.pop(0)
        if _key in obj:
            return TestDshieldResultsToStix.exists(obj[_key], chain) if chain else obj[_key]
    
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestDshieldResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)
    
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
        stix_identity = TestDshieldResultsToStix.get_first_of_type(self.result_bundle_objects, DATA_SOURCE['type'])
        assert 'type' in stix_identity and stix_identity['type'] == DATA_SOURCE['type']
        assert 'name' in stix_identity and stix_identity['name'] == DATA_SOURCE['name']
        assert 'identity_class' in stix_identity and stix_identity['identity_class'] == DATA_SOURCE['identity_class']
    
    @check_stix_bundle_type
    def test_stix_extension_prop(self):
        """
        to test the extension stix object properties
        """
        sdo_type = 'extension-definition'
        stix_extension = TestDshieldResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
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
        stix_indicator = TestDshieldResultsToStix.get_first_of_type(self.result_bundle_objects, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == dshield_test_query_pattern
        assert 'valid_from' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'benign'
    
    @check_stix_bundle_type
    def test_stix_indicator_prop_none(self):
        """
        to test the indicator stix object properties
        """
        sdo_type = 'indicator'
        stix_indicator = TestDshieldResultsToStix.get_first_of_type(self.result_bundle_objects_none, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == dshield_test_query_pattern
        assert 'valid_from' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'unknown'
    
    @check_stix_bundle_type
    def test_stix_indicator_prop_anoma(self):
        """
        to test the indicator stix object properties
        """
        sdo_type = 'indicator'
        stix_indicator = TestDshieldResultsToStix.get_first_of_type(self.result_bundle_objects_anoma, sdo_type)
        assert 'type' in stix_indicator and stix_indicator['type'] == sdo_type
        assert 'pattern' in stix_indicator and stix_indicator['pattern'] == dshield_test_query_pattern
        assert 'valid_from' in stix_indicator
        assert 'indicator_types' in stix_indicator and len(stix_indicator['indicator_types']) == 1 \
               and stix_indicator['indicator_types'][0] == 'anomalous-activity'
    
    @check_stix_bundle_type
    def test_stix_indicator_extensions_prop(self):
        """
        to test the indicator stix object extensions properties
        """
        stix_extension = TestDshieldResultsToStix.get_first_of_type(self.result_bundle_objects, 'extension-definition')
        stix_indicator = TestDshieldResultsToStix.get_first_of_type(self.result_bundle_objects, 'indicator')
        assert 'x_ibm_original_threat_feed_data' in stix_indicator
        extension_property = extension_properties[0]
        property_name = "x_ibm_original_threat_feed_data.full"
        is_exist = TestDshieldResultsToStix.exists(stix_indicator, property_name.split("."))
        assert is_exist is not None
        assert stix_indicator[extension_property]["full"][0]