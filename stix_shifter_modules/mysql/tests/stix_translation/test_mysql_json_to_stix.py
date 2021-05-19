from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.mysql.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = 'mysql'
RESULTS = 'results'
TRANSFORMERS = get_module_transformers(MODULE)
epoch_to_timestamp_class = TRANSFORMERS.get('EpochToTimestamp')
EPOCH_START = 1531169112
EPOCH_END = 1531169254
START_TIMESTAMP = epoch_to_timestamp_class.transform(EPOCH_START)
END_TIMESTAMP = epoch_to_timestamp_class.transform(EPOCH_END)
entry_point = EntryPoint()
MAP_DATA = entry_point.get_results_translator().map_data
DATA_SOURCE = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "MySQL",
    "identity_class": "events"
}

DATA = {
            "source_ipaddr": "0.0.0.0", 
            "dest_ipaddr": "255.255.255.1", 
            "url": "https://example.com", 
            "username": "someuserid2018", 
            "protocol": 'tcp',
            "source_port": 3000, 
            "dest_port": 2000, 
            "filename": "somefile.exe", 
            "sha256hash": "sha256_hash", 
            "md5hash": "md5_hash", 
            "file_path": "C:/some/path/"
        }

OPTIONS = {}


class TestTransform(object):
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestTransform.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    @staticmethod
    def get_object_keys(objects):
        for k, v in objects.items():
            if k == 'type':
                yield v
            elif isinstance(v, dict):
                for id_val in TestTransform.get_object_keys(v):
                    yield id_val

    def test_common_prop(self):
        DATA = {"entry_time": EPOCH_START, "entry_time": EPOCH_END, "eventcount": 1}

        result_bundle = json_to_stix_translator.convert_to_stix(
            DATA_SOURCE, MAP_DATA, [DATA], TRANSFORMERS, OPTIONS)

        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == DATA_SOURCE['type']
        assert result_bundle_identity['id'] == DATA_SOURCE['id']
        assert result_bundle_identity['name'] == DATA_SOURCE['name']
        assert result_bundle_identity['identity_class'] == DATA_SOURCE['identity_class']

        observed_data = result_bundle_objects[1]

        assert observed_data['id']
        assert observed_data['type'] == "observed-data"
        assert observed_data['created_by_ref'] == result_bundle_identity['id']

        assert observed_data['number_observed'] == 1
        assert observed_data['created']
        assert observed_data['modified']
        assert observed_data['first_observed']
        assert observed_data['last_observed']

    def test_cybox_observables(self):
        
        result_bundle = json_to_stix_translator.convert_to_stix(
            DATA_SOURCE, MAP_DATA, [DATA], TRANSFORMERS, OPTIONS)

        assert result_bundle['type'] == 'bundle'

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        # network-traffic
        stix_object = TestTransform.get_first_of_type(objects.values(), 'network-traffic')
        assert stix_object, 'network-traffic object type not found'
        assert "src_ref" in stix_object
        assert "dst_ref" in stix_object
        assert "src_port" in stix_object and stix_object['src_port'] == 3000
        assert "dst_port" in stix_object and stix_object['dst_port'] == 2000
        assert "protocols" in stix_object and stix_object['protocols'] == ['tcp'] 
        
        # destination ipv4-addr
        ip_ref = stix_object['dst_ref']
        assert ip_ref in objects, f"dst_ref with key {stix_object['dst_ref']} not found"
        
        ip_obj = objects[ip_ref]
        assert "type" in ip_obj and ip_obj['type'] == 'ipv4-addr'
        assert "value" in ip_obj and ip_obj['value'] == DATA["dest_ipaddr"]

        # source ipv4-addr
        ip_ref = stix_object['src_ref']
        assert ip_ref in objects, f"src_ref with key {stix_object['src_ref']} not found"

        ip_obj = objects[ip_ref]
        assert "type" in ip_obj and ip_obj['type'] == 'ipv4-addr'
        assert "value" in ip_obj and ip_obj['value'] == DATA["source_ipaddr"]

        # url
        stix_object = TestTransform.get_first_of_type(objects.values(), 'url')
        assert stix_object, 'url object type not found'
        assert "value" in stix_object and stix_object['value'] == DATA['url']

        # user-account
        stix_object = TestTransform.get_first_of_type(objects.values(), 'user-account')
        assert  stix_object, 'user-account object type not found'
        assert  "user_id" in stix_object and stix_object['user_id'] == DATA['username']

        # file
        stix_object = TestTransform.get_first_of_type(objects.values(), 'file')
        assert stix_object, 'file object type not found'
        assert "name" in stix_object and stix_object['name'] == DATA['filename']
        assert "hashes" in stix_object 
        hashes = stix_object["hashes"]
        assert "MD5" in hashes and hashes["MD5"] == DATA["md5hash"]
        assert "SHA-256" in hashes and hashes["SHA-256"] == DATA["sha256hash"] 

        directory_ref = stix_object['parent_directory_ref']
        assert directory_ref in objects, f"dst_ref with key {stix_object['parent_directory_ref']} not found"

        # directory
        stix_object = TestTransform.get_first_of_type(objects.values(), 'directory')
        assert stix_object, 'directory object type not found'
        assert "path" in stix_object and stix_object["path"] == DATA["file_path"]

        
