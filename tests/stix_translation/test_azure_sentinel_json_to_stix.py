import json
from stix_shifter.stix_translation.src.utils import transformers
from stix_shifter.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter.stix_translation.src.modules.azure_sentinel import azure_sentinel_translator
import unittest

interface = azure_sentinel_translator.Translator()
map_file = open(interface.mapping_filepath).read()
map_data = json.loads(map_file)
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "azure_sentinel",
    "identity_class": "events"
}
options = {}


class TestAzureSentinelResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for azure_sentinel translate results
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
        return TestAzureSentinelResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def test_common_prop():
        """
        to test the common stix object properties
        """
        data = {'id': '2518268485253060642_52b1a353-2fd8-4c45-8f8a-94db98dca29d',
                'azureTenantId': 'b73e5ba8-34d5-495a-9901-06bdb84cf13e',
                'azureSubscriptionId': '083de1fb-cd2d-4b7c-895a-2b5af1d091e8', 'category': 'SuspiciousSVCHOSTRareGroup',
                'createdDateTime': '2019-12-04T09:38:05.2024952Z',
                'description': 'The system process SVCHOST was observed running a rare service group. Malware often '
                               'use SVCHOST to masquerade its malicious activity.',
                'eventDateTime': '2019-12-04T09:37:54.6939357Z', 'lastModifiedDateTime': '2019-12-04T09:38:06.7571701Z',
                'recommendedActions_0': '1. Run Process Explorer and try to identify unknown running processes (see '
                                        'https://technet.microsoft.com/en-us/sysinternals/bb896653.aspx)',
                'recommendedActions_1': '2. Make sure the machine is completely updated and has an updated '
                                        'anti-malware application installed',
                'recommendedActions_2': '3. Run a full anti-malware scan and verify that the threat was removed',
                'recommendedActions_3': '4. Install and run Microsoft’s Malicious Software Removal Tool (see '
                                        'https://www.microsoft.com/en-us/download/malicious-software-removal-tool'
                                        '-details.aspx)',
                'recommendedActions_4': '5. Run Microsoft’s Autoruns utility and try to identify unknown applications '
                                        'that are configured to run at login (see '
                                        'https://technet.microsoft.com/en-us/sysinternals/bb963902.aspx)',
                'severity': 'informational', 'status': 'newAlert', 'title': 'Rare SVCHOST service group executed',
                'vendorInformation_provider': 'ASC', 'vendorInformation_subProvider': 'Detection',
                'vendorInformation_vendor': 'Microsoft', 'fileStates_0_name': 'services.exe',
                'fileStates_0_path': 'c:\\windows\\system32\\services.exe', 'fileStates_1_name': 'svchost.exe',
                'fileStates_1_path': 'c:\\windows\\system32\\svchost.exe', 'hostStates_0_netBiosName': 'TEST-WINDOW',
                'hostStates_0_os': 'Windows', 'processes_0_commandLine': '', 'processes_0_name': 'services.exe',
                'processes_0_path': 'c:\\windows\\system32\\services.exe', 'processes_1_accountName': 'test-window$',
                'processes_1_commandLine': 'c:\\windows\\system32\\svchost.exe -k clipboardsvcgroup -p -s cbdhsvc',
                'processes_1_createdDateTime': '2019-12-04T09:37:54.6939357Z', 'processes_1_name': 'svchost.exe',
                'processes_1_parentProcessName': 'services.exe',
                'processes_1_path': 'c:\\windows\\system32\\svchost.exe', 'userStates_0_accountName': 'test-window$',
                'userStates_0_domainName': 'WORKGROUP', 'userStates_0_emailRole': 'unknown',
                'userStates_0_logonId': '0x3e7', 'userStates_0_onPremisesSecurityIdentifier': 'S-1-5-18',
                'userStates_0_userPrincipalName': 'test-window$@TEST-WINDOW', 'event_count': '1'}
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

        assert observed_data['modified'] is not None
        assert observed_data['created'] is not None
        assert observed_data['first_observed'] is not None
        assert observed_data['last_observed'] is not None
        assert observed_data['number_observed'] is not None

    @staticmethod
    def test_custom_property():
        """
        to test the custom stix object properties
        """
        data = {'id': '2518268485253060642_52b1a353-2fd8-4c45-8f8a-94db98dca29d',
                'azureTenantId': 'b73e5ba8-34d5-495a-9901-06bdb84cf13e',
                'azureSubscriptionId': '083de1fb-cd2d-4b7c-895a-2b5af1d091e8', 'category': 'SuspiciousSVCHOSTRareGroup',
                'createdDateTime': '2019-12-04T09:38:05.2024952Z',
                'description': 'The system process SVCHOST was observed running a rare service group. Malware often '
                               'use SVCHOST to masquerade its malicious activity.',
                'eventDateTime': '2019-12-04T09:37:54.6939357Z', 'lastModifiedDateTime': '2019-12-04T09:38:06.7571701Z',
                'recommendedActions_0': '1. Run Process Explorer and try to identify unknown running processes (see '
                                        'https://technet.microsoft.com/en-us/sysinternals/bb896653.aspx)',
                'recommendedActions_1': '2. Make sure the machine is completely updated and has an updated '
                                        'anti-malware application installed',
                'recommendedActions_2': '3. Run a full anti-malware scan and verify that the threat was removed',
                'recommendedActions_3': '4. Install and run Microsoft’s Malicious Software Removal Tool (see '
                                        'https://www.microsoft.com/en-us/download/malicious-software-removal-tool'
                                        '-details.aspx)',
                'recommendedActions_4': '5. Run Microsoft’s Autoruns utility and try to identify unknown applications '
                                        'that are configured to run at login (see '
                                        'https://technet.microsoft.com/en-us/sysinternals/bb963902.aspx)',
                'severity': 'informational', 'status': 'newAlert', 'title': 'Rare SVCHOST service group executed',
                'vendorInformation_provider': 'ASC', 'vendorInformation_subProvider': 'Detection',
                'vendorInformation_vendor': 'Microsoft', 'fileStates_0_name': 'services.exe',
                'fileStates_0_path': 'c:\\windows\\system32\\services.exe', 'fileStates_1_name': 'svchost.exe',
                'fileStates_1_path': 'c:\\windows\\system32\\svchost.exe', 'hostStates_0_netBiosName': 'TEST-WINDOW',
                'hostStates_0_os': 'Windows', 'processes_0_commandLine': '', 'processes_0_name': 'services.exe',
                'processes_0_path': 'c:\\windows\\system32\\services.exe', 'processes_1_accountName': 'test-window$',
                'processes_1_commandLine': 'c:\\windows\\system32\\svchost.exe -k clipboardsvcgroup -p -s cbdhsvc',
                'processes_1_createdDateTime': '2019-12-04T09:37:54.6939357Z', 'processes_1_name': 'svchost.exe',
                'processes_1_parentProcessName': 'services.exe',
                'processes_1_path': 'c:\\windows\\system32\\svchost.exe', 'userStates_0_accountName': 'test-window$',
                'userStates_0_domainName': 'WORKGROUP', 'userStates_0_emailRole': 'unknown',
                'userStates_0_logonId': '0x3e7', 'userStates_0_onPremisesSecurityIdentifier': 'S-1-5-18',
                'userStates_0_userPrincipalName': 'test-window$@TEST-WINDOW', 'event_count': '1'}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        observed_data = result_bundle_objects[1]
        custom_object_1 = observed_data['x_com_msazure_sentinel']
        custom_object_2 = observed_data['x_com_msazure_sentinel_alert']

        assert custom_object_1.keys() == {'tenant_id', 'subscription_id'}
        assert custom_object_2.keys() == {'id','title', 'provider', 'vendor'}

        assert custom_object_1['tenant_id'] == 'b73e5ba8-34d5-495a-9901-06bdb84cf13e'
        assert custom_object_1['subscription_id'] == '083de1fb-cd2d-4b7c-895a-2b5af1d091e8'
        assert custom_object_2['id'] == '2518268485253060642_52b1a353-2fd8-4c45-8f8a-94db98dca29d'
        assert custom_object_2['title'] == 'Rare SVCHOST service group executed'
        assert custom_object_2['provider'] == 'ASC'
        assert custom_object_2['vendor'] == 'Microsoft'

    @staticmethod
    def test_file_process_json_to_stix():
        """
        to test file stix object properties
        """
        data = {'id': '2518268485253060642_52b1a353-2fd8-4c45-8f8a-94db98dca29d',
                'azureTenantId': 'b73e5ba8-34d5-495a-9901-06bdb84cf13e',
                'azureSubscriptionId': '083de1fb-cd2d-4b7c-895a-2b5af1d091e8', 'category': 'SuspiciousSVCHOSTRareGroup',
                'createdDateTime': '2019-12-04T09:38:05.2024952Z',
                'description': 'The system process SVCHOST was observed running a rare service group. Malware often '
                               'use SVCHOST to masquerade its malicious activity.',
                'eventDateTime': '2019-12-04T09:37:54.6939357Z', 'lastModifiedDateTime': '2019-12-04T09:38:06.7571701Z',
                'recommendedActions_0': '1. Run Process Explorer and try to identify unknown running processes (see '
                                        'https://technet.microsoft.com/en-us/sysinternals/bb896653.aspx)',
                'recommendedActions_1': '2. Make sure the machine is completely updated and has an updated '
                                        'anti-malware application installed',
                'recommendedActions_2': '3. Run a full anti-malware scan and verify that the threat was removed',
                'recommendedActions_3': '4. Install and run Microsoft’s Malicious Software Removal Tool (see '
                                        'https://www.microsoft.com/en-us/download/malicious-software-removal-tool'
                                        '-details.aspx)',
                'recommendedActions_4': '5. Run Microsoft’s Autoruns utility and try to identify unknown applications '
                                        'that are configured to run at login (see '
                                        'https://technet.microsoft.com/en-us/sysinternals/bb963902.aspx)',
                'severity': 'informational', 'status': 'newAlert', 'title': 'Rare SVCHOST service group executed',
                'vendorInformation_provider': 'ASC', 'vendorInformation_subProvider': 'Detection',
                'vendorInformation_vendor': 'Microsoft', 'fileStates_0_name': 'services.exe',
                'fileStates_0_path': 'c:\\windows\\system32\\services.exe', 'fileStates_1_name': 'svchost.exe',
                'fileStates_1_path': 'c:\\windows\\system32\\svchost.exe', 'hostStates_0_netBiosName': 'TEST-WINDOW',
                'hostStates_0_os': 'Windows', 'processes_0_commandLine': '', 'processes_0_name': 'services.exe',
                'processes_0_path': 'c:\\windows\\system32\\services.exe', 'processes_1_accountName': 'test-window$',
                'processes_1_commandLine': 'c:\\windows\\system32\\svchost.exe -k clipboardsvcgroup -p -s cbdhsvc',
                'processes_1_createdDateTime': '2019-12-04T09:37:54.6939357Z', 'processes_1_name': 'svchost.exe',
                'processes_1_parentProcessName': 'services.exe',
                'processes_1_path': 'c:\\windows\\system32\\svchost.exe', 'userStates_0_accountName': 'test-window$',
                'userStates_0_domainName': 'WORKGROUP', 'userStates_0_emailRole': 'unknown',
                'userStates_0_logonId': '0x3e7', 'userStates_0_onPremisesSecurityIdentifier': 'S-1-5-18',
                'userStates_0_userPrincipalName': 'test-window$@TEST-WINDOW', 'event_count': '1'}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)

        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        file_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'file')
        process_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'process')

        assert file_obj is not None, 'file object type not found'
        assert file_obj .keys() == {'type', 'name', 'parent_directory_ref'}
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'services.exe'
        assert file_obj['parent_directory_ref'] == '1'
        assert process_obj is not None, 'file object type not found'
        assert process_obj.keys() == {'type', 'name', 'binary_ref'}
        assert process_obj['type'] == 'process'
        assert process_obj['name'] == 'services.exe'
        assert process_obj['binary_ref'] == '0'

    @staticmethod
    def test_network_json_to_stix():
        """
        to test network stix object properties
        """
        data = {'id': '2518267967999999999_13d684ad-1397-4db8-be04-9a7fe750bb1d',
                'azureTenantId': 'b73e5ba8-34d5-495a-9901-06bdb84cf13e',
                'azureSubscriptionId': '083de1fb-cd2d-4b7c-895a-2b5af1d091e8',
                'category': 'AdaptiveNetworkHardeningInbound', 'createdDateTime': '2019-12-06T10:25:09.1750985Z',
                'description': 'Azure security center has detected incoming traffic from IP addresses, which have '
                               'been identified as IP addresses that should be blocked by the Adaptive Network '
                               'Hardening control',
                'eventDateTime': '2019-12-05T00:00:00Z', 'lastModifiedDateTime': '2019-12-06T10:25:12.3478085Z',
                'recommendedActions_0': '{"kind":"openBlade","displayValue":"Enforce rule",'
                                        '"extension":"Microsoft_Azure_Security_R3",'
                                        '"detailBlade":"AdaptiveNetworkControlsResourceBlade",'
                                        '"detailBladeInputs":"protectedResourceId=/subscriptions/083de1fb-cd2d-4b7c'
                                        '-895a-2b5af1d091e8/resourcegroups/eastus/providers/microsoft.compute'
                                        '/virtualmachines/bigfixcentos"}',
                'severity': 'low', 'status': 'newAlert',
                'title': 'Traffic from unrecommended IP addresses was detected', 'vendorInformation_provider': 'ASC',
                'vendorInformation_subProvider': 'AdaptiveNetworkHardenings', 'vendorInformation_vendor': 'Microsoft',
                'networkConnections_0_destinationPort': '22', 'networkConnections_0_protocol': 'tcp',
                'networkConnections_0_sourceAddress': '118.32.223.14', 'event_count': '1'}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert network_obj is not None, 'network-traffic object type not found'
        assert network_obj.keys() == {'type', 'dst_port', 'protocols', 'src_ref'}
        assert network_obj['type'] == 'network-traffic'
        assert network_obj['dst_port'] == 22
        assert network_obj['protocols'] == ['tcp']
        assert network_obj['src_ref'] == '1'

    @staticmethod
    def test_network_json_to_stix_negative():
        """
        to test negative test case for stix object
        """
        data = [{'id': '2518267967999999999_13d684ad-1397-4db8-be04-9a7fe750bb1d',
                 'azureTenantId': 'b73e5ba8-34d5-495a-9901-06bdb84cf13e',
                 'azureSubscriptionId': '083de1fb-cd2d-4b7c-895a-2b5af1d091e8',
                 'category': 'AdaptiveNetworkHardeningInbound', 'createdDateTime': '2019-12-06T10:25:09.1750985Z',
                 'description': 'Azure security center has detected incoming traffic from IP addresses, which have '
                                'been identified as IP addresses that should be blocked by the Adaptive Network '
                                'Hardening control',
                 'eventDateTime': '2019-12-05T00:00:00Z', 'lastModifiedDateTime': '2019-12-06T10:25:12.3478085Z',
                 'recommendedActions_0': '{"kind":"openBlade","displayValue":"Enforce rule",'
                                         '"extension":"Microsoft_Azure_Security_R3",'
                                         '"detailBlade":"AdaptiveNetworkControlsResourceBlade",'
                                         '"detailBladeInputs":"protectedResourceId=/subscriptions/083de1fb-cd2d-4b7c'
                                         '-895a-2b5af1d091e8/resourcegroups/eastus/providers/microsoft.compute'
                                         '/virtualmachines/bigfixcentos"}',
                 'severity': 'low', 'status': 'newAlert',
                 'title': 'Traffic from unrecommended IP addresses was detected', 'vendorInformation_provider': 'ASC',
                 'vendorInformation_subProvider': 'AdaptiveNetworkHardenings', 'vendorInformation_vendor': 'Microsoft',
                 'networkConnections_0_destinationPort': '22', 'networkConnections_0_protocol': 'tcp',
                 'networkConnections_0_sourceAddress': '118.32.223.14', 'event_count': '1'}]
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, data, transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'file')
        assert network_obj is None

    @staticmethod
    def test_unmapped_attribute_with_mapped_attribute():
        message = "\"GET /blog HTTP/1.1\" 200 2571"
        data = {"message": message, "unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']
        assert objects == {}
        curr_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'message')
        assert (curr_obj is None), 'url object type not found'

    @staticmethod
    def test_unmapped_attribute_alone():
        data = {"unmapped": "nothing to see here"}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']
        assert objects == {}
