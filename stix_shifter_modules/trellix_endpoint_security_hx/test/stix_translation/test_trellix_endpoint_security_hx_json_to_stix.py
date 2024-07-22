""" test script to perform unit test case for trellix_endpoint_security_hx translate results """
import unittest
from stix_shifter_modules.trellix_endpoint_security_hx.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "trellix_endpoint_security_hx"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "trellix_endpoint_security_hx",
    "identity_class": "events"
}
options = {}

trellix_sample_response = {
    "Process Name": "svchost.exe",
    "Process ID": "3096",
    "Username": "NT AUTHORITY\\SYSTEM",
    "Remote IP Address": "111.111.111.111",
    "IP Address": "111.111.111.111",
    "Port": "80",
    "Local Port": "12345",
    "Remote Port": "80",
    "DNS Hostname": "download.windowsupdate.com",
    "URL": "/c/msdownload/update/others.cab",
    "HTTP Header": {
        "User-Agent": "Windows-Update-Agent/10.0 Client-Protocol/2.51",
        "Host": "download.windowsupdate.com"
    },
    "HTTP Method": "GET",
    "Timestamp - Event": "2024-03-07T09:09:10.391Z",
    "Timestamp - Accessed": "2024-03-07T09:09:10.391Z",
    "Timestamp - Modified": "2024-03-07T09:09:10.391Z",
    "Host ID": "TCJ",
    "Hostname": "EC21",
    "Event Type": "URL Event",
    "Host Set": "test_host_set1",
    "Port Protocol": "http",
    "File Name": "svchost.exe"
}


class TestTrellixEndpointSecurityHxResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for trellix endpoint security HX translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """
        return the obj in the itr if constraint is true
        """
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        """
        to check whether the object belongs to respective stix object
        """
        return TestTrellixEndpointSecurityHxResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get(
            'type') == typ)

    @staticmethod
    def get_observed_data_objects(data):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        return observed_data['objects']

    def test_ipv4_addr_json_to_stix(self):
        """
        to test ipv4-addr stix object properties
        """
        objects = TestTrellixEndpointSecurityHxResultsToStix.get_observed_data_objects(trellix_sample_response)
        ipv4_obj = TestTrellixEndpointSecurityHxResultsToStix.get_first_of_type(objects.values(), 'ipv4-addr')
        assert (ipv4_obj.keys() == {'type', 'value'})
        assert ipv4_obj is not None
        assert ipv4_obj['type'] == 'ipv4-addr'
        assert ipv4_obj['value'] == '111.111.111.111'

    def test_network_traffic_json_to_stix(self):
        """
        to test network_traffic stix object properties
        """
        objects = TestTrellixEndpointSecurityHxResultsToStix.get_observed_data_objects(trellix_sample_response)
        network_traffic_obj = TestTrellixEndpointSecurityHxResultsToStix.get_first_of_type(objects.values(),
                                                                                           'network-traffic')
        assert (network_traffic_obj.keys() == {'type', 'dst_ref', 'src_port', 'dst_port', 'extensions', 'protocols'})
        assert network_traffic_obj is not None
        assert network_traffic_obj['type'] == 'network-traffic'
        assert network_traffic_obj['src_port'] == 12345
        assert network_traffic_obj['dst_port'] == 80
        dst_ref = network_traffic_obj['dst_ref']
        assert (dst_ref in objects), f"dst_ref with key {network_traffic_obj['dst_ref']} " \
                                     f"not found"
        assert (network_traffic_obj['extensions']['http-request-ext']['request_value'] ==
                '/c/msdownload/update/others.cab')
        assert (network_traffic_obj['extensions']['http-request-ext']['request_header']['User-Agent'] ==
                'Windows-Update-Agent/10.0 Client-Protocol/2.51')
        assert network_traffic_obj['extensions']['http-request-ext']['request_method'] == "GET"
        assert network_traffic_obj['protocols'] == ["http"]

    def test_process_json_to_stix(self):
        """
        to test process stix object properties
        """
        process_response = {
            "File Name": "chrome.exe",
            "File Full Path": "C:\\Google\\Application\\chrome.exe",
            "Process Name": "chrome.exe",
            "Parent Process Name": "explorer.exe",
            "Parent Process Path": "\\Device\\explorer.exe",
            "Process Event Type": "running",
            "Process ID": "2460",
            "Username": "user1",
            "Timestamp - Event": "2024-01-25T14:40:20.105Z",
            "Timestamp - Modified": "2024-01-25T14:40:20.105Z",
            "Timestamp - Accessed": "2024-01-25T14:40:20.105Z",
            "Host ID": "hostid11",
            "Hostname": "ec21",
            "Event Type": "Process Event",
            "Host Set": "test_host_set1"
        }
        objects = TestTrellixEndpointSecurityHxResultsToStix.get_observed_data_objects(process_response)
        process_obj = TestTrellixEndpointSecurityHxResultsToStix.get_first_of_type(objects.values(),
                                                                                   'process')
        assert (process_obj.keys() == {'type', 'name', 'pid', 'creator_user_ref', 'parent_ref', 'binary_ref',
                                       'x_event_type'})
        assert process_obj is not None
        assert process_obj['type'] == 'process'
        assert process_obj['name'] == 'chrome.exe'
        assert process_obj['pid'] == 2460
        creator_user_ref = process_obj['creator_user_ref']
        assert (creator_user_ref in objects), f"creator_user_ref with key {process_obj['creator_user_ref']} " \
                                              f"not found"
        parent_ref = process_obj['parent_ref']
        assert (parent_ref in objects), f"parent_ref with key {process_obj['parent_ref']} not found"
        parent_obj = objects[parent_ref]
        assert parent_obj['type'] == 'process'
        assert parent_obj['name'] == 'explorer.exe'
        assert parent_obj['cwd'] == "\\Device"

    def test_file_json_to_stix(self):
        """
        to test file stix object properties
        """
        data = {
            "Process Name": "msedge.exe",
            "Process ID": "5692",
            "Username": "user-admin",
            "Timestamp - Event": "2024-05-30T08:44:06.312Z",
            "Timestamp - Modified": "2024-05-30T08:44:06.312Z",
            "Host ID": "xfR",
            "Hostname": "EC2-HCF",
            "Event Type": "File Write Event",
            "Host Set": "test_host_set1",
            "Write Event File Name": "LOG",
            "Write Event File Full Path": "C:\\Users\\indexeddb.leveldb\\LOG",
            "Write Event File Text Written": "2024/05/30-08:44:06.310 1728 Reusing MANIFEST C:\\Users\\Administr",
            "Write Event File Bytes Written": "609",
            "Write Event File MD5 Hash": "010101010010101010010101010101010",
            "Write Event Size in bytes": "392",
            "File Name": "msedge.exe"
        }
        objects = TestTrellixEndpointSecurityHxResultsToStix.get_observed_data_objects(data)
        file_obj = TestTrellixEndpointSecurityHxResultsToStix.get_first_of_type(objects.values(),
                                                                                'file')
        assert (file_obj.keys() == {'type', 'name', 'x_path', 'parent_directory_ref', 'content_ref',
                                    'x_bytes_written', 'hashes', 'size'})
        assert file_obj is not None
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'LOG'
        assert file_obj['x_path'] == 'C:\\Users\\indexeddb.leveldb\\LOG'
        assert file_obj['size'] == 392
        directory_ref = file_obj['parent_directory_ref']
        assert (directory_ref in objects), f"parent_ref with key {file_obj['parent_directory_ref']} not found"
        dir_obj = objects[directory_ref]
        assert dir_obj['type'] == 'directory'
        assert dir_obj['path'] == 'C:\\Users\\indexeddb.leveldb'
        content_ref = file_obj['content_ref']
        assert (content_ref in objects), f"parent_ref with key {file_obj['content_ref']} not found"
        content_obj = objects[content_ref]
        assert content_obj['type'] == 'artifact'

        event_obj = TestTrellixEndpointSecurityHxResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert('file_ref' in event_obj.keys())

    def test_windows_registry_key_json_to_stix(self):
        """
        to test windows-registry-key stix object properties
        """
        data = {
            "Process Name": "spoolsv.exe",
            "Process ID": "2600",
            "Username": "NT AUTHORITY\\SYSTEM",
            "Registry Key Full Path": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows",
            "Registry Key Values": [{'name': 'ChangeID', 'data': '....', 'data_type': 'REG_DWORD'}],
            "Timestamp - Event": "2024-02-27T15:30:52.926Z",
            "Timestamp - Modified": "2024-02-27T15:30:52.926Z"
        }
        objects = TestTrellixEndpointSecurityHxResultsToStix.get_observed_data_objects(data)
        windows_registry_key_obj = TestTrellixEndpointSecurityHxResultsToStix.get_first_of_type(objects.values(),
                                                                                                'windows'
                                                                                                '-registry-key')
        assert (windows_registry_key_obj.keys() == {'type', 'key', 'values'})
        assert windows_registry_key_obj is not None
        assert windows_registry_key_obj['type'] == 'windows-registry-key'
        assert windows_registry_key_obj['key'] == 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows'
        assert windows_registry_key_obj['values'] == [{'name': 'ChangeID', 'data': '....', 'data_type': 'REG_DWORD'}]

    def test_domain_json_to_stix(self):
        """
        to test domain name stix object properties
        """
        objects = TestTrellixEndpointSecurityHxResultsToStix.get_observed_data_objects(trellix_sample_response)
        domain_obj = TestTrellixEndpointSecurityHxResultsToStix.get_first_of_type(objects.values(), 'domain-name')
        assert (domain_obj.keys() == {'type', 'value'})
        assert domain_obj is not None
        assert domain_obj['type'] == 'domain-name'
        assert domain_obj['value'] == 'download.windowsupdate.com'

    def test_user_account_json_to_stix(self):
        """
        to test user account stix object properties
        """
        objects = TestTrellixEndpointSecurityHxResultsToStix.get_observed_data_objects(trellix_sample_response)
        user_obj = TestTrellixEndpointSecurityHxResultsToStix.get_first_of_type(objects.values(), 'user-account')
        assert (user_obj.keys() == {'type', 'user_id'})
        assert user_obj is not None
        assert user_obj['type'] == 'user-account'
        assert user_obj['user_id'] == 'NT AUTHORITY\\SYSTEM'

    def test_asset_json_to_stix(self):
        """
        to test x-oca-asset stix object properties
        """
        objects = TestTrellixEndpointSecurityHxResultsToStix.get_observed_data_objects(trellix_sample_response)
        asset_obj = TestTrellixEndpointSecurityHxResultsToStix.get_first_of_type(objects.values(), 'x-oca-asset')
        assert (asset_obj.keys() == {'type', 'device_id', 'hostname', 'x_host_set'})
        assert asset_obj is not None
        assert asset_obj['type'] == 'x-oca-asset'
        assert asset_obj['device_id'] == 'TCJ'
        assert asset_obj['x_host_set'] == "test_host_set1"

    def test_oca_event_json_to_stix(self):
        """
        to test x-oca-event stix object properties
        """
        objects = TestTrellixEndpointSecurityHxResultsToStix.get_observed_data_objects(trellix_sample_response)
        event_obj = TestTrellixEndpointSecurityHxResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert (event_obj.keys() == {'type', 'process_ref', 'user_ref', 'ip_refs', 'network_ref', 'domain_ref',
                                     'created', 'x_accessed_time', 'host_ref', 'action', 'modified'})
        assert event_obj is not None
        assert event_obj['type'] == 'x-oca-event'
        assert event_obj['action'] == 'URL Event'

        process_ref = event_obj['process_ref']
        assert (process_ref in objects), f"process_ref with key {event_obj['process_ref']} not found"
        process_obj = objects[process_ref]
        assert process_obj['type'] == 'process'

        user_ref = event_obj['user_ref']
        assert (user_ref in objects), f"user_ref with key {event_obj['user_ref']} not found"
        user_obj = objects[user_ref]
        assert user_obj['type'] == 'user-account'

        network_ref = event_obj['network_ref']
        assert (network_ref in objects), f"network_ref with key {event_obj['network_ref']} not found"
        network_obj = objects[network_ref]
        assert network_obj['type'] == 'network-traffic'

        domain_ref = event_obj['domain_ref']
        assert (domain_ref in objects), f"domain_ref with key {event_obj['domain_ref']} not found"
        domain_obj = objects[domain_ref]
        assert domain_obj['type'] == 'domain-name'

        host_ref = event_obj['host_ref']
        assert (host_ref in objects), f"host_ref with key {event_obj['host_ref']} not found"
        host_obj = objects[host_ref]
        assert host_obj['type'] == 'x-oca-asset'
