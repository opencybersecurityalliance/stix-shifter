import json
import logging
import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter.stix_translation import stix_translation
from stix_shifter_modules.splunk.entry_point import EntryPoint
from stix2validator import validate_instance
from stix_shifter_modules.splunk.stix_translation.splunk_utils import hash_type_lookup
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "splunk"
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "Splunk",
    "identity_class": "events"
}
options = {}

sample_splunk_data_x_oca = {
    "src_ip": "123.123.123.123",
    "src_mac": "12-5d-6a-52.78",
    "src_port": "56109",
    "dest_ip": "1.1.1.1",
    "dest_port": "9389",
    "user": "SYSTEM",
    "protocol": "-",
    "process_id": "912",
    "process_name": "powershell.exe",
    "process_exec": "powershell.exe",
    "process_path": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe",
    "host": "WIN01",
    "source": "XmlWinEventLog:Microsoft-Windows-Sysmon/Operational",
    "signature": "Network Connect",
    "signature_id": "3",
    "_bkt": "main~13~01865622-E388-4D42-93EA-81D878D7EE08",
    "_cd": "13:783766",
    "_indextime": "1611052433",
    "_kv": "1",
    "_raw": "<raw data>",
    "_serial": "3",
    "_si": [
        "abc",
        "main"
    ],
    "_sourcetype": "XmlWinEventLog:Microsoft-Windows-Sysmon/Operational",
    "_time": "2021-01-19T12:33:52.000+02:00"
}


