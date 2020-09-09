import unittest
import json
from stix_shifter_utils.stix_translation.src.json_to_stix.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils import transformers
from stix_shifter_modules.elastic_ecs.entry_point import EntryPoint
from stix_shifter.stix_translation import stix_translation

entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "ElasticEcs",
    "identity_class": "events"
}
options = {}

data = {
          "@timestamp": "2019-04-21T11:05:07.000Z",
          "event": {
            "action": "get",
            "dataset": "apache.access",
            "original": "10.42.42.42 - - [07/Dec/2018:11:05:07 +0100] \"GET /blog HTTP/1.1\" 200 2571 \"-\" \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36\""
          },
          "process": {
            "args": [
              "/System/Library/CoreServices/SubmitDiagInfo",
              "server-init"
            ],
            "pid": 609,
            "ppid": 1,
            "working_directory": "/",
            "executable": "/System/Library/CoreServices/SubmitDiagInfo",
            "start": "2019-04-10T11:33:57.571Z",
            "entity_id": "I2bdm9mEE1xzKvc0",
            "name": "SubmitDiagInfo"
          },
          "message": "\"GET /blog HTTP/1.1\" 200 2571",
          "service": {
            "name": "Company blog",
            "type": "apache"
          },
          "source": {
            "mac": "00:01:a7:a5:b2:b1",
            "ip": "107.0.0.48",
            "port": 49745,
            "bytes": 217,
            "packets": 3
          },
          "destination": {
            "mac": "00:9a:4c:83:dc:f1",
            "ip": "100.101.0.69",
            "port": 443,
            "packets": 11,
            "bytes": 943
          },
          "network": {
            "type": "ipv4",
            "transport": "tcp",
            "community_id": "1:kL4GhKYBNaX4O45xnu+pPYEmq70=",
            "bytes": 4488,
            "packets": 14
          },
          "url": {
            "original": "/blog"
          },
          "user": {
            "name": "-"
          },
          "file": {
              "name": "example.png",
              "directory": "/home/alice"
          },
          "dns": {
            "question": {
                "name": "officehomeblobs.blob.core.windows.net",
            },
            "resolved_ip": [
                "40.116.120.16", "1.2.3.4"
            ]
          }
}

