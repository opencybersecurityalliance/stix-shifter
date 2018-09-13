from stix_shifter.src.modules.splunk.cim_to_stix import cim_to_stix_translator
from stix_shifter.src import transformers
from stix_shifter.src.modules.splunk import splunk_translator
from stix2validator import validate_instance
import json

interface = splunk_translator.Translator()
map_file = open(interface.mapping_filepath).read()
map_data = json.loads(map_file)
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "Splunk",
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
        data = {"_time": "2018-08-21T15:11:55.000+00:00", "event_count": 5}

        result_bundle = cim_to_stix_translator.convert_to_stix(
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


    def test_change_cim_to_stix(self):
        tag = "change"
        count = 1
        time = "2018-08-21T15:11:55.000+00:00"
        file_bytes = "300"
        user = "ibm_user"
        objPath = "hkey_local_machine\\system\\bar\\foo"
        filePath = "C:\\Users\\someuser\\sample.dll"
        create_time = "2018-08-15T15:11:55.676+00:00"
        modify_time = "2018-08-15T18:10:30.456+00:00"
        file_hash = "aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f"
        file_name = "sample.dll"
        file_size = 25536
        
        data = { 
            "tag": tag, "event_count": count, "_time": time, "user": user,
            "bytes": file_bytes, "object_path": objPath, "file_path": filePath, 
            "file_create_time": create_time, "file_modify_time": modify_time, 
            "file_hash": file_hash, "file_size": file_size, "file_name": file_name
        }

        result_bundle = cim_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)

        assert(result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        
        validated_result = validate_instance(observed_data)
        assert(validated_result.is_valid == True)

        assert('objects' in observed_data)
        objects = observed_data['objects']

        # Test objects in Stix observable data model after transform
        wrk_obj = TestTransform.get_first_of_type(objects.values(), 'windows-registry-key')
        assert(wrk_obj is not None), 'windows-registry-key object type not found'
        assert(wrk_obj.keys() == {'type', 'creator_user_ref', 'key'})
        assert(wrk_obj['key'] == "hkey_local_machine\\system\\bar\\foo")

        user_ref = wrk_obj['creator_user_ref']
        assert(user_ref in objects), f"creator_user_ref with key {wrk_obj['creator_user_ref']} not found"
        user_obj = objects[user_ref]

        assert(user_obj is not None), 'user-account object type not found'
        assert(user_obj.keys() == {'type', 'account_login', 'user_id'})
        assert(user_obj['account_login'] == "ibm_user")
        assert(user_obj['user_id'] == "ibm_user")

        file_obj = TestTransform.get_first_of_type(objects.values(), 'file')
        assert(file_obj is not None), 'file object type not found'
        assert(file_obj.keys() == {'type','parent_directory_ref','created','modified','hashes','name','size'})
        
        assert(file_obj['created'] == "2018-08-15T15:11:55.676Z")
        assert(file_obj['modified'] == "2018-08-15T18:10:30.456Z")
        assert(file_obj['name'] == "sample.dll")
        assert(file_obj['size'] == 25536)
        assert(file_obj['hashes']['SHA-256'] == "aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f")

        dir_ref = file_obj['parent_directory_ref']
        assert(dir_ref in objects), f"parent_directory_ref with key {file_obj['parent_directory_ref']} not found"
        dir_obj = objects[dir_ref]


        assert(dir_obj is not None), 'directory object type not found'
        assert(dir_obj.keys() == {'type', 'path', 'created', 'modified'})
        assert(dir_obj['path'] == "C:\\Users\\someuser\\sample.dll")
        assert(dir_obj['created'] == "2018-08-15T15:11:55.676Z")
        assert(dir_obj['modified'] == "2018-08-15T18:10:30.456Z")

        assert(objects.keys() == set(map(str, range(0, 4))))
       
       
    def test_certificate_cim_to_stix(self):
        tag = "certificate"
        count = 1
        time = "2018-08-21T15:11:55.000+00:00"
        serial = "1234"
        version = "1"
        sig_algorithm = "md5WithRSAEncryption"
        key_algorithm = "rsaEncryption"
        issuer = "C=US, ST=California, O=www.example.com, OU=new, CN=new"
        subject = "C=US, ST=Maryland, L=Baltimore, O=John Doe, OU=ExampleCorp, CN=www.example.com/emailAddress=doe@example.com"
        ssl_hash = "aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f"

        data = { 
            "tag": tag, "event_count": count, "_time": time, "ssl_serial": serial,
            "ssl_version": version, "ssl_signature_algorithm": sig_algorithm, 
            "ssl_issuer": issuer, "ssl_subject": subject, 
            "ssl_hash": ssl_hash, "ssl_publickey_algorithm": key_algorithm
        }

        result_bundle = cim_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        
        assert(result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        
        validated_result = validate_instance(observed_data)
        assert(validated_result.is_valid == True)

        assert('objects' in observed_data)
        objects = observed_data['objects']

        # Test objects in Stix observable data model after transform
        cert_obj = TestTransform.get_first_of_type(objects.values(), 'x509-certificate')
       
        assert(cert_obj is not None), 'x509-certificate object type not found'
        assert(cert_obj.keys() == {'type', 'serial_number', 'version', "signature_algorithm", "subject_public_key_algorithm", "issuer", "subject", "hashes"})
        assert(cert_obj['serial_number'] == "1234")
        assert(cert_obj['version'] == "1")
        assert(cert_obj['signature_algorithm'] == "md5WithRSAEncryption")
        assert(cert_obj['issuer'] == "C=US, ST=California, O=www.example.com, OU=new, CN=new")
        assert(cert_obj['subject'] == "C=US, ST=Maryland, L=Baltimore, O=John Doe, OU=ExampleCorp, CN=www.example.com/emailAddress=doe@example.com")
        assert(cert_obj['subject_public_key_algorithm'] == "rsaEncryption")
        assert(cert_obj['hashes']['SHA-256'] == "aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f")
        assert(objects.keys() == set(map(str, range(0, 1))))


       
    def test_process_cim_to_stix(self):
        tag = "process"
        count = 1
        time = "2018-08-21T15:11:55.000+00:00"
        user = "test_user"
        pid = 0
        name = "test_process"
        filePath = "C:\\Users\\someuser\\sample.dll"
        create_time = "2018-08-15T15:11:55.676+00:00"
        modify_time = "2018-08-15T18:10:30.456+00:00"
        file_hash = "aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f"
        file_name = "sample.dll"
        file_size = 25536
        
        data = { 
            "tag": tag, "event_count": count, "_time": time, "user": user, 
            "process_name": name, "process_id": pid, "file_path": filePath, 
            "file_create_time": create_time, "file_modify_time": modify_time, 
            "file_hash": file_hash, "file_size": file_size, "file_name": file_name
        }

        result_bundle = cim_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        
        assert(result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        
        validated_result = validate_instance(observed_data)
        assert(validated_result.is_valid == True)

        assert('objects' in observed_data)
        objects = observed_data['objects']

        # Test objects in Stix observable data model after transform
        proc_obj = TestTransform.get_first_of_type(objects.values(), 'process')
        assert(proc_obj is not None), 'process object type not found'
        assert(proc_obj.keys() == {'type', 'creator_user_ref', 'name', 'pid', 'binary_ref'})
        
        assert(proc_obj['name'] == "test_process")
        assert(proc_obj['pid'] == 0)

        user_ref = proc_obj['creator_user_ref']
        assert(user_ref in objects), f"creator_user_ref with key {proc_obj['creator_user_ref']} not found"
        user_obj = objects[user_ref]

        assert(user_obj is not None), 'user-account object type not found'
        assert(user_obj.keys() == {'type', 'account_login', 'user_id'})
        assert(user_obj['account_login'] == "test_user")
        assert(user_obj['user_id'] == "test_user")

        bin_ref = proc_obj['binary_ref']
        assert(bin_ref in objects), f"binary_ref with key {proc_obj['binary_ref']} not found"
        file_obj = objects[bin_ref]

    
        assert(file_obj is not None), 'file object type not found'
        assert(file_obj.keys() == {'type','parent_directory_ref','created','modified','hashes','name','size'})
        assert(file_obj['created'] == "2018-08-15T15:11:55.676Z")
        assert(file_obj['modified'] == "2018-08-15T18:10:30.456Z")
        assert(file_obj['name'] == "sample.dll")
        assert(file_obj['size'] == 25536)
        assert(file_obj['hashes']['SHA-256'] == "aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f")


        dir_ref = file_obj['parent_directory_ref']
        assert(dir_ref in objects), f"parent_directory_ref with key {file_obj['parent_directory_ref']} not found"
        dir_obj = objects[dir_ref]

        assert(dir_obj is not None), 'directory object type not found'
        assert(dir_obj.keys() == {'type', 'path', 'created', 'modified'})
        assert(dir_obj['path'] == "C:\\Users\\someuser\\sample.dll")
        assert(dir_obj['created'] == "2018-08-15T15:11:55.676Z")
        assert(dir_obj['modified'] == "2018-08-15T18:10:30.456Z")

        assert(objects.keys() == set(map(str, range(0, 4))))


    def test_network_cim_to_stix(self):

        tag = "network"
        count = 2
        time = "2018-08-21T15:11:55.000+00:00"
        user = "ibm_user"
        dest_ip = "127.0.0.1"
        dest_port = "8090"
        src_ip = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        src_port = "8080"
        transport = "http"

        data = {"tag": tag, "event_count": count, "_time": time, "user": user,
                "dest_ip": dest_ip, "dest_port": dest_port, "src_ip": src_ip, 
                "src_port": src_port, "transport": transport
        }

        result_bundle = cim_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        validated_result = validate_instance(observed_data)
        assert(validated_result.is_valid == True)

        assert('objects' in observed_data)
        objects = observed_data['objects']


        nt_obj = TestTransform.get_first_of_type(objects.values(), 'network-traffic')
        assert(nt_obj is not None), 'network-traffic object type not found'
        assert(nt_obj.keys() == {'type', 'src_port', 'dst_port', 'src_ref', 'dst_ref', 'protocols'})
        assert(nt_obj['src_port'] == 8080)
        assert(nt_obj['dst_port'] == 8090)
        assert(nt_obj['protocols'] == ['http'])

        ip_ref = nt_obj['dst_ref']
        assert(ip_ref in objects), f"dst_ref with key {nt_obj['dst_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == dest_ip)

        ip_ref = nt_obj['src_ref']
        assert(ip_ref in objects), f"src_ref with key {nt_obj['src_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value'})
        assert(ip_obj['type'] == 'ipv6-addr')
        assert(ip_obj['value'] == src_ip)



    def test_email_cim_to_stix(self):

        tag = "email"
        count = 3
        time = "2018-08-21T15:11:55.000+00:00"
        src_user = "Jane_Doe@ibm.com"
        subject = "Test Subject"
        multi = "False"

        data = {"tag": tag, "event_count": count, "_time": time, 
                "src_user": src_user, "subject": subject, "is_multipart": multi 
        }

        result_bundle = cim_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        validated_result = validate_instance(observed_data)
        assert(validated_result.is_valid == True)

        assert('objects' in observed_data)
        objects = observed_data['objects']


        msg_obj = TestTransform.get_first_of_type(objects.values(), 'email-message')
        assert(msg_obj is not None), 'email-message object type not found'
        assert(msg_obj.keys() == {'type', 'subject', 'sender_ref', 'from_ref', 'is_multipart'})
        assert(msg_obj['subject'] == "Test Subject")
        assert(msg_obj['is_multipart'] == False)
       

        sender_ref = msg_obj['sender_ref']
        assert(sender_ref in objects), f"sender_ref with key {msg_obj['sender_ref']} not found"
        
        addr_obj = objects[sender_ref]
        assert(addr_obj.keys() == {'type', 'value'})
        assert(addr_obj['type'] == 'email-addr')
        assert(addr_obj['value'] == src_user)

        from_ref = msg_obj['from_ref']
        assert(sender_ref in objects), f"from_ref with key {msg_obj['from_ref']} not found"
        
        addr_obj = objects[from_ref]
        assert(addr_obj.keys() == {'type', 'value'})
        assert(addr_obj['type'] == 'email-addr')
        assert(addr_obj['value'] == src_user)
        