from stix_shifter.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter.stix_translation.src.utils import transformers
from stix_shifter.stix_translation.src.modules.qradar import qradar_translator
import json
from stix_shifter.stix_translation import stix_translation
import base64

interface = qradar_translator.Translator()
map_file = open(interface.mapping_filepath).read()
# Using default mapping in modules/qradar/json/to_stix_map.json
map_data = json.loads(map_file)
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "QRadar",
    "identity_class": "events"
}
options = {}


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

    def test_common_prop(self):
        data = {"starttime": 1531169112, "endtime": 1531169254, "eventcount": 5}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)

        assert(result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert(result_bundle_identity['type'] == data_source['type'])
        assert(result_bundle_identity['id'] == data_source['id'])
        assert(result_bundle_identity['name'] == data_source['name'])
        assert(result_bundle_identity['identity_class']
               == data_source['identity_class'])

        observed_data = result_bundle_objects[1]

        assert(observed_data['id'] is not None)
        assert(observed_data['type'] == "observed-data")
        assert(observed_data['created_by_ref'] == result_bundle_identity['id'])

        assert(observed_data['number_observed'] == 5)
        assert(observed_data['created'] is not None)
        assert(observed_data['modified'] is not None)
        assert(observed_data['first_observed'] is not None)
        assert(observed_data['last_observed'] is not None)

    def test_cybox_observables(self):
        payload = "Payload"
        user_id = "someuserid2018"
        url = "https://example.com"
        source_ip = "fd80:655e:171d:30d4:fd80:655e:171d:30d4"
        destination_ip = "255.255.255.1"
        file_name = "somefile.exe"
        source_mac = "00-00-5E-00-53-00"
        destination_mac = "00-00-5A-00-55-01"
        data = {"sourceip": source_ip, "destinationip": destination_ip, "url": url, "base64_payload": payload, "username": user_id, "protocol": 'TCP',
                "sourceport": "3000", "destinationport": 2000, "filename": file_name, "domainname": url, "sourcemac": source_mac, "destinationmac": destination_mac}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        nt_object = TestTransform.get_first_of_type(objects.values(), 'network-traffic')
        assert(nt_object is not None), 'network-traffic object type not found'
        assert(nt_object.keys() ==
               {'type', 'src_port', 'dst_port', 'src_ref', 'dst_ref', 'protocols'})
        assert(nt_object['src_port'] == 3000)
        assert(nt_object['dst_port'] == 2000)
        assert(nt_object['protocols'] == ['tcp'])

        ip_ref = nt_object['dst_ref']
        assert(ip_ref in objects), f"dst_ref with key {nt_object['dst_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == destination_ip)

        ip_ref = nt_object['src_ref']
        assert(ip_ref in objects), f"src_ref with key {nt_object['src_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert(ip_obj['type'] == 'ipv6-addr')
        assert(ip_obj['value'] == source_ip)

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'url')
        assert(curr_obj is not None), 'url object type not found'
        assert(curr_obj.keys() == {'type', 'value'})
        assert(curr_obj['value'] == url)

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'artifact')
        assert(curr_obj is not None), 'artifact object type not found'
        assert(curr_obj.keys() == {'type', 'payload_bin'})
        assert(curr_obj['payload_bin'] == payload)

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'user-account')
        assert(curr_obj is not None), 'user-account object type not found'
        assert(curr_obj.keys() == {'type', 'user_id'})
        assert(curr_obj['user_id'] == user_id)

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'file')
        assert(curr_obj is not None), 'file object type not found'
        assert(curr_obj.keys() == {'type', 'name'})
        assert(curr_obj['name'] == file_name)

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'domain-name')
        assert(curr_obj is not None), 'domain-name object type not found'
        assert(curr_obj.keys() == {'type', 'value'})
        assert(curr_obj['value'] == 'example.com')

        assert(objects.keys() == set(map(str, range(0, 10))))

    def test_custom_props(self):
        data = {"logsourceid": 126, "qid": 55500004,
                "identityip": "0.0.0.0", "magnitude": 4, "logsourcename": "someLogSourceName"}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        observed_data = result_bundle['objects'][1]

        assert('x_com_ibm_ariel' in observed_data)
        custom_props = observed_data['x_com_ibm_ariel']
        assert(custom_props['identity_ip'] == data['identityip'])
        assert(custom_props['log_source_id'] == data['logsourceid'])
        assert(custom_props['qid'] == data['qid'])
        assert(custom_props['magnitude'] == data['magnitude'])
        assert(custom_props['log_source_name'] == data['logsourcename'])

    def test_custom_mapping(self):
        data_source_string = json.dumps(data_source)
        data = [{
            "custompayload": "SomeBase64Payload",
            "url": "www.example.com",
            "filename": "somefile.exe",
            "username": "someuserid2018"
        }]
        data_string = json.dumps(data)

        options = {"mapping": {
            "username": {"key": "user-account.user_id"},
            "identityip": {"key": "x_com_ibm_ariel.identity_ip", "cybox": False},
            "qidname": {"key": "x_com_ibm_ariel.qid_name", "cybox": False},
            "url": {"key": "url.value"},
            "custompayload": {"key": "artifact.payload_bin"}
        }}

        translation = stix_translation.StixTranslation()
        result = translation.translate('qradar', 'results', data_source_string, data_string, options)
        result_bundle = json.loads(result)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        file_object = TestTransform.get_first_of_type(objects.values(), 'file')
        assert(file_object is None), 'default file object type was returned even though it was not included in the custom mapping'

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'artifact')
        assert(curr_obj is not None), 'artifact object type not found'
        assert(curr_obj.keys() == {'type', 'payload_bin'})
        assert(curr_obj['payload_bin'] == "SomeBase64Payload")

    def test_unmapped_attribute_with_mapped_attribute(self):
        url = "https://example.com"
        data = {"url": url, "unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert('objects' in observed_data)
        objects = observed_data['objects']
        assert(objects != {})
        curr_obj = TestTransform.get_first_of_type(objects.values(), 'url')
        assert(curr_obj is not None), 'url object type not found'
        assert(curr_obj.keys() == {'type', 'value'})
        assert(curr_obj['value'] == url)

    def test_unmapped_attribute_alone(self):
        data = {"unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert('objects' in observed_data)
        objects = observed_data['objects']
        assert(objects == {})

    def test_file_hash_mapping_with_type(self):
        data_source_string = json.dumps(data_source)

        data = [{
            "filename": "somefile.exe",
            "sha256hash": "someSHA-256hash",
            "sha1hash": "someSHA-1hash",
            "md5hash": "someMD5hash",
            "logsourceid": 65
        }]

        data_string = json.dumps(data)

        translation = stix_translation.StixTranslation()
        result = translation.translate('qradar', 'results', data_source_string, data_string, options)
        result_bundle = json.loads(result)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        file_object = TestTransform.get_first_of_type(objects.values(), 'file')
        assert(file_object is not None), 'file object not found'
        assert('hashes' in file_object), 'file object did not contain hashes'
        assert('name' in file_object), 'file object did not contain name'
        assert('type' in file_object), 'file object did not contain type'
        assert(file_object['type'] == 'file'), 'file object had the wrong type'
        assert(file_object['name'] == 'somefile.exe'), 'file object did not contain the expected name'
        hashes = file_object['hashes']
        assert('SHA-256' in hashes), 'SHA-256 hash not included'
        assert('SHA-1' in hashes), 'SHA-1 hash not included'
        assert('MD5' in hashes), 'MD5 hash not included'
        assert(hashes['SHA-256'] == 'someSHA-256hash')
        assert(hashes['SHA-1'] == 'someSHA-1hash')
        assert(hashes['MD5'] == 'someMD5hash')

    def test_hashtype_lookup_with_matching_logsource_id(self):
        data_source_string = json.dumps(data_source)

        data = [{
            "sha256hash": "someSHA-256hash",
            "filehash": "unknownTypeHash",
            "logsourceid": 65
        }]

        data_string = json.dumps(data)

        options = {
            "hash_options": {
                "generic_name": "filehash",
                "log_source_id_map": {"2345": "sha-256", "65": "md5"}
            }
        }

        translation = stix_translation.StixTranslation()
        result = translation.translate('qradar', 'results', data_source_string, data_string, options)
        result_bundle = json.loads(result)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        file_object = TestTransform.get_first_of_type(objects.values(), 'file')
        assert(file_object is not None), 'file object not found'
        assert('hashes' in file_object), 'file object did not contain hashes'
        assert('type' in file_object), 'file object did not contain type'
        assert(file_object['type'] == 'file'), 'file object had the wrong type'
        hashes = file_object['hashes']
        assert('SHA-256' in hashes), 'SHA-256 hash not included'
        assert('MD5' in hashes), 'MD5 hash not included'
        assert('SHA-1' not in hashes), 'SHA-1 hash included'
        assert(hashes['SHA-256'] == 'someSHA-256hash')
        assert(hashes['MD5'] == 'unknownTypeHash')
        assert('UNKNOWN' not in hashes), 'UNKNOWN hash included'

    def test_hashtype_lookup_without_matching_logsource_id(self):
        data_source_string = json.dumps(data_source)

        data = [{
            "sha256hash": "someSHA-256hash",
            "filehash": "unknownTypeHash",
            "logsourceid": 123
        }]

        data_string = json.dumps(data)

        options = {
            "hash_options": {
                "generic_name": "filehash",
                "log_source_id_map": {"2345": "sha-256", "65": "md5"}
            }
        }

        translation = stix_translation.StixTranslation()
        result = translation.translate('qradar', 'results', data_source_string, data_string, options)
        result_bundle = json.loads(result)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        file_object = TestTransform.get_first_of_type(objects.values(), 'file')
        assert(file_object is not None), 'file object not found'
        assert('hashes' in file_object), 'file object did not contain hashes'
        assert('type' in file_object), 'file object did not contain type'
        assert(file_object['type'] == 'file'), 'file object had the wrong type'
        hashes = file_object['hashes']
        assert('SHA-256' in hashes), 'SHA-256 hash not included'
        assert('MD5' not in hashes), 'MD5 hash included'
        assert('SHA-1' not in hashes), 'SHA-1 hash included'
        assert('UNKNOWN' in hashes), 'UNKNOWN hash not included'
        assert(hashes['SHA-256'] == 'someSHA-256hash')
        assert(hashes['UNKNOWN'] == 'unknownTypeHash')

    def test_hashtype_lookup_without_matching_generic_hash_name(self):
        data_source_string = json.dumps(data_source)

        data = [{
            "filehash": "unknownTypeHash",
            "sha256hash": "someSHA-256hash",
            "logsourceid": 123,
            "filename": "someFile.exe"
        }]

        data_string = json.dumps(data)
        options = {
            "hash_options": {
                "generic_name": "someUnknownHashName",
                "log_source_id_map": {"2345": "sha-256", "65": "md5"}
            }
        }

        translation = stix_translation.StixTranslation()
        result = translation.translate('qradar', 'results', data_source_string, data_string, options)
        result_bundle = json.loads(result)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        file_object = TestTransform.get_first_of_type(objects.values(), 'file')
        assert(file_object is not None), 'file object not found'
        hashes = file_object['hashes']
        assert('UNKNOWN' in hashes), 'UNKNOWN hash not included'
        assert(hashes['UNKNOWN'] == 'unknownTypeHash')

    def test_hashtype_lookup_without_hash_options(self):
        data_source_string = json.dumps(data_source)

        data = [{
            "filehash": "unknownTypeHash",
            "sha256hash": "someSHA-256hash",
            "logsourceid": 123,
            "filename": "someFile.exe",
            "filepath": "C:/my/file/path"
        }]

        data_string = json.dumps(data)
        options = {}

        translation = stix_translation.StixTranslation()
        result = translation.translate('qradar', 'results', data_source_string, data_string, options)
        result_bundle = json.loads(result)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        file_object = TestTransform.get_first_of_type(objects.values(), 'file')
        assert(file_object is not None), 'file object not found'
        hashes = file_object['hashes']
        assert('UNKNOWN' in hashes), 'UNKNOWN hash not included'
        directory_object = TestTransform.get_first_of_type(objects.values(), 'directory')
        directory_object_path = directory_object.get('path', '')
        assert(directory_object_path == "C:/my/file/path")

    def test_hashtype_lookup_by_length(self):
        data_source_string = json.dumps(data_source)
        hashes = {'SHA-256': '05503abea7b8ac0a01db3cb35179242c0c1d43c7002c51e5982318244bdcaba9',
                  'SHA-1': '05503abea7b8ac0a01db3cb35179242c0c1d43c7',
                  'MD5': '05503abea7b8ac0a01db3cb35179242c',
                  'UNKNOWN': '05503abea'}
        for key, value in hashes.items():
            data = [{'filehash': value}]
            data_string = json.dumps(data)
            options = {}
            translation = stix_translation.StixTranslation()
            result = translation.translate('qradar', 'results', data_source_string, data_string, options)
            result_bundle = json.loads(result)

            result_bundle_objects = result_bundle['objects']
            observed_data = result_bundle_objects[1]
            objects = observed_data['objects']

            file_object = TestTransform.get_first_of_type(objects.values(), 'file')
            hashes = file_object['hashes']
            assert(key in hashes), "{} hash not included".format(key)
            assert(hashes[key] == value)
