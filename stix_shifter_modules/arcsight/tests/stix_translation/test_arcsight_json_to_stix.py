import unittest

from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.arcsight.entry_point import EntryPoint


MODULE = "arcsight"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data

data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "arcsight",
    "identity_class": "events"
}
options = {}


class TestArcsightResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for arcsight translate results
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
        return TestArcsightResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def test_common_prop():
        """to test the common stix object properties"""
        data = {"network_events": {
            "_rowId": "189D1-C@Local", "Event Time": 1592820270804,
            "Logger": "Local", "spid": "2497",
            "agentHostName": "ip-172-31-62-249.ec2.internal", "destinationProcessName": "/usr/sbin/sshd",
            "categoryOutcome": "/Success", "sourceHostName": "176.122.190.164.16clouds.com",
            "priority": 3, "destinationUserId": "4294967295",
            "deviceVendor": "Unix", "deviceProcessName": "auditd",
            "destinationPort": 22, "name": "CRYPTO_KEY_USER|success",
            "eventId": 2815858, "deviceProduct": "auditd",
            "destinationHostName": "ip-172-31-66-30.ec2.internal", "destinationAddress": "172.31.66.30",
            "sourceUserId": "0", "sourceAddress": "176.122.190.164", "requestUrl": ""
        }}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        assert result_bundle_identity['id'] == data_source['id']
        assert result_bundle_identity['name'] == data_source['name']
        assert result_bundle_identity['identity_class'] == data_source['identity_class']

        observed_data = result_bundle_objects[1]
        assert observed_data['id'] is not None
        assert observed_data['type'] == "observed-data"
        assert observed_data['created_by_ref'] == result_bundle_identity['id']

        assert observed_data['modified'] is not None
        assert observed_data['created'] is not None
        assert observed_data['first_observed'] is not None
        assert observed_data['last_observed'] is not None
        assert observed_data['number_observed'] is not None

    @staticmethod
    def test_process_json_to_stix():
        """to test process and mac address stix object properties"""
        data = {"other_events": {
            "_rowId": "2055B-7@Local", "Event Time": 1593431345494, "Logger": "Local", "dpid": "2044",
            "fileHash": "MD5=C9A51BDEC4B4E0B6EF51B64637677D14,SHA256=DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF284"
                        "6BBF8E60610016142A,IMPHASH=EF6872A34285CD44908CCC3A70EA5DAB",
            "spid": "716", "oldFileName": "TSThemeS.exe",
            "agentHostName": "ip-172-31-62-249.ec2.internal", "name": "Process Created",
            "destinationProcessName": "C:\\Windows\\System32\\TSTheme.exe",
            "sourceServiceName": "C:\\Windows\\system32\\svchost.exe -k DcomLaunch",
            "destinationUserName": "SYSTEM", "eventId": 3223643, "priority": 3, 'sourceMacAddress': '00-D0-09-D6-73-E9',
            "deviceProduct": "Sysmon", "sourceProcessName": "C:\\Windows\\System32\\svchost.exe",
            "sourceUserId": "0x40911", "deviceVendor": "Microsoft", 'destinationMacAddress': '00-0B-46-A8-98-81',
            "severity": "0", "destinationServiceName": "C:\\Windows\\system32\\TSTheme.exe -Embedding",
            "destinationUserId": "", "destinationHostName": "WIN-SD458DHHD07", "destinationAddress": "172.31.59.74",
            "sourceHostName": "workstation", "MD5": "C9A51BDEC4B4E0B6EF51B64637677D14",
            "SHA256": "DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A"
        }}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)

        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        process_obj = TestArcsightResultsToStix.get_first_of_type(objects.values(), 'process')
        mac_obj = TestArcsightResultsToStix.get_first_of_type(objects.values(), 'mac-addr')

        assert process_obj is not None, 'file object type not found'
        assert process_obj.keys() == {'type', 'pid', 'parent_ref', 'name', 'command_line'}
        assert process_obj['type'] == 'process'
        assert process_obj['name'] == 'C:\\Windows\\System32\\TSTheme.exe'
        assert process_obj['pid'] == 2044
        assert process_obj['command_line'] == 'C:\\Windows\\system32\\TSTheme.exe -Embedding'
        assert mac_obj['value'] == '00:d0:09:d6:73:e9'

    @staticmethod
    def test_network_json_to_stix():
        """to test network stix object properties"""
        data = {"network_events": {
            "_rowId": "189D1-C@Local", "Event Time": 1592820270804,
            "Logger": "Local", "spid": "2497", "transportProtocol": "TCP",
            "agentHostName": "ip-172-31-62-249.ec2.internal", "destinationProcessName": "/usr/sbin/sshd",
            "categoryOutcome": "/Success", "sourceHostName": "176.122.190.164.16clouds.com",
            "priority": 3, "destinationUserId": "4294967295",
            "deviceVendor": "Unix", "deviceProcessName": "auditd",
            "destinationPort": 22, "name": "CRYPTO_KEY_USER|success",
            "eventId": 2815858, "deviceProduct": "auditd",
            "destinationHostName": "ip-172-31-66-30.ec2.internal", "destinationAddress": "172.31.66.30",
            "sourceUserId": "0", "sourceAddress": "176.122.190.164", "requestUrl": "", "protocols": ["TCP"]
        }}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestArcsightResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert network_obj is not None, 'network-traffic object type not found'
        assert network_obj.keys() == {'type', 'dst_port', 'dst_ref', 'src_ref', 'protocols'}
        assert network_obj['type'] == 'network-traffic'
        assert network_obj['dst_port'] == 22
        assert network_obj['protocols'] == ['tcp']
        assert network_obj['src_ref'] == '14'

    @staticmethod
    def test_file_json_to_stix():
        """to test file stix object properties"""
        data = {"network_events": {
            "_rowId": "2053B-B3@Local", "Event Time": 1593431344528,
            "Logger": "Local", "name": "The Windows Filtering Platform has permitted a bind to a local port.",
            "eventId": 3208541, "fileName": "svchost.exe", "priority": 3,
            "deviceVendor": "Microsoft", "deviceHostName": "WIN-SD458DHHD07", "severity": "0",
            "filePath": "\\device\\harddiskvolume2\\windows\\system32",
            "fileHash": "MD5 = C9A51BDEC4B4E0B6EF51B64637677D14, SHA256 = DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF"
                        "2846BBF8E60610016142A,IMPHASH=EF6872A34285CD44908CCC3A70EA5DAB",
            "fileType": "Application", "destinationHostName": "WIN-SD458DHHD07", "sourceAddress": "",
            "transportProtocol": "TCP", "destinationAddress": "172.31.59.74",
            "sourceHostName": "", "protocols": ["TCP"],
            "MD5": "C9A51BDEC4B4E0B6EF51B64637677D14",
            "SHA256": "DBDF0C85B1A39656E616E428FCEFEDC930761ACC5CF2846BBF8E60610016142A"}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)

        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        file_obj = TestArcsightResultsToStix.get_first_of_type(objects.values(), 'file')
        directory_obj = TestArcsightResultsToStix.get_first_of_type(objects.values(), 'directory')

        assert file_obj is not None, 'file object type not found'
        assert file_obj.keys() == {'type', 'name', 'parent_directory_ref', 'hashes'}
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'svchost.exe'
        assert file_obj['parent_directory_ref'] == '5'
        assert directory_obj['path'] == '\\device\\harddiskvolume2\\windows'

    @staticmethod
    def test_network_json_to_stix_negative():
        """to test negative test case for stix object"""
        data = {"other_events": {
            "_rowId": "189D1-C@Local", "Event Time": 1592820270804,
            "Logger": "Local", "spid": "2497",
            "agentHostName": "ip-172-31-62-249.ec2.internal", "destinationProcessName": "/usr/sbin/sshd",
            "categoryOutcome": "/Success", "sourceHostName": "176.122.190.164.16clouds.com",
            "priority": 3, "destinationUserId": "4294967295",
            "deviceVendor": "Unix", "deviceProcessName": "auditd",
            "destinationPort": 22, "name": "CRYPTO_KEY_USER|success",
            "eventId": 2815858, "deviceProduct": "auditd",
            "destinationHostName": "ip-172-31-66-30.ec2.internal", "destinationAddress": "172.31.66.30",
            "sourceUserId": "0", "sourceAddress": "176.122.190.164", "requestUrl": ""
        }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, data, get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestArcsightResultsToStix.get_first_of_type(objects.values(), 'file')
        assert network_obj is None

    @staticmethod
    def test_custom_property():
        """to test the custom stix object properties"""
        data = {"network_events": {
            "_rowId": "8DD40-48@Local", "Event Time": 1597324482685,
            "Logger": "Local", "name": "GET /favicon.ico HTTP/1.1",
            "destinationProcessName": "apache", "applicationProtocol": "http",
            "eventId": 9741541, "requestUrlFileName": "/favicon.ico",
            "priority": 3, "transportProtocol": "TCP",
            "deviceProduct": "Tomcat", "requestUrl": "/favicon.ico",
            "requestMethod": "GET", "c6a2": "0:0:0:0:0:0:0:1",
            "sourceUserId": "-", "deviceVendor": "Apache",
            "deviceProcessName": "apache", "categoryObject": "/Host/Application/Service",
            "categoryOutcome": "/Success", "categoryBehavior": "/Communicate/Query",
            "categorySignificance": "/Normal", "deviceReceiptTime": 1597324461000,
            "baseEventCount": 1, "categoryDeviceGroup": "/Application",
            "protocols": [
                "TCP",
                "http"
            ]}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        observed_data = result_bundle_objects[1]
        objects = observed_data['objects']
        event_obj = TestArcsightResultsToStix.get_first_of_type(objects.values(), 'x-arcsight-event')
        event_category_obj = TestArcsightResultsToStix.get_first_of_type(objects.values(), 'x-arcsight-event-category')
        device_obj = TestArcsightResultsToStix.get_first_of_type(objects.values(), 'x-arcsight-event-device')

        assert device_obj['device_vendor'] == 'Apache'
        assert device_obj['device_product'] == 'Tomcat'

        assert event_obj['priority'] == 3
        assert event_obj['event_id'] == 9741541
        assert event_obj['request_method'] == 'GET'
        assert event_obj['base_event_count'] == 1

        assert event_category_obj['category_object'] == '/Host/Application/Service'
        assert event_category_obj['category_outcome'] == '/Success'
        assert event_category_obj['category_device_group'] == '/Application'

    @staticmethod
    def test_registry_json_to_stix():
        """to test registry and custom cybox object stix object properties"""
        data = {"other_events": {
            "_rowId": "2055B-11@Local", "Event Time": 1593431345495,
            "categoryObject": "/Host/Resource/Registry", "dpid": "1196",
            "name": "Registry value set", "destinationProcessName": "C:\\Windows\\System32\\spoolsv.exe",
            "sourceAddress": "172.31.59.74", "deviceAction": "Registry value set",
            "categoryOutcome": "/Success", "destinationUserName": "SYSTEM",
            "eventId": 3223653, "categoryBehavior": "/Execute/Query",
            "categorySignificance": "/Informational", "priority": 3,
            "deviceProduct": "Sysmon", "deviceReceiptTime": 1593164565229,
            "deviceCustomString4": "DWORD (0x00000401)", "ad.arcSightEventPath": "3sdGZ73IBABCDMQjbx1dwOQ==",
            "bytesOut": -2147483648, "deviceVendor": "Microsoft",
            "deviceHostName": "WIN-SD458DHHD07", "deviceEventCategory": "Microsoft-Windows-Sysmon/Operational",
            "endTime": 1593164565229, "severity": "0",
            "baseEventCount": 1, "categoryDeviceGroup": "/Operating System",
            'registry_key': 'HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Print\\Printers\\Fax '
                            '(redirected 2)\\DsDriver\\driverVersion',
            'registry_data': [{'name': 'driverVersion', 'registry_string': 'DWORD (0x00000401)'}]
        }}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)

        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        registry_obj = TestArcsightResultsToStix.get_first_of_type(objects.values(), 'windows-registry-key')
        custom_obj = TestArcsightResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')

        assert registry_obj is not None, 'file object type not found'
        assert registry_obj.keys() == {'type', 'key', 'values'}
        assert registry_obj['type'] == 'windows-registry-key'
        assert registry_obj['values'] == [{'name': 'driverVersion', 'data_type': 'REG_DWORD', 'data': '(0x00000401)'}]

        assert custom_obj['type'] == 'x-ibm-finding'
        assert custom_obj['name'] == 'Registry value set'
        assert custom_obj['finding_type'] == '/Informational'
        assert custom_obj['severity'] == '0'
        assert custom_obj['src_ip_ref'] == '4'
