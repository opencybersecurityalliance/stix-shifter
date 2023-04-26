import base64
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.qradar_perf_test.entry_point import EntryPoint
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = 'qradar_perf_test'
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

    @staticmethod
    def get_object_keys(objects):
        for k, v in objects.items():
            if k == 'type':
                yield v
            elif isinstance(v, dict):
                for id_val in TestTransform.get_object_keys(v):
                    yield id_val

    def test_common_prop(self):
        data = {"starttime": EPOCH_START, "endtime": EPOCH_END, "eventcount": 5}

        result_bundle = json_to_stix_translator.convert_to_stix(
            DATA_SOURCE, MAP_DATA, [data], TRANSFORMERS, options)

        assert(result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert(result_bundle_identity['type'] == DATA_SOURCE['type'])
        assert(result_bundle_identity['id'] == DATA_SOURCE['id'])
        assert(result_bundle_identity['name'] == DATA_SOURCE['name'])
        assert(result_bundle_identity['identity_class']
               == DATA_SOURCE['identity_class'])

        observed_data = result_bundle_objects[1]

        assert(observed_data['id'] is not None)
        assert(observed_data['type'] == "observed-data")
        assert(observed_data['created_by_ref'] == result_bundle_identity['id'])

        assert(observed_data['number_observed'] == 5)
        assert(observed_data['created'] is not None)
        assert(observed_data['modified'] is not None)
        assert(observed_data['first_observed'] == START_TIMESTAMP)
        assert(observed_data['last_observed'] == END_TIMESTAMP)

    def test_cybox_observables(self):
        payload = "utf payload"
        base64_payload = base64.b64encode(payload.encode('ascii')).decode('ascii')
        user_id = "someuserid2018"
        url = "https://example.com"
        domain = "test.com"
        source_ip = "fd80:655e:171d:30d4:fd80:655e:171d:30d4"
        destination_ip = "255.255.255.1"
        file_name = "somefile.exe"
        source_mac = "00-00-5E-00-53-00"
        destination_mac = "00-00-5A-00-55-01"
        process_image_dir = "C:\\example\\process\\image"
        process_image_file = "proc_img.exe"
        process_image = process_image_dir + "\\" + process_image_file
        process_parent_image_dir = "C:\\example\\process\\parent\\image"
        process_parent_image_file = "proc_parent_img.exe"
        process_parent_image = process_parent_image_dir + "\\" + process_parent_image_file
        process_command_line = "C:\\example\\executable.exe --example"
        process_parent_command_line = "C:\\example\\parent.exe --example"
        process_loaded_image = "C:\\example\\some.dll"
        
        data = {"sourceip": source_ip, "destinationip": destination_ip, "url": url, "eventpayload": payload, "username": user_id, "protocol": 'TCP',
                "sourceport": "3000", "destinationport": 2000, "filename": file_name, "domainname": domain, "sourcemac": source_mac, "destinationmac": destination_mac, 
                "Image": process_image, "ParentImage": process_parent_image, "ProcessCommandLine": process_command_line, "ParentCommandLine": process_parent_command_line, "LoadedImage": process_loaded_image }

        result_bundle = json_to_stix_translator.convert_to_stix(
            DATA_SOURCE, MAP_DATA, [data], TRANSFORMERS, options)

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
        assert (isinstance(ip_obj['resolves_to_refs'], list) and isinstance(ip_obj['resolves_to_refs'][0], str))

        ip_ref = nt_object['src_ref']
        assert(ip_ref in objects), f"src_ref with key {nt_object['src_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert(ip_obj['type'] == 'ipv6-addr')
        assert(ip_obj['value'] == source_ip)
        assert (isinstance(ip_obj['resolves_to_refs'], list) and isinstance(ip_obj['resolves_to_refs'][0], str))

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'url')
        assert(curr_obj is not None), 'url object type not found'
        assert(curr_obj.keys() == {'type', 'value'})
        assert(curr_obj['value'] == url)

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'artifact')
        assert(curr_obj is not None), 'artifact object type not found'
        assert(curr_obj.keys() == {'type', 'payload_bin'})
        assert(curr_obj['payload_bin'] == base64_payload)

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'user-account')
        assert(curr_obj is not None), 'user-account object type not found'
        assert(curr_obj.keys() == {'type', 'user_id'})
        assert(curr_obj['user_id'] == user_id)

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'file')
        assert(curr_obj is not None), 'file object type not found'
        assert(curr_obj.keys() == {'type', 'name'})
        assert(curr_obj['name'] == file_name)

        proc_obj = TestTransform.get_first_of_type(objects.values(), 'process')

        assert(proc_obj is not None), 'process object type not found'
        assert(proc_obj.keys() == {'type', 'creator_user_ref', 'binary_ref', 'parent_ref', 'command_line'})
        user_ref = proc_obj['creator_user_ref']
        assert(user_ref in objects), f"creator_user_ref with key {proc_obj['creator_user_ref']} not found"
        binary_ref = proc_obj['binary_ref']
        assert(binary_ref in objects), f"binary_ref with key {proc_obj['binary_ref']} not found"
        binary = objects[binary_ref]
        assert(binary.keys() == { 'type', 'name', 'parent_directory_ref' })
        assert(binary['name'] == process_image_file)
        assert(binary['parent_directory_ref'] in objects), f"binary.parent_directory_ref with key {binary_ref['parent_directory_ref']} not found"
        assert(objects[binary['parent_directory_ref']]['path'] == process_image_dir)

        #todo: check filename and file path and also for parent
        parent_ref = proc_obj['parent_ref']
        assert(parent_ref in objects), f"parent_ref with key {proc_obj['parent_ref']} not found"

        assert(proc_obj['command_line'] == process_command_line)

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'domain-name')
        assert(curr_obj is not None), 'domain-name object type not found'
        assert(curr_obj.keys() == {'type', 'value'})
        assert(curr_obj['value'] == 'test.com')

    def test_x_ibm_event(self):
        payload = "utf payload"
        base64_payload = base64.b64encode(payload.encode('ascii')).decode('ascii')
        user_id = "someuserid2018"
        url = "https://test.com"
        domain = "test.com"
        sourceip = "fd80:655e:171d:30d4:fd80:655e:171d:30d4"
        destination_ip = "255.255.255.1"
        filename = "somefile.exe"
        filepath = "C:\\example\\filepath"
        sourcemac = "00-00-5E-00-53-00"
        destination_mac = "00-00-5A-00-55-01"
        process_image_dir = "C:\\example\\process\\image"
        process_image_file = "proc_img.exe"
        process_image = process_image_dir + "\\" + process_image_file
        process_parent_image_dir = "C:\\example\\process\\parent\\image"
        process_parent_image_file = "proc_parent_img.exe"
        process_parent_image = process_parent_image_dir + "\\" + process_parent_image_file
        process_command_line = "C:\\example\\executable.exe --example"
        process_parent_command_line = "C:\\example\\parent.exe --example"
        process_loaded_image = "C:\\example\\some.dll"
        logsourceid = 126
        logsourcename = "WindowsAuthServer"
        logsourcetypename = "Microsoft Windows Security Event Log"
        qidname = "Process Create"
        categoryname = "Process Creation Success"
        hostname = "example host"
        high_level_category_name = "System"
        identityip = "1.2.3.4"
        username = "username"
        object_name = "HKLM\\a\\b\\c\\val"
        registry_key = "a\\b\\c"
        registry_value_name = "val"


        data = {"qidname": qidname, "categoryname": categoryname, "identityip": identityip, "identityhostname": hostname, 
                "devicetime": EPOCH_START, "logsourcetypename": logsourcetypename, "sourceip": sourceip, "sourcemac": sourcemac, 
                "url": url, "filename": filename, "filepath": filepath + "\\" + filename, "Image": process_image, "ParentImage": process_parent_image, 
                "ProcessCommandLine": process_command_line, "ParentCommandLine": process_parent_command_line, 
                "high_level_category_name": high_level_category_name, "eventpayload": payload, "logsourcename": logsourcename, "username": username,
                "UrlHost": domain, "ObjectName": object_name, "RegistryKey": registry_key, "RegistryValueName": registry_value_name }
        result_bundle = json_to_stix_translator.convert_to_stix(
            DATA_SOURCE, MAP_DATA, [data], TRANSFORMERS, options)
        observed_data = result_bundle['objects'][1]
        objects = observed_data['objects']

        event = TestTransform.get_first_of_type(objects.values(), 'x-oca-event')

        assert(event['type']) == "x-oca-event"
        assert(event['outcome'] == categoryname)
        assert(event['action'] == qidname)
        assert(event['created'] == START_TIMESTAMP)
        assert(event['provider'] == logsourcetypename)
        assert(event['category'] == [high_level_category_name])
        assert(event['agent'] == logsourcename)
        
        host_ref = event['host_ref']
        assert(host_ref in objects), f"host_ref with key {event['host_ref']} not found"
        host = objects[host_ref]
        assert(host['type'] == "x-oca-asset")
        assert(host['hostname'] == hostname)

        original_ref = event['original_ref']
        assert(original_ref in objects), f"original_ref with key {event['original_ref']} not found"
        original = objects[original_ref]
        assert(original['type'] == "artifact")
        assert(original['payload_bin'] == base64_payload)
        
        mac_refs = host['mac_refs']
        assert(mac_refs is not None), "host mac_refs not found"
        assert(len(mac_refs) == 1)
        mac_obj = objects[mac_refs[0]]
        assert(mac_obj.keys() == {'type', 'value'})
        assert(mac_obj['type'] == 'mac-addr')
        assert(mac_obj['value'] == sourcemac)

        ip_refs = host['ip_refs']
        assert(ip_refs is not None), "host ip_refs not found"
        assert(len(ip_refs) == 2)
        hostip = objects[ip_refs[0]]
        assert(hostip.keys() == {'type', 'value'})
        assert((hostip['type'] == 'ipv6-addr' and hostip['value'] == sourceip) or (hostip['type'] == 'ipv4-addr' and hostip['value'] == identityip))

        user_ref = event['user_ref']
        assert(user_ref in objects), f"user_ref with key {event['user_ref']} not found"
        user_obj = objects[user_ref]
        assert(user_obj.keys() == {'type', 'user_id'})
        assert(user_obj['type'] == 'user-account')
        assert(user_obj['user_id'] == username)

        domain_ref = event['domain_ref']
        assert(domain_ref in objects), f"domain_ref with key {event['domain_ref']} not found"
        domain_obj = objects[domain_ref]
        assert(domain_obj.keys() == {'type', 'value'})
        assert(domain_obj['type'] == 'domain-name')
        assert(domain_obj['value'] == domain)

        url_ref = event['url_ref']
        assert(url_ref in objects), f"url_ref with key {event['url_ref']} not found"
        url_obj = objects[url_ref]
        assert(url_obj.keys() == {'type', 'value'})
        assert(url_obj['type'] == 'url')
        assert(url_obj['value'] == url)

        file_ref = event['file_ref']
        assert(file_ref in objects), f"file_ref with key {event['file_ref']} not found"
        file_obj = objects[file_ref]
        assert(file_obj.keys() == {'type', 'name', 'parent_directory_ref'})
        assert(file_obj['type'] == 'file')
        assert(file_obj['name'] == filename)
        parent_obj = objects[file_obj['parent_directory_ref']]
        assert(parent_obj is not None), "file parent ref not found"
        assert(parent_obj.keys() == {'type', 'path'})
        assert(parent_obj['type'] == "directory")
        assert(parent_obj['path'] == filepath)

        process_ref = event['process_ref']
        assert(process_ref in objects), f"process_ref with key {event['process_ref']} not found"
        process_obj = objects[process_ref]
        assert(process_obj.keys() == {'type', 'binary_ref', 'parent_ref', 'command_line', 'creator_user_ref'})
        assert(process_obj['type'] == 'process')
        assert(process_obj['command_line'] == process_command_line)
        binary_obj = objects[process_obj['binary_ref']]
        assert(binary_obj is not None), "process binary ref not found"
        assert(binary_obj.keys() == {'type', 'name', 'parent_directory_ref'})
        assert(binary_obj['type'] == "file")
        assert(binary_obj['name'] == process_image_file)
        binary_parent_dir_obj = objects[binary_obj['parent_directory_ref']]
        assert(binary_parent_dir_obj is not None), "process binary parent directory ref not found"
        assert(binary_parent_dir_obj['type'] == "directory")
        assert(binary_parent_dir_obj['path'] == process_image_dir)

        process_parent_ref = process_obj['parent_ref']
        assert(process_parent_ref in objects), f"parent_ref with key {process_obj['parent_ref']} not found"
        parent_obj = objects[process_parent_ref]
        assert(parent_obj.keys() == {'type', 'binary_ref', 'command_line'})
        assert(parent_obj['type'] == "process")
        assert(parent_obj['command_line'] == process_parent_command_line)
        binary_obj = objects[parent_obj['binary_ref']]
        assert(binary_obj is not None), "process parent binary ref not found"
        assert(binary_obj.keys() == {'type', 'name', 'parent_directory_ref'})
        assert(binary_obj['type'] == "file")
        assert(binary_obj['name'] == process_parent_image_file)
        binary_parent_dir_obj = objects[binary_obj['parent_directory_ref']]
        assert(binary_parent_dir_obj is not None), "process parent binary parent directory ref not found"
        assert(binary_parent_dir_obj['type'] == "directory")
        assert(binary_parent_dir_obj['path'] == process_parent_image_dir)

        registry_ref = event['registry_ref']
        assert(registry_ref in objects), f"registry_ref with key {event['registry_ref']} not found"
        registry_obj = objects[registry_ref]
        assert(registry_obj.keys() == {'type', 'key', 'values'})
        assert(registry_obj['type'] == 'windows-registry-key')
        assert(registry_obj['key'] == "HKEY_LOCAL_MACHINE\\a\\b\\c")
        assert(registry_obj['values'] is not None)
        assert(len(registry_obj['values']) == 1)
        assert(registry_obj['values'][0].keys() == {'name'})
        assert(registry_obj['values'][0]['name'] == "val")


    def test_event_finding(self):
        data = {"logsourceid": 126, "qidname": "event name", "creeventlist": ["one", "two"], 
                "crename": "cre name", "credescription": "cre description", "identityip": "0.0.0.0", 
                "eventseverity": 4, "magnitude": 8, "devicetypename": "device type name", "devicetype": 15, 
                "rulenames": ["one", "two"], "eventcount": 25, "starttime": EPOCH_START, "endtime": EPOCH_END}
        result_bundle = json_to_stix_translator.convert_to_stix(
            DATA_SOURCE, MAP_DATA, [data], TRANSFORMERS, options)
        observed_data = result_bundle['objects'][1]
        objects = observed_data['objects']
        finding = TestTransform.get_first_of_type(objects.values(), 'x-ibm-finding')

        assert(finding['type']) == "x-ibm-finding"
        assert(finding['name'] == data['crename'])
        assert(finding['description'] == data['credescription'])
        assert(finding['severity'] == data['eventseverity'])
        assert(finding['magnitude'] == data['magnitude'])
        assert(finding['rule_names'] == data['rulenames'])
        assert(finding['event_count'] == data['eventcount'])
        assert(finding['finding_type'] == 'event')
        assert(finding['start'] == START_TIMESTAMP)
        assert(finding['end'] == END_TIMESTAMP)

        custom_object = TestTransform.get_first_of_type(objects.values(), 'x-qradar')
        assert(custom_object is not None), 'domain-name object type not found'
        assert(custom_object['device_type'] == data['devicetype'])
        assert(custom_object['cre_event_list'] == data['creeventlist'])

    def test_custom_props(self):
        data = {"logsourceid": 126, "qid": None,
                "identityip": "0.0.0.0", "logsourcename": "someLogSourceName"}

        result_bundle = json_to_stix_translator.convert_to_stix(
            DATA_SOURCE, MAP_DATA, [data], TRANSFORMERS, options)
        observed_data = result_bundle['objects'][1]
        objects = observed_data['objects']

        custom_object = TestTransform.get_first_of_type(objects.values(), 'x-qradar')
        assert(custom_object is not None), 'domain-name object type not found'
        assert(custom_object['log_source_id'] == data['logsourceid'])
        assert 'qid' not in custom_object.keys()

    def test_custom_mapping(self):
        data_source_string = DATA_SOURCE
        data = [{
            "custompayload": "SomeBase64Payload",
            "url": "www.example.com",
            "filename": "somefile.exe",
            "username": "someuserid2018"
        }]
        data_string = data

        options = {
            "mapping": {
                "to_stix_map": {
                    "username": {"key": "user-account.user_id"},
                    "identityip": {"key": "x_ibm_ariel.identity_ip"},
                    "qidname": {"key": "x_ibm_ariel.qid_name"},
                    "url": {"key": "url.value"},
                    "custompayload": {"key": "artifact.payload_bin"}
                }
            }
        }

        translation = stix_translation.StixTranslation()
        result_bundle = translation.translate(MODULE, RESULTS, data_source_string, data_string, options)

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
            DATA_SOURCE, MAP_DATA, [data], TRANSFORMERS, options)
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
            DATA_SOURCE, MAP_DATA, [data], TRANSFORMERS, options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert('objects' in observed_data)
        objects = observed_data['objects']
        assert(objects == {})

    def test_file_hash_mapping_with_type(self):
        data_source_string = DATA_SOURCE

        data = [{
            "filename": "somefile.exe",
            "sha256hash": "someSHA-256hash",
            "sha1hash": "someSHA-1hash",
            "md5hash": "someMD5hash",
            "logsourceid": 65
        }]

        data_string = data

        translation = stix_translation.StixTranslation()
        result_bundle = translation.translate(MODULE, RESULTS, data_source_string, data_string, options)

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
        data_source_string = DATA_SOURCE

        data = [{
            "sha256hash": "someSHA-256hash",
            "filehash": "unknownTypeHash",
            "logsourceid": 65
        }]

        data_string = data

        options = {
            "hash_options": {
                "generic_name": "filehash",
                "log_source_id_map": {"2345": "sha-256", "65": "md5"}
            }
        }

        translation = stix_translation.StixTranslation()
        result_bundle = translation.translate(MODULE, RESULTS, data_source_string, data_string, options)

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
        data_source_string = DATA_SOURCE

        data = [{
            "sha256hash": "someSHA-256hash",
            "filehash": "unknownTypeHash",
            "logsourceid": 123
        }]

        data_string = data

        options = {
            "hash_options": {
                "generic_name": "filehash",
                "log_source_id_map": {"2345": "sha-256", "65": "md5"}
            }
        }

        translation = stix_translation.StixTranslation()
        result_bundle = translation.translate(MODULE, RESULTS, data_source_string, data_string, options)

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
        data_source_string = DATA_SOURCE

        data = [{
            "filehash": "unknownTypeHash",
            "sha256hash": "someSHA-256hash",
            "logsourceid": 123,
            "filename": "someFile.exe"
        }]

        data_string = data
        options = {
            "hash_options": {
                "generic_name": "someUnknownHashName",
                "log_source_id_map": {"2345": "sha-256", "65": "md5"}
            }
        }

        translation = stix_translation.StixTranslation()
        result_bundle = translation.translate(MODULE, RESULTS, data_source_string, data_string, options)

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
        data_source_string = DATA_SOURCE

        data = [{
            "filehash": "unknownTypeHash",
            "sha256hash": "someSHA-256hash",
            "logsourceid": 123,
            "filename": "someFile.exe",
            "filepath": "C:/my/file/path/someFile.exe"
        }]

        data_string = data
        options = {}

        translation = stix_translation.StixTranslation()
        result_bundle = translation.translate(MODULE, RESULTS, data_source_string, data_string, options)

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
        assert directory_object_path == "C:/my/file/path"

    def test_hashtype_lookup_by_length(self):
        data_source_string = DATA_SOURCE
        hashes = {'SHA-256': '05503abea7b8ac0a01db3cb35179242c0c1d43c7002c51e5982318244bdcaba9',
                  'SHA-1': '05503abea7b8ac0a01db3cb35179242c0c1d43c7',
                  'MD5': '05503abea7b8ac0a01db3cb35179242c',
                  'UNKNOWN': '05503abea'}
        for key, value in hashes.items():
            data = [{'filehash': value}]
            data_string = data
            options = {}
            translation = stix_translation.StixTranslation()
            result_bundle = translation.translate(MODULE, RESULTS, data_source_string, data_string, options)

            result_bundle_objects = result_bundle['objects']
            observed_data = result_bundle_objects[1]
            objects = observed_data['objects']

            file_object = TestTransform.get_first_of_type(objects.values(), 'file')
            hashes = file_object['hashes']
            assert(key in hashes), "{} hash not included".format(key)
            assert(hashes[key] == value)

    def test_none_empty_values_in_results(self):
        payload = "Payload"
        user_id = "someuserid2018"
        url = None 
        source_ip = "fd80:655e:171d:30d4:fd80:655e:171d:30d4"
        destination_ip = "255.255.255.1"
        file_name = ""
        source_mac = "00-00-5E-00-53-00"
        destination_mac = "00-00-5A-00-55-01"
        data = {"sourceip": source_ip, "destinationip": destination_ip, "url": url, "base64_payload": payload, "username": user_id, "protocol": 'TCP',
                "sourceport": "3000", "destinationport": 2000, "filename": file_name, "domainname": url, "sourcemac": source_mac, "destinationmac": destination_mac}
        
        result_bundle = json_to_stix_translator.convert_to_stix(
            DATA_SOURCE, MAP_DATA, [data], TRANSFORMERS, options)
        
        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']
        
        obj_keys = []
        for key in TestTransform.get_object_keys(objects):
            obj_keys.append(key)

        # url object has None in results so url object will be skipped while creating the observables
        assert('url' not in obj_keys)
        # file object has empty string in results so url object will be skipped while creating the observables
        assert('file' not in obj_keys)

    def test_filepath_with_directory_transformer(self):
        data_source_string = DATA_SOURCE

        data = [{
            "filehash": "unknownTypeHash",
            "sha256hash": "someSHA-256hash",
            "logsourceid": 123,
            "filename": "testfile.txt",
            "filepath": "/unix/files/system/testfile.txt"
        }]

        data_string = data
        options = {}

        translation = stix_translation.StixTranslation()
        result_bundle = translation.translate(MODULE, RESULTS, data_source_string, data_string, options)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        directory_object = TestTransform.get_first_of_type(objects.values(), 'directory')
        directory_object_path = directory_object.get('path')
        assert directory_object_path == "/unix/files/system"
    
    def test_unmapped_fallback(self):
        data_source_string = DATA_SOURCE

        data = [{
            "sourceip": "127.0.0.1",
            "destinationip": "127.0.0.2",
            "sha256hash": "someSHA-256hash",
            "logsourceid": 123,
            "filename": "testfile.txt",
            "filepath": "/unix/files/system/testfile.txt",
            "unmapped1": "value1",
            "unmapped2": "value2",
            "unmapped3": None,
            "unmapped4": ""
        }]

        options = {}

        translation = stix_translation.StixTranslation()
        result_bundle = translation.translate('qradar', 'results', data_source_string, data, options)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert('first_observed' in observed_data)
        assert('last_observed' in observed_data)
        assert('created' in observed_data)
        assert('modified' in observed_data)
        assert('objects' in observed_data)
        objects = observed_data['objects']
        
        custom_objects = TestTransform.get_first_of_type(objects.values(), 'x-QRadar')

        assert(custom_objects['unmapped1'] == "value1")
        assert(custom_objects['unmapped2'] == "value2")
        assert 'unmapped3' not in custom_objects.keys()
        assert 'unmapped4' not in custom_objects.keys()