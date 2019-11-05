from stix_shifter.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter.stix_translation.src.modules.car import car_translator
import json
import base64

interface = car_translator.Translator()
data_source = {
    "type": "identity",
    "id": "identity--56c5a276-a192-4c46-a61f-b81724c61096",
    "name": "CAR",
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

    def test_observed_data(self):
        data = {
          "first_observed": "2018-04-20T12:36:17.191Z",
          "last_observed": "2018-04-20T12:36:17.191Z",
          "number_observed": 3
        }

        result_bundle = json.loads(interface.result_translator.translate_results(
            json.dumps(data_source), json.dumps([data]), options))

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        assert(observed_data['objects'] == {})

        assert('type' in observed_data)
        assert(observed_data['type'] == 'observed-data')

        assert('first_observed' in observed_data)
        assert(observed_data['first_observed'] == data['first_observed'])

        assert('last_observed' in observed_data)
        assert(observed_data['last_observed'] == data['last_observed'])

        assert('number_observed' in observed_data)
        assert(observed_data['number_observed'] == data['number_observed'])

    def test_process(self):
        data = {
          "object": "process",
          "fields":
          {
            "pid": 4000,
            "exe": "blah.exe",
            "current_directory": "C:\\",
            "command_line": "blah.exe rofl copter",
            "user": "myuser",
            "md5_hash": "00000000000000000000000000000000",
            "sha1_hash": "1111111111111111111111111111111111111111",
            "sha256_hash": "2222222222222222222222222222222222222222222222222222222222222222",
            "parent_exe": "cmd.exe",
            "ppid": 1024,
            "sid": "S-1-1-0"
          }
        }

        result_bundle = json.loads(interface.result_translator.translate_results(
            json.dumps(data_source), json.dumps([data]), options))

        fields = data['fields']

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        process_obj = TestTransform.get_first_of_type(objects.values(), 'process')
        assert(process_obj is not None), 'process object type not found'
        assert(process_obj.keys() ==
            {'type', 'pid', 'binary_ref', 'cwd', 'command_line', 'creator_user_ref', 'parent_ref', 'extensions'})
        assert(process_obj['pid'] == fields['pid'])
        assert(process_obj['cwd'] == fields['current_directory'])
        assert(process_obj['command_line'] == fields['command_line'])
        assert(process_obj['extensions'] == {'windows-process-ext': {'owner_sid': fields['sid']}})

        binary_ref = process_obj['binary_ref']
        assert(binary_ref in objects), f"binary_ref with key {binary_ref} not found"
        binary_obj = objects[binary_ref]
        assert(binary_obj.keys() == {'type', 'name', 'hashes'})
        assert(binary_obj['type'] == 'file')
        assert(binary_obj['name'] == fields['exe'])
        assert(binary_obj['hashes'] == {'MD5': fields['md5_hash'], 'SHA1': fields['sha1_hash'], 'SHA-256': fields['sha256_hash']})

        user_ref = process_obj['creator_user_ref']
        assert(user_ref in objects), f"creator_user_ref with key {user_ref} not found"
        user_obj = objects[user_ref]
        assert(user_obj.keys() == {'type', 'account_login'})
        assert(user_obj['type'] == 'user-account')
        assert(user_obj['account_login'] == fields['user'])

        parent_ref = process_obj['parent_ref']
        assert(parent_ref in objects), f"parent_ref with key {parent_ref} not found"
        parent_obj = objects[parent_ref]
        assert(parent_obj.keys() == {'type', 'pid', 'binary_ref'})
        assert(parent_obj['type'] == 'process')
        assert(parent_obj['pid'] == fields['ppid'])

        parent_binary_ref = parent_obj['binary_ref']
        assert(parent_binary_ref in objects), f"binary_ref with key {parent_binary_ref} not found"
        parent_binary_obj = objects[parent_binary_ref]
        assert(parent_binary_obj.keys() == {'type', 'name'})
        assert(parent_binary_obj['type'] == 'file')
        assert(parent_binary_obj['name'] == fields['parent_exe'])

        assert(objects.keys() == set(map(str, range(0, 5))))

    def test_process_paths(self):
        data = {
          "object": "process",
          "fields":
          {
            "image_path": "C:\\mydir\\blah.exe",
            "parent_image_path": "C:\\Windows\\System32\\cmd.exe"
          }
        }

        result_bundle = json.loads(interface.result_translator.translate_results(
            json.dumps(data_source), json.dumps([data]), options))

        fields = data['fields']

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        def root_proc(obj):
            return (type(obj) == dict and
            obj.get('type') == 'process' and
            len(obj.keys()) == 3)

        process_obj = TestTransform.get_first(objects.values(), root_proc)
        assert(process_obj is not None), 'root process object not found'
        assert(process_obj.keys() == {'type', 'binary_ref', 'parent_ref'})

        binary_ref = process_obj['binary_ref']
        assert(binary_ref in objects), f"binary_ref with key {binary_ref} not found"
        binary_obj = objects[binary_ref]
        assert(binary_obj.keys() == {'type', 'name', 'parent_directory_ref'})
        assert(binary_obj['type'] == 'file')
        assert(binary_obj['name'] == 'blah.exe')

        directory_ref = binary_obj['parent_directory_ref']
        assert(directory_ref in objects), f"parent_directory_ref with key {directory_ref} not found"
        directory_obj = objects[directory_ref]
        assert(directory_obj.keys() == {'type', 'path'})
        assert(directory_obj['type'] == 'directory')
        assert(directory_obj['path'] == 'C:\\mydir\\')

        parent_ref = process_obj['parent_ref']
        assert(parent_ref in objects), f"parent_ref with key {parent_ref} not found"
        parent_obj = objects[parent_ref]
        assert(parent_obj.keys() == {'type', 'binary_ref'})
        assert(parent_obj['type'] == 'process')

        parent_binary_ref = parent_obj['binary_ref']
        assert(parent_binary_ref in objects), f"binary_ref with key {parent_binary_ref} not found"
        parent_binary_obj = objects[parent_binary_ref]
        assert(parent_binary_obj.keys() == {'type', 'name', 'parent_directory_ref'})
        assert(parent_binary_obj['type'] == 'file')
        assert(parent_binary_obj['name'] == 'cmd.exe')

        parent_directory_ref = parent_binary_obj['parent_directory_ref']
        assert(parent_directory_ref in objects), f"parent_directory_ref with key {parent_directory_ref} not found"
        parent_directory_obj = objects[parent_directory_ref]
        assert(parent_directory_obj.keys() == {'type', 'path'})
        assert(parent_directory_obj['type'] == 'directory')
        assert(parent_directory_obj['path'] == 'C:\\Windows\\System32\\')

        assert(objects.keys() == set(map(str, range(0, 6))))


    def test_flow(self):
        data = {
          "object": "flow",
          "fields":
          {
              "start_time": "2018-04-20T12:36:17.191Z",
              "end_time": "2018-04-20T12:36:17.191Z",
              "src_ip": "192.168.0.2",
              "dest_ip": "192.168.0.3",
              "src_port": 12345,
              "dest_port": 80,
              "protocol": "HTTP",
              "content": "GET https://www.example.com/ HTTP/1.1"
          }
        }

        result_bundle = json.loads(interface.result_translator.translate_results(
            json.dumps(data_source), json.dumps([data]), options))

        fields = data['fields']

        assert(result_bundle['type'] == 'bundle')

        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        assert('objects' in observed_data)
        objects = observed_data['objects']

        network_obj = TestTransform.get_first_of_type(objects.values(), 'network-traffic')
        assert(network_obj is not None), 'network-traffic object get_first_of_type not found'
        assert(network_obj.keys() =={'type', 'start', 'end', 'src_ref', 'dst_ref',
            'src_port', 'dst_port', 'protocols', 'src_payload_ref'})
        assert(network_obj['start'] == fields['start_time'])
        assert(network_obj['end'] == fields['end_time'])
        assert(network_obj['src_port'] == fields['src_port'])
        assert(network_obj['dst_port'] == fields['dest_port'])
        assert(network_obj['protocols'] == [fields['protocol'].lower()])

        src_ref = network_obj['src_ref']
        assert(src_ref in objects), f"src_ref with key {src_ref} not found"
        src_obj = objects[src_ref]
        assert(src_obj.keys() == {'type', 'value'})
        assert(src_obj['type'] == 'ipv4-addr')
        assert(src_obj['value'] == fields['src_ip'])

        dst_ref = network_obj['dst_ref']
        assert(dst_ref in objects), f"dst_ref with key {dst_ref} not found"
        dst_obj = objects[dst_ref]
        assert(dst_obj.keys() == {'type', 'value'})
        assert(dst_obj['type'] == 'ipv4-addr')
        assert(dst_obj['value'] == fields['dest_ip'])

        payload_ref = network_obj['src_payload_ref']
        assert(payload_ref in objects), f"src_payload_ref with key {payload_ref} not found"
        payload_obj = objects[payload_ref]
        assert(payload_obj.keys() == {'type', 'payload_bin'})
        assert(payload_obj['type'] == 'artifact')
        assert(payload_obj['payload_bin'] == base64.b64encode(fields['content'].encode('ascii')).decode('ascii'))

        assert(objects.keys() == set(map(str, range(0, 4))))