class TestElasticEcsTransform(unittest.TestCase, object):
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestElasticEcsTransform.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    def test_common_prop(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert (result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert (result_bundle_identity['type'] == data_source['type'])
        assert (result_bundle_identity['id'] == data_source['id'])
        assert (result_bundle_identity['name'] == data_source['name'])
        assert (result_bundle_identity['identity_class']
                == data_source['identity_class'])

        observed_data = result_bundle_objects[1]

        assert (observed_data['id'] is not None)
        assert (observed_data['type'] == "observed-data")
        assert (observed_data['created_by_ref'] == result_bundle_identity['id'])

    def test_custom_mapping(self):
        data_source_string = json.dumps(data_source)
        data = [{
            "custompayload": "SomeBase64Payload",
            "url": "www.example.com",
            "filename": "somefile.exe",
            "username": "someuserid2018"
        }]
        data_string = json.dumps(data)

        options = {
            "mapping": {
                "default": {
                    "to_stix": {
                        "username": {"key": "user-account.user_id"},
                        "url": {"key": "url.value"},
                        "custompayload": {"key": "artifact.payload_bin"}
                    }
                }
            }
        }

        translation = stix_translation.StixTranslation()
        result_bundle = translation.translate('elastic_ecs', 'results', data_source_string, data_string, options)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        file_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'file')
        assert(file_object is None), 'default file object type was returned even though it was not included in the custom mapping'

        curr_obj = TestElasticEcsTransform.get_first_of_type(objects.values(), 'artifact')
        #TODO fix test translation.translate: qradar-> elastic_ecs in line 132
        # >> results: {
        #     "type": "bundle",
        #     "id": "bundle--c7650e4e-b6f7-430a-b9d1-1a501f394b5a",
        #     "spec_version": "2.0",
        #     "objects": [
        #         {
        #             "type": "identity",
        #             "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
        #             "name": "ElasticEcs",
        #             "identity_class": "events"
        #         },
        #         {
        #             "id": "observed-data--92592394-f272-469f-b8c9-45b9795dd71e",
        #             "type": "observed-data",
        #             "created_by_ref": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
        #             "created": "2020-04-19T20:06:41.756Z",
        #             "modified": "2020-04-19T20:06:41.756Z",
        #             "objects": {},
        #             "number_observed": 1
        #         }
        #     ]
        # }
        # assert(curr_obj is not None), 'artifact object type not found'
        # assert(curr_obj.keys() == {'type', 'payload_bin'})
        # assert(curr_obj['payload_bin'] == "SomeBase64Payload")


    def test_network_traffic_prop(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        nt_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'network-traffic')
        assert (nt_object is not None), 'network-traffic object type not found'
        assert (nt_object.keys() ==
                {'type', 'src_port', 'src_byte_count', 'src_packets', 'dst_port', 'dst_byte_count', 'dst_packets', 'src_ref', 'dst_ref', 'protocols'})
        assert (nt_object['type'] == 'network-traffic')
        assert (nt_object['src_port'] == 49745)
        assert (nt_object['dst_port'] == 443)
        assert (nt_object['protocols'] == ['ipv4', 'tcp'])

        ip_ref = nt_object['dst_ref']
        assert (ip_ref in objects), f"dst_ref with key {nt_object['dst_ref']} not found"
        ip_obj = objects[ip_ref]
        assert (ip_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert (ip_obj['type'] == 'ipv4-addr')
        assert (ip_obj['value'] == '100.101.0.69')
        assert (isinstance(ip_obj['resolves_to_refs'], list) and isinstance(ip_obj['resolves_to_refs'][0], str))

        ip_ref = nt_object['src_ref']
        assert (ip_ref in objects), f"src_ref with key {nt_object['src_ref']} not found"
        ip_obj = objects[ip_ref]
        assert (ip_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert (ip_obj['type'] == 'ipv4-addr')
        assert (ip_obj['value'] == '107.0.0.48')
        assert (isinstance(ip_obj['resolves_to_refs'], list) and isinstance(ip_obj['resolves_to_refs'][0], str))


    def test_process_prop(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        proc_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'process')
        assert (proc_object is not None), 'process object type not found'
        assert (proc_object.keys() ==
                {'type', 'pid', 'name', 'created', 'creator_user_ref', 'binary_ref'})
        assert (proc_object['type'] == 'process')
        assert (proc_object['pid'] == 609)
        assert (proc_object['created'] == '2019-04-10T11:33:57.571Z')

        creator_user_ref = proc_object['creator_user_ref']
        assert (creator_user_ref in objects), f"dst_ref with key {proc_object['creator_user_ref']} not found"
        creator_user_ref_obj = objects[creator_user_ref]
        assert (creator_user_ref_obj.keys() == {'type', 'user_id'})
        assert (creator_user_ref_obj['type'] == 'user-account')
        assert (creator_user_ref_obj['user_id'] == '-')

    def test_artifact_prop(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        artifact_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'artifact')
        assert (artifact_object is not None), 'artifact object type not found'
        assert (artifact_object.keys() ==
                {'type', 'payload_bin'})
        assert (artifact_object['type'] == 'artifact')
        assert (artifact_object['payload_bin'] == 'MTAuNDIuNDIuNDIgLSAtIFswNy9EZWMvMjAxODoxMTowNTowNyArMDEwMF0gIkdFVCAvYmxvZyBIVFRQLzEuMSIgMjAwIDI1NzEgIi0iICJNb3ppbGxhLzUuMCAoTWFjaW50b3NoOyBJbnRlbCBNYWMgT1MgWCAxMF8xNF8wKSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNzAuMC4zNTM4LjEwMiBTYWZhcmkvNTM3LjM2Ig==')

    def test_url_prop(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        url_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'url')
        assert (url_object is not None), 'url object type not found'
        assert (url_object.keys() ==
                {'type', 'value'})
        assert (url_object['type'] == 'url')
        assert (url_object['value'] == '/blog')

    def test_file_prop(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']

        file_object = TestElasticEcsTransform.get_first_of_type(objects.values(), 'file')
        assert (file_object is not None), 'file object type not found'
        assert (file_object.keys() ==
                {'type', 'name', 'parent_directory_ref'})
        assert (file_object['type'] == 'file')
        assert (file_object['name'] == 'example.png')

    def test_unmapped_attribute_with_mapped_attribute(self):
        message = "\"GET /blog HTTP/1.1\" 200 2571"
        data = {"message": message, "unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert('objects' in observed_data)
        objects = observed_data['objects']
        assert(objects == {})
        curr_obj = TestElasticEcsTransform.get_first_of_type(objects.values(), 'message')
        assert(curr_obj is None), 'url object type not found'


    def test_unmapped_attribute_alone(self):
        data = {"unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert('objects' in observed_data)
        objects = observed_data['objects']
        assert(objects == {})
    
    def test_unwrap_flag_in_mapping(self):        
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        
        assert ('objects' in observed_data)
        objects = observed_data['objects']

        custom_dns_obj = TestElasticEcsTransform.get_first_of_type(objects.values(), 'x-ecs-dns')
        assert (isinstance(custom_dns_obj['resolved_ip_refs'], list) and isinstance(custom_dns_obj['resolved_ip_refs'][0], str))

        assert objects[custom_dns_obj['resolved_ip_refs'][0]].get('value') == "40.116.120.16"
        assert objects[custom_dns_obj['resolved_ip_refs'][1]].get('value') == "1.2.3.4"