import unittest
import json
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.msatp.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "msatp"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "msatp",
    "identity_class": "events"
}
options = {}
device_registry_event = {
    'DeviceRegistryEvents':
        {
            'ReportId': 123,
            'DeviceName': 'host.test.com',
            'Timestamp': '2023-03-20T17:12:54.5122634Z',
            'Timestamp3': '2023-03-20T16:42:53.4896508Z',
            'Timestamp2': '2023-03-20T16:42:53.4896508Z',
            'DeviceId': 'deviceid',
            'ActionType': 'RegistryValueSet',
            'RegistryKey': 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Advanced Threat Protection',
            'PreviousRegistryValueName': 'CrashHeartbeat',
            'PreviousRegistryValueData': '12344',
            'InitiatingProcessAccountDomain': 'nt authority',
            'InitiatingProcessAccountName': 'system',
            'InitiatingProcessAccountSid': 'S-1-5-18',
            'InitiatingProcessSHA1': '186d3710b3e909b23e6254480520f247564b4005',
            'InitiatingProcessSHA256': 'a9b445863dd123b4b6cb9749228d9ce19448edd1f610347d8e4011f9fdf584de',
            'InitiatingProcessMD5': '5f278fa24e89535896acb13d42a8f764',
            'InitiatingProcessFileName': 'mssense.exe',
            'InitiatingProcessFileSize': 224184,
            'InitiatingProcessVersionInfoCompanyName': 'Microsoft Corporation',
            'InitiatingProcessVersionInfoProductName': 'Microsoft® Windows® Operating System',
            'InitiatingProcessVersionInfoInternalFileName': 'MsSense.exe',
            'InitiatingProcessVersionInfoOriginalFileName': 'MsSense.exe',
            'InitiatingProcessVersionInfoFileDescription': 'Windows Defender Advanced Threat Protection Service Executable',
            'InitiatingProcessId': 5380,
            'InitiatingProcessCommandLine': '"MsSense.exe"',
            'InitiatingProcessCreationTime': '2023-03-20T11:12:48.6790505Z',
            'InitiatingProcessFolderPath': 'c:\\program files\\windows defender advanced threat protection\\mssense.exe',
            'InitiatingProcessParentId': 1048,
            'InitiatingProcessParentFileName': 'services.exe',
            'InitiatingProcessParentCreationTime': '2023-03-20T11:12:47.7246449Z',
            'InitiatingProcessIntegrityLevel': 'System',
            'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault',
            'DeviceId1': 'deviceid',
            'MacAddressSet': ['AA-BB-11-22-CC-AA'],
            'DeviceId2': 'deviceid',
            'PublicIP': '9.9.9.1',
            'OSArchitecture': '64-bit',
            'OSPlatform': 'Windows10',
            'OSVersion': '10.0',
            'rn': 1,
            'category': '',
            'provider': '',
            'event_link': 'https://security.microsoft.com/machines/deviceid/timeline?from=2023-03-20T17:12:53.000Z&to=2023-03-20T17:12:55.000Z',
            'IPAddresses': ['9.9.9.1'],
            'RegistryValues': [
                {
                    'RegistryValueType': 'Qword',
                    'RegistryValueName': 'CrashHeartbeat',
                    'RegistryValueData': '12345'
                }],
            'event_count': '1'
        }
}

