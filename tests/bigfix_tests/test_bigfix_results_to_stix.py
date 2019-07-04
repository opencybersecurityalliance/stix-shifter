import json
from stix_shifter.stix_translation.src.utils import transformers
from stix_shifter.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter.stix_translation.src.modules.bigfix import bigfix_translator

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


class TestBigFixResultsToStix(object):
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestBigFixResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    def test_common_prop(self):
        data = {"computer_identity": "12369754-bigdata4545.canlab.ibm.com", "subQueryID": 1, "start_time": "1541424881", "type": "process", "process_name": "systemd", "process_id": "1",
                "sha256hash": "9c74c625b2aba7a2e8d8a42e2e94715c355367f7cbfa9bd5404ba52b726792a6", "sha1hash": "916933045c5c91ebcaa325e7f8302f3a732a0a3d", "md5hash": "28a9beb86c4d4c31ba572805bea8494f", "file_path": "/usr/lib/systemd/systemd"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        print(json.dumps(result_bundle, indent=2))
        assert(result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert(result_bundle_identity['type'] == data_source['type'])
        assert(result_bundle_identity['id'] == data_source['id'])
        assert(result_bundle_identity['name'] == data_source['name'])
        assert(result_bundle_identity['identity_class']
               == data_source['identity_class'])

        observed_data = result_bundle_objects[1]
        print(observed_data)
        assert(observed_data['id'] is not None)
        assert(observed_data['type'] == "observed-data")
        assert(observed_data['created_by_ref'] == result_bundle_identity['id'])

        assert(observed_data['created'] is not None)
        assert(observed_data['first_observed'] is not None)
        assert(observed_data['last_observed'] is not None)

    def test_file_results_to_stix(self):
        file_name = '.X0-lock'
        data = {"computer_identity": "12369754-bigdata4545.canlab.ibm.com", "subQueryID": 1, "type": "file", "file_name": ".X0-lock", "sha256hash": "7236f966f07259a1de3ee0d48a3ef0ee47c4a551af7f0d76dcabbbb9d6e00940",
                "sha1hash": "8b5e953be1db90172af66631132f6f27dda402d2", "md5hash": "e5307d27f0eb9a27af8597a1ddc51e89", "file_path": "/tmp/.X0-lock", "modified_time": "1541424894"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)

        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert(result_bundle_identity['type'] == data_source['type'])

        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        file_obj = TestBigFixResultsToStix.get_first_of_type(objects.values(), 'file')
        assert(file_obj is not None), 'file object type not found'
        assert(file_obj.keys() == {'type', 'name', 'hashes', 'parent_directory_ref'})
        assert(file_obj['name'] == file_name)

    def test_process_results_to_stix(self):
        process_name = 'systemd'
        data = {"computer_identity": "12369754-bigdata4545.canlab.ibm.com", "subQueryID": 1, "start_time": "1541424881", "type": "process", "process_name": "systemd", "process_id": "1",
                "sha256hash": "9c74c625b2aba7a2e8d8a42e2e94715c355367f7cbfa9bd5404ba52b726792a6", "sha1hash": "916933045c5c91ebcaa325e7f8302f3a732a0a3d", "md5hash": "28a9beb86c4d4c31ba572805bea8494f", "file_path": "/usr/lib/systemd/systemd"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        print(json.dumps(result_bundle, indent=2))
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert(result_bundle_identity['type'] == data_source['type'])

        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        process_obj = TestBigFixResultsToStix.get_first_of_type(objects.values(), 'process')
        assert(process_obj is not None), 'process object type not found'
        assert(process_obj.keys() == {'type', 'name', 'pid', 'binary_ref'})
        assert(process_obj['name'] == process_name)
