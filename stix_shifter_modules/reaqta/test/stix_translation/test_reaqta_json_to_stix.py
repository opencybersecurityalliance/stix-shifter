import json
from pickle import FALSE
import unittest
from stix_shifter_modules.reaqta.entry_point import EntryPoint


def find(element, dd, default=None):
    try:
        keys = element.split('.')
        rv = dd
        for key in keys:
            rv = rv[key]
        return rv
    except Exception:
        return default

ENTRY_POINT = EntryPoint()

RESULT_FILE = open('stix_shifter_modules/reaqta/test/stix_translation/json/event_result.json', 'r').read()
DATA = json.loads(RESULT_FILE)

DATA_RECEIVED_AR_TIMESTAMP = find('receivedAt', DATA)
DATA_HAPPENED_AT_TIMESTAMP = find('happenedAt', DATA)
DATA_EVENT_ID = int(find('eventId', DATA))
DATA_EVENT_TYPE = find('payload.eventType', DATA)
DATA_LOCAL_ID = find('payload.localId', DATA)
DATA_PROCESS_GUID = find('payload.process.id', DATA)
DATA_PROCESS_PARENT_ID = find('payload.process.parentId', DATA)
DATA_PROCESS_ID_ENDPOINT_ID = find('payload.process.endpointId', DATA)
DATA_PROCESS_IMAGE_FILE = find('payload.process.program.filename', DATA)
DATA_PROCESS_IMAGE_FILE_MD5 = find('payload.process.program.md5', DATA)
DATA_PROCESS_IMAGE_FILE_SHA1 = find('payload.process.program.sha1', DATA)
DATA_PROCESS_IMAGE_FILE_SHA256 = find('payload.process.program.sha256', DATA)
DATA_PROCESS_IMAGE_FILE_SIZE = find('payload.process.program.size', DATA)
DATA_PROCESS_IMAGE_ARCH = find('payload.process.program.arch', DATA)
DATA_PROCESS_IMAGE_DIR = find('payload.process.program.path', DATA).replace('\\' + DATA_PROCESS_IMAGE_FILE, '')
DATA_PROCESS_SIGNER = find('payload.process.program.certInfo.signer', DATA)
DATA_PROCESS_ISSUER = find('payload.process.program.certInfo.issuer', DATA)
DATA_PROCESS_TRUSTED = find('payload.process.program.certInfo.trusted', DATA)
DATA_PROCESS_EXPIRED = find('payload.process.program.certInfo.expired', DATA)
DATA_PROCESS_COMMAND_LINE = find('payload.data.cmdLine', DATA)
DATA_PROCESS_PRIVILEGE_LEVEL = find('payload.process.privilegeLevel', DATA)
DATA_PROCESS_NO_GUI = find('payload.process.noGui', DATA)
DATA_PROCESS_LOGON_ID = find('payload.process.logonId', DATA)
DATA_PROCESS_USER_SID = find('payload.process.userSID', DATA)
DATA_PROCESS_USER = find('payload.process.user', DATA)
DATA_PROCESS_PPID = find('payload.process.ppid', DATA)
DATA_LOCAL_PORT = find('payload.data.localPort', DATA)
DATA_REMOTE_PORT = find('payload.data.remotePort', DATA)
DATA_LOCAL_IP = find('payload.data.localAddr', DATA)
DATA_REMOTE_IP = find('payload.data.remoteAddr', DATA)
DATA_SERVICE_NAME = find('payload.data.serviceName', DATA)
DATA_ROOT_OBJECT = find('payload.data.rootObject', DATA)
DATA_START_TYPE = find('payload.data.startType', DATA)
DATA_SERVICE_TYPE = find('payload.data.serviceType', DATA)
DATA_TECHNIQUE = find('payload.data.technique', DATA)
DATA_TACTICS = find('payload.data.tactics', DATA)
DATA_TAGS = find('payload.data.tags', DATA)
DATA_RELEVANCE = find('payload.data.relevance', DATA)
DATA_VERSION = find('payload.data.version', DATA)