class TestTransform(unittest.TestCase, object):
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
    def get_nth_of_type(itr, typ, n):
        of_type = [x for x in itr if isinstance(x, dict) and x['type'] == typ]
        return None if len(of_type) <= n else of_type[n]

    def test_common_prop(self):
        data = {"_time": "2018-08-21T15:11:55.000+00:00", "event_count": 5}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)

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
        count = 1
        time = "2018-08-21T15:11:55.000+00:00"
        file_bytes = "300"
        user = "ibm_user"
        objPath = "hkey_local_machine\\system\\bar\\foo"
        filePath = "C:\\Users\\someuser\\sample.dll"
        create_time = "2018-08-15T15:11:55.676+00:00"
        modify_time = "2018-08-15T18:10:30.456+00:00"
        file_hash = "41a26255d16d121dc525a6445144b895"
        file_name = "sample.dll"
        file_size = 25536

        data = {
            "event_count": count, "_time": time, "user": user,
            "bytes": file_bytes, "object_path": objPath, "file_path": filePath,
            "file_create_time": create_time, "file_modify_time": modify_time,
            "file_hash": file_hash, "file_size": file_size, "file_name": file_name
        }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options, callback=hash_type_lookup)

        assert(result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        # validated_result = validate_instance(observed_data)
        # assert(validated_result.is_valid == True)

        assert('objects' in observed_data)
        objects = observed_data['objects']

        # Test objects in Stix observable data model after transform
        wrk_obj = TestTransform.get_first_of_type(objects.values(), 'windows-registry-key')
        assert(wrk_obj is not None)
        assert(wrk_obj.keys() == {'type', 'key'})
        assert(wrk_obj['key'] == "hkey_local_machine\\system\\bar\\foo")

        user_obj = TestTransform.get_first_of_type(objects.values(), 'user-account')

        assert(user_obj is not None), 'user-account object type not found'
        assert(user_obj.keys() == {'type', 'account_login', 'user_id'})
        assert(user_obj['account_login'] == "ibm_user")
        assert(user_obj['user_id'] == "ibm_user")

        file_obj = TestTransform.get_first_of_type(objects.values(), 'file')

        assert(file_obj is not None), 'file object type not found'
        assert(file_obj.keys() == {'type', 'parent_directory_ref', 'created', 'modified', 'hashes', 'name', 'size'})

        assert(file_obj['created'] == "2018-08-15T15:11:55.676Z")
        assert(file_obj['modified'] == "2018-08-15T18:10:30.456Z")
        assert(file_obj['name'] == "sample.dll")
        assert(file_obj['size'] == 25536)
        assert (file_obj['hashes']['MD5'] == "41a26255d16d121dc525a6445144b895")

        dir_ref = file_obj['parent_directory_ref']
        assert(dir_ref in objects), f"parent_directory_ref with key {file_obj['parent_directory_ref']} not found"
        dir_obj = objects[dir_ref]

        assert(dir_obj is not None), 'directory object type not found'
        assert(dir_obj.keys() == {'type', 'path', 'created', 'modified'})
        assert(dir_obj['path'] == "C:\\Users\\someuser\\sample.dll")
        assert (dir_obj['created'] == "2018-08-15T15:11:55.676Z")
        assert (dir_obj['modified'] == "2018-08-15T18:10:30.456Z")

        assert(objects.keys() == set(map(str, range(0, 5))))

    def test_certificate_cim_to_stix(self):
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
            "event_count": count, "_time": time, "ssl_serial": serial,
            "ssl_version": version, "ssl_signature_algorithm": sig_algorithm,
            "ssl_issuer": issuer, "ssl_subject": subject,
            "ssl_hash": ssl_hash, "ssl_publickey_algorithm": key_algorithm
        }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)

        assert(result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        # validated_result = validate_instance(observed_data)
        # assert(validated_result.is_valid == True)

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
        assert(objects.keys() == set(map(str, range(0, 2))))

    def test_process_cim_to_stix(self):
        count = 1
        time = "2018-08-21T15:11:55.000+00:00"
        user = "test_user"
        pid = 0
        name = "test_process"
        filePath = "C:\\Users\\someuser\\sample.dll"
        create_time = "2018-08-15T15:11:55.676+00:00"
        modify_time = "2018-08-15T18:10:30.456+00:00"
        #file_hash = "aec070645fe53ee3b3763059376134f058cc337247c978add178b6ccdfb0019f"
        file_hash = "MD5=5A0B0E6F407C89916515328F318842A1,SHA256=8FC86B75926043F048971696BC7A407615C9A03D9B1BFACC54785C8903B82A91,IMPHASH=406DD24835F1447987FB607C78597252"
        file_name = "sample.dll"
        file_size = 25536

        data = {
            "event_count": count, "_time": time, "user": user,
            "process_name": name, "process_id": pid, "process_path": filePath,
            "process_hash": file_hash, "process_exec": file_name
        }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options, callback=hash_type_lookup)

        assert(result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        # validated_result = validate_instance(observed_data)
        # assert(validated_result.is_valid == True)

        assert('objects' in observed_data)
        objects = observed_data['objects']

        # Test objects in Stix observable data model after transform
        event_obj = TestTransform.get_first_of_type(objects.values(), 'x-oca-event')
        assert (event_obj is not None), 'event object type not found'
        self.assertEqual(event_obj.keys(), {'type', 'process_ref', 'created', 'user_ref', 'file_ref'})

        proc_obj = TestTransform.get_first_of_type(objects.values(), 'process')
        assert (proc_obj is not None), 'process object type not found'
        assert (proc_obj['name'] == "test_process")
        assert (proc_obj['pid'] == 0)

        user_obj = TestTransform.get_first_of_type(objects.values(), 'user-account')

        assert (user_obj is not None), 'user-account object type not found'
        assert (user_obj.keys() == {'type', 'account_login', 'user_id'})
        assert (user_obj['account_login'] == "test_user")
        assert (user_obj['user_id'] == "test_user")

        bin_ref = proc_obj['binary_ref']
        assert (bin_ref in objects), f"binary_ref with key {proc_obj['binary_ref']} not found"
        file_obj = objects[bin_ref]

        assert (file_obj is not None), 'file object type not found'
        assert (file_obj.keys() == {'type', 'parent_directory_ref', 'name', 'hashes'})
        assert (file_obj['name'] == "sample.dll")
        assert (file_obj['hashes']['MD5'] == '5A0B0E6F407C89916515328F318842A1')
        assert (file_obj['hashes']['SHA256'] == '8FC86B75926043F048971696BC7A407615C9A03D9B1BFACC54785C8903B82A91')
        assert (file_obj['hashes']['IMPHASH'] == '406DD24835F1447987FB607C78597252')
        dir_ref = file_obj['parent_directory_ref']
        assert (dir_ref in objects), f"parent_directory_ref with key {file_obj['parent_directory_ref']} not found"
        dir_obj = objects[dir_ref]

        assert(dir_obj is not None), 'directory object type not found'
        assert(dir_obj.keys() == {'type', 'path'})
        assert(dir_obj['path'] == "C:\\Users\\someuser\\sample.dll")


        assert (objects.keys() == set(map(str, range(0, 5))))

    def test_network_cim_to_stix(self):
        count = 2
        time = "2018-08-21T15:11:55.000+00:00"
        user = "ibm_user"
        dest_ip = "127.0.0.1"
        dest_port = "8090"
        src_ip = "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
        src_port = "8080"
        transport = "http"

        data = {"event_count": count, "_time": time, "user": user,
                "dest_ip": dest_ip, "dest_port": dest_port, "src_ip": src_ip,
                "src_port": src_port, "protocol": transport
                }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)

        assert (result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        # validated_result = validate_instance(observed_data)
        # assert(validated_result.is_valid == True)
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
        count = 3
        time = "2018-08-21T15:11:55.000+00:00"
        src_user = "Jane_Doe@ibm.com"
        subject = "Test Subject"
        multi = "False"

        data = {"event_count": count, "_time": time,
                "src_user": src_user, "subject": subject, "is_multipart": multi
                }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        # validated_result = validate_instance(observed_data)
        # assert(validated_result.is_valid == True)

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

    def test_custom_mapping(self):

        data_source = "{\"type\": \"identity\", \"id\": \"identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3\", \"name\": \"Splunk\", \"identity_class\": \"events\"}"
        data = "[{\"tag\":\"network\", \"src_ip\": \"127.0.0.1\"}]"

        options = {
            "mapping": {
                "cim": {
                    "to_stix": {
                        "tag_to_model": {
                            "network": [
                                "network-traffic",
                                "dst_ip",
                                "src_ip"
                            ]
                        },
                        "event_count": {
                            "key": "number_observed",
                            "cybox": False,
                            "transformer": "ToInteger"
                        },
                        "src_ip": [
                            {
                                "key": "ipv4-addr.value",
                                "object": "src_ip"
                            },
                            {
                                "key": "ipv6-addr.value",
                                "object": "src_ip"
                            },
                            {
                                "key": "network-traffic.src_ref",
                                "object": "network-traffic",
                                "references": "src_ip"
                            }
                        ]
                    }
                }
            }
        }

        translation = stix_translation.StixTranslation()
        result_bundle = translation.translate('splunk', 'results', data_source, data, options)

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        curr_obj = TestTransform.get_first_of_type(objects.values(), 'ipv4-addr')
        assert(curr_obj is not None), 'ipv4-addr object type not found'
        assert(curr_obj.keys() == {'type', 'value'})
        assert(curr_obj['value'] == "127.0.0.1")

    def test_cim_to_stix_no_tags(self):

        data = {"src_ip": "169.250.0.1", "src_port": "1220", "src_mac": "aa:bb:cc:dd:11:22",
                "dest_ip": "127.0.0.1", "dest_port": "1120", "dest_mac": "ee:dd:bb:aa:cc:11",
                "file_hash": "cf23df2207d99a74fbe169e3eba035e633b65d94",
                "user": "sname", "url": "https://wally.fireeye.com/malware_analysis/analyses?maid=1",
                "protocol": "tcp", "_bkt": "main~44~6D3E49A0-31FE-44C3-8373-C3AC6B1ABF06", "_cd": "44:12606114",
                "_indextime": "1546960685",
                "_raw": "Jan 08 2019 15:18:04 192.168.33.131 fenotify-2.alert: CEF:0|FireEye|MAS|6.2.0.74298|MO|"
                        "malware-object|4|rt=Jan 08 2019 15:18:04 Z src=169.250.0.1 dpt=1120 dst=127.0.0.1"
                        " spt=1220 smac=AA:BB:CC:DD:11:22 dmac=EE:DD:BB:AA:CC:11 cn2Label=sid cn2=111"
                        " fileHash=41a26255d16d121dc525a6445144b895 proto=tcp "
                        "request=http://qa-server.eng.fireeye.com/QE/NotificationPcaps/"
                        "58.253.68.29_80-192.168.85.128_1165-2119283109_T.exe cs3Label=osinfo"
                        " cs3=Microsoft Windows7 Professional 6.1 sp1 dvchost=wally dvc=10.2.101.101 cn1Label=vlan"
                        " cn1=0 externalId=1 cs4Label=link "
                        "cs4=https://wally.fireeye.com/malware_analysis/analyses?maid=1 cs2Label=anomaly"
                        " cs2=misc-anomaly cs1Label=sname cs1=FE_UPX;Trojan.PWS.OnlineGames",
                "_serial": "0", "_si": ["splunk3-01.internal.resilientsystems.com", "main"],
                "_sourcetype": "fe_cef_syslog", "_time": "2019-01-08T15:18:04.000+00:00", "event_count": 1
                }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options, callback=hash_type_lookup)

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        # somehow breaking the stix validation
        # validated_result = validate_instance(observed_data)
        # assert(validated_result.is_valid == True)
        assert('objects' in observed_data)
        objects = observed_data['objects']
        nt_obj = TestTransform.get_first_of_type(objects.values(), 'network-traffic')
        assert(nt_obj is not None), 'network-traffic object type not found'
        assert(nt_obj.keys() == {'type', 'src_ref', 'src_port', 'dst_ref', 'dst_port', 'protocols'})
        assert(nt_obj['src_port'] == 1220)
        assert(nt_obj['dst_port'] == 1120)
        assert(nt_obj['protocols'] == ['tcp'])

        ip_ref = nt_obj['dst_ref']
        assert(ip_ref in objects), "dst_ref with key {nt_obj['dst_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == '127.0.0.1')
        assert (isinstance(ip_obj['resolves_to_refs'], list) and isinstance(ip_obj['resolves_to_refs'][0], str))

        ip_ref = nt_obj['src_ref']
        assert(ip_ref in objects), "src_ref with key {nt_obj['src_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value', 'resolves_to_refs'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == '169.250.0.1')
        assert (isinstance(ip_obj['resolves_to_refs'], list) and isinstance(ip_obj['resolves_to_refs'][0], str))

        file_obj = TestTransform.get_first_of_type(objects.values(), 'file')
        assert (file_obj is not None), 'file object type not found'
        assert (file_obj.keys() == {'type', 'hashes'})
        assert (file_obj['hashes']['SHA-1'] == "cf23df2207d99a74fbe169e3eba035e633b65d94")
        user_obj = TestTransform.get_first_of_type(objects.values(), 'user-account')
        assert (user_obj is not None), 'user object type not found'
        assert (user_obj.keys() == {'type', 'account_login', 'user_id'})
        assert (user_obj['account_login'] == "sname")
        assert (user_obj['user_id'] == "sname")

        url_obj = TestTransform.get_first_of_type(objects.values(), 'url')
        assert (url_obj is not None), 'url object type not found'
        assert (url_obj.keys() == {'type', 'value'})
        assert (url_obj['value'] == "https://wally.fireeye.com/malware_analysis/analyses?maid=1")

        domain_obj = TestTransform.get_first_of_type(objects.values(), 'domain-name')
        assert (domain_obj is not None), 'domain object type not found'
        assert (domain_obj.keys() == {'type', 'value'})
        assert (domain_obj['value'] == "wally.fireeye.com")

        payload_obj = TestTransform.get_first_of_type(objects.values(), 'artifact')
        assert (payload_obj is not None), 'payload object type not found'
        assert (payload_obj.keys() == {'type', 'payload_bin'})
        payload = 'SmFuIDA4IDIwMTkgMTU6MTg6MDQgMTkyLjE2OC4zMy4xMzEgZmVub3RpZnktMi5hbGVydDogQ0VGOjB8RmlyZUV5ZXxNQV' \
                  'N8Ni4yLjAuNzQyOTh8TU98bWFsd2FyZS1vYmplY3R8NHxydD1KYW4gMDggMjAxOSAxNToxODowNCBaIHNyYz0xNjkuMjUw' \
                  'LjAuMSBkcHQ9MTEyMCBkc3Q9MTI3LjAuMC4xIHNwdD0xMjIwIHNtYWM9QUE6QkI6Q0M6REQ6MTE6MjIgZG1hYz1FRTpERD' \
                  'pCQjpBQTpDQzoxMSBjbjJMYWJlbD1zaWQgY24yPTExMSBmaWxlSGFzaD00MWEyNjI1NWQxNmQxMjFkYzUyNWE2NDQ1MTQ0' \
                  'Yjg5NSBwcm90bz10Y3AgcmVxdWVzdD1odHRwOi8vcWEtc2VydmVyLmVuZy5maXJlZXllLmNvbS9RRS9Ob3RpZmljYXRpb2' \
                  '5QY2Fwcy81OC4yNTMuNjguMjlfODAtMTkyLjE2OC44NS4xMjhfMTE2NS0yMTE5MjgzMTA5X1QuZXhlIGNzM0xhYmVsPW9z' \
                  'aW5mbyBjczM9TWljcm9zb2Z0IFdpbmRvd3M3IFByb2Zlc3Npb25hbCA2LjEgc3AxIGR2Y2hvc3Q9d2FsbHkgZHZjPTEwLj' \
                  'IuMTAxLjEwMSBjbjFMYWJlbD12bGFuIGNuMT0wIGV4dGVybmFsSWQ9MSBjczRMYWJlbD1saW5rIGNzND1odHRwczovL3dh' \
                  'bGx5LmZpcmVleWUuY29tL21hbHdhcmVfYW5hbHlzaXMvYW5hbHlzZXM/bWFpZD0xIGNzMkxhYmVsPWFub21hbHkgY3MyPW' \
                  '1pc2MtYW5vbWFseSBjczFMYWJlbD1zbmFtZSBjczE9RkVfVVBYO1Ryb2phbi5QV1MuT25saW5lR2FtZXM='
        assert (payload_obj['payload_bin'] == payload)

    def test_event_cim_to_stix(self):
        data = {
            "_time": "2018-08-21T15:11:55.000+00:00",
            "process_name": "powershell.exe",
            "process_exec": "powershell.exe",
            "process_id": 2,
            "process_path": "C:\\Windows\\SysWOW64\\WindowsPowerShell\\v1.0",
            "parent_process_name": "cmd.exe",
            "parent_process_id": 1,
            "answer": "1.2.3.4",
            "query": "test-domain.com",
            "host": "test_host",
            "user": "test_user"
        }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options, callback=hash_type_lookup)

        assert (result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        # validated_result = validate_instance(observed_data)
        # assert(validated_result.is_valid is True)

        assert ('objects' in observed_data)
        objects = observed_data['objects']
        object_vals = objects.values()

        # Test objects in Stix observable data model after transform

        proc_obj = TestTransform.get_nth_of_type(object_vals, 'process', 0)
        parent_proc_obj = TestTransform.get_nth_of_type(object_vals, 'process', 1)
        assert (proc_obj is not None and parent_proc_obj is not None), 'process object type not found'
        assert ('parent_ref' in proc_obj or 'parent_ref' in parent_proc_obj)
        if 'parent_ref' in parent_proc_obj:
            proc_obj, parent_proc_obj = parent_proc_obj, proc_obj
        assert (proc_obj.keys() == {'type', 'name', 'pid', 'binary_ref', 'parent_ref', 'opened_connection_refs'})
        assert (proc_obj['name'] == "powershell.exe")
        assert (proc_obj['pid'] == 2)
        assert (objects[proc_obj['parent_ref']] == parent_proc_obj)
        assert (parent_proc_obj['name'] == 'cmd.exe')
        assert (parent_proc_obj['pid'] == 1)

        user_obj = TestTransform.get_first_of_type(object_vals, 'user-account')

        assert (user_obj is not None), 'user-account object type not found'
        assert (user_obj.keys() == {'type', 'account_login', 'user_id'})
        assert (user_obj['account_login'] == "test_user")
        assert (user_obj['user_id'] == "test_user")

        bin_ref = proc_obj['binary_ref']
        assert (bin_ref in objects), f"binary_ref with key {proc_obj['binary_ref']} not found"
        file_obj = objects[bin_ref]

        assert (file_obj is not None), 'file object type not found'
        assert (file_obj.keys() == {'type', 'parent_directory_ref', 'name'})
        assert (file_obj['name'] == "powershell.exe")
        dir_ref = file_obj['parent_directory_ref']
        assert (dir_ref in objects), f"parent_directory_ref with key {file_obj['parent_directory_ref']} not found"
        dir_obj = objects[dir_ref]

        assert (dir_obj is not None), 'directory object type not found'
        assert (dir_obj.keys() == {'type', 'path'})
        assert (dir_obj['path'] == "C:\\Windows\\SysWOW64\\WindowsPowerShell\\v1.0")

        host_obj = TestTransform.get_first_of_type(object_vals, 'x-oca-asset')
        assert (host_obj is not None)
        assert (host_obj["hostname"] == "test_host")

        ip_obj = TestTransform.get_first_of_type(object_vals, 'ipv4-addr')
        assert (ip_obj is not None)
        assert (ip_obj['value'] == '1.2.3.4')

        domain_obj = TestTransform.get_first_of_type(object_vals, 'domain-name')
        assert (domain_obj is not None)
        assert (domain_obj['value'] == "test-domain.com")

        nt_obj = TestTransform.get_first_of_type(object_vals, 'network-traffic')
        assert (nt_obj is not None)
        assert (objects[nt_obj["extensions"]["dns-ext"]["question"]["domain_ref"]] == domain_obj)
        assert (objects[nt_obj["extensions"]["dns-ext"]["resolved_ip_refs"][0]] == ip_obj)

        event_obj = TestTransform.get_first_of_type(object_vals, 'x-oca-event')
        assert (event_obj is not None), 'event object type not found'
        self.assertEqual(event_obj.keys(),
                         {'user_ref', 'file_ref', 'parent_process_ref', 'network_ref', 'created', 'host_ref',
                          'domain_ref', 'type', 'process_ref'})

        for key, obj in [('process_ref', proc_obj), ('user_ref', user_obj), ('parent_process_ref', parent_proc_obj),
                         ('domain_ref', domain_obj), ('host_ref', host_obj)]:
            assert (objects[event_obj[key]] == obj)
        assert (objects.keys() == set(map(str, range(0, 10))))

    def test_x_oca_event_fields(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [sample_splunk_data_x_oca], get_module_transformers(MODULE), options,
            callback=hash_type_lookup)

        assert (result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        # validated_result = validate_instance(observed_data)
        # assert(validated_result.is_valid is True)

        assert ('objects' in observed_data)
        objects = observed_data['objects']
        object_vals = objects.values()

        x_oca_event = TestTransform.get_first_of_type(object_vals, 'x-oca-event')
        self.assertEqual(x_oca_event['module'], 'XmlWinEventLog:Microsoft-Windows-Sysmon/Operational')
        self.assertEqual(x_oca_event['action'], 'Network Connect')
        self.assertEqual(x_oca_event['code'], '3')

    def test_x_oca_event_network_ref(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [sample_splunk_data_x_oca], get_module_transformers(MODULE), options,
            callback=hash_type_lookup)

        assert (result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        # validated_result = validate_instance(observed_data)
        # assert(validated_result.is_valid is True)

        self.assertTrue('objects' in observed_data, "non-empty objects is expected")
        objects = observed_data['objects']
        object_vals = objects.values()

        x_oca_event = TestTransform.get_first_of_type(object_vals, 'x-oca-event')

        network_ref = x_oca_event.get("network_ref")
        self.assertIsNotNone(network_ref)
        network_ref_obj = objects.get(network_ref)
        self.assertIsNotNone(network_ref_obj)
        self.assertEqual(56109, network_ref_obj['src_port'])
        self.assertEqual(9389, network_ref_obj['dst_port'])

        src_ip_obj = objects[network_ref_obj['src_ref']]
        dst_ip_obj = objects[network_ref_obj['dst_ref']]

        self.assertEqual("ipv4-addr", src_ip_obj['type'])
        self.assertEqual("ipv4-addr", dst_ip_obj['type'])

        self.assertEqual(src_ip_obj['value'], '123.123.123.123')
        self.assertEqual(dst_ip_obj['value'], '1.1.1.1')

    def test_x_oca_event_file_ref(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [sample_splunk_data_x_oca], get_module_transformers(MODULE), options,
            callback=hash_type_lookup)

        assert (result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        # validated_result = validate_instance(observed_data)
        # self.assertTrue(validated_result.is_valid)

        self.assertTrue('objects' in observed_data, "non-empty objects is expected")
        objects = observed_data['objects']
        object_vals = objects.values()

        x_oca_event = TestTransform.get_first_of_type(object_vals, 'x-oca-event')

        file_ref = x_oca_event.get("file_ref")
        self.assertIsNotNone(file_ref)
        file_ref_obj = objects.get(file_ref)
        self.assertIsNotNone(file_ref_obj)
        self.assertEqual("file", file_ref_obj['type'])
        self.assertEqual("powershell.exe", file_ref_obj['name'])
        parent_directory_obj = objects[file_ref_obj['parent_directory_ref']]
        self.assertEqual("directory", parent_directory_obj['type'])
        self.assertEqual("C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe", parent_directory_obj['path'])

    def test_x_oca_asset(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [sample_splunk_data_x_oca], get_module_transformers(MODULE), options,
            callback=hash_type_lookup)

        assert (result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        # validated_result = validate_instance(observed_data)
        # assert(validated_result.is_valid is True)

        assert ('objects' in observed_data)
        objects = observed_data['objects']
        object_vals = objects.values()

        x_oca_asset = TestTransform.get_first_of_type(object_vals, 'x-oca-asset')
        self.assertEqual(x_oca_asset['hostname'], 'WIN01')


    def test_mac_addr(self):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [sample_splunk_data_x_oca], get_module_transformers(MODULE), options,
            callback=hash_type_lookup)

        assert (result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert ('objects' in observed_data)
        objects = observed_data['objects']
        object_vals = objects.values()

        mac = TestTransform.get_first_of_type(object_vals, 'mac-addr')
        self.assertEqual(mac['value'], '00:12:5d:6a:52:78')

if __name__ == '__main__':
    unittest.main()