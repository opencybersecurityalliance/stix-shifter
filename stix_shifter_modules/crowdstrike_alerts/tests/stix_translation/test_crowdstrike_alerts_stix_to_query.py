import json
import os
import unittest
from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils import logger

translation = stix_translation.StixTranslation()


class TestCrowdStrikeAlertsTransformResults(unittest.TestCase, object):
    logger = logger.set_logger(__name__)

    @staticmethod
    def write_to_query_results_file(data):    
        if os.path.exists(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_translation/sample_query_output.json"):      
            with open(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_translation/sample_query_output.json", "w") as file:
                json.dump(data, file)
    
    @staticmethod
    def get_translated_results_file():    
        if os.path.exists(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_translation/sample_query_output.json"):
            with open(os.getcwd() + "/stix_shifter_modules/crowdstrike_alerts/tests/stix_translation/sample_query_output.json", "r") as file:
                return json.load(file)
    
    def test_valid_parameters(self):
        """
            Makes a query for each parameter type.
        """
        query_list = []
        for query_param in Valid_Stix_Parameters:
            query = translation.translate('crowdstrike_alerts', 'query', '{}', f"[{query_param} != '1.1.1.1'] START t'2024-05-01T11:00:00.000Z' STOP t'2024-05-31T11:54:00.000Z'" )
            query_list.append(query)
            if("success" in query):
                self.logger.error(f"Failed because of the following query: [{query_param} != '1.1.1.1'] START t'2024-05-01T11:00:00.000Z' STOP t'2024-05-31T11:54:00.000Z")
                assert False
                
        assert query_list == TestCrowdStrikeAlertsTransformResults.get_translated_results_file()
    
    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for index, each_query in enumerate(query.get('queries'), start=0):
            self.assertEqual(each_query, queries[index])
    
    def test_comparison_and(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1' AND ipv4-addr:value = '1.1.1.2' AND mac-addr:value = '48:4D:7E:9D:BD:97'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike_alerts', 'query', '{}', stix_pattern)
        queries = ["(((device.external_ip: '1.1.1.1',device.local_ip: '1.1.1.1',network_accesses.local_address: '1.1.1.1',network_accesses.remote_address: '1.1.1.1') %2B (device.external_ip: '1.1.1.2',device.local_ip: '1.1.1.2',network_accesses.local_address: '1.1.1.2',network_accesses.remote_address: '1.1.1.2')) %2B (device.mac_address: '48:4D:7E:9D:BD:97')) %2B (timestamp:>= '2019-09-01T08:43:10' %2B timestamp:<= '2019-10-10T10:43:10')"]
        self._test_query_assertions(query, queries)
        
    def test_comparison_or(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1' OR ipv4-addr:value = '1.1.1.2' OR mac-addr:value = '48:4D:7E:9D:BD:97'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike_alerts', 'query', '{}', stix_pattern)
        queries = ["(((device.external_ip: '1.1.1.1',device.local_ip: '1.1.1.1',network_accesses.local_address: '1.1.1.1',network_accesses.remote_address: '1.1.1.1') , (device.external_ip: '1.1.1.2',device.local_ip: '1.1.1.2',network_accesses.local_address: '1.1.1.2',network_accesses.remote_address: '1.1.1.2')) , (device.mac_address: '48:4D:7E:9D:BD:97')) %2B (timestamp:>= '2019-09-01T08:43:10' %2B timestamp:<= '2019-10-10T10:43:10')"]
        self._test_query_assertions(query, queries)
        
    def test_equals(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike_alerts', 'query', '{}', stix_pattern)
        queries = ["((device.external_ip: '1.1.1.1',device.local_ip: '1.1.1.1',network_accesses.local_address: '1.1.1.1',network_accesses.remote_address: '1.1.1.1') %2B (timestamp:>= '2019-09-01T08:43:10' %2B timestamp:<= '2019-10-10T10:43:10'))"]
        self._test_query_assertions(query, queries)
        
    def test_not_equals(self):
        stix_pattern = "[ipv4-addr:value != '1.1.1.1'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike_alerts', 'query', '{}', stix_pattern)
        queries = ["((device.external_ip:! '1.1.1.1',device.local_ip:! '1.1.1.1',network_accesses.local_address:! '1.1.1.1',network_accesses.remote_address:! '1.1.1.1') %2B (timestamp:>= '2019-09-01T08:43:10' %2B timestamp:<= '2019-10-10T10:43:10'))"]
        self._test_query_assertions(query, queries)
        
    def test_greater_than(self):
        stix_pattern = "[x-oca-asset:x_device_cid > '1000'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike_alerts', 'query', '{}', stix_pattern)
        queries = ["((device.cid:> '1000') %2B (timestamp:>= '2019-09-01T08:43:10' %2B timestamp:<= '2019-10-10T10:43:10'))"]
        self._test_query_assertions(query, queries)
        
    def test_greater_than_or_equals(self):
        stix_pattern = "[x-oca-asset:x_device_cid >= '1000'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike_alerts', 'query', '{}', stix_pattern)
        queries = ["((device.cid:>= '1000') %2B (timestamp:>= '2019-09-01T08:43:10' %2B timestamp:<= '2019-10-10T10:43:10'))"]
        self._test_query_assertions(query, queries)
        
    def test_less_than(self):
        stix_pattern = "[x-oca-asset:x_device_cid < '1000'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike_alerts', 'query', '{}', stix_pattern)
        queries = ["((device.cid:< '1000') %2B (timestamp:>= '2019-09-01T08:43:10' %2B timestamp:<= '2019-10-10T10:43:10'))"]
        self._test_query_assertions(query, queries)
        
    def test_less_than_or_equals(self):
        stix_pattern = "[x-oca-asset:x_device_cid <= '1000'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike_alerts', 'query', '{}', stix_pattern)
        queries = ["((device.cid:<= '1000') %2B (timestamp:>= '2019-09-01T08:43:10' %2B timestamp:<= '2019-10-10T10:43:10'))"]
        self._test_query_assertions(query, queries)
        
    def test_in(self):
        stix_pattern = "[ipv4-addr:value IN ('1.1.1.1','1.1.1.2','1.1.1.3','1.1.1.4','1.1.1.5')] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike_alerts', 'query', '{}', stix_pattern)
        queries = ["((device.external_ip: '1.1.1.1',device.local_ip: '1.1.1.1',network_accesses.local_address: '1.1.1.1',network_accesses.remote_address: '1.1.1.1',device.external_ip: '1.1.1.2',device.local_ip: '1.1.1.2',network_accesses.local_address: '1.1.1.2',network_accesses.remote_address: '1.1.1.2',device.external_ip: '1.1.1.3',device.local_ip: '1.1.1.3',network_accesses.local_address: '1.1.1.3',network_accesses.remote_address: '1.1.1.3',device.external_ip: '1.1.1.4',device.local_ip: '1.1.1.4',network_accesses.local_address: '1.1.1.4',network_accesses.remote_address: '1.1.1.4',device.external_ip: '1.1.1.5',device.local_ip: '1.1.1.5',network_accesses.local_address: '1.1.1.5',network_accesses.remote_address: '1.1.1.5') %2B (timestamp:>= '2019-09-01T08:43:10' %2B timestamp:<= '2019-10-10T10:43:10'))"]
        self._test_query_assertions(query, queries)
        
    def test_negate_equals(self):
        stix_pattern = "[mac-addr:value NOT = '48:4D:7E:9D:BD:97'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike_alerts', 'query', '{}', stix_pattern)
        queries = ["((device.mac_address:! '48:4D:7E:9D:BD:97') %2B (timestamp:>= '2019-09-01T08:43:10' %2B timestamp:<= '2019-10-10T10:43:10'))"]
        self._test_query_assertions(query, queries)
        
    def test_negate_not_equals(self):
        stix_pattern = "[mac-addr:value NOT != '48:4D:7E:9D:BD:97'] START t'2019-09-01T08:43:10.003Z' STOP t'2019-10-10T10:43:10.003Z'"
        query = translation.translate('crowdstrike_alerts', 'query', '{}', stix_pattern)
        queries = ["((device.mac_address:! '48:4D:7E:9D:BD:97') %2B (timestamp:>= '2019-09-01T08:43:10' %2B timestamp:<= '2019-10-10T10:43:10'))"]
        self._test_query_assertions(query, queries)

Valid_Stix_Parameters = [
"file:name",
"file:hashes.'MD5'",
"file:hashes.'SHA-256'",
"file:accessed",
"file:parent_directory_ref.path",
"file:parent_directory_ref.accessed",
"file:parent_directory_ref.accessed",
"directory:path",
"directory:accessed",
"process:command_line",
"process:pid",
"process:name",
"process:cwd",
"process:created",
"process:creator_user_ref.user_id",
"process:creator_user_ref.account_login",
"process:binary_ref.name",
"process:binary_ref.accessed",
"process:binary_ref.hashes.'MD5'",
"process:binary_ref.hashes.'SHA-256'",
"process:binary_ref.parent_directory_ref.path",
"process:binary_ref.parent_directory_ref.accessed",
"process:parent_process_ref.command_line ",
"process:parent_process_ref.pid ",
"process:parent_process_ref.name ",
"process:parent_process_ref.cwd ",
"process:parent_process_ref.created ",
"process:parent_process_ref.creator_user_ref.user_id ",
"process:parent_process_ref.creator_user_ref.account_login ",
"process:parent_process_ref.binary_ref.name ",
"process:parent_process_ref.binary_ref.accessed ",
"process:parent_process_ref.binary_ref.hashes.'MD5' ",
"process:parent_process_ref.binary_ref.hashes.'SHA-256' ",
"process:parent_process_ref.binary_ref.parent_directory_ref.path ",
"process:parent_process_ref.binary_ref.parent_directory_ref.accessed ",
"process:parent_process_ref.child_refs.command_line ",
"process:parent_process_ref.child_refs.pid ",
"process:parent_process_ref.child_refs.name ",
"process:parent_process_ref.child_refs.cwd ",
"process:parent_process_ref.child_refs.created ",
"process:parent_process_ref.child_refs.creator_user_ref.user_id ",
"process:parent_process_ref.child_refs.creator_user_ref.account_login ",
"process:parent_process_ref.child_refs.binary_ref.name ",
"process:parent_process_ref.child_refs.binary_ref.accessed ",
"process:parent_process_ref.child_refs.binary_ref.hashes.'MD5' ",
"process:parent_process_ref.child_refs.binary_ref.hashes.'SHA-256' ",
"process:parent_process_ref.child_refs.binary_ref.parent_directory_ref.path ",
"process:parent_process_ref.child_refs.binary_ref.parent_directory_ref.accessed ",
"process:parent_process_ref.parent_process_ref.command_line ",
"process:parent_process_ref.parent_process_ref.pid ",
"process:parent_process_ref.parent_process_ref.name ",
"process:parent_process_ref.parent_process_ref.cwd ",
"process:parent_process_ref.parent_process_ref.created ",
"process:parent_process_ref.parent_process_ref.creator_user_ref.user_id ",
"process:parent_process_ref.parent_process_ref.creator_user_ref.account_login ",
"process:parent_process_ref.parent_process_ref.binary_ref.name ",
"process:parent_process_ref.parent_process_ref.binary_ref.accessed ",
"process:parent_process_ref.parent_process_ref.binary_ref.hashes.'MD5' ",
"process:parent_process_ref.parent_process_ref.binary_ref.hashes.'SHA-256' ",
"process:parent_process_ref.parent_process_ref.binary_ref.parent_directory_ref.path ",
"process:parent_process_ref.parent_process_ref.binary_ref.parent_directory_ref.accessed ",
"user-account:user_id ",
"user-account:account_login ",
"url:value ",
"x-oca-event:action ",
"x-oca-event:description ",
"x-oca-event:category ",
"x-oca-event:severity ",
"x-oca-event:x_severity_name ",
"x-oca-event:created ",
"x-oca-event:start ",
"x-oca-event:url_ref.value ",
"x-oca-event:file_ref.name ",
"x-oca-event:file_ref.hashes.'MD5' ",
"x-oca-event:file_ref.hashes.'SHA-256' ",
"x-oca-event:file_ref.accessed ",
"x-oca-event:file_ref.parent_directory_ref.path ",
"x-oca-event:file_ref.parent_directory_ref.accessed ",
"x-oca-event:domain_ref.value ",
"x-oca-event:domain_ref.resolves_to_refs.value ",
"x-oca-event:ip_refs.value ",
"x-oca-event:user_ref.user_id ",
"x-oca-event:user_ref.account_login ",
"x-oca-event:process_ref.command_line ",
"x-oca-event:process_ref.pid ",
"x-oca-event:process_ref.name ",
"x-oca-event:process_ref.cwd ",
"x-oca-event:process_ref.created ",
"x-oca-event:process_ref.creator_user_ref.user_id ",
"x-oca-event:process_ref.creator_user_ref.account_login ",
"x-oca-event:process_ref.binary_ref.name ",
"x-oca-event:process_ref.binary_ref.accessed ",
"x-oca-event:process_ref.binary_ref.hashes.'MD5' ",
"x-oca-event:process_ref.binary_ref.hashes.'SHA-256' ",
"x-oca-event:process_ref.binary_ref.parent_directory_ref.path ",
"x-oca-event:process_ref.binary_ref.parent_directory_ref.accessed ",
"x-oca-event:parent_process_ref.command_line ",
"x-oca-event:parent_process_ref.pid ",
"x-oca-event:parent_process_ref.name ",
"x-oca-event:parent_process_ref.cwd ",
"x-oca-event:parent_process_ref.created ",
"x-oca-event:parent_process_ref.creator_user_ref.user_id ",
"x-oca-event:parent_process_ref.creator_user_ref.account_login ",
"x-oca-event:parent_process_ref.binary_ref.name ",
"x-oca-event:parent_process_ref.binary_ref.accessed ",
"x-oca-event:parent_process_ref.binary_ref.hashes.'MD5' ",
"x-oca-event:parent_process_ref.binary_ref.hashes.'SHA-256' ",
"x-oca-event:parent_process_ref.binary_ref.parent_directory_ref.path ",
"x-oca-event:parent_process_ref.binary_ref.parent_directory_ref.accessed  ",
"ipv4-addr:value ",
"ipv6-addr:value  ",
"network-traffic:start ",
"network-traffic:x_access_type ",
"network-traffic:x_connection_direction ",
"network-traffic:x_network_isIPV6 ",
"network-traffic:local_port ",
"network-traffic:protocols ",
"network-traffic:dst_port ",
"mac-addr:value  ",
"software:version ",
"software:name ",
"x-oca-asset:device_id ",
"x-oca-asset:hostname ",
"x-oca-asset:ip_refs.value ",
"x-oca-asset:mac_refs.value ",
"x-oca-asset:os_ref.version ",
"x-oca-asset:os_ref.name ",
"x-oca-asset:x_agent_load_flags ",
"x-oca-asset:x_agent_local_time ",
"x-oca-asset:x_agent_version ",
"x-oca-asset:x_bios_manufacturer ",
"x-oca-asset:x_bios_version ",
"x-oca-asset:x_device_cid ",
"x-oca-asset:x_config_id_base ",
"x-oca-asset:x_config_id_build ",
"x-oca-asset:x_config_id_platform ",
"x-oca-asset:x_first_seen ",
"x-oca-asset:x_instance_id ",
"x-oca-asset:x_last_seen ",
"x-oca-asset:x_major_version ",
"x-oca-asset:x_minor_version ",
"x-oca-asset:x_modified_timestamp ",
"x-oca-asset:x_device_ou ",
"x-oca-asset:x_platform_id ",
"x-oca-asset:x_pod_labels ",
"x-oca-asset:x_product_type ",
"x-oca-asset:x_product_type_desc ",
"x-oca-asset:x_service_provider ",
"x-oca-asset:x_service_provider_account_id ",
"x-oca-asset:x_device_status ",
"x-oca-asset:x_system_manufacturer ",
"x-oca-asset:x_system_product_name ",
"x-crowdstrike:agent_id ",
"x-crowdstrike:aggregate_id ",
"x-crowdstrike:alleged_filetype ",
"x-crowdstrike:author ",
"x-crowdstrike:child_process_ids ",
"x-crowdstrike:cid ",
"x-crowdstrike:cloud_indicator ",
"x-crowdstrike:composite_id ",
"x-crowdstrike:confidence ",
"x-crowdstrike:context_timestamp ",
"x-crowdstrike:control_graph_id ",
"x-crowdstrike:crawled_timestamp ",
"x-crowdstrike:data_domains ",
"x-crowdstrike:display_name ",
"x-crowdstrike:email_sent ",
"x-crowdstrike:entity_values ",
"x-crowdstrike:event_status ",
"x-crowdstrike:global_prevalence ",
"x-crowdstrike:grandparent_user_graph_id ",
"x-crowdstrike:id ",
"x-crowdstrike:incident_start_time ",
"x-crowdstrike:incident_start_time_epoch ",
"x-crowdstrike:incident_end_time ",
"x-crowdstrike:incident_end_time_epoch ",
"x-crowdstrike:indicator_id ",
"x-crowdstrike:ioc_context ",
"x-crowdstrike:ioc_description ",
"x-crowdstrike:ioc_source ",
"x-crowdstrike:ioc_type ",
"x-crowdstrike:ioc_value ",
"x-crowdstrike:ioc_values ",
"x-crowdstrike:local_prevalence ",
"x-crowdstrike:logon_domain ",
"x-crowdstrike:no_signal ",
"x-crowdstrike:objective ",
"x-crowdstrike:parent_process_id ",
"x-crowdstrike:parent_user_graph_id ",
"x-crowdstrike:pattern_disposition ",
"x-crowdstrike:pattern_disposition_description ",
"x-crowdstrike:pattern_id ",
"x-crowdstrike:poly_id ",
"x-crowdstrike:parent_process_graph_id ",
"x-crowdstrike:grandparent_process_graph_id ",
"x-crowdstrike:process_id ",
"x-crowdstrike:grandparent_process_id ",
"x-crowdstrike:scenario ",
"x-crowdstrike:sha1 ",
"x-crowdstrike:seconds_to_resolved ",
"x-crowdstrike:seconds_to_triaged ",
"x-crowdstrike:show_in_ui ",
"x-crowdstrike:source_event_model ",
"x-crowdstrike:source_products ",
"x-crowdstrike:source_vendors ",
"x-crowdstrike:source_vertex_id ",
"x-crowdstrike:source_vertex_type ",
"x-crowdstrike:template_instance_id ",
"x-crowdstrike:tactic ",
"x-crowdstrike:tactic_id ",
"x-crowdstrike:technique ",
"x-crowdstrike:technique_id ",
"x-crowdstrike:tree_id ",
"x-crowdstrike:tree_root ",
"x-crowdstrike:triggering_process_graph_id ",
"x-crowdstrike:type ",
"x-crowdstrike:updated_timestamp ",
"x-crowdstrike:xdr_detection_id ",
"x-crowdstrike:xdr_pattern_id ",
"x-crowdstrike:xdr_rule_id ",
"x-crowdstrike:xdr_source_event_id ",
"x-crowdstrike:xdr_type ",
"x-crowdstrike:incident_classification ",
"x-crowdstrike:incident_created_time ",
"x-crowdstrike:incident_highest_score ",
"x-crowdstrike:incident_host_ids ",
"x-crowdstrike:incident_score ",
"x-crowdstrike:incident_state ",
"x-crowdstrike:incident_type ",
"x-crowdstrike:incident_version ",
"x-crowdstrike:incident_created ",
"x-crowdstrike:incident_end ",
"x-crowdstrike:incident_id ",
"x-crowdstrike:incident_start ",
"x-crowdstrike:has_script_or_module_ioc ",
"x-crowdstrike:process_end_time ",
"x-crowdstrike:agent_scan_id ",
"x-crowdstrike:event_id ",
"x-crowdstrike:quarantined ",
"x-crowdstrike:scan_id ",
"x-crowdstrike:list_of_agent_ids ",
"x-crowdstrike:list_of_alert_ids ",
"x-crowdstrike:list_of_detection_ids ",
"x-crowdstrike:list_of_vertex_ids ",
"x-crowdstrike:list_of_indicator_ids ",
"x-crowdstrike:list_of_tactic_ids ",
"x-crowdstrike:list_of_tactics ",
"x-crowdstrike:list_of_technique_ids ",
"x-crowdstrike:list_of_techniques ",
"x-crowdstrike:list_of_domains ",
"x-crowdstrike:list_of_file_names ",
"x-crowdstrike:list_of_image_file_names ",
"x-crowdstrike:list_of_ipv4 ",
"x-crowdstrike:list_of_processes ",
"x-crowdstrike:list_of_sha256 ",
"x-crowdstrike:blocking_unsupported_or_disabled ",
"x-crowdstrike:bootup_safeguard_enabled ",
"x-crowdstrike:critical_process_disabled ",
"x-crowdstrike:detect ",
"x-crowdstrike:handle_operation_downgraded ",
"x-crowdstrike:inddet_mask ",
"x-crowdstrike:indicator ",
"x-crowdstrike:fs_operation_blocked ",
"x-crowdstrike:kill_action_failed ",
"x-crowdstrike:kill_parent ",
"x-crowdstrike:kill_process ",
"x-crowdstrike:kill_subprocess ",
"x-crowdstrike:operation_blocked ",
"x-crowdstrike:policy_disabled ",
"x-crowdstrike:process_blocked ",
"x-crowdstrike:quarantine_file ",
"x-crowdstrike:quarantine_machine ",
"x-crowdstrike:registry_operation_blocked ",
"x-crowdstrike:rooting ",
"x-crowdstrike:sensor_only ",
"x-crowdstrike:suspend_parent ",
"x-crowdstrike:suspend_process ",
]