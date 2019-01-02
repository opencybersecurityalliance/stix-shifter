import json
from stix_shifter.stix_translation.src import transformers 
from stix_shifter.stix_translation.src.modules.bigfix.bigfix_to_stix import bigfix_to_stix_translator
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
        data = {"computerID": 1111222, "computerName": "DESKTOP-TEST", "subQueryID": 1, "isFailure": False, "result": "process, System, 4, sha256, n/a, sha1, n/a, md5, n/a, n/a, 1541424881", "ResponseTime": 2000}

        result_bundle = bigfix_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        print(result_bundle)
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

        # assert(observed_data['number_observed'] == 5)
        assert(observed_data['created'] is not None)
        # assert(observed_data['modified'] is not None)
        # assert(observed_data['first_observed'] is not None)
        # assert(observed_data['last_observed'] is not None)
    
    def test_file_relevance_to_stix(self):
    #     # "[{\"computerID\": 14821900, \"computerName\": \"DESKTOP-C30V1JF\", \"subQueryID\": 1, \"isFailure\": True, \"result\": \"Singular expression refers to nonexistent object.\", \"ResponseTime\": 1000}, {\"computerID\": 12369754, \"computerName\": \"bigdata4545.canlab.ibm.com\", \"subQueryID\": 1, \"isFailure\": False, \"result\": \"file, .X0-lock, sha256, 7236f966f07259a1de3ee0d48a3ef0ee47c4a551af7f0d76dcabbbb9d6e00940, sha1, 8b5e953be1db90172af66631132f6f27dda402d2, md5, e5307d27f0eb9a27af8597a1ddc51e89, /tmp/.X0-lock, 1541424894\", \"ResponseTime\": 5000}, {\"computerID\": 12369754, \"computerName\": \"bigdata4545.canlab.ibm.com\", \"subQueryID\": 1, \"isFailure\": False, \"result\": \"file, yum_save_tx.2018-12-11.06-47.29se2j.yumtx, sha256, 80f0be6226a036ade71acda0d1002f13ed1a2ef02ed4c1d51b897025d6351529, sha1, 468ffec645354007f12d401bf61c4a3c5c16ac65, md5, 8d683d83c1bcfa95a9ab428eeb54f52c, /tmp/yum_save_tx.2018-12-11.06-47.29se2j.yumtx, 1544528864\", \"ResponseTime\": 5000}]
        file_name = '.X0-lock'
        data = {"computerID": 1111222, "computerName": "canlab.ibm.com", "subQueryID": 1, "isFailure": False, "result": "file, .X0-lock, sha256, 7236f966f07259a1de3ee0d48a3ef0ee47c4a551af7f0d76dcabbbb9d6e00940, sha1, 8b5e953be1db90172af66631132f6f27dda402d2, md5, e5307d27f0eb9a27af8597a1ddc51e89, /tmp/.X0-lock, 1541424894", "ResponseTime": 5000}
        result_bundle = bigfix_to_stix_translator.convert_to_stix(
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