device_network_event = {
    'DeviceNetworkEvents':
        {
            'ReportId': 1234,
            'DeviceName': 'host.test.com',
            'Timestamp': '2023-03-13T22:08:58.8407802Z',
            'Timestamp3': '2023-03-13T21:42:09.8518066Z',
            'Timestamp2': '2023-03-13T21:42:09.8518066Z',
            'DeviceId': 'deviceid',
            'ActionType': 'ConnectionSuccess',
            'RemoteIP': '9.9.9.9',
            'RemotePort': 443,
            'RemoteUrl': 'quad9.net',
            'LocalIP': '9.9.9.1',
            'LocalPort': 60773,
            'Protocol': 'Tcp',
            'LocalIPType': 'Private',
            'RemoteIPType': 'Public',
            'InitiatingProcessSHA1': '4a65b267d5fc37527f567f0300e1624845600be1',
            'InitiatingProcessSHA256': 'b84257d238582d3768799e08df03f0b3378a7f8d7342b8c8ffcc453cf6a7b867',
            'InitiatingProcessMD5': '58f918b86a4798177032abcb12c9c605',
            'InitiatingProcessFileName': 'OUTLOOK.EXE',
            'InitiatingProcessFileSize': 42954600,
            'InitiatingProcessVersionInfoCompanyName': 'Microsoft Corporation',
            'InitiatingProcessVersionInfoProductName': 'Microsoft Outlook',
            'InitiatingProcessVersionInfoProductVersion': '16.0.15601.20538',
            'InitiatingProcessVersionInfoInternalFileName': 'Outlook',
            'InitiatingProcessVersionInfoOriginalFileName': 'Outlook.exe',
            'InitiatingProcessVersionInfoFileDescription': 'Microsoft Outlook',
            'InitiatingProcessId': 13748,
            'InitiatingProcessCommandLine': '"OUTLOOK.EXE" ',
            'InitiatingProcessCreationTime': '2023-03-13T14:36:08.6982223Z',
            'InitiatingProcessFolderPath': 'c:\\program files\\microsoft office\\root\\office16\\outlook.exe',
            'InitiatingProcessParentFileName': 'explorer.exe',
            'InitiatingProcessParentId': 18936,
            'InitiatingProcessParentCreationTime': '2023-03-13T14:31:51.6553402Z',
            'InitiatingProcessAccountDomain': 'asd',
            'InitiatingProcessAccountName': 'username',
            'InitiatingProcessAccountSid': 'S-1-5-21',
            'InitiatingProcessAccountUpn': 'username@test.com',
            'InitiatingProcessAccountObjectId': 'asdasd',
            'InitiatingProcessIntegrityLevel': 'Medium',
            'InitiatingProcessTokenElevation': 'TokenElevationTypeLimited',
            'RegistryValueName': '',
            'DeviceId1': 'deviceid',
            'MacAddressSet': ['00-01-02-03-04-AA'],
            'DeviceId2': 'deviceid',
            'PublicIP': '9.9.9.1',
            'OSArchitecture': '64-bit',
            'OSPlatform': 'Windows10',
            'OSVersion': '10.0',
            'rn': 1,
            'category': '',
            'provider': '',
            'event_link': 'https://{domain}/machines/{device}/timeline?from=2023-03-13T22:08:57.000Z&'
                          'to=2023-03-13T22:08:59.000Z',
            'IPAddresses': ['192.168.86.46'],
            'event_count': '1',
            'original_ref': 'reducted'
        }
}


def all_keys_in_object(keys_to_check, process_obj):
    return all(key in process_obj for key in keys_to_check)


class TestMsatpResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for msatp translate results
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
        return TestMsatpResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    def test_common_prop(self):
        """
        to test the common stix object properties
        """
        data = {'DeviceProcessEvents': {'Timestamp': '2019-09-20T06:57:11.8218304Z',
                                        'DeviceId': '8330ed311f1b21b861d63448984eb2632cc9c07c',
                                        'DeviceName': 'desktop-536bt46', 'ActionType': 'ProcessCreated',
                                        'FileName': 'consent.exe', 'FolderPath': 'C:\\Windows\\System32\\consent.exe',
                                        'SHA1': '9329b2362078de27242dd4534f588af3264bf0bf',
                                        'SHA256': '8f112431143a22baaafb448eefd63bf90e7691c890ac69a296574fd07ba03ec6',
                                        'MD5': '27992d7ebe51aec655a088de88bad5c9', 'ProcessId': 20948,
                                        'ProcessCommandLine': 'consent.exe 10088 288 000001CB3AA92A80',
                                        'ProcessIntegrityLevel': 'System',
                                        'ProcessTokenElevation': 'TokenElevationTypeDefault',
                                        'ProcessCreationTime': '2019-09-20T06:57:11.8212034Z',
                                        'AccountDomain': 'nt authority', 'AccountName': 'system',
                                        'AccountSid': 'S-1-5-18', 'LogonId': 999,
                                        'InitiatingProcessAccountDomain': 'nt authority',
                                        'InitiatingProcessAccountName': 'system',
                                        'InitiatingProcessAccountSid': 'S-1-5-18', 'InitiatingProcessLogonId': 999,
                                        'InitiatingProcessIntegrityLevel': 'System',
                                        'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault',
                                        'InitiatingProcessSHA1': 'a1385ce20ad79f55df235effd9780c31442aa234',
                                        'InitiatingProcessMD5': '8a0a29438052faed8a2532da50455756',
                                        'InitiatingProcessFileName': 'svchost.exe', 'InitiatingProcessId': 10088,
                                        'InitiatingProcessCommandLine': 'svchost.exe -k netsvcs -p -s Appinfo',
                                        'InitiatingProcessCreationTime': '2019-09-18T05:56:15.268893Z',
                                        'InitiatingProcessFolderPath': 'c:\\windows\\system32\\svchost.exe',
                                        'InitiatingProcessParentId': 856,
                                        'InitiatingProcessParentFileName': 'services.exe',
                                        'InitiatingProcessParentCreationTime': '2019-09-17T14:54:59.5778638Z',
                                        'ReportId': 12048, 'rn': 1, 'event_count': '1'}}
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
        assert observed_data['first_observed'] is not None
        assert observed_data['last_observed'] is not None
        assert observed_data['number_observed'] is not None

    def test_custom_property(self):
        """
        to test the custom stix object properties
        """
        data = {'DeviceProcessEvents': {'Timestamp': '2019-09-20T06:57:11.8218304Z',
                                        'DeviceId': '8330ed311f1b21b861d63448984eb2632cc9c07c',
                                        'DeviceName': 'desktop-536bt46', 'ActionType': 'ProcessCreated',
                                        'FileName': 'consent.exe', 'FolderPath': 'C:\\Windows\\System32\\consent.exe',
                                        'SHA1': '9329b2362078de27242dd4534f588af3264bf0bf',
                                        'SHA256': '8f112431143a22baaafb448eefd63bf90e7691c890ac69a296574fd07ba03ec6',
                                        'MD5': '27992d7ebe51aec655a088de88bad5c9', 'ProcessId': 20948,
                                        'ProcessCommandLine': 'consent.exe 10088 288 000001CB3AA92A80',
                                        'ProcessIntegrityLevel': 'System',
                                        'ProcessTokenElevation': 'TokenElevationTypeDefault',
                                        'ProcessCreationTime': '2019-09-20T06:57:11.8212034Z',
                                        'AccountDomain': 'nt authority', 'AccountName': 'system',
                                        'AccountSid': 'S-1-5-18', 'LogonId': 999,
                                        'InitiatingProcessAccountDomain': 'nt authority',
                                        'InitiatingProcessAccountName': 'system',
                                        'InitiatingProcessAccountSid': 'S-1-5-18', 'InitiatingProcessLogonId': 999,
                                        'InitiatingProcessIntegrityLevel': 'System',
                                        'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault',
                                        'InitiatingProcessSHA1': 'a1385ce20ad79f55df235effd9780c31442aa234',
                                        'InitiatingProcessMD5': '8a0a29438052faed8a2532da50455756',
                                        'InitiatingProcessFileName': 'svchost.exe', 'InitiatingProcessId': 10088,
                                        'InitiatingProcessCommandLine': 'svchost.exe -k netsvcs -p -s Appinfo',
                                        'InitiatingProcessCreationTime': '2019-09-18T05:56:15.268893Z',
                                        'InitiatingProcessFolderPath': 'c:\\windows\\system32\\svchost.exe',
                                        'InitiatingProcessParentId': 856,
                                        'InitiatingProcessParentFileName': 'services.exe',
                                        'InitiatingProcessParentCreationTime': '2019-09-17T14:54:59.5778638Z',
                                        'ReportId': 12048, 'rn': 1, 'event_count': '1'}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        observed_data = result_bundle_objects[1]

    def test_file_json_to_stix(self):
        """
        to test file stix object properties
        """
        data = {'DeviceFileEvents': {'Timestamp': '2019-09-20T06:50:17.3764965Z',
                                     'DeviceId': '8330ed311f1b21b861d63448984eb2632cc9c07c',
                                     'DeviceName': 'desktop-536bt46', 'ActionType': 'FileCreated',
                                     'FileName': 'updater.exe',
                                     'FolderPath': '<C:\\Program Files\\Mozilla Firefox\\updated\\updater.exe>',
                                     'SHA1': 'cf864398950658185fad8207957b46c12f133ea5',
                                     'MD5': '64c52647783e6b3c0964e41aa38fa5c1',
                                     'InitiatingProcessAccountDomain': 'nt authority',
                                     'InitiatingProcessAccountName': 'system',
                                     'InitiatingProcessAccountSid': 'S-1-5-18',
                                     'InitiatingProcessMD5': '620f00789f37c453710ebf758bf1772e',
                                     'InitiatingProcessSHA1': '8bd812436b301dd30d55f76ae418a0e85f7dd020',
                                     'InitiatingProcessFolderPath': 'c:\\program files (x86)\\mozilla maintenance '
                                                                    'service\\update\\updater.exe',
                                     'InitiatingProcessFileName': 'updater.exe', 'InitiatingProcessId': 13980,
                                     'InitiatingProcessCommandLine': '"updater.exe" '
                                                                     'C:\\ProgramData\\Mozilla\\updates\\3080'
                                                                     '46B0AF4A39CB\\updates\\0 "<C:\\Program '
                                                                     'Files\\Mozilla Firefox>" "<C:\\Program '
                                                                     'Files\\Mozilla Firefox\\updated>" -1',
                                     'InitiatingProcessCreationTime': '2019-09-20T06:50:08.1793244Z',
                                     'InitiatingProcessIntegrityLevel': 'System',
                                     'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault',
                                     'InitiatingProcessParentId': 17088,
                                     'InitiatingProcessParentFileName': 'maintenanceservice.exe',
                                     'InitiatingProcessParentCreationTime': '2019-09-20T06:50:07.6324849Z',
                                     'RequestProtocol': 'Unknown', 'ReportId': 11844, 'rn': 1, 'event_count': '1'}}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)

        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        file_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'file')
        assert file_obj is not None, 'file object type not found'
        assert file_obj.keys() == {'type', 'hashes', 'parent_directory_ref', 'name'}
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'updater.exe'
        assert file_obj['hashes'] == {'SHA-1': 'cf864398950658185fad8207957b46c12f133ea5',
                                      'MD5': '64c52647783e6b3c0964e41aa38fa5c1'}
        assert file_obj['parent_directory_ref'] == '3'
        directory_object = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'directory')
        file_path = get_module_transformers(MODULE)['ToDirectoryPath'].transform(data['DeviceFileEvents']['FolderPath'])
        assert directory_object.get('path') == file_path

    def test_process_json_to_stix(self):
        """
        to test process stix object properties
        """
        data = {'DeviceProcessEvents': {'Timestamp': '2019-09-20T06:57:11.8218304Z',
                                        'DeviceId': '8330ed311f1b21b861d63448984eb2632cc9c07c',
                                        'DeviceName': 'desktop-536bt46', 'ActionType': 'ProcessCreated',
                                        'FileName': 'consent.exe', 'FolderPath': 'C:\\Windows\\System32\\consent.exe',
                                        'SHA1': '9329b2362078de27242dd4534f588af3264bf0bf',
                                        'SHA256': '8f112431143a22baaafb448eefd63bf90e7691c890ac69a296574fd07ba03ec6',
                                        'MD5': '27992d7ebe51aec655a088de88bad5c9', 'ProcessId': 20948,
                                        'ProcessCommandLine': 'consent.exe 10088 288 000001CB3AA92A80',
                                        'ProcessIntegrityLevel': 'System',
                                        'ProcessTokenElevation': 'TokenElevationTypeDefault',
                                        'ProcessCreationTime': '2019-09-20T06:57:11.8212034Z',
                                        'AccountDomain': 'nt authority', 'AccountName': 'system', 'AccountUpn': '',
                                        'AccountSid': 'S-1-5-18', 'LogonId': 999,
                                        'InitiatingProcessAccountDomain': 'nt authority',
                                        'InitiatingProcessAccountName': 'system',
                                        'InitiatingProcessAccountSid': 'S-1-5-18', 'InitiatingProcessLogonId': 999,
                                        'InitiatingProcessIntegrityLevel': 'System',
                                        'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault',
                                        'InitiatingProcessSHA1': 'a1385ce20ad79f55df235effd9780c31442aa234',
                                        'InitiatingProcessMD5': '8a0a29438052faed8a2532da50455756',
                                        'InitiatingProcessFileName': 'svchost.exe', 'InitiatingProcessId': 10088,
                                        'InitiatingProcessCommandLine': 'svchost.exe -k netsvcs -p -s Appinfo',
                                        'InitiatingProcessCreationTime': '2019-09-18T05:56:15.268893Z',
                                        'InitiatingProcessFolderPath': 'c:\\windows\\system32\\svchost.exe',
                                        'InitiatingProcessParentId': 856,
                                        'InitiatingProcessParentFileName': 'services.exe',
                                        'InitiatingProcessParentCreationTime': '2019-09-17T14:54:59.5778638Z',
                                        'ReportId': 12048, 'rn': 1, 'Event_count': '1'}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        process_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'process')
        assert process_obj is not None, 'process object type not found'
        assert all_keys_in_object({'type', 'name', 'binary_ref', 'pid', 'command_line', 'created', 'creator_user_ref'}, process_obj)
        assert process_obj['type'] == 'process'
        assert process_obj['name'] == 'consent.exe'
        assert objects[process_obj['binary_ref']]['type'] == 'file'
        assert objects[process_obj['binary_ref']]['name'] == 'consent.exe'
        assert process_obj['pid'] == 20948
        assert process_obj['command_line'] == 'consent.exe 10088 288 000001CB3AA92A80'
        assert process_obj['created'] == '2019-09-20T06:57:11.821Z'
        assert objects[process_obj['creator_user_ref']]['type'] == "user-account"
        assert objects[process_obj['creator_user_ref']]['user_id'] == "system"
        assert 'account_login' not in objects[process_obj['creator_user_ref']]

    def test_network_json_to_stix(self):
        """to test network stix object properties"""
        data = device_network_event
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert network_obj is not None, 'network-traffic object type not found'
        assert network_obj.keys() == {'type', 'dst_ref', 'dst_port', 'src_ref', 'src_port', 'protocols'}
        assert network_obj['type'] == 'network-traffic'
        assert objects[network_obj['dst_ref']]['type'] == "ipv4-addr"
        assert objects[network_obj['dst_ref']]['value'] == "9.9.9.9"
        assert network_obj['dst_port'] == 443
        assert objects[network_obj['src_ref']]['type'] == "ipv4-addr"
        assert objects[network_obj['src_ref']]['value'] == "9.9.9.1"
        assert network_obj['src_port'] == 60773
        assert network_obj['protocols'] == ['tcp']

    def test_network_json_to_stix_negative(self):
        """to test negative test case for stix object"""
        data = device_network_event
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, data, get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'file')
        assert network_obj is None

    def test_mac_json_to_stix(self):
        """to test mac stix object properties"""
        data = device_network_event

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'mac-addr')
        assert network_obj is not None, 'mac-addr object type not found'
        assert network_obj.keys() == {'type', 'value'}
        assert network_obj['type'] == 'mac-addr'
        assert network_obj['value'] == '00:01:02:03:04:aa'

    def test_registry_json_to_stix(self):
        """to test registry stix object properties"""
        data = device_registry_event
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        registry_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'windows-registry-key')
        assert registry_obj is not None, 'windows-registry-key object type not found'
        assert all_keys_in_object({'type', 'key', 'values'}, registry_obj)
        assert registry_obj['type'] == 'windows-registry-key'
        assert registry_obj['key'] == 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Advanced Threat Protection'
        assert len(registry_obj['values']) == 1
        assert all_keys_in_object({'data','data_type', 'name'}, registry_obj['values'][0])
        assert registry_obj['values'][0]['data'] == '12345'
        assert registry_obj['values'][0]['data_type'] == 'REG_QWORD'
        assert registry_obj['values'][0]['name'] == 'CrashHeartbeat'
