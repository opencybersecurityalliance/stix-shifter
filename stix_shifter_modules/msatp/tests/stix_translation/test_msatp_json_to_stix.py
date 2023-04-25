import unittest
import json

from stix_shifter_modules.msatp.tests.test_utils import resolve_ref, all_keys_in_object, hashes_are_correct, \
    resolve_refs
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.msatp.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers
from stix_shifter.stix_translation import stix_translation

HASHES = {'SHA-1', 'SHA-256', 'MD5'}

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

device_process_event = {
    'DeviceProcessEvents':
        {
            'ReportId': 1234,
            'DeviceName': 'host.test.com',
            'Timestamp': '2023-03-17T20:23:03.7116107Z',
            'Timestamp3': '2023-03-17T19:40:08.8911345Z',
            'Timestamp2': '2023-03-17T19:40:08.8911345Z',
            'DeviceId': 'deviceid',
            'ActionType': 'ProcessCreated',
            'FileName': 'msedge.exe',
            'FolderPath': 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
            'SHA1': 'c737742b81292c764ac2a7e419a37ed7fdf4a1ed',
            'SHA256': '470ea019c1ea8882b258dea27e77261dd297eb225fd08edbe591c82796189d75',
            'MD5': 'e180c9a532c45eba99eefd01601f5c41',
            'FileSize': 4243360,
            'ProcessVersionInfoCompanyName': 'Microsoft Corporation',
            'ProcessVersionInfoProductName': 'Microsoft Edge',
            'ProcessVersionInfoProductVersion': '110.0.1587.50',
            'ProcessVersionInfoInternalFileName': 'msedge_exe',
            'ProcessVersionInfoOriginalFileName': 'msedge.exe',
            'ProcessVersionInfoFileDescription': 'Microsoft Edge',
            'ProcessId': 37384,
            'ProcessCommandLine': '"msedge.exe" --type=gpu-process',
            'ProcessIntegrityLevel': 'Low',
            'ProcessTokenElevation': 'TokenElevationTypeDefault',
            'ProcessCreationTime': '2023-03-17T20:23:03.7021445Z',
            'AccountDomain': 'asd',
            'AccountName': 'username',
            'AccountSid': 'S-1-5-21',
            'AccountObjectId': 'aaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'AccountUpn': 'username@test.com',
            'LogonId': 111111111,
            'InitiatingProcessAccountDomain': 'asd',
            'InitiatingProcessAccountName': 'username',
            'InitiatingProcessAccountSid': 'S-1-5-21',
            'InitiatingProcessAccountUpn': 'username@test.com',
            'InitiatingProcessAccountObjectId': 'aaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
            'InitiatingProcessLogonId': 111111111,
            'InitiatingProcessIntegrityLevel': 'Medium',
            'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault',
            'InitiatingProcessSHA1': 'c737742b81292c764ac2a7e419a37ed7fdf4a1ed',
            'InitiatingProcessSHA256': '470ea019c1ea8882b258dea27e77261dd297eb225fd08edbe591c82796189d75',
            'InitiatingProcessMD5': 'e180c9a532c45eba99eefd01601f5c41',
            'InitiatingProcessFileName': 'msedge.exe',
            'InitiatingProcessFileSize': 4243360,
            'InitiatingProcessVersionInfoCompanyName': 'Microsoft Corporation',
            'InitiatingProcessVersionInfoProductName': 'Microsoft Edge',
            'InitiatingProcessVersionInfoProductVersion': '110.0.1587.50',
            'InitiatingProcessVersionInfoInternalFileName': 'msedge_exe',
            'InitiatingProcessVersionInfoOriginalFileName': 'msedge.exe',
            'InitiatingProcessVersionInfoFileDescription': 'Microsoft Edge',
            'InitiatingProcessId': 400,
            'InitiatingProcessCommandLine': '"msedge.exe" -- "https://test.com/login/login.asp"',
            'InitiatingProcessCreationTime': '2023-03-17T20:23:03.441179Z',
            'InitiatingProcessFolderPath': 'c:\\program files (x86)\\microsoft\\edge\\application\\msedge.exe',
            'InitiatingProcessParentId': 30972,
            'InitiatingProcessParentFileName': 'iexplore.exe',
            'InitiatingProcessParentCreationTime': '2023-03-17T20:23:03.1696537Z',
            'InitiatingProcessSignerType': 'OsVendorApplication',
            'InitiatingProcessSignatureStatus': 'Valid',
            'RegistryValueName': '',
            'DeviceId1': 'deviceid',
            'MacAddressSet': ['11-22-33-44-55-66'],
            'DeviceId2': 'deviceid',
            'PublicIP': '9.9.9.1',
            'OSArchitecture': '64-bit',
            'OSPlatform': 'Windows10',
            'OSVersion': '10.0',
            'rn': 1,
            'category': '',
            'provider': '',
            'event_link': 'https://security.microsoft.com/machines/deviceid/timeline?from=2023-03-17T20:23:02.000Z&to=2023-03-17T20:23:04.000Z',
            'event_count': '1'
        }
}

