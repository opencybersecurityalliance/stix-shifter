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
        data = {'computer_identity': '1626351170-xlcr.hcl.local', 'subQueryID': 1,
                'sha256hash': '89698504cb73fefacd012843a5ba2e0acda7fd8d5db4efaad22f7fe54fa422f5',
                'sha1hash': '41838ed7a546aeefe184fb8515973ffee7c3ba7e', 'md5hash': '958d9ba84826e48094e361102a272fd6',
                'file_path': '/tmp/big42E1.tmp', 'file_name': 'big42E1.tmp', 'file_size': '770', 'type': 'file',
                'timestamp': '1567046172', 'event_count': '1'}
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

        assert observed_data['modified'] is not None
        assert observed_data['created'] is not None
        assert observed_data['first_observed'] is not None
        assert observed_data['last_observed'] is not None
        assert observed_data['number_observed'] is not None
        assert observed_data['x_com_bigfix_relevance'] is not None

    def test_custom_property(self):
        """
        to test the custom stix object properties
        """
        data = {'computer_identity': '1626351170-xlcr.hcl.local', 'subQueryID': 1,
                'sha256hash': '89698504cb73fefacd012843a5ba2e0acda7fd8d5db4efaad22f7fe54fa422f5',
                'sha1hash': '41838ed7a546aeefe184fb8515973ffee7c3ba7e',
                'md5hash': '958d9ba84826e48094e361102a272fd6',
                'file_path': '/tmp/big42E1.tmp', 'file_name': 'big42E1.tmp', 'file_size': '770', 'type': 'file',
                'timestamp': '1567046172', 'event_count': '1'}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        observed_data = result_bundle_objects[1]
        custom_object = observed_data['x_com_bigfix_relevance']
        assert custom_object.keys() == {'computer_identity'}
        assert custom_object['computer_identity'] == '1626351170-xlcr.hcl.local'

    def test_file_json_to_stix(self):
        """
        to test file stix object properties
        """
        data = {'computer_identity': '1626351170-xlcr.hcl.local', 'subQueryID': 1,
                'sha256hash': '89698504cb73fefacd012843a5ba2e0acda7fd8d5db4efaad22f7fe54fa422f5',
                'sha1hash': '41838ed7a546aeefe184fb8515973ffee7c3ba7e', 'md5hash': '958d9ba84826e48094e361102a272fd6',
                'file_path': '/tmp/big42E1.tmp', 'file_name': 'big42E1.tmp', 'file_size': '770', 'type': 'file',
                'timestamp': '1567046172', 'event_count': '1'}
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
        assert file_obj.keys() == {'type', 'hashes', 'parent_directory_ref', 'name', 'size'}
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'big42E1.tmp'
        assert file_obj['hashes'] == {'SHA-256': '89698504cb73fefacd012843a5ba2e0acda7fd8d5db4efaad22f7fe54fa422f5',
                                      'SHA-1': '41838ed7a546aeefe184fb8515973ffee7c3ba7e',
                                      'MD5': '958d9ba84826e48094e361102a272fd6'}
        assert file_obj['parent_directory_ref'] == '1'
        assert file_obj['size'] == 770

    def test_process_json_to_stix(self):
        """
        to test process stix object properties
        """
        data = {'computer_identity': '13476923-archlinux', 'subQueryID': 1,
                'sha256hash': '2f2f74f4083b95654a742a56a6c7318f3ab378c94b69009ceffc200fbc22d4d8',
                'sha1hash': '0c8e8b1d4eb31e1e046fea1f1396ff85068a4c4a', 'md5hash': '148fd5f2a448b69a9f21d4c92098c4ca',
                'file_path': '/usr/lib/systemd/systemd', 'process_ppid': '0', 'process_user': 'root',
                'timestamp': '1565616101', 'process_name': 'systemd', 'process_id': '1', 'file_size': '1468376',
                'type': 'process', 'event_count': '1'}
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
        assert process_obj.keys() == {'type', 'binary_ref', 'parent_ref', 'creator_user_ref', 'name', 'pid'}
        assert process_obj['type'] == 'process'
        assert process_obj['name'] == 'systemd'
        assert process_obj['pid'] == 1
        assert process_obj['binary_ref'] == '0'
        assert process_obj['parent_ref'] == '3'
        assert process_obj['creator_user_ref'] == '4'

    def test_network_json_to_stix(self):
        """
        to test network stix object properties
        """
        data = {'computer_identity': '550872812-WIN-N11M78AV7BP', 'subQueryID': 1, 'local_address': '192.168.36.10',
                'local_port': '139', 'process_ppid': '0', 'process_user': 'NT AUTHORITY\\SYSTEM',
                'timestamp': '1565875693', 'process_name': 'System', 'process_id': '4', 'type': 'Socket',
                'protocol': 'udp', 'event_count': '1'}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestBigFixResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert network_obj is not None, 'network-traffic object type not found'
        assert network_obj.keys() == {'type', 'src_ref', 'src_port', 'protocols'}
        assert network_obj['type'] == 'network-traffic'
        assert network_obj['src_ref'] == '0'
        assert network_obj['src_port'] == 139
        assert network_obj['protocols'] == ['udp']

    def test_mac_addr_json_to_stix(self):
        """
        to test network stix object properties
        """
        data = {'computer_identity': '541866979-suse01', 'subQueryID': 1, 'local_address': '192.168.36.110',
                'mac': '0a-ab-41-e0-89-f8', 'type': 'Address', 'event_count': '1'}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestBigFixResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert network_obj is not None, 'network-traffic object type not found'
        assert network_obj.keys() == {'type', 'src_ref'}
        assert network_obj['type'] == 'network-traffic'
        assert network_obj['src_ref'] == '0'

    def test_network_json_to_stix_negative(self):
        """
        to test negative test case for stix object
        """
        data = {'computer_identity': '550872812-WIN-N11M78AV7BP', 'subQueryID': 1, 'local_address': '192.168.36.10',
                'local_port': '139', 'process_ppid': '0', 'process_user': 'NT AUTHORITY\\SYSTEM',
                'timestamp': '1565875693', 'process_name': 'System', 'process_id': '4', 'type': 'Socket',
                'protocol': 'udp', 'event_count': '1'}
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

    def test_unmapped_attribute_with_mapped_attribute(self):
        message = "\"GET /blog HTTP/1.1\" 200 2571"
        data = {"message": message, "unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert ('objects' in observed_data)
        objects = observed_data['objects']
        assert (objects == {})
        curr_obj = TestBigFixResultsToStix.get_first_of_type(objects.values(), 'message')
        assert (curr_obj is None), 'url object type not found'

    def test_unmapped_attribute_alone(self):
        data = {"unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert ('objects' in observed_data)
        objects = observed_data['objects']
        assert (objects == {})
