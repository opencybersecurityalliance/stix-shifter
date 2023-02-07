import unittest
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_modules.paloalto.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "paloalto"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "paloalto",
    "identity_class": "events"
}
options = {}


class TestPaloaltoResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for paloalto translate results
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
        return TestPaloaltoResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    def test_file_json_to_stix(self):
        """to test File stix object properties"""

        data = {'xdr_data': {'action_file_name': 'arp_cache_periodic.py',
                             'action_file_size': '7943',
                             'action_file_md5': 'f9d1ba13674eaf75c129534aba30487e',
                             'action_module_md5': 'a2f22af507acc1961cf9504491f3e4b0',
                             'action_process_image_md5': '93f1eb1ed4475f58f6870a385021c92d',
                             'action_file_sha256': 'f6c82fe48662c1e6fa1b4732c020672bd6a929d0e0102712a4064d5c1351bfaf',
                             'action_module_sha256': '2e365914142b4c0f8340594e253e8fa25f452338238b87e7d303af89d0747d78',
                             'action_process_image_sha256': 'b55e59f545cdb5866b538c46fc280e51b4955df6b3a\
                                                                                76686a73e80333757f003',
                             'actor_process_file_access_time': '1634092022616',
                             'os_actor_process_file_access_time': '1634096052944',
                             'actor_process_file_mod_time': '1640745638339',
                             'os_actor_process_file_mod_time': '1634096052944',
                             'actor_process_file_create_time': '1631299512000',
                             'os_actor_process_file_create_time': '1644385345812',
                             'action_file_path': 'C:\\Program Files (x86)\\Google\\Policies',
                             'action_process_image_path': 'C:\\Windows\\System32\\wevtutil.exe',
                             'action_registry_file_path': 'C:\\Windows\\AppCompat\\Programs\\Amcache.hve',
                             'actor_process_image_path': 'C:\\Program Files\\Amazon\\SSM\\amazon-ssm-agent.exe',
                             'causality_actor_process_image_path': 'C:\\Windows\\System32\\lsass.exe',
                             'os_actor_process_image_path': 'C:\\Program Files\\Amazon\\SSM\\amazon-ssm-agent.exe'
                             }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        file_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'file')
        assert file_obj is not None
        assert file_obj['type'] == 'file'
        assert file_obj['name'] == 'arp_cache_periodic.py'
        assert file_obj['size'] == 7943

    def test_process_json_to_stix(self):
        """  to test process stix object properties  """
        data = {'xdr_data': {'action_process_image_command_line': 'C:\\Windows\\system32\\lsass.exe',
                             'actor_process_command_line': 'C:\\Windows\\system32\\lsass.exe',
                             'causality_actor_process_command_line': 'C:\\Windows\\system32\\lsass.exe',
                             'os_actor_process_command_line': 'C:\\Windows\\system32\\lsass.exe',
                             'actor_process_file_create_time': '1631299512000',
                             'causality_actor_process_file_create_time': '1536995564723',
                             'os_actor_process_file_create_time': '1637334466002',
                             'action_process_image_name': 'wevtutil.exe',
                             'actor_process_image_name': 'amazon-ssm-agent.exe',
                             'causality_actor_process_image_name': 'pycharm64.exe',
                             'os_actor_process_image_name': 'lsass.exe',
                             'action_process_os_pid': '6228',
                             'actor_process_os_pid': '4300',
                             'causality_actor_process_os_pid': '5144',
                             'os_actor_process_os_pid': '2744',
                             'action_process_requested_parent_pid': '5144',
                             'action_process_username': 'NT AUTHORITY\\NETWORK SERVICE',
                             'actor_effective_username': 'EC2AMAZ-4KPRAA7\\Administrator'
                             }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        process_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'process')
        assert process_obj is not None
        assert process_obj['type'] == 'process'
        assert process_obj['name'] == 'wevtutil.exe'
        assert process_obj['pid'] == 6228
        assert process_obj['command_line'] == 'C:\\Windows\\system32\\lsass.exe'

    def test_network_traffic_json_to_stix(self):
        """to test network-traffic stix object properties"""

        data = {'xdr_data': {'action_local_port': '54083',
                             'action_remote_port': '80',
                             'action_network_protocol': 'TCP',
                             'action_local_ip': '172.28.32.1',
                             'action_remote_ip': '23.205.106.166'
                             }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'network-traffic')

        assert network_obj is not None
        assert network_obj["type"] == 'network-traffic'
        assert network_obj["src_port"] == 54083
        assert network_obj['src_ref'] == '2'
        assert 'tcp' in network_obj["protocols"]
        assert network_obj["dst_port"] == 80
        assert network_obj['dst_ref'] == '4'

    def test_mac_addr_json_to_stix(self):
        """
        to test mac stix object properties
        """
        data = {'xdr_data': {'associated_mac': '00:15:5d:6a:79:52'}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        mac_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'mac-addr')
        assert mac_obj is not None, 'mac-aadr object type not found'
        assert mac_obj.keys() == {'type', 'value'}
        assert mac_obj['type'] == 'mac-addr'
        assert mac_obj['value'] == '00:15:5d:6a:79:52'

    def test_user_account_json_to_stix(self):
        """to test user-account stix object properties"""

        data = {'xdr_data': {'actor_process_logon_id': '794419589',
                             'action_process_username': 'EC2AMAZ-IQFSLIL\\Administrator',
                             'actor_primary_username': 'NT AUTHORITY\\SYSTEM',
                             'actor_primary_user_sid': 'S-1-5-18'
                             }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        user_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'user-account')

        assert user_obj is not None
        assert user_obj['type'] == 'user-account'
        assert user_obj['user_id'] == "S-1-5-18"
        assert user_obj['extensions']['x-paloalto-user']['process_user_name'] == 'EC2AMAZ-IQFSLIL\\Administrator'

    def test_domain_name_json_to_stix(self):
        """to test domain-name stix object properties"""

        data = {'xdr_data': {'auth_domain': 'dl.delivery.mp.microsoft.com',
                             'dst_host_metadata_domain': '8.tlu.dl.delivery.mp.microsoft.com',
                             'host_metadata_domain': '7.tlu.dl.delivery.mp.microsoft.com'
                             }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        domain_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'domain-name')
        assert domain_obj is not None
        assert domain_obj['type'] == 'domain-name'
        assert domain_obj['value'] == 'dl.delivery.mp.microsoft.com'

    def test_windows_registry_key_json_to_stix(self):
        """to test Windows registry stix object properties"""

        data = {'xdr_data': {'action_registry_key_name': 'HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Services\\terminpt'
                                                         '\\Enum',
                             'action_registry_value_name': 'Start'

                             }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        windows_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'windows-registry-key')
        assert windows_obj is not None
        assert windows_obj['type'] == 'windows-registry-key'
        assert windows_obj['key'] == 'HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Services\\terminpt\\Enum'
        assert windows_obj['values'] == [{'name': 'Start'}]

    def test_url_json_to_stix(self):
        """to test url stix object properties"""

        data = {'xdr_data': {'dst_action_url_category': 'https://paloalto/index.com'

                             }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        url_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'url')
        assert url_obj is not None
        assert url_obj['type'] == 'url'
        assert url_obj['value'] == 'https://paloalto/index.com'

    def test_custom_file_json_to_stix(self):
        """to test custom file stix object properties"""
        data = {'xdr_data': {
                            'action_file_extension': 'json',
                            'action_file_attributes': 128,
                            'action_file_last_writer_actor': 'AdgAsdUgVlUAAAbYAAAAAA==',
                            'action_file_signature_status': 3,
                            'action_file_type': 18,
                            'manifest_file_version': 5
                             }}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        custom_file_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'file')
        assert custom_file_obj is not None
        assert custom_file_obj['type'] == 'file'
        assert custom_file_obj['extensions']['x-paloalto-file']['extension'] == "json"
        assert custom_file_obj['extensions']['x-paloalto-file']['attributes'] == 128
        assert custom_file_obj['extensions']['x-paloalto-file']['writer'] == "AdgAsdUgVlUAAAbYAAAAAA=="
        assert custom_file_obj['extensions']['x-paloalto-file']['manifest_version'] == 5

    def test_custom_process_json_to_stix(self):
        """to test custom process stix object properties"""
        data = {'xdr_data': {
                            'actor_process_instance_id': 'AdgAsdUgVlUAAAbYAAAAAA==',
                            'actor_process_causality_id': 'AdgdeB9glMcAAAOYAAAAAA==',
                            'actor_process_signature_vendor': 'Microsoft Corporation',
                            'actor_process_signature_status': 'SIGNED',
                            'actor_process_signature_product': 'Microsoft Windows',
                            'action_process_termination_date': 1646315246849,
                            'actor_process_execution_time': 1641280255000,
                            'actor_process_is_native': 'FALSE'
                             }}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        custom_process_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'process')
        assert custom_process_obj is not None
        assert custom_process_obj['type'] == 'process'
        assert custom_process_obj['x_unique_id'] == 'AdgAsdUgVlUAAAbYAAAAAA=='
        assert custom_process_obj['extensions']['x-paloalto-process']['signature_vendor'] == "Microsoft Corporation"
        assert custom_process_obj['extensions']['x-paloalto-process']['signature_status'] == "SIGNED"
        assert custom_process_obj['extensions']['x-paloalto-process']['execution_time'] == "2022-01-04T07:10:55.000Z"
        assert custom_process_obj['extensions']['x-paloalto-process']['is_native'] is False

    def test_asset_json_to_stix(self):
        """to test custom oca-asset stix object properties"""
        data = {'xdr_data': {
                            'agent_version': '7.6.1.46600',
                            'agent_hostname': 'EC2AMAZ-IQFSLIL',
                            'agent_content_version': '350-80787',
                            'agent_session_start_time': 1642662241933,
                            'agent_id': '45.9.20.38',
                            'agent_os_sub_type': 'Windows Server 2016',
                            'agent_is_vdi': 'FALSE'
                             }}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        asset_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'x-oca-asset')
        assert asset_obj is not None
        assert asset_obj['type'] == 'x-oca-asset'
        assert asset_obj['extensions']['x-paloalto-agent']['agent_version'] == "7.6.1.46600"
        assert asset_obj['hostname'] == "EC2AMAZ-IQFSLIL"
        assert asset_obj['extensions']['x-paloalto-agent']['content_version'] == "350-80787"
        assert asset_obj['extensions']['x-paloalto-agent']['start_time'] == "2022-01-20T07:04:01.933Z"
        assert asset_obj['extensions']['x-paloalto-agent']['os_sub_type'] == "Windows Server 2016"
        assert asset_obj['extensions']['x-paloalto-agent']['is_vdi'] is False

    def test_evtlog_json_to_stix(self):
        """to test custom evtlog stix object properties"""
        data = {'xdr_data': {
                            'action_evtlog_description': 'An account was logged off',
                            'action_evtlog_source': 3,
                            'action_evtlog_event_id': 4625,
                            'action_evtlog_uid': 'S-1-5-19',
                            'action_evtlog_level': 'INFO',
                            'action_evtlog_version': 2
                             }}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        evtlog_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'x-paloalto-evtlog')
        assert evtlog_obj is not None
        assert evtlog_obj['type'] == 'x-paloalto-evtlog'
        assert evtlog_obj['description'] == "An account was logged off"
        assert evtlog_obj['source'] == 3
        assert evtlog_obj['evtlog_id'] == 4625
        assert evtlog_obj['uid'] == "S-1-5-19"
        assert evtlog_obj['level'] == "INFO"

    def test_event_json_to_stix(self):
        """to test custom event stix object properties"""
        data = {'xdr_data': {
                            'event_id': 'OTE0MTk5MTg2MDI1NzUyODc0NQ==',
                            'event_timestamp': 164632333729,
                            'event_version': 25,
                            'event_rpc_interface_uuid': '{00000136-0000-0000-C000-000000000046}',
                            'event_type': 'EVENT_LOG'
                             }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        event_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'x-oca-event')
        assert event_obj is not None
        assert event_obj['code'] == "OTE0MTk5MTg2MDI1NzUyODc0NQ=="
        assert event_obj['created'] == '1975-03-21T11:12:13.729Z'
        assert event_obj['extensions']['x-paloalto-event']['version'] == 25
        assert event_obj['extensions']['x-paloalto-event']['uuid'] == '{00000136-0000-0000-C000-000000000046}'
        assert event_obj['category'] == ["event_log"]

    def test_custom_network_json_to_stix(self):
        """to test custom network stix object properties"""
        data = {'xdr_data': {
                            'action_network_creation_time': 164632333729,
                            'action_network_connection_id': 'AdgAsdUgVlUAAAbYAAAAAA==',
                            'action_proxy': 'FALSE',
                            'action_external_hostname': 'Windows 8'
                             }}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']
        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        network_obj = TestPaloaltoResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert network_obj is not None
        assert network_obj['extensions']['x-paloalto-network']['creation_time'] == '1975-03-21T11:12:13.729Z'
        assert network_obj['extensions']['x-paloalto-network']['connection_id'] == "AdgAsdUgVlUAAAbYAAAAAA=="
        assert network_obj['extensions']['x-paloalto-network']['is_proxy'] is False
        assert network_obj['extensions']['x-paloalto-network']['external_hostname'] == 'Windows 8'
