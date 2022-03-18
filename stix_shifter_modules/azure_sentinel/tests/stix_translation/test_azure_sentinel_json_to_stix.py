import json
import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.azure_sentinel.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "azure_sentinel"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--3532c56d-ea72-48be-a2ad-1a53f4c9c6d3",
    "name": "azure_sentinel",
    "identity_class": "events"
}
options = {}

DATA1 = {'id': '2518268485253060642_52b1a353-2fd8-4c45-8f8a-94db98dca29d',
                'azureTenantId': 'b73e5ba8-34d5-495a-9901-06bdb84cf13e',
                'azureSubscriptionId': '083de1fb-cd2d-4b7c-895a-2b5af1d091e8', 'category': 'SuspiciousSVCHOSTRareGroup',
                'createdDateTime': '2019-12-04T09:38:05.2024952Z',
                'description': 'The system process SVCHOST was observed running a rare service group. Malware often '
                               'use SVCHOST to masquerade its malicious activity.',
                'eventDateTime': '2019-12-04T09:37:54.6939357Z', 'lastModifiedDateTime': '2019-12-04T09:38:06.7571701Z',
                'recommendedActions': ['1. Run Process Explorer and try to identify unknown running processes (see '
                                        'https://technet.microsoft.com/en-us/sysinternals/bb896653.aspx)', 
                                        '2. Make sure the machine is completely updated and has an updated '
                                        'anti-malware application installed',
                                        '3. Run a full anti-malware scan and verify that the threat was removed',
                                        '4. Install and run Microsoft’s Malicious Software Removal Tool (see '
                                        'https://www.microsoft.com/en-us/download/malicious-software-removal-tool'                                       '-details.aspx)',
                                        '5. Run Microsoft’s Autoruns utility and try to identify unknown applications '
                                        'that are configured to run at login (see '
                                        'https://technet.microsoft.com/en-us/sysinternals/bb963902.aspx)'],
                'severity': 'informational', 'status': 'newAlert', 'title': 'Rare SVCHOST service group executed',
                'vendorInformation_provider': 'ASC', 'vendorInformation_subProvider': 'Detection',
                'vendorInformation_vendor': 'Microsoft', 'fileStates': [{'name': 'services.exe',
                'path': 'c:\\windows\\system32\\services.exe'}, {'name': 'svchost.exe',
                'path': 'c:\\windows\\system32\\svchost.exe'}], 'hostStates': [{'netBiosName': 'TEST-WINDOW',
                'os': 'Windows', 'commandLine': '', 'name': 'services.exe',
                'path': 'c:\\windows\\system32\\services.exe'}, {'accountName': 'test-window$',
                'commandLine': 'c:\\windows\\system32\\svchost.exe -k clipboardsvcgroup -p -s cbdhsvc',
                'createdDateTime': '2019-12-04T09:37:54.6939357Z', 'name': 'svchost.exe',
                'parentProcessName': 'services.exe', 'path': 'c:\\windows\\system32\\svchost.exe'}],
                'userStates': [{'accountName': 'test-window$', 'domainName': 'WORKGROUP', 'emailRole': 'unknown',
                'logonId': '0x3e7', 'onPremisesSecurityIdentifier': 'S-1-5-18', 'userPrincipalName': 'test-window$@TEST-WINDOW'}], 'event_count': '1'}

