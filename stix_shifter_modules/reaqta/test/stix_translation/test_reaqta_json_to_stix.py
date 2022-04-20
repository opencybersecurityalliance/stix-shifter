import json
import base64
import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.reaqta.entry_point import EntryPoint
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers
from stix_shifter_utils.utils.helpers import find


MODULE = 'reaqta'
RESULTS = 'results'
TRANSFORMERS = get_module_transformers(MODULE)
entry_point = EntryPoint()
MAP_DATA = entry_point.get_results_translator().map_data

RESULT_FILE = open('stix_shifter_modules/reaqta/test/stix_translation/json/result.json', 'r').read()
DATA = json.loads(RESULT_FILE)
DATA_RECEIVED_AR_TIMESTAMP = find('receivedAt', DATA)
DATA_HAPPENED_AT_TIMESTAMP = find('happenedAt', DATA)
DATA_PROCESS_IMAGE_FILE = find('payload.process.program.filename', DATA)
DATA_PROCESS_IMAGE_DIR = find('payload.process.program.path', DATA).replace('\\' + DATA_PROCESS_IMAGE_FILE, '')
DATA_PROCESS_COMMAND_LINE = find('payload.data.cmdLine', DATA)
DATA_EVENT_ID = int(find('eventId', DATA))
DATA_PROCESS_USER = find('payload.process.user', DATA)
DATA_PROCESS_PPID = find('payload.process.ppid', DATA)
DATA_LOCAL_PORT = find('payload.data.localPort', DATA)
DATA_REMOTE_PORT = find('payload.data.remotePort', DATA)
DATA_LOCAL_IP = find('payload.data.localAddr', DATA)
DATA_REMOTE_IP = find('payload.data.remoteAddr', DATA)

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
        assert ('objects' in observed_data)
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

        assert(event['type']) == "x-ibm-finding"
        # TODO
        

    def test_x_reaqta_event(self):
        objects = TestReaqtaResultsToStix.get_observed_data_objects()
        event = TestReaqtaResultsToStix.get_first_of_type(objects.values(), 'x-reaqta-event')

        assert(event['type']) == "x-reaqta-event"
        # TODO

    def test_x509_certificate(self):
        objects = TestReaqtaResultsToStix.get_observed_data_objects()
        event = TestReaqtaResultsToStix.get_first_of_type(objects.values(), 'x509-certificate')

        assert(event['type']) == "x509-certificate"
        # TODO