STIX_2_1_OBJECT_REFS = [
    "directory--9d6f3ae4-4fb1-5eaf-a295-7ae1189befeb",
    "file--697ce471-a30e-5867-83ab-69d38fc4c07c",
    "user-account--80bb9f7c-1010-5f6f-bc9c-d862451be62c",
    "file--6463fa96-e6e4-50d6-b636-792bc7fe096e",
    "network-traffic--1447b4e4-99c4-552d-b140-07fa908504af",
    "directory--c616d2f7-3b0a-5ccb-843c-e4592f5d5c50",
    "user-account--a50c0708-1b89-55c6-92e9-6d93a80d2708",
    "url--91ba42cf-130a-58f8-8a18-7613abffd412",
    "user-account--c0152e8f-c3db-55c6-8881-7e8d8373e8a0",
    "file--0af4f45b-8970-5c87-819f-814b93e472ca",
    "user-account--4fe2a8d1-b519-5701-b521-1145606b1903",
    "directory--5c0ad0f9-38c5-56c0-a059-85994be2032a",
    "file--ffc24f98-eb84-500d-a5d5-52376ce5ffa9",
    "user-account--da9a51b3-80fa-5e94-adb9-a78bf00d9a56",
    "directory--0c5773ea-0ddb-5b4d-bef7-2c29818f0170",
    "file--ce0f32cf-1b48-59f9-8139-11e01d198bfc",
    "directory--2f2498e1-8be8-53fa-93cd-6e54220b452a",
    "file--1b887397-3edf-5eba-961c-83f62a816661",
    "file--19a3ab44-7c99-570a-918a-61d3bb96ecad",
    "ipv4-addr--a47ff5c6-efeb-5caa-b606-62198d19839d",
    "ipv4-addr--adac2d17-0bea-5ec1-8d7a-653cba4476e4"
]

DATA_SOURCE = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "Reaqta",
    "identity_class": "events"
}

class TestReaqtaResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for reaqta translate results
    """
    @staticmethod
    def get_first(itr, constraint):
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        return TestReaqtaResultsToStix.get_first(itr, lambda o: type(o) == dict and o.get('type') == typ)

    @staticmethod
    def get_first_cybox_of_type_stix_2_1(itr, type):
        for obj in itr:
            if obj["type"] ==  type:
                return obj

    @staticmethod
    def get_observed_data_objects():
        result_bundle = ENTRY_POINT.translate_results(json.dumps(DATA_SOURCE), json.dumps([DATA]))
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        return observed_data['objects']

    def test_common_prop(self):
        result_bundle = ENTRY_POINT.translate_results(json.dumps(DATA_SOURCE), json.dumps([DATA]))

        assert(result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert(result_bundle_identity['type'] == DATA_SOURCE['type'])
        assert(result_bundle_identity['id'] == DATA_SOURCE['id'])
        assert(result_bundle_identity['name'] == DATA_SOURCE['name'])
        assert(result_bundle_identity['identity_class'] == DATA_SOURCE['identity_class'])

        observed_data = result_bundle_objects[1]

        assert(observed_data['id'] is not None)
        assert(observed_data['type'] == "observed-data")
        assert(observed_data['created_by_ref'] == result_bundle_identity['id'])

        assert(observed_data['number_observed'] == 1)
        assert(observed_data['created'] is not None)
        assert(observed_data['modified'] is not None)
        assert(observed_data['first_observed'] == DATA_HAPPENED_AT_TIMESTAMP)
        assert(observed_data['last_observed'] == DATA_HAPPENED_AT_TIMESTAMP)

    def test_cybox_observables_process(self):
        objects = TestReaqtaResultsToStix.get_observed_data_objects()
        proc_obj = TestReaqtaResultsToStix.get_first_of_type(objects.values(), 'process')
        
        assert(proc_obj is not None), 'process object type not found'
        assert(proc_obj.keys() == {'type', 'extensions', 'binary_ref', 'creator_user_ref', 'pid', 'created', 'parent_ref', 'command_line'})
        
        user_ref = proc_obj['creator_user_ref']
        assert(user_ref in objects), f"creator_user_ref with key {proc_obj['creator_user_ref']} not found"
        
        binary_ref = proc_obj['binary_ref']
        assert(binary_ref in objects), f"binary_ref with key {proc_obj['binary_ref']} not found"
        
        binary = objects[binary_ref]
        assert(binary.keys() == {'type', 'parent_directory_ref', 'name', 'hashes', 'size', 'extensions'})
        assert(binary['name'] == DATA_PROCESS_IMAGE_FILE)
        assert(binary['parent_directory_ref'] in objects), f"binary.parent_directory_ref with key {binary_ref['parent_directory_ref']} not found"
        assert(objects[binary['parent_directory_ref']]['path'] == DATA_PROCESS_IMAGE_DIR)

        parent_ref = proc_obj['parent_ref']
        assert(parent_ref in objects), f"parent_ref with key {proc_obj['parent_ref']} not found"
        assert(proc_obj['command_line'] == DATA_PROCESS_COMMAND_LINE)

        extensions = find('extensions.x-reaqta-process', proc_obj)
        assert(extensions is not None), "file extensions not found"
        assert(extensions.keys() == {'privilege_level', 'no_gui', 'logon_id', 'command_line_args'})
        assert(extensions['privilege_level'] == DATA_PROCESS_PRIVILEGE_LEVEL)
        assert(extensions['no_gui'] == DATA_PROCESS_NO_GUI)
        assert(extensions['logon_id'] == DATA_PROCESS_LOGON_ID)
        assert(extensions['command_line_args'] == [])

        extensions = find('extensions.windows-process-ext', proc_obj)
        assert(extensions is not None), "file extensions not found"
        assert(extensions.keys() == {'owner_sid'})
        assert(extensions['owner_sid'] == DATA_PROCESS_USER_SID)

        extensions = find('extensions.x-process-ext', proc_obj)
        assert(extensions is not None), "process extensions not found"
        assert(extensions.keys() == {'process_uid'})
        assert(extensions['process_uid'] == DATA_PROCESS_GUID)

    def test_cybox_observables_file(self):
        objects = TestReaqtaResultsToStix.get_observed_data_objects()
        file_obj = TestReaqtaResultsToStix.get_first_of_type(objects.values(), 'file')

        assert(file_obj is not None), 'file object type not found'
        assert(file_obj.keys() == {'type', 'parent_directory_ref', 'name', 'hashes', 'size', 'extensions'})
        assert(file_obj['type'] == 'file')
        assert(file_obj['name'] == DATA_PROCESS_IMAGE_FILE)
        assert(file_obj['size'] == DATA_PROCESS_IMAGE_FILE_SIZE)
        
        parent_obj = objects[file_obj['parent_directory_ref']]
        assert(parent_obj is not None), "file parent ref not found"
        assert(parent_obj.keys() == {'type', 'path'})
        assert(parent_obj['type'] == "directory")
        assert(parent_obj['path'] == DATA_PROCESS_IMAGE_DIR)

        hashes = file_obj['hashes']
        assert(hashes.keys() == {'MD5', 'SHA-1', 'SHA-256'})
        assert(hashes['MD5'] == DATA_PROCESS_IMAGE_FILE_MD5)
        assert(hashes['SHA-1'] == DATA_PROCESS_IMAGE_FILE_SHA1)
        assert(hashes['SHA-256'] == DATA_PROCESS_IMAGE_FILE_SHA256)

        extensions = find('extensions.x-reaqta-program', file_obj)
        assert(extensions is not None), "file extensions not found"
        assert(extensions.keys() == {'arch', 'fsname'})
        assert(extensions['arch'] == DATA_PROCESS_IMAGE_ARCH)
        assert(extensions['fsname'] == DATA_PROCESS_IMAGE_FILE)

    def test_cybox_observables_network_traffic(self):
        objects = TestReaqtaResultsToStix.get_observed_data_objects()
        network_obj = TestReaqtaResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert(network_obj is not None), 'network-traffic object type not found'
        assert(network_obj.keys() == {'type', 'extensions', 'protocols', 'src_port', 'dst_port', 'src_ref', 'dst_ref'})
        assert(network_obj['type'] == 'network-traffic')
        assert(network_obj['src_port'] == DATA_LOCAL_PORT)
        assert(network_obj['dst_port'] == DATA_REMOTE_PORT)

        ip_ref = network_obj['src_ref']
        assert(ip_ref in objects), f"src_ref with key {network_obj['src_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == DATA_LOCAL_IP)

        ip_ref = network_obj['dst_ref']
        assert(ip_ref in objects), f"dst_ref with key {network_obj['dst_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == DATA_REMOTE_IP)

        extensions = find('extensions.x-reaqta-network', network_obj)
        assert(extensions is not None), "file extensions not found"
        assert(extensions.keys() == {'address_family', 'outbound'})
        assert(extensions['address_family'] == 'IPv4')
        assert(extensions['outbound'] == True)

    def test_x_oca_event(self):
        objects = TestReaqtaResultsToStix.get_observed_data_objects()
        event = TestReaqtaResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')

        assert(event['type']) == "x-oca-event"
        assert(event['code']) == DATA_EVENT_ID
        assert(event['created'] == DATA_RECEIVED_AR_TIMESTAMP)
        assert(event['category'] == DATA_EVENT_TYPE)
        assert(event['action'] == "Service Stopped")

        file_ref = event['file_ref']
        assert(file_ref in objects), f"file_ref with key {event['file_ref']} not found"
        file_obj = objects[file_ref]
        assert(file_obj.keys() == {'type', 'parent_directory_ref', 'name', 'hashes', 'size', 'extensions'})
        assert(file_obj['type'] == 'file')
        assert(file_obj['name'] == DATA_PROCESS_IMAGE_FILE)
        parent_obj = objects[file_obj['parent_directory_ref']]
        assert(parent_obj is not None), "file parent ref not found"
        assert(parent_obj.keys() == {'type', 'path'})
        assert(parent_obj['type'] == "directory")
        assert(parent_obj['path'] == DATA_PROCESS_IMAGE_DIR)

        user_ref = event['user_ref']
        assert(user_ref in objects), f"user_ref with key {event['user_ref']} not found"
        user_obj = objects[user_ref]
        assert(user_obj.keys() == {'type', 'user_id'})
        assert(user_obj['type'] == 'user-account')
        assert(user_obj['user_id'] == DATA_PROCESS_USER)

        process_ref = event['process_ref']
        assert(process_ref in objects), f"process_ref with key {event['process_ref']} not found"
        process_obj = objects[process_ref]
        assert(process_obj.keys() == {'type', 'extensions', 'binary_ref', 'creator_user_ref', 'pid', 'created', 'parent_ref', 'command_line'})
        assert(process_obj['type'] == 'process')
        assert(process_obj['command_line'] == DATA_PROCESS_COMMAND_LINE)
        binary_obj = objects[process_obj['binary_ref']]
        assert(binary_obj is not None), "process binary ref not found"
        assert(binary_obj.keys() == {'type', 'parent_directory_ref', 'name', 'hashes', 'size', 'extensions'})
        assert(binary_obj['type'] == "file")
        assert(binary_obj['name'] == DATA_PROCESS_IMAGE_FILE)
        binary_parent_dir_obj = objects[binary_obj['parent_directory_ref']]
        assert(binary_parent_dir_obj is not None), "process binary parent directory ref not found"
        assert(binary_parent_dir_obj['type'] == "directory")
        assert(binary_parent_dir_obj['path'] == DATA_PROCESS_IMAGE_DIR)

        parent_process_ref = event['parent_process_ref']
        assert(parent_process_ref in objects), f"parent_process_ref with key {event['parent_process_ref']} not found"
        parent_process_obj = objects[parent_process_ref]
        assert(parent_process_obj.keys() == {'type', 'pid','extensions'})
        assert(parent_process_obj['type'] == 'process')
        assert(parent_process_obj['pid'] == DATA_PROCESS_PPID)

        network_ref = event['network_ref']
        assert(network_ref in objects), f"network_ref with key {event['network_ref']} not found"
        network_obj = objects[network_ref]
        assert(network_obj.keys() == {'type', 'extensions', 'protocols', 'src_port', 'dst_port', 'src_ref', 'dst_ref'})
        assert(network_obj['type'] == 'network-traffic')
        assert(network_obj['src_port'] == DATA_LOCAL_PORT)
        assert(network_obj['dst_port'] == DATA_REMOTE_PORT)

        ip_ref = network_obj['src_ref']
        assert(ip_ref in objects), f"src_ref with key {network_obj['src_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == DATA_LOCAL_IP)

        ip_ref = network_obj['dst_ref']
        assert(ip_ref in objects), f"dst_ref with key {network_obj['dst_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == DATA_REMOTE_IP)

    
    def test_x_ibm_finding(self):
        objects = TestReaqtaResultsToStix.get_observed_data_objects()
        event = TestReaqtaResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')

        assert(event is not None), "x-ibm-finding not found"
        assert(event.keys() == {'type', 'extensions', 'src_ip_ref', 'dst_ip_ref'})
        assert(event['type'] == "x-ibm-finding")

        ip_ref = event['src_ip_ref']
        assert(ip_ref in objects), f"src_ip_ref with key {event['src_ip_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == DATA_LOCAL_IP)

        ip_ref = event['dst_ip_ref']
        assert(ip_ref in objects), f"dst_ip_ref with key {event['dst_ip_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == DATA_REMOTE_IP)

        extensions = find('extensions.x-reaqta-alert', event)
        assert(extensions is not None), "file extensions not found"
        assert(extensions.keys() == {'incidents', 'triggered_incidents'})
        assert(extensions['incidents'] == [])
        assert(extensions['triggered_incidents'] == [])

    def test_x_reaqta_event(self):
        objects = TestReaqtaResultsToStix.get_observed_data_objects()
        event = TestReaqtaResultsToStix.get_first_of_type(objects.values(), 'x-reaqta-event')

        assert(event is not None), "x-reaqta-event not found"
        assert(event.keys() == {'type', 'local_id', 'root_object', 'name', 'data', 'version', 'namespace_name', 'operation', 'is_local', 'queryName', 'custom_type', 'custom_name', 'relevance', 'tags', 'region_size', 'pe_type', 'return_code', 'technique', 'tactics', 'task_name', 'action_name', 'service_name', 'start_type', 'service_type'})
        assert(event['type'] == "x-reaqta-event")
        assert(event['local_id'] == DATA_LOCAL_ID)
        assert(event['technique'] == DATA_TECHNIQUE)
        assert(event['tactics'] == DATA_TACTICS)
        assert(event['tags'] == DATA_TAGS)
        assert(event['relevance'] == DATA_RELEVANCE)
        assert(event['version'] == DATA_VERSION)
        assert(event['service_name'] == DATA_SERVICE_NAME)
        assert(event['root_object'] == DATA_ROOT_OBJECT)
        assert(event['start_type'] == DATA_START_TYPE)
        assert(event['service_type'] == DATA_SERVICE_TYPE)


    def test_x509_certificate(self):
        objects = TestReaqtaResultsToStix.get_observed_data_objects()
        event = TestReaqtaResultsToStix.get_first_of_type(objects.values(), 'x509-certificate')
        
        assert(event is not None), "x509-certificate not found"
        assert(event.keys() == {'type', 'extensions', 'issuer'})
        assert(event['type'] == "x509-certificate")
        assert(event['issuer'] == DATA_PROCESS_ISSUER)

        extensions = find('extensions.x-reaqta-cert', event)
        assert(extensions is not None), "x-reaqta-cert extensions not found"
        assert(extensions.keys() == {'signer', 'trusted', 'expired'})
        assert(extensions['signer'] == DATA_PROCESS_SIGNER)
        assert(extensions['trusted'] == DATA_PROCESS_TRUSTED)
        assert(extensions['expired'] == DATA_PROCESS_EXPIRED)


    def test_stix_21_prop(self):
        result_bundle = EntryPoint(options={"stix_2.1": True}).translate_results(json.dumps(DATA_SOURCE), json.dumps([DATA]))

        assert(result_bundle['type'] == 'bundle')
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert(result_bundle_identity['type'] == DATA_SOURCE['type'])
        assert(result_bundle_identity['id'] == DATA_SOURCE['id'])
        assert(result_bundle_identity['name'] == DATA_SOURCE['name'])
        assert(result_bundle_identity['identity_class'] == DATA_SOURCE['identity_class'])

        observed_data = result_bundle_objects[1]
        assert(observed_data['id'] is not None)
        assert(observed_data['type'] == "observed-data")
        assert(observed_data['created_by_ref'] == result_bundle_identity['id'])
        assert(observed_data['number_observed'] == 1)
        assert(observed_data['created'] is not None)
        assert(observed_data['modified'] is not None)
        assert(observed_data['first_observed'] == DATA_HAPPENED_AT_TIMESTAMP)
        assert(observed_data['last_observed'] == DATA_HAPPENED_AT_TIMESTAMP)

        # Count object types
        assert(sum(obj['type'] == 'directory' for obj in result_bundle_objects) == 5)
        assert(sum(obj['type'] == 'file' for obj in result_bundle_objects) == 7)
        assert(sum(obj['type'] == 'ipv4-addr' for obj in result_bundle_objects) == 2)
        assert(sum(obj['type'] == 'network-traffic' for obj in result_bundle_objects) == 1)
        assert(sum(obj['type'] == 'process' for obj in result_bundle_objects) == 12)
        assert(sum(obj['type'] == 'url' for obj in result_bundle_objects) == 1)
        assert(sum(obj['type'] == 'user-account' for obj in result_bundle_objects) == 5)
        assert(sum(obj['type'] == 'x-ibm-finding' for obj in result_bundle_objects) == 1)
        assert(sum(obj['type'] == 'x-oca-asset' for obj in result_bundle_objects) == 3)
        assert(sum(obj['type'] == 'x-oca-event' for obj in result_bundle_objects) == 4)
        assert(sum(obj['type'] == 'x-reaqta-etw' for obj in result_bundle_objects) == 1)
        assert(sum(obj['type'] == 'x-reaqta-event' for obj in result_bundle_objects) == 1)

        # Insure fixed deterministic IDs are present
        assert(set(STIX_2_1_OBJECT_REFS).issubset(observed_data['object_refs']))

        event = TestReaqtaResultsToStix.get_first_cybox_of_type_stix_2_1(result_bundle_objects, 'x-reaqta-event')
        assert(event is not None), "x-reaqta-event not found"
        assert(event.keys() == {'type', 'id', 'spec_version', 'local_id', 'root_object', 'name', 'data', 'version', 'namespace_name', 'operation', 'is_local', 'queryName', 'custom_type', 'custom_name', 'relevance', 'tags', 'region_size', 'pe_type', 'return_code', 'technique', 'tactics', 'task_name', 'action_name', 'service_name', 'start_type', 'service_type'})
        assert(event['type'] == "x-reaqta-event")
        assert(event['local_id'] == DATA_LOCAL_ID)
        assert(event['technique'] == DATA_TECHNIQUE)
        assert(event['tactics'] == DATA_TACTICS)
        assert(event['tags'] == DATA_TAGS)
        assert(event['relevance'] == DATA_RELEVANCE)
        assert(event['version'] == DATA_VERSION)
        assert(event['service_name'] == DATA_SERVICE_NAME)
        assert(event['root_object'] == DATA_ROOT_OBJECT)
        assert(event['start_type'] == DATA_START_TYPE)
        assert(event['service_type'] == DATA_SERVICE_TYPE)

        proc_obj = TestReaqtaResultsToStix.get_first_cybox_of_type_stix_2_1(result_bundle_objects, 'process')
        assert(proc_obj is not None), 'process object type not found'
        assert(proc_obj.keys() == {'type', 'extensions', 'id', 'spec_version', 'binary_ref', 'creator_user_ref', 'pid', 'created', 'parent_ref', 'command_line'})
        
        user_ref = proc_obj['creator_user_ref']
        assert(user_ref.object_id in observed_data['object_refs']), f"creator_user_ref with key {proc_obj['creator_user_ref']} not found"
        
        binary_ref = proc_obj['binary_ref']
        assert(binary_ref.object_id in observed_data['object_refs']), f"binary_ref with key {proc_obj['binary_ref']} not found"
        
        parent_ref = proc_obj['parent_ref']
        assert(parent_ref.object_id in observed_data['object_refs']), f"parent_ref with key {proc_obj['parent_ref']} not found"
        assert(proc_obj['command_line'] == DATA_PROCESS_COMMAND_LINE)

        extensions = find('extensions.x-reaqta-process-ext', proc_obj)
        assert(extensions is not None), "file extensions not found"
        assert(extensions.keys() == {'privilege_level', 'no_gui', 'logon_id', 'command_line_args'})
        assert(extensions['privilege_level'] == DATA_PROCESS_PRIVILEGE_LEVEL)
        assert(extensions['no_gui'] == DATA_PROCESS_NO_GUI)
        assert(extensions['logon_id'] == DATA_PROCESS_LOGON_ID)
        assert(extensions['command_line_args'] == [])

        extensions = find('extensions.windows-process-ext', proc_obj)
        assert(extensions is not None), "file extensions not found"
        assert(extensions.keys() == {'owner_sid'})
        assert(extensions['owner_sid'] == DATA_PROCESS_USER_SID)

        extensions = find('extensions.x-process-ext', proc_obj)
        assert(extensions is not None), "process extensions not found"
        assert(extensions.keys() == {'process_uid'})
        assert(extensions['process_uid'] == DATA_PROCESS_GUID)
    
    def test_cybox_observables_network_traffic_inbound(self):
        DATA['payload']['data']['outbound'] = False
        objects = TestReaqtaResultsToStix.get_observed_data_objects()
        DATA['payload']['data']['outbound'] = True
        network_obj = TestReaqtaResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert(network_obj is not None), 'network-traffic object type not found'
        assert(network_obj.keys() == {'type', 'extensions', 'protocols', 'src_port', 'dst_port', 'src_ref', 'dst_ref'})
        assert(network_obj['type'] == 'network-traffic')
        assert(network_obj['src_port'] == DATA_REMOTE_PORT)
        assert(network_obj['dst_port'] == DATA_LOCAL_PORT)

        ip_ref = network_obj['src_ref']
        assert(ip_ref in objects), f"src_ref with key {network_obj['src_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == DATA_REMOTE_IP)

        ip_ref = network_obj['dst_ref']
        assert(ip_ref in objects), f"dst_ref with key {network_obj['dst_ref']} not found"
        ip_obj = objects[ip_ref]
        assert(ip_obj.keys() == {'type', 'value'})
        assert(ip_obj['type'] == 'ipv4-addr')
        assert(ip_obj['value'] == DATA_LOCAL_IP)

        extensions = find('extensions.x-reaqta-network', network_obj)
        assert(extensions is not None), "file extensions not found"
        assert(extensions.keys() == {'address_family', 'outbound'})
        assert(extensions['address_family'] == 'IPv4')
        assert(extensions['outbound'] == False)

        x_oca_asset = TestReaqtaResultsToStix.get_first_of_type(objects.values(), 'x-oca-asset')
        ip_refs =  x_oca_asset['ip_refs']
        obj_num = ip_refs[0]
        ip_obj = objects[obj_num]
        assert(ip_obj['value'] == DATA_REMOTE_IP)