import json
import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.onelogin.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "onelogin"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "onelogin",
    "identity_class": "events"
}
options = {}


class TestOneloginResultsToStix(unittest.TestCase):
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
        return TestOneloginResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def test_common_prop():
        """
        to test the common stix object properties
        """
        data = {
            "id": 81004691744,
            "created_at": "2021-06-22T13:12:06.437Z",
            "account_id": 192204,
            "user_id": 138593517,
            "event_type_id": 149,
            "notes": "Default",
            "ipaddr": "52.34.255.228",
            "actor_user_id": 12345,
            "assuming_acting_user_id": 12345,
            "role_id": 441778,
            "app_id": "Default",
            "group_id": "Default",
            "otp_device_id": "Default",
            "policy_id": 123,
            "actor_system": "Mapping",
            "custom_message": "Default",
            "role_name": "Default",
            "app_name": "Default",
            "group_name": "Default",
            "actor_user_name": "Mapping",
            "user_name": "Akshay Pange",
            "policy_name": "policy_name",
            "otp_device_name": "Default",
            "operation_name": "Default",
            "directory_sync_run_id": "Default",
            "directory_id": 12345678,
            "resolution": "resolution",
            "client_id": 12345678,
            "resource_type_id": "Default",
            "error_description": "error_description",
            "proxy_ip": "127.0.0.1",
            "risk_score": 2,
            "risk_reasons": "risk_reasons",
            "risk_cookie_id": 123,
            "browser_fingerprint": True
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
            "id": 81004691744,
            "created_at": "2021-06-22T13:12:06.437Z",
            "account_id": 192204,
            "user_id": 138593517,
            "event_type_id": 149,
            "notes": "Default",
            "ipaddr": "52.34.255.228",
            "actor_user_id": 12345,
            "assuming_acting_user_id": 12345,
            "role_id": 441778,
            "app_id": "Default",
            "group_id": "Default",
            "otp_device_id": "Default",
            "policy_id": 123,
            "actor_system": "Mapping",
            "custom_message": "Default",
            "role_name": "Default",
            "app_name": "Default",
            "group_name": "Default",
            "actor_user_name": "Mapping",
            "user_name": "Akshay Pange",
            "policy_name": "policy_name",
            "otp_device_name": "Default",
            "operation_name": "Default",
            "directory_sync_run_id": "Default",
            "directory_id": 12345678,
            "resolution": "resolution",
            "client_id": 12345678,
            "resource_type_id": "Default",
            "error_description": "error_description",
            "proxy_ip": "127.0.0.1",
            "risk_score": 2,
            "risk_reasons": "risk_reasons",
            "risk_cookie_id": 123,
            "browser_fingerprint": True
        }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)

        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        custom_object_1 = TestOneloginResultsToStix.get_first_of_type(objects.values(), 'x-onelogin-finding')
        custom_object_2 = TestOneloginResultsToStix.get_first_of_type(objects.values(), 'x-onelogin-risk')

        assert custom_object_1 is not None, 'Custom object type not found'
        assert custom_object_1.keys() == {'type', 'unique_id', 'event_type_id', 'notes', 'role_id', 'app_id', 'custom_message', 'role_name', 'app_name', 'group_name', 'otp_device_name', 'operation_name', 'directory_sync_run_id', 'directory_id', 'resolution', 'client_id', 'resource_type_id', 'proxy_ip', 'browser_fingerprint'}
        assert custom_object_1['unique_id'] == 81004691744
        assert custom_object_1['event_type_id'] == 149

        assert custom_object_2 is not None, 'Custom object type not found'
        assert custom_object_2.keys() == {'type', 'error_description', 'risk_score', 'risk_cookie_id', 'risk_reasons'}
        assert custom_object_2['error_description'] == 'error_description'
        assert custom_object_2['risk_reasons'] == 'risk_reasons'