DATA2 = {'id': '2518267967999999999_13d684ad-1397-4db8-be04-9a7fe750bb1d',
                'azureTenantId': 'b73e5ba8-34d5-495a-9901-06bdb84cf13e',
                'azureSubscriptionId': '083de1fb-cd2d-4b7c-895a-2b5af1d091e8',
                'category': 'AdaptiveNetworkHardeningInbound', 'createdDateTime': '2019-12-06T10:25:09.1750985Z',
                'description': 'Azure security center has detected incoming traffic from IP addresses, which have '
                               'been identified as IP addresses that should be blocked by the Adaptive Network '
                               'Hardening control',
                'eventDateTime': '2019-12-05T00:00:00Z', 'lastModifiedDateTime': '2019-12-06T10:25:12.3478085Z',
                'recommendedActions': ['{"kind":"openBlade","displayValue":"Enforce rule",'
                                        '"extension":"Microsoft_Azure_Security_R3",'
                                        '"detailBlade":"AdaptiveNetworkControlsResourceBlade",'
                                        '"detailBladeInputs":"protectedResourceId=/subscriptions/083de1fb-cd2d-4b7c'
                                        '-895a-2b5af1d091e8/resourcegroups/eastus/providers/microsoft.compute'
                                        '/virtualmachines/bigfixcentos"}'],
                'severity': 'low', 'status': 'newAlert',
                'title': 'Traffic from unrecommended IP addresses was detected', 'vendorInformation_provider': 'ASC',
                'vendorInformation_subProvider': 'AdaptiveNetworkHardenings', 'vendorInformation_vendor': 'Microsoft',
                "networkConnections": [{"applicationName": "Microsoft", "destinationAddress": "61.23.79.168", "destinationDomain": None, 
                "destinationLocation": None, "destinationPort": "22", "destinationUrl": None, "direction": None, 
                "domainRegisteredDateTime": None, "localDnsName": None, "natDestinationAddress": None, "natDestinationPort": None, 
                "natSourceAddress": None, "natSourcePort": None, "protocol": "tcp", "riskScore": None, "sourceAddress": "118.32.223.14", 
                "sourceLocation": None, "sourcePort": "9475", "status": None, "urlParameters": None}], 'event_count': '1'}

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
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA1], get_module_transformers(MODULE), options)
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
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA1], get_module_transformers(MODULE), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        
        assert 'objects' in observed_data
        objects = observed_data['objects']
        
        x_msazure_sentinel = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'x-msazure-sentinel')
        x_msazure_sentinel_alert = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'x-msazure-sentinel-alert')
        x_ibm_finding = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        x_oca_event = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')

        assert x_msazure_sentinel is not None, 'Custom object type not found'
        assert x_msazure_sentinel.keys() == {'type', 'tenant_id', 'subscription_id'}
        assert x_msazure_sentinel['tenant_id'] == 'b73e5ba8-34d5-495a-9901-06bdb84cf13e'
        assert x_msazure_sentinel['subscription_id'] == '083de1fb-cd2d-4b7c-895a-2b5af1d091e8'

        assert x_msazure_sentinel_alert is not None, 'Custom object type not found'

        assert x_msazure_sentinel_alert.keys() == {'type', 'recommendedactions', 'status', 'userStates'}
        assert type(x_msazure_sentinel_alert['recommendedactions']) is list
        assert x_ibm_finding.keys() == {'type', 'createddatetime', 'description', 'time_observed', 'severity', 'name', 'src_os_ref'}
        assert x_ibm_finding['name'] == 'Rare SVCHOST service group executed'
        assert x_oca_event.keys() == {'type', 'code', 'category', 'created', 'action'}
        assert x_oca_event['category'] == 'SuspiciousSVCHOSTRareGroup'
        # assert False

    @staticmethod
    def test_file_process_json_to_stix():
        """
        to test file stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA1], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        file_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'file')
        directory_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'directory')

        assert file_obj is not None, 'file object type not found'
        assert file_obj .keys() == {'type', 'name', 'parent_directory_ref'}
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'services.exe'
        assert file_obj['parent_directory_ref'] == '5'
        assert directory_obj['path'] == 'c:\\windows\\system32'

    @staticmethod
    def test_network_json_to_stix():
        """
        to test network stix object properties
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA2], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestAzureSentinelResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert network_obj is not None, 'network-traffic object type not found'
        assert network_obj.keys() == {'type', 'dst_ref', 'dst_port', 'protocols', 'src_ref','src_port'}
        assert network_obj['type'] == 'network-traffic'
        assert network_obj['src_port'] == 9475
        assert network_obj['dst_port'] == 22
        assert network_obj['protocols'] == ['tcp']
        assert network_obj['src_ref'] == '7'
        assert network_obj['dst_ref'] == '5'

    @staticmethod
    def test_network_json_to_stix_negative():
        """
        to test negative test case for stix object
        """
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [DATA2], get_module_transformers(MODULE), options)
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
            data_source, map_data, [data], get_module_transformers(MODULE), options)
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
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        observed_data = result_bundle_objects[1]
        assert 'objects' in observed_data
        objects = observed_data['objects']
        assert objects == {}
