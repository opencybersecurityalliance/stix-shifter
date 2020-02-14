from stix_shifter.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter.stix_translation.src.utils import transformers
from stix_shifter.stix_translation.src.modules.msatp import msatp_translator
import json
import unittest

interface = msatp_translator.Translator()
map_file = open(interface.mapping_filepath).read()

map_data = json.loads(map_file)
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "msatp",
    "identity_class": "events"
}
options = {}


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
        data = {'ProcessCreationEvents': {'EventTime': '2019-09-20T06:57:11.8218304Z',
                                          'MachineId': '8330ed311f1b21b861d63448984eb2632cc9c07c',
                                          'ComputerName': 'desktop-536bt46', 'ActionType': 'ProcessCreated',
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
            data_source, map_data, [data], transformers.get_all_transformers(), options)
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
        assert observed_data['x_com_msatp'] is not None

    def test_custom_property(self):
        """
        to test the custom stix object properties
        """
        data = {'ProcessCreationEvents': {'EventTime': '2019-09-20T06:57:11.8218304Z',
                                          'MachineId': '8330ed311f1b21b861d63448984eb2632cc9c07c',
                                          'ComputerName': 'desktop-536bt46', 'ActionType': 'ProcessCreated',
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
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        observed_data = result_bundle_objects[1]
        custom_object = observed_data['x_com_msatp']
        assert custom_object.keys() == {'computer_name', 'machine_id'}
        assert custom_object['computer_name'] == 'desktop-536bt46'

    def test_file_json_to_stix(self):
        """
        to test file stix object properties
        """
        data = {'FileCreationEvents': {'EventTime': '2019-09-20T06:50:17.3764965Z',
                                       'MachineId': '8330ed311f1b21b861d63448984eb2632cc9c07c',
                                       'ComputerName': 'desktop-536bt46', 'ActionType': 'FileCreated',
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
            data_source, map_data, [data], transformers.get_all_transformers(), options)

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
        assert file_obj['parent_directory_ref'] == '1'
        directory_object = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'directory')
        assert directory_object.get('path') == data['FileCreationEvents']['FolderPath']

    def test_process_json_to_stix(self):
        """
        to test process stix object properties
        """
        data = {'ProcessCreationEvents': {'EventTime': '2019-09-20T06:57:11.8218304Z',
                                          'MachineId': '8330ed311f1b21b861d63448984eb2632cc9c07c',
                                          'ComputerName': 'desktop-536bt46', 'ActionType': 'ProcessCreated',
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
                                          'ReportId': 12048, 'rn': 1, 'Event_count': '1'}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        process_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'process')
        assert process_obj is not None, 'process object type not found'
        assert process_obj.keys() == {'type', 'name', 'binary_ref', 'pid', 'command_line', 'created',
                                      'creator_user_ref', 'parent_ref'}
        assert process_obj['type'] == 'process'
        assert process_obj['name'] == 'consent.exe'
        assert process_obj['binary_ref'] == '0'
        assert process_obj['pid'] == 20948
        assert process_obj['command_line'] == 'consent.exe 10088 288 000001CB3AA92A80'
        assert process_obj['created'] == '2019-09-20T06:57:11.821Z'
        assert process_obj['creator_user_ref'] == '3'
        assert process_obj['parent_ref'] == '5'

    def test_network_json_to_stix(self):
        """to test network stix object properties"""
        data = {'NetworkCommunicationEvents': {'EventTime': '2019-09-26T09:47:52.7091342Z',
                                               'MachineId': '8330ed311f1b21b861d63448984eb2632cc9c07c',
                                               'ComputerName': 'desktop-536bt46', 'ActionType': 'ConnectionSuccess',
                                               'RemoteIP': '168.159.213.203', 'RemotePort': 80,
                                               'LocalIP': '172.16.2.22', 'LocalPort': 52240, 'Protocol': 'TcP',
                                               'LocalIPType': 'Private', 'RemoteIPType': 'Public',
                                               'InitiatingProcessSHA1': 'c12506914be39ee4f152369b6a6692733b1b70e9',
                                               'InitiatingProcessMD5': 'e407c42454e8520daca3eea0353967fb',
                                               'InitiatingProcessFileName': 'Microsoft.Photos.exe',
                                               'InitiatingProcessId': 10756,
                                               'InitiatingProcessCommandLine': '"Microsoft.Photos.exe" '
                                                                               '-ServerName:App.AppXzst44mncqdg8'
                                                                               '4v7sv6p7yznqwssy6f7f.mca',
                                               'InitiatingProcessCreationTime': '2019-09-26T09:32:10.8711434Z',
                                               'InitiatingProcessFolderPath': 'c:\\program '
                                                                              'files\\windowsapps\\microsoft.windows'
                                                                              '.photos_2019.19071.17920.0_x64__8wekyb'
                                                                              '3d8bbwe\\microsoft.photos.exe',
                                               'InitiatingProcessParentFileName': 'svchost.exe',
                                               'InitiatingProcessParentId': 1020,
                                               'InitiatingProcessParentCreationTime': '2019-09-17T14:55:00.5337848Z',
                                               'InitiatingProcessAccountDomain': 'desktop-536bt46',
                                               'InitiatingProcessAccountName': 'admin',
                                               'InitiatingProcessAccountSid':
                                                   'S-1-5-21-2603683697-4187888953-3873858-1001',
                                               'InitiatingProcessIntegrityLevel': 'Low',
                                               'InitiatingProcessTokenElevation': 'TokenElevationTypeLimited',
                                               'ReportId': 24239, 'rn': 1, 'event_count': '1'}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
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
        assert network_obj['dst_ref'] == '0'
        assert network_obj['dst_port'] == 80
        assert network_obj['src_ref'] == '2'
        assert network_obj['src_port'] == 52240
        assert network_obj['protocols'] == ['tcp']

    def test_network_json_to_stix_negative(self):
        """to test negative test case for stix object"""
        data = {'NetworkCommunicationEvents': {'EventTime': '2019-09-20T06:24:16.830101Z',
                                               'MachineId': '8330ed311f1b21b861d63448984eb2632cc9c07c',
                                               'ComputerName': 'desktop-536bt46', 'ActionType': 'ConnectionSuccess',
                                               'RemoteIP': '168.159.213.203', 'RemotePort': 80,
                                               'RemoteUrl': 'https://play.google.com', 'LocalIP': '172.16.2.22',
                                               'LocalPort': 63043, 'Protocol': 'TcpV4',
                                               'InitiatingProcessSHA1': 'f6af6cd298f660ff5bb4f89398d1d3edac020a7d',
                                               'InitiatingProcessMD5': '94e4f3e52bae1a934889aaeb7238dccc',
                                               'InitiatingProcessFileName': 'chrome.exe', 'InitiatingProcessId': 10404,
                                               'InitiatingProcessCommandLine': '"chrome.exe" --type=utility '
                                                                               '--field-trial-handle=1632,'
                                                                               '12328523307506075385,'
                                                                               '13359799139346648205,'
                                                                               '131072 --lang=en-US '
                                                                               '--service-sandbox-type=network '
                                                                               '--service-request-channel-token='
                                                                               '12003267709621771016 --mojo-platform'
                                                                               '-channel-handle=2064 /prefetch:8',
                                               'InitiatingProcessCreationTime': '2019-09-18T04:54:26.1863029Z',
                                               'InitiatingProcessFolderPath': 'c:\\program files ('
                                                                              'x86)\\google\\chrome\\application\\chrome.exe',
                                               'InitiatingProcessParentFileName': 'chrome.exe',
                                               'InitiatingProcessParentId': 9792,
                                               'InitiatingProcessParentCreationTime': '2019-09-18T04:54:24.3181704Z',
                                               'InitiatingProcessAccountDomain': 'desktop-536bt46',
                                               'InitiatingProcessAccountName': 'admin',
                                               'InitiatingProcessAccountSid':
                                                   'S-1-5-21-2603683697-4187888953-3873858-1001',
                                               'InitiatingProcessIntegrityLevel': 'Medium',
                                               'InitiatingProcessTokenElevation': 'TokenElevationTypeLimited',
                                               'ReportId': 10787, 'rn': 1, 'event_count': '1'}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, data, transformers.get_all_transformers(), options)
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
        data = {'NetworkCommunicationEvents': {'EventTime': '2019-09-20T06:24:16.830101Z',
                                               'MachineId': '8330ed311f1b21b861d63448984eb2632cc9c07c',
                                               'ComputerName': 'desktop-536bt46', 'LocalIP': '172.16.2.22',
                                               'MacAddress': '484D7E9DBD97', 'RemoteIP': '168.159.213.203',
                                               'LocalPort': 63043, 'RemotePort': 80, 'Protocol': 'TcpV4',
                                               'RemoteUrl': 'https://play.google.com',
                                               'InitiatingProcessSHA1': 'f6af6cd298f660ff5bb4f89398d1d3edac020a7d',
                                               'InitiatingProcessMD5': '94e4f3e52bae1a934889aaeb7238dccc',
                                               'InitiatingProcessFileName': 'chrome.exe',
                                               'InitiatingProcessParentFileName': 'chrome.exe',
                                               'InitiatingProcessId': 10404, 'InitiatingProcessParentId': 9792,
                                               'InitiatingProcessCommandLine': '"chrome.exe" --type=utility '
                                                                               '--field-trial-handle=1632,'
                                                                               '12328523307506075385,'
                                                                               '13359799139346648205,'
                                                                               '131072 --lang=en-US '
                                                                               '--service-sandbox-type=network '
                                                                               '--service-request-channel-token'
                                                                               '=12003267709621771016 --mojo-platform-'
                                                                               'channel-handle=2064 /prefetch:8',
                                               'InitiatingProcessCreationTime': '2019-09-18T04:54:26.1863029Z',
                                               'InitiatingProcessParentCreationTime': '2019-09-18T04:54:24.3181704Z',
                                               'InitiatingProcessAccountSid':
                                                   'S-1-5-21-2603683697-4187888953-3873858-1001',
                                               'InitiatingProcessAccountName': 'admin',
                                               'InitiatingProcessFolderPath': 'c:\\program files ('
                                                                              'x86)\\google\\chrome\\application\\chrome.exe',
                                               'rn': 1, 'event_count': '1'}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
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
        assert network_obj['value'] == '48:4d:7e:9d:bd:97'

    def test_registry_json_to_stix(self):
        """to test registry stix object properties"""
        data = {'RegistryEvents': {'EventTime': '2019-10-10T10:41:43.0469296Z',
                                   'MachineId': 'db40e68dd7358aa450081343587941ce96ca4777',
                                   'ComputerName': 'testmachine1', 'ActionType': 'RegistryValueSet',
                                   'RegistryKey': 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Advanced Threat '
                                                  'Protection',
                                   'PreviousRegistryValueName': 'Configuration',
                                   'InitiatingProcessAccountDomain': 'nt authority',
                                   'InitiatingProcessAccountName': 'system', 'InitiatingProcessAccountSid': 'S-1-5-18',
                                   'InitiatingProcessSHA1': '657cd516b52b861ae98670c2ab10dc4a467cfd80',
                                   'InitiatingProcessMD5': 'b97799c4a1ed64e97c9fa83401e8d67c',
                                   'InitiatingProcessFileName': 'mssense.exe', 'InitiatingProcessId': 1040,
                                   'InitiatingProcessCommandLine': '"MsSense.exe"',
                                   'InitiatingProcessCreationTime': '2019-10-10T10:41:29.2621221Z',
                                   'InitiatingProcessFolderPath': 'c:\\program files\\windows defender advanced threat '
                                                                  'protection\\mssense.exe',
                                   'InitiatingProcessParentId': 776, 'InitiatingProcessParentFileName': 'services.exe',
                                   'InitiatingProcessParentCreationTime': '2019-10-10T10:26:00.1611536Z',
                                   'InitiatingProcessIntegrityLevel': 'System',
                                   'InitiatingProcessTokenElevation': 'TokenElevationTypeDefault', 'ReportId': 89,
                                   'rn': 1, 'RegistryValues':
                                       [{'RegistryValueType': 'Binary', 'RegistryValueName': 'Configuration'}],
                                   'event_count': '1'}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestMsatpResultsToStix.get_first_of_type(objects.values(), 'windows-registry-key')
        assert network_obj is not None, 'windows-registry-key object type not found'
        assert network_obj.keys() == {'type', 'key', 'values'}
        assert network_obj['type'] == 'windows-registry-key'
        assert network_obj['key'] == 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows Advanced Threat Protection'
        assert network_obj['values'] == [{'data_type': 'REG_BINARY', 'name': 'Configuration'}]