device_file_event = {
    'DeviceFileEvents':
        {
            'ReportId': 1234,
            'DeviceName': 'host.test.com',
            'Timestamp': '2023-03-17T20:19:41.7007151Z',
            'Timestamp3': '2023-03-17T19:40:08.8911345Z',
            'Timestamp2': '2023-03-17T19:40:08.8911345Z',
            'DeviceId': 'deviceid',
            'ActionType': 'FileModified',
            'FileName': 'asdasdasd.html',
            'FolderPath': 'C:\\Users\\username\\Downloads\\asdasdasd.html',
            'SHA1': '3ee189ca7db084de9d630cd6091125d99b3af1e1',
            'SHA256': '92200a5da4433f86af6009486817fc068714ac49050d7f5c6f1f393f17e72411',
            'MD5': '8c541a9caed9f9b52be730cc16df4dc1',
            'FileSize': 33785,
            'InitiatingProcessAccountDomain': 'nt authority',
            'InitiatingProcessAccountName': 'system',
            'InitiatingProcessAccountSid': 'S-1-5-18',
            'InitiatingProcessIntegrityLevel': 'System',
            'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault',
            'InitiatingProcessSHA1': 'e31d842f36952d41d6cc39b0baafeb59c0cbac42',
            'InitiatingProcessSHA256': 'a3e2ef7e6f46566c7f0b56c6a2ac4d07b7ed3c927d9232bbd28483a1100a0e82',
            'InitiatingProcessMD5': 'c977a7757d71bf51d42703ba1799a191',
            'InitiatingProcessFileName': 'AsdService.exe',
            'InitiatingProcessFileSize': 4958832,
            'InitiatingProcessVersionInfoCompanyName': 'asd Corp.',
            'InitiatingProcessVersionInfoProductName': 'asd Privilege Management',
            'InitiatingProcessVersionInfoProductVersion': '21.6.153.0',
            'InitiatingProcessVersionInfoInternalFileName': 'AsdService.exe',
            'InitiatingProcessVersionInfoOriginalFileName': 'AsdService.exe',
            'InitiatingProcessVersionInfoFileDescription': 'asd Privilege Management Service',
            'InitiatingProcessId': 3892,
            'InitiatingProcessCommandLine': '"AsdService.exe"',
            'InitiatingProcessCreationTime': '2023-02-23T03:48:44.4729635Z',
            'InitiatingProcessFolderPath': 'c:\\program files\\asd\\guard client\\asdservice.exe',
            'InitiatingProcessParentId': 1016,
            'InitiatingProcessParentFileName': 'services.exe',
            'InitiatingProcessParentCreationTime': '2023-02-23T03:48:43.6251262Z',
            'RegistryValueName': '',
            'RequestProtocol': 'Local',
            'RequestAccountName': 'username',
            'RequestAccountDomain': 'ASD',
            'RequestAccountSid': 'S-1-5-21-1111111111-111111111-1111111111-1111111',
            'DeviceId1': 'deviceid',
            'MacAddressSet': ['11-22-33-44-55-66'],
            'DeviceId2': 'deviceid',
            'PublicIP': '9.9.9.1',
            'OSArchitecture': '64-bit',
            'OSPlatform': 'Windows10',
            'OSVersion': '10.0',
            'rn': 1,
            'category': '',
            'provider': '',
            'event_link': 'https://security.microsoft.com/machines/deviceid/timeline?from=2023-03-17T20:19:40.000Z&to=2023-03-17T20:19:42.000Z',
            'event_count': '1'
        }
}

