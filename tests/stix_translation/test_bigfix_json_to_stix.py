import json
from stix_shifter.stix_translation.src.utils import transformers
from stix_shifter.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter.stix_translation.src.modules.bigfix import bigfix_translator
import unittest

interface = bigfix_translator.Translator()
map_file = open(interface.mapping_filepath).read()
map_data = json.loads(map_file)
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "BigFix",
    "identity_class": "events"
}
options = {}


class TestBigFixResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for bigfix translate results
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
        return TestBigFixResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    def test_common_prop(self):
        """
        to test the common stix object properties
        """
        data = {"computer_identity": "12369754-bigdata4545.canlab.ibm.com", "subQueryID": 1, "start_time": "1541424881",
                "type": "process", "process_name": "systemd", "process_id": "1",
                "sha256hash": "9c74c625b2aba7a2e8d8a42e2e94715c355367f7cbfa9bd5404ba52b726792a6",
                "sha1hash": "916933045c5c91ebcaa325e7f8302f3a732a0a3d", "md5hash": "28a9beb86c4d4c31ba572805bea8494f",
                "file_path": "/usr/lib/systemd/systemd"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
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

        assert observed_data['created'] is not None
        assert observed_data['first_observed'] is not None
        assert observed_data['last_observed'] is not None

    def test_file_json_to_stix(self):
        """
        to test file stix object properties
        """
        data = {"computer_identity": "12369754-bigdata4545.canlab.ibm.com", "subQueryID": 1, "type": "file",
                "file_name": ".X0-lock",
                "sha256hash": "7236f966f07259a1de3ee0d48a3ef0ee47c4a551af7f0d76dcabbbb9d6e00940",
                "sha1hash": "8b5e953be1db90172af66631132f6f27dda402d2", "md5hash": "e5307d27f0eb9a27af8597a1ddc51e89",
                "file_path": "/tmp/.X0-lock", "modified_time": "1541424894"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)

        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        file_obj = TestBigFixResultsToStix.get_first_of_type(objects.values(), 'file')
        assert file_obj is not None, 'file object type not found'
        assert file_obj.keys() == {'type', 'name', 'hashes', 'parent_directory_ref'}
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == '.X0-lock'
        assert file_obj['hashes'] == {'SHA-256': '7236f966f07259a1de3ee0d48a3ef0ee47c4a551af7f0d76dcabbbb9d6e00940',
                                      'SHA-1': '8b5e953be1db90172af66631132f6f27dda402d2',
                                      'MD5': 'e5307d27f0eb9a27af8597a1ddc51e89'}
        assert file_obj['parent_directory_ref'] == '1'

    def test_process_json_to_stix(self):
        """
        to test process stix object properties
        """
        data = {"computer_identity": "12369754-bigdata4545.canlab.ibm.com", "subQueryID": 1, "start_time": "1541424881",
                "type": "process", "process_name": "systemd", "process_id": "1",
                "sha256hash": "9c74c625b2aba7a2e8d8a42e2e94715c355367f7cbfa9bd5404ba52b726792a6",
                "sha1hash": "916933045c5c91ebcaa325e7f8302f3a732a0a3d", "md5hash": "28a9beb86c4d4c31ba572805bea8494f",
                "file_path": "/usr/lib/systemd/systemd"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        process_obj = TestBigFixResultsToStix.get_first_of_type(objects.values(), 'process')
        assert process_obj is not None, 'process object type not found'
        assert process_obj.keys() == {'type', 'name', 'pid', 'binary_ref'}
        assert process_obj['type'] == 'process'
        assert process_obj['name'] == 'systemd'
        assert process_obj['pid'] == 1
        assert process_obj['binary_ref'] == '1'

    def test_network_json_to_stix(self):
        """
        to test network stix object properties
        """
        data = {'computer_identity': '550872812-WIN-N11M78AV7BP', 'subQueryID': 1, 'local_address': '192.168.36.10',
                'local_port': '139', 'remote_port': '-1', 'process_name': 'System', 'process_id': '4',
                'start_time': '1565875693', 'protocol': 'tcp'}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestBigFixResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert network_obj is not None, 'process object type not found'
        assert network_obj.keys() == {'type', 'src_ref', 'src_port', 'dst_port', 'protocols'}
        assert network_obj['type'] == 'network-traffic'
        assert network_obj['src_ref'] == '0'
        assert network_obj['src_port'] == 139
        assert network_obj['dst_port'] == -1
        assert network_obj['protocols'] == ['tcp']

    def test_mac_addr_json_to_stix(self):
        """
        to test network stix object properties
        """
        data = {'computer_identity': '1625765403-BIGFIX01', 'subQueryID': 1, 'local_address': '192.168.36.146',
                'mac': '0a-65-a4-7f-ad-88', 'type': 'Address'}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestBigFixResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert network_obj is not None, 'process object type not found'
        assert network_obj.keys() == {'type', 'src_ref'}
        assert network_obj['type'] == 'network-traffic'
        assert network_obj['src_ref'] == '0'

    def test_network_json_to_stix_negative(self):
        """
        to test negative test case for stix object
        """
        data = {'computer_identity': '550872812-WIN-N11M78AV7BP', 'subQueryID': 1, 'local_address': '192.168.36.10',
                'local_port': '139', 'remote_port': '-1', 'process_name': 'System', 'process_id': '4',
                'start_time': '1565875693', 'protocol': 'tcp'}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, data, transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestBigFixResultsToStix.get_first_of_type(objects.values(), 'file')
        assert network_obj is None
