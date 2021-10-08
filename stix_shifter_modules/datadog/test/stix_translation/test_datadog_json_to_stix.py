import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.datadog.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "datadog"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "datadog",
    "identity_class": "events"
}
options = {}


class TestDatadogResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for onelogin translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """
        return the obj in the itr if constraint is true
        """
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        """
        to check whether the object belongs to respective stix object
        """
        return TestDatadogResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def test_common_prop():
        """
        to test the common stix object properties
        """
        data = {
            "date_happened": 1628017283,
            "alert_type": "info",
            "title": "An API key has been created.",
            "url": "/event/event?id=6102786433786642502",
            "text": "API key getevents created by qradar10.34.38.141@gmail.com in org qradar",
            "tags": [
                "account",
                "audit"
            ],
            "device_name": "windows-GS-2190",
            "priority": "normal",
            "host": "121.0.0.1",
            "resource": "/api/event/6102786433786642502",
            "id": 6102786433786642502
        }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        assert result_bundle_identity['id'] == data_source['id']
        assert result_bundle_identity['name'] == data_source['name']
        assert result_bundle_identity['identity_class'] == data_source['identity_class']

        observed_data = result_bundle_objects[1]
        assert observed_data['id'] is not None
        assert observed_data['type'] == "observed-data"
        assert observed_data['created_by_ref'] == result_bundle_identity['id']

        assert observed_data['modified'] is not None
        assert observed_data['created'] is not None
        assert observed_data['first_observed'] is not None
        assert observed_data['last_observed'] is not None
        assert observed_data['number_observed'] is not None

    @staticmethod
    def test_custom_property():
        """
        to test the custom stix object properties
        """
        data = {
            "date_happened": 1628017283,
            "alert_type": "info",
            "url": "/event/event?id=6102786433786642502",
            "text": "API key getevents created by qradar10.34.38.141@gmail.com in org qradar",
            "tags": [
                "account",
                "audit"
            ],
            "device_name": "windows-2190",
            "priority": "normal",
            "host": "i-deadbeef",
            "resource": "/api/event/6102786433786642502",
            "id": 6102786433786642502
        }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)

        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        custom_object_1 = TestDatadogResultsToStix.get_first_of_type(objects.values(), 'domain-name')
        custom_object_2 = TestDatadogResultsToStix.get_first_of_type(objects.values(), 'x-datadog-event')

        assert custom_object_1 is not None, 'Custom object type not found'
        assert custom_object_1.keys() == {'type', "value"}
        assert custom_object_1['value'] == "i-deadbeef"

        assert custom_object_2 is not None, 'Custom object type not found'
        assert custom_object_2.keys() == {'type', 'alert_type', 'tags', 'priority'}
        assert custom_object_2['alert_type'] == 'info'