device_event_with_alert = {
    'DeviceEvents':
        {
            'ReportId': 1234,
            'DeviceName': 'host.test.com',
            'Timestamp': '2023-03-27T08:32:10.8787764Z',
            'TableName': 'DeviceEvents',
            'DeviceId': 'deviceid',
            'RemoteUrl': 'https://malicious.com',
            'RemoteIP': '9.9.9.9',
            'RemotePort': 443,
            'LocalIP': '9.9.9.1',
            'LocalPort': 58993,
            'ActionType': 'OtherAlertRelatedActivity',
            'FileName': 'rundll32.exe',
            'FolderPath': 'C:\\Windows\\System32\\rundll32.exe',
            'SHA1': 'dd399ae46303343f9f0da189aee11c67bd868222',
            'SHA256': 'b53f3c0cd32d7f20849850768da6431e5f876b7bfa61db0aa0700b02873393fa',
            'MD5': 'ef3179d498793bf4234f708d3be28633',
            'AccountDomain': 'ASD',
            'AccountName': 'username',
            'InitiatingProcessAccountDomain': 'ASD',
            'InitiatingProcessAccountName': 'username',
            'InitiatingProcessAccountSid': 'S-1-5-21-1111111111-111111111-1111111111-1111111',
            'InitiatingProcessSHA1': '75cf2cc2e76eb99c4de584a3f2917c5cce3bc1bd',
            'InitiatingProcessSHA256': '0f4e87fab2e5455b89c7263456c461cef80c4ef4b05c893a455d70e2ccd4c387',
            'InitiatingProcessMD5': '1cc2723f23e452686f2426024bf666e5',
            'InitiatingProcessFileName': 'WcInstaller.exe',
            'InitiatingProcessId': 18808,
            'InitiatingProcessCommandLine': '"WcInstaller.exe" --silent',
            'InitiatingProcessCreationTime': '2023-03-27T08:31:19.2589344Z',
            'InitiatingProcessFolderPath': 'C:\\Users\\username\\AppData\\Local\\Temp\\WcInstaller.exe',
            'InitiatingProcessParentId': 18428,
            'InitiatingProcessParentFileName': 'setup_win64.exe',
            'InitiatingProcessParentCreationTime': '2023-03-27T08:31:08.2841083Z',
            'AdditionalFields': '{"Description":"File WcInstaller.exe observed on machine host.test.com"}',
            'PublicIP': '9.9.9.1',
            'OSArchitecture': '64-bit',
            'OSPlatform': 'Windows10',
            'OSVersion': '10.0',
            'MacAddressSet': ['11-22-33-44-55-66'],
            'rn': 1,
            'category': '1',
            'provider': '1',
            'event_link': 'https://security.microsoft.com/machines/deviceid/timeline?from=2023-03-27T08:32:09.000Z&to=2023-03-27T08:32:11.000Z',
            'Alerts': '[{"AlertId": "1234567890-1234-1234-1234-123456789012_1", "Severity": "Medium", "Title": "A suspicious file was observed", "Category": "Malware", "AttackTechniques": ["Obfuscated Files or Information (T1027)", "Malicious File (T1204.002)"]}]',
            'IPAddresses': ['9.9.9.1'],
            'missingChildShouldMapInitiatingPid': 18808,
            'event_count': '1',
            'original_ref': 'base64'
        }
}


