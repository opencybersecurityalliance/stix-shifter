import json
import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.cbcloud.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "cbcloud"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d1",
    "name": "cbcloud",
    "identity_class": "events"
}
options = {}

DATA = {
            "backend_timestamp": "2021-01-04T00:23:39.202Z",
            "childproc_count": 27,
            "crossproc_count": 549,
            "device_external_ip": "46.135.79.144",
            "device_group_id": 1730,
            "device_id": 13964,
            "device_name": "iestestmachine1",
            "device_os": "WINDOWS",
            "device_policy_id": 2928,
            "device_timestamp": "2021-01-04T00:17:14.262Z",
            "filemod_count": 0,
            "ingress_time": 1609719770320,
            "modload_count": 0,
            "netconn_count": 0,
            "org_id": "X79DF22N",
            "parent_guid": "X79DF22N-0000368c-0000022c-00000000-1d6dcd71a37dfe5",
            "parent_hash": [
                "083bb4f3b20419c87db656f1465e5f782acde76838cde6207f26aad035c69de0",
                "e0c7813a97ca7947ff5c18a8f3b61a45"
            ],
            "parent_pid": 556,
            "process_cmdline": [
                "C:\\windows\\system32\\svchost.exe -k DcomLaunch"
            ],
            "process_guid": "X79DF22N-0000368c-00000280-00000000-1d6dcd7308af9c9",
            "process_hash": [
                "e3a2ad05e24105b35e986cf9cb38ec47",
                "c7db4ae8175c33a47baa3ddfa089fad17bc8e362f21e835d78ab22c9231fe370"
            ],
            "process_name": "c:\\windows\\system32\\svchost.exe",
            "process_pid": [
                640
            ],
            "process_start_time": "2020-12-28T05:06:24.450Z",
            "process_username": [
                "NT AUTHORITY\\SYSTEM"
            ],
            "regmod_count": 0,
            "scriptload_count": 0
        }

class TestCBCloudResultsToStix(unittest.TestCase):
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
        return TestCBCloudResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)
    
    @staticmethod
    def test_common_prop():
        """
        to test the common stix object properties
        """

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA], get_module_transformers(MODULE), options)
        
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
        # assert False
    
    def test_file_process_json_to_stix(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA], get_module_transformers(MODULE), options)

        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        file_obj = TestCBCloudResultsToStix.get_first_of_type(objects.values(), 'file')
        process_obj = TestCBCloudResultsToStix.get_first_of_type(objects.values(), 'process')

        assert file_obj is not None, 'file object type not found'
        assert file_obj .keys() == {'type', 'name'}
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'c:\\windows\\system32\\svchost.exe'

        assert process_obj is not None, 'file object type not found'
        assert process_obj.keys() == {'type', 'x_unique_id', 'pid'}
        assert process_obj['type'] == 'process'
        assert process_obj['x_unique_id'] == 'X79DF22N-0000368c-0000022c-00000000-1d6dcd71a37dfe5'
        assert process_obj['pid'] == 556