from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.mysql.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers
import json

MODULE = 'mysql'
RESULTS = 'results'
TRANSFORMERS = get_module_transformers(MODULE)
EPOCH = 1634657528000
TIMESTAMP = "2021-10-19T15:32:08.000Z"

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
            "file_path": "C:/some/path/",
            "file_created_time": EPOCH,
            "file_modified_time": EPOCH,
            "file_accessed_time": EPOCH,
            "directory_created_time": EPOCH,
            "directory_modified_time": EPOCH,
            "directory_accessed_time": EPOCH,
            "process_id": 12345, 
            "process_name": "file executed", 
            "process_arguments": "some args", 
            "process_created_time": EPOCH
        }

CYBOX_ID = {
            "source-ipv4-addr": "ipv4-addr--0b6a89e3-e345-51b7-a8ee-aaff7ebf2df5", 
            "dest-ipv4-addr": "ipv4-addr--cb8e152d-60f0-596a-81e4-a22cc4a7f063", 
            "url": "url--8265905f-c609-52e3-ae52-6681bcd6086d", 
            "user-account": "user-account--3cd7ffc9-89f7-5b58-948c-117ec9b3e22a", 
            "network-traffic": "network-traffic--2ec70516-29b5-59f3-9743-3b93e97db6d8",
            "file": "file--243f1b5f-0391-501c-bed0-17e9f204f1d2",
            "directory": "directory--9ce39e76-d59e-5db2-8f0e-2001f689ea9d"
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
    def get_first_cybox_of_type_stix_2_1(itr, type):
        for obj in itr:
            if obj["type"] ==  type:
                return obj

    @staticmethod
    def get_first_cybox_of_id_stix_2_1(itr, id):
        for obj in itr:
            if obj["id"] ==  id:
                return obj

    @staticmethod
    def get_object_keys(objects):
        for k, v in objects.items():
            if k == 'type':
                yield v
            elif isinstance(v, dict):
                for id_val in TestTransform.get_object_keys(v):
                    yield id_val

    def test_common_prop(self):
        DATA = {"entry_time": EPOCH, "entry_time": EPOCH, "eventcount": 1}
        entry_point = EntryPoint()
        result_bundle = entry_point.translate_results(json.dumps(DATA_SOURCE), json.dumps([DATA]))

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

    def test_STIX_2_0_cybox_observables(self):
        entry_point = EntryPoint()
        result_bundle = entry_point.translate_results(json.dumps(DATA_SOURCE), json.dumps([DATA]))

        assert result_bundle['type'] == 'bundle'
        assert "spec_version" in result_bundle
        assert result_bundle['spec_version'] == '2.0'

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
        file_object = TestTransform.get_first_of_type(objects.values(), 'file')
        assert file_object, 'file object type not found'
        assert "name" in file_object and file_object['name'] == DATA['filename']
        assert "created" in file_object and file_object['created'] == TIMESTAMP
        assert "ctime" not in file_object
        assert "modified" in file_object and file_object['modified'] == TIMESTAMP
        assert "mtime" not in file_object
        assert "accessed" in file_object and file_object['accessed'] == TIMESTAMP
        assert "atime" not in file_object
        assert "parent_directory_ref" in file_object
        assert "hashes" in file_object 
        hashes = file_object["hashes"]
        assert "MD5" in hashes and hashes["MD5"] == DATA["md5hash"]
        assert "SHA-256" in hashes and hashes["SHA-256"] == DATA["sha256hash"]

        directory_ref = file_object['parent_directory_ref']
        assert directory_ref in objects, f"dst_ref with key {file_object['parent_directory_ref']} not found"

        # directory
        directory_object = TestTransform.get_first_of_type(objects.values(), 'directory')
        assert directory_object, 'directory object type not found'
        assert "path" in directory_object and directory_object["path"] == DATA["file_path"]
        assert "created" in directory_object and directory_object['created'] == TIMESTAMP
        assert "ctime" not in directory_object
        assert "modified" in directory_object and directory_object['modified'] == TIMESTAMP
        assert "mtime" not in directory_object
        assert "accessed" in directory_object and directory_object['accessed'] == TIMESTAMP
        assert "atime" not in directory_object

        # process
        process_object = TestTransform.get_first_of_type(objects.values(), 'process')
        assert process_object, 'process object type not found'
        assert "name" in process_object and process_object['name'] == DATA['process_name']
        assert "pid" in process_object and process_object['pid'] == DATA['process_id']
        assert "arguments" in process_object and process_object['arguments'] == DATA['process_arguments']
        assert "created" in process_object and process_object['created'] ==  TIMESTAMP
        assert "binary_ref" in process_object
        assert "image_ref" not in process_object

    def test_STIX_2_1_cybox_observables(self):
        options = {
            "stix_2.1": True
        }
        entry_point = EntryPoint(options=options)
        result_bundle = entry_point.translate_results(json.dumps(DATA_SOURCE), json.dumps([DATA]))

        assert result_bundle['type'] == 'bundle'
        assert "spec_version" not in result_bundle

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert 'objects' not in observed_data

        # network-traffic
        network_traffic_object = TestTransform.get_first_cybox_of_type_stix_2_1(result_bundle_objects, 'network-traffic')
        assert network_traffic_object, 'network-traffic object type not found'
        assert "src_ref" in network_traffic_object
        assert "dst_ref" in network_traffic_object
        assert "src_port" in network_traffic_object and network_traffic_object['src_port'] == 3000
        assert "dst_port" in network_traffic_object and network_traffic_object['dst_port'] == 2000
        assert "protocols" in network_traffic_object and network_traffic_object['protocols'] == ['tcp'] 
        assert "id" in network_traffic_object and str(network_traffic_object['id']) == CYBOX_ID["network-traffic"]
        
        # destination ipv4-addr
        destination_ipv4_object = TestTransform.get_first_cybox_of_id_stix_2_1(result_bundle_objects, network_traffic_object["dst_ref"])
        assert "type" in destination_ipv4_object and destination_ipv4_object['type'] == 'ipv4-addr'
        assert "value" in destination_ipv4_object and destination_ipv4_object['value'] == DATA["dest_ipaddr"]
        assert "id" in destination_ipv4_object and str(destination_ipv4_object['id']) == CYBOX_ID["dest-ipv4-addr"]

        # source ipv4-addr
        source_ipv4_object = TestTransform.get_first_cybox_of_id_stix_2_1(result_bundle_objects, network_traffic_object["src_ref"])
        assert "type" in source_ipv4_object and source_ipv4_object['type'] == 'ipv4-addr'
        assert "value" in source_ipv4_object and source_ipv4_object['value'] == DATA["source_ipaddr"]
        assert "id" in source_ipv4_object and str(source_ipv4_object['id']) == CYBOX_ID["source-ipv4-addr"]

        # url
        url_object = TestTransform.get_first_cybox_of_type_stix_2_1(result_bundle_objects, 'url')
        assert url_object, 'url object type not found'
        assert "value" in url_object and url_object['value'] == DATA['url']
        assert "id" in url_object and str(url_object['id']) == CYBOX_ID["url"]

        # user-account
        user_account_object = TestTransform.get_first_cybox_of_type_stix_2_1(result_bundle_objects, 'user-account')
        assert  user_account_object, 'user-account object type not found'
        assert  "user_id" in user_account_object and user_account_object['user_id'] == DATA['username']
        assert "id" in user_account_object and str(user_account_object['id']) == CYBOX_ID["user-account"]

        # file
        file_object = TestTransform.get_first_cybox_of_type_stix_2_1(result_bundle_objects, 'file')
        assert file_object, 'file object type not found'
        assert "name" in file_object and file_object['name'] == DATA['filename']
        assert "ctime" in file_object and file_object['ctime'] == TIMESTAMP
        assert "created" not in file_object
        assert "mtime" in file_object and file_object['mtime'] == TIMESTAMP
        assert "modified" not in file_object
        assert "atime" in file_object and file_object['atime'] == TIMESTAMP
        assert "accessed" not in file_object
        assert "parent_directory_ref" in file_object
        assert "hashes" in file_object 
        hashes = file_object["hashes"]
        assert "MD5" in hashes and hashes["MD5"] == DATA["md5hash"]
        assert "SHA-256" in hashes and hashes["SHA-256"] == DATA["sha256hash"] 
        assert "parent_directory_ref" in file_object
        assert "id" in file_object and str(file_object['id']) == CYBOX_ID["file"]

        # directory
        directory_object = TestTransform.get_first_cybox_of_id_stix_2_1(result_bundle_objects, file_object["parent_directory_ref"])
        assert directory_object, 'directory object type not found'
        assert "path" in directory_object and directory_object["path"] == DATA["file_path"]
        assert "ctime" in directory_object and directory_object['ctime'] == TIMESTAMP
        assert "created" not in directory_object
        assert "mtime" in directory_object and directory_object['mtime'] == TIMESTAMP
        assert "modified" not in directory_object
        assert "atime" in directory_object and directory_object['atime'] == TIMESTAMP
        assert "accessed" not in directory_object

        # process
        process_object = TestTransform.get_first_of_type(result_bundle_objects, 'process')
        assert process_object, 'process object type not found'
        assert "name" not in process_object
        assert "pid" in process_object and process_object['pid'] == DATA['process_id']
        assert "arguments" in process_object and process_object['pid'] == DATA['process_id']
        assert "created_time" in process_object and process_object['arguments'] == DATA['process_arguments']
        assert "created" not in process_object
        assert "image_ref" in process_object
        assert "binary_ref" not in process_object
        assert "id" in directory_object and str(directory_object['id']) == CYBOX_ID["directory"]

        