def translate_to_objects(data):
    translation = stix_translation.StixTranslation()
    result_bundle = translation.translate(module='msatp', translate_type='results', data_source=data_source,
                                          data=[data])
    result_bundle_objects = result_bundle['objects']
    result_bundle_identity = result_bundle_objects[0]
    assert result_bundle_identity['type'] == data_source['type']
    observed_data = result_bundle_objects[1]
    assert 'objects' in observed_data
    objects = observed_data['objects']
    return objects


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
        data = device_process_event
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

    def test_file_json_to_stix(self):
        """
        to test file stix object properties
        """
        objects = translate_to_objects(device_file_event)

        event_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert event_obj is not None, 'event object type not found'
        assert 'file_ref' in event_obj, 'file_ref missing from event'
        file_obj = resolve_ref(objects, event_obj, 'file_ref', 'file', 'file object missing')
        assert all_keys_in_object({'type', 'hashes', 'parent_directory_ref', 'name'}, file_obj)
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'asdasdasd.html'
        assert all_keys_in_object(HASHES, file_obj['hashes'])
        hashes_are_correct(file_obj, {
            'MD5': '8c541a9caed9f9b52be730cc16df4dc1',
            'SHA1': '3ee189ca7db084de9d630cd6091125d99b3af1e1',
            'SHA256': '92200a5da4433f86af6009486817fc068714ac49050d7f5c6f1f393f17e72411'
        })
        parent_dir = resolve_ref(objects, file_obj, 'parent_directory_ref', 'directory', 'parent dir missing')
        assert parent_dir.get('path') == "C:\\Users\\username\\Downloads"

    def test_process_json_to_stix(self):
        """
        to test process stix object properties
        """
        objects = translate_to_objects(device_process_event)

        event_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert event_obj is not None, 'event object type not found'
        assert 'process_ref' in event_obj, 'process_ref missing from event'
        process_obj = resolve_ref(objects, event_obj, 'process_ref', 'process', 'process object missing')
        assert all_keys_in_object({'type', 'name', 'binary_ref', 'pid', 'command_line', 'created', 'creator_user_ref'},
                                  process_obj)
        assert process_obj['name'] == 'msedge.exe'
        file_obj = resolve_ref(objects, process_obj, 'binary_ref', "file", "binary ref missing from process")
        assert file_obj['name'] == 'msedge.exe'
        assert all_keys_in_object(HASHES, file_obj['hashes'])
        hashes_are_correct(file_obj, {'SHA1': 'c737742b81292c764ac2a7e419a37ed7fdf4a1ed',
                                      'SHA256': '470ea019c1ea8882b258dea27e77261dd297eb225fd08edbe591c82796189d75',
                                      'MD5': 'e180c9a532c45eba99eefd01601f5c41'})
        dir_obj = resolve_ref(objects, file_obj, 'parent_directory_ref', 'directory',
                              'parent dir missing from file binary ref')
        assert dir_obj.get("path") == "C:\\Program Files (x86)\\Microsoft\\Edge\\Application"
        assert process_obj['pid'] == 37384
        assert process_obj['command_line'] == '"msedge.exe" --type=gpu-process'
        assert process_obj['created'] == '2023-03-17T20:23:03.702Z'
        user_obj = resolve_ref(objects, process_obj, 'creator_user_ref', "user-account", "missing creator user ref")
        assert user_obj['user_id'] == "username"
        assert user_obj['account_login'] == "username@test.com"
        parent_obj = resolve_ref(objects, process_obj, 'parent_ref', "process", "parent process missing")
        assert parent_obj['name'] == "msedge.exe"
        assert parent_obj['pid'] == 400
        assert parent_obj['created'] == '2023-03-17T20:23:03.441Z'
        assert parent_obj['command_line'] == '"msedge.exe" -- "https://test.com/login/login.asp"'
        parent_parent_obj = resolve_ref(objects, parent_obj, 'parent_ref', "process", 'parent parent process missing')
        assert parent_parent_obj['name'] == 'iexplore.exe'
        assert parent_parent_obj['pid'] == 30972
        assert parent_parent_obj['created'] == '2023-03-17T20:23:03.169Z'

    def test_network_json_to_stix(self):
        """to test network stix object properties"""
        objects = translate_to_objects(device_network_event)

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

    def test_mac_json_to_stix(self):
        """to test mac stix object properties"""
        objects = translate_to_objects(device_network_event)

        network_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'mac-addr')
        assert network_obj is not None, 'mac-addr object type not found'
        assert network_obj.keys() == {'type', 'value'}
        assert network_obj['type'] == 'mac-addr'
        assert network_obj['value'] == '00:01:02:03:04:aa'

    def test_registry_json_to_stix(self):
        """to test registry stix object properties"""
        objects = translate_to_objects(device_registry_event)

        registry_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'windows-registry-key')
        assert registry_obj is not None, 'windows-registry-key object type not found'
        assert all_keys_in_object({'type', 'key', 'values'}, registry_obj)
        assert registry_obj['type'] == 'windows-registry-key'
        assert registry_obj['key'] == 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Advanced Threat Protection'
        assert len(registry_obj['values']) == 1
        assert all_keys_in_object({'data', 'data_type', 'name'}, registry_obj['values'][0])
        assert registry_obj['values'][0]['data'] == '12345'
        assert registry_obj['values'][0]['data_type'] == 'REG_QWORD'
        assert registry_obj['values'][0]['name'] == 'CrashHeartbeat'

    def test_alert_json_to_stix(self):
        """
        test device event with alert
        """
        objects = translate_to_objects(device_event_with_alert)

        event = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert event is not None, 'event object type not found'
        findings = resolve_refs(objects, event, "finding_refs", "x-ibm-finding", "finding refs missing in event")
        assert len(findings) == 1
        finding = findings[0]
        assert finding.get("name") == "A suspicious file was observed"
        assert finding.get("severity") == 66
        assert finding.get("alert_id") == "1234567890-1234-1234-1234-123456789012_1"
        ttps = resolve_refs(objects, finding, "ttp_tagging_refs", "x-ibm-ttp-tagging",
                            "ttp tagging refs missing from finding")
        assert len(ttps) == 3
        ttp = ttps[0]
        assert "kill_chain_phases" in ttp
        phases = ttp["kill_chain_phases"]
        assert len(phases) == 1
        assert phases[0].get("phase_name") == "Malware"
        assert phases[0].get("kill_chain_name") == "microsoft"

    def test_alert_non_mitre_tactic(self):
        data = json.loads(json.dumps(device_event_with_alert))
        # alerts = json.loads(data['DeviceEvents']['Alerts'])
        # alerts[0]['Category'] = "Malware"
        # data['DeviceEvents']['Alerts'] = json.dumps(alerts)
        objects = translate_to_objects(data)
        finding = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        ttps = resolve_refs(objects, finding, "ttp_tagging_refs", "x-ibm-ttp-tagging",
                            "ttp tagging refs missing from finding")
        assert len(ttps) == 3
        ttp = ttps[0]
        assert "kill_chain_phases" in ttp
        phases = ttp["kill_chain_phases"]
        assert len(phases) == 1
        assert phases[0].get("phase_name") == "Malware"
        assert phases[0].get("kill_chain_name") == "microsoft"

    def test_alert_mitre_technique(self):
        data = json.loads(json.dumps(device_event_with_alert))
        alerts = json.loads(data['DeviceEvents']['Alerts'])
        alerts[0]['AttackTechniques'] = ['Spearphishing Link (T1566.002)']
        alerts[0]['Category'] = 'CredentialAccess'
        data['DeviceEvents']['Alerts'] = json.dumps(alerts)
        objects = translate_to_objects(data)
        finding = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        ttps = resolve_refs(objects, finding, "ttp_tagging_refs", "x-ibm-ttp-tagging",
                            "ttp tagging refs missing from finding")
        assert len(ttps) == 2
        tactic = ttps[0]
        assert "kill_chain_phases" in tactic
        phases = tactic["kill_chain_phases"]
        assert len(phases) == 1
        assert phases[0].get("phase_name") == "Credential Access"
        assert phases[0].get("kill_chain_name") == "mitre-attack"
        technique = ttps[1]
        assert "extensions" in technique
        assert "mitre-attack-ext" in technique["extensions"]
        assert technique["extensions"]["mitre-attack-ext"]["technique_name"] == "Spearphishing Link"
        assert technique["extensions"]["mitre-attack-ext"]["technique_id"] == "T1566.002"

    def test_event(self):
        """
        test x-oca-event
        """
        objects = translate_to_objects(device_event_with_alert)

        event = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert event is not None, 'event object type not found'
        assert event['action'] == "OtherAlertRelatedActivity"
        assert event.get("provider") == "Microsoft Defender for Endpoint"
        assert event.get("created") == "2023-03-27T08:32:10.8787764Z"
        external = resolve_ref(objects, event, "external_ref", "external-reference",
                               "missing external ref link in event")
        assert external.get(
            "url") == "https://security.microsoft.com/machines/deviceid/timeline?from=2023-03-27T08:32:09.000Z&to=2023-03-27T08:32:11.000Z"
        url = resolve_ref(objects, event, 'url_ref', "url", "missing url ref in event")
        assert url.get("value") == "https://malicious.com"
        domain = resolve_ref(objects, event, 'domain_ref', 'domain-name', 'missing domain ref in event')
        assert domain.get("value") == "malicious.com"
        resolve_ref(objects, event, "host_ref", "x-oca-asset", "missing host ref in event")
        process = resolve_ref(objects, event, "process_ref", "process", "missing process ref in event")
        assert process.get("pid") == 18808
        network = resolve_ref(objects, event, "network_ref", "network-traffic", "missing network ref in event")
        assert network.get("src_port") == 58993
        assert network.get("dst_port") == 443
        dst = resolve_ref(objects, network, "dst_ref", "ipv4-addr", "missing dst ip in network")
        assert dst.get("value") == "9.9.9.9"
        src = resolve_ref(objects, network, "src_ref", "ipv4-addr", "missing src ip in network")
        assert src.get("value") == "9.9.9.1"
        orig = resolve_ref(objects, event, "original_ref", "artifact", "missing original ref in event")
        assert orig.get("payload_bin") == "YmFzZTY0"

    def test_asset(self):
        """test x-oca-asset"""
        objects = translate_to_objects(device_process_event)

        event = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert event is not None, 'event object type not found'
        asset = resolve_ref(objects, event, "host_ref", "x-oca-asset", "host is missing")
        assert asset.get("hostname") == "host.test.com"
        assert asset.get("device_id") == "deviceid"
        assert asset.get("os_name") == "Windows10"
        ip_refs = resolve_refs(objects, asset, "ip_refs", "ipv4-addr", "ip refs are missing")
        assert len(ip_refs) == 1
        ip = ip_refs[0]
        assert ip.get("value") == "9.9.9.1"
        mac_refs = resolve_refs(objects, asset, "mac_refs", "mac-addr", "mac refs are missing")
        assert len(mac_refs) == 1
        mac = mac_refs[0]
        assert mac.get("value") == "11:22:33:44:55:66"

    def test_get_next_index_remove_ref(self):
        objects = {
            '0': {
                'type': 'x-oca-event',
                'ip_ref': '1',
                'ip_refs': ['2', '3']
            },
            '2': {
                'type': 'ipv4-addr',
                'value': '9.9.9.9'
            }
        }
        from stix_shifter_modules.msatp.stix_translation import results_translator
        index = results_translator.get_next_index(objects)
        assert index == "1"
        assert 'ip_ref' not in objects['0']

    def test_get_next_index_remove_refs(self):
        objects = {
            '0': {
                'type': 'x-oca-event',
                'ip_ref': '1',
                'ip_refs': ['2', '3']
            },
            '1': {
                'type': 'ipv4-addr',
                'value': '9.9.9.9'
            }
        }
        from stix_shifter_modules.msatp.stix_translation import results_translator
        index = results_translator.get_next_index(objects)
        assert index == "2"
        assert 'ip_ref' in objects['0']
        assert 'ip_refs' in objects['0']
        assert len(objects['0']['ip_refs']) == 1
        assert objects['0']['ip_refs'][0] == '3'

    def test_get_next_index_pops_refs(self):
        objects = {
            '0': {
                'type': 'x-oca-event',
                'ip_refs': ['1']
            }
        }
        from stix_shifter_modules.msatp.stix_translation import results_translator
        index = results_translator.get_next_index(objects)
        assert index == "1"
        assert 'ip_refs' not in objects['0']

    def test_extract_pipe_name(self):
        xmsatp = {
            'AdditionalFields': r'DesiredAccess: 1180063, FileOperation: File opened, NamedPipeEnd: Client, PipeName: \\Device\\NamedPipe\\PrinterProviderProbePipe01, RemoteClientsAccess: AcceptRemote, SessionId: 1, ThreadId: 11660'
        }
        from stix_shifter_modules.msatp.stix_translation import results_translator
        event = {}
        results_translator.extract_pipe_name(xmsatp, event)
        assert 'pipe_name' in event
        assert event['pipe_name'] == r'\\Device\\NamedPipe\\PrinterProviderProbePipe01'

    def test_delete_object(self):
        objects = {
            '0': {
                'type': 'x-oca-event',
                'ip_ref': '1',
                'other_ref': '2',
                'ip_refs': ['1', '2']
            },
            '1': {
                'type': 'ipv4-addr',
                'value': '9.9.9.9'
            },
            '2': {
                'type': 'ipv4-addr',
                'value': '9.9.9.1'
            }
        }
        from stix_shifter_modules.msatp.stix_translation import results_translator
        results_translator.delete_object(objects, '1')
        assert len(objects) == 2
        event = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert event is not None, 'event object type not found'
        assert 'ip_ref' not in event, 'ip_ref should have been removed'
        assert 'other_ref' in event, 'other_ref should not have been removed'
        assert event['other_ref'] == '1', 'other_ref reference was not decreased by one'
        assert 'ip_refs' in event
        assert len(event['ip_refs']) == 1
        assert event['ip_refs'][0] == '1'
        assert objects['1']['value'] == '9.9.9.1'

    def test_sort_objects(self):
        objects = {
            '0': {
                'type': 'x-oca-event'
            },
            '2': {
                'type': 'ipv4-addr',
                'value': '9.9.9.9'
            },
            '1': {
                'type': 'ipv4-addr',
                'value': '9.9.9.1'
            }
        }
        wanted_result = {
            '0': {
                'type': 'x-oca-event'
            },
            '1': {
                'type': 'ipv4-addr',
                'value': '9.9.9.1'
            },
            '2': {
                'type': 'ipv4-addr',
                'value': '9.9.9.9'
            }
        }
        from stix_shifter_modules.msatp.stix_translation import results_translator
        sorted_objects = results_translator.sort_objects(objects)
        list1 = [(key, value) for key, value in sorted_objects.items()]
        list2 = [(key, value) for key, value in wanted_result.items()]

        assert list1 == list2

    def test_add_object(self):
        observed = {
            'objects': {
                '0': {
                    'type': 'x-oca-event',
                    'ip_ref': '1',
                    'other_ref': '2',
                    'ip_refs': ['1', '2']
                },
                '1': {
                    'type': 'ipv4-addr',
                    'value': '9.9.9.9'
                },
                '2': {
                    'type': 'ipv4-addr',
                    'value': '9.9.9.1'
                }
            }
        }
        new_obj = {
            'type': 'url',
            'value': 'https://quad9.net'
        }
        from stix_shifter_modules.msatp.stix_translation import results_translator
        index = results_translator.add_to_objects(observed, new_obj)
        assert index == '3'
        assert observed['objects'] == {
            '0': {
                'type': 'x-oca-event',
                'ip_ref': '1',
                'other_ref': '2',
                'ip_refs': ['1', '2']
            },
            '1': {
                'type': 'ipv4-addr',
                'value': '9.9.9.9'
            },
            '2': {
                'type': 'ipv4-addr',
                'value': '9.9.9.1'
            },
            '3': {
                'type': 'url',
                'value': 'https://quad9.net'
            }
        }

    def test_add_object_unordered(self):
        observed = {
            'objects': {
                '0': {
                    'type': 'x-oca-event',
                    'ip_ref': '2',
                    'other_ref': '3',
                    'ip_refs': ['2', '3']
                },
                '2': {
                    'type': 'ipv4-addr',
                    'value': '9.9.9.9'
                },
                '3': {
                    'type': 'ipv4-addr',
                    'value': '9.9.9.1'
                }
            }
        }
        new_obj = {
            'type': 'url',
            'value': 'https://quad9.net'
        }
        from stix_shifter_modules.msatp.stix_translation import results_translator
        index = results_translator.add_to_objects(observed, new_obj)
        assert index == '1'
        assert observed['objects'] == {
            '0': {
                'type': 'x-oca-event',
                'ip_ref': '2',
                'other_ref': '3',
                'ip_refs': ['2', '3']
            },
            '1': {
                'type': 'url',
                'value': 'https://quad9.net'
            },
            '2': {
                'type': 'ipv4-addr',
                'value': '9.9.9.9'
            },
            '3': {
                'type': 'ipv4-addr',
                'value': '9.9.9.1'
            }
        }
