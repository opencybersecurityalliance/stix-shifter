import json
import unittest
from stix_shifter_modules.reaqta.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers
from stix_shifter_utils.utils.helpers import find


MODULE = 'reaqta'
RESULTS = 'results'
TRANSFORMERS = get_module_transformers(MODULE)
entry_point = EntryPoint()
MAP_DATA = entry_point.get_results_translator().map_data

RESULT_FILE = open('stix_shifter_modules/reaqta/test/stix_translation/json/event_result.json', 'r').read()
DATA = json.loads(RESULT_FILE)

DATA_RECEIVED_AR_TIMESTAMP = find('receivedAt', DATA)
DATA_HAPPENED_AT_TIMESTAMP = find('happenedAt', DATA)
DATA_EVENT_ID = int(find('eventId', DATA))
DATA_LOCAL_ID = find('payload.localId', DATA)
DATA_PROCESS_ID = find('payload.process.id', DATA)
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


DATA_SOURCE = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "Reaqta",
    "identity_class": "events"
}
options = {}

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
    def get_observed_data_objects():
        result_bundle = entry_point.translate_results(json.dumps(DATA_SOURCE), json.dumps([DATA]))
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]

        return observed_data['objects']

    def test_common_prop(self):
        result_bundle = entry_point.translate_results(json.dumps(DATA_SOURCE), json.dumps([DATA]))

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
        assert(extensions.keys() == {'process_id', 'parent_process_id', 'process_endpoint_id', 'privilege_level', 'no_gui', 'logon_id', 'command_line_args'})
        assert(extensions['process_id'] == DATA_PROCESS_ID)
        assert(extensions['parent_process_id'] == DATA_PROCESS_PARENT_ID)
        assert(extensions['process_endpoint_id'] == DATA_PROCESS_ID_ENDPOINT_ID)
        assert(extensions['privilege_level'] == DATA_PROCESS_PRIVILEGE_LEVEL)
        assert(extensions['no_gui'] == DATA_PROCESS_NO_GUI)
        assert(extensions['logon_id'] == DATA_PROCESS_LOGON_ID)
        assert(extensions['command_line_args'] == [])

        extensions = find('extensions.windows-process-ext', proc_obj)
        assert(extensions is not None), "file extensions not found"
        assert(extensions.keys() == {'owner_sid'})
        assert(extensions['owner_sid'] == DATA_PROCESS_USER_SID)

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
        assert(network_obj.keys() == {'type', 'extensions', 'src_port', 'dst_port', 'src_ref', 'dst_ref'})
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
        assert(parent_process_obj.keys() == {'type', 'pid'})
        assert(parent_process_obj['type'] == 'process')
        assert(parent_process_obj['pid'] == DATA_PROCESS_PPID)

        network_ref = event['network_ref']
        assert(network_ref in objects), f"network_ref with key {event['network_ref']} not found"
        network_obj = objects[network_ref]
        assert(network_obj.keys() == {'type', 'extensions', 'src_port', 'dst_port', 'src_ref', 'dst_ref'})
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
        assert(event.keys() == {'type', 'extensions', 'src_ip_ref', 'dst_ip_ref', 'finding_type', 'name'})
        assert(event['type'] == "x-ibm-finding")
        assert(event['finding_type'] == "88")
        assert(event['name'] == "Service Stopped")

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
        assert(event.keys() == {'type', 'endpoint_id', 'local_id', 'technique', 'tactics', 'tags', 'relevance', 'version', 'service_name', 'root_object', 'start_type', 'service_type'})
        assert(event['type'] == "x-reaqta-event")
        assert(event['endpoint_id'] == DATA_PROCESS_ID_ENDPOINT_ID)
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

