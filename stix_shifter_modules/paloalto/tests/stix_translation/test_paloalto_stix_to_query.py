from stix_shifter.stix_translation import stix_translation
from stix_shifter_utils.utils.error_response import ErrorCode
import unittest
import re

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(queries):
    pattern1 = r"to_epoch\(_time,\"millis\"\)\s*.=\s*\d{0,13}\s*and\s*to_epoch\(_time,\"millis\"\)\s*.=\s*\d{0,13}"
    pattern2 = r"\{'from':\s*\d{0,13},\s*'to':\s*\d{0,13}\}"
    if isinstance(queries, list):
        modified_queries = []
        for query in queries:
            replace_pat1 = re.sub(pattern1, '', str(query))
            replace_pat2 = re.sub(pattern2, '{}', replace_pat1)
            modified_queries.append(replace_pat2)
        return modified_queries
    elif isinstance(queries, str):
        replace_pat1 = re.sub(pattern1, '', queries)
        return re.sub(pattern2, '{}', replace_pat1)


all_fields = "dataset_name,action_local_ip,action_remote_ip,agent_ip_addresses,agent_ip_addresses_v6," \
             "dst_agent_ip_addresses_v6," \
             "action_local_port,action_remote_port,action_network_protocol,action_pkts_sent,action_pkts_received," \
             "action_file_name,action_process_image_name,actor_process_image_name,causality_actor_process_image_name," \
             "os_actor_process_image_name,action_file_size,action_file_md5,action_module_md5," \
             "action_process_image_md5,action_file_authenticode_sha1,action_file_authenticode_sha2," \
             "action_file_sha256,action_module_sha256,action_process_image_sha256,action_file_access_time," \
             "actor_process_file_access_time,os_actor_process_file_access_time,action_file_mod_time," \
             "actor_process_file_mod_time,os_actor_process_file_mod_time,action_file_create_time,action_file_path," \
             "action_process_image_path,action_registry_file_path,actor_process_image_path," \
             "causality_actor_process_image_path,os_actor_process_image_path,action_process_image_command_line," \
             "actor_process_command_line,causality_actor_process_command_line,os_actor_process_command_line," \
             "action_process_file_create_time,actor_process_file_create_time," \
             "causality_actor_process_file_create_time,os_actor_process_file_create_time," \
             "action_module_process_os_pid,action_process_os_pid,actor_process_os_pid,causality_actor_process_os_pid," \
             "os_actor_process_os_pid,action_process_requested_parent_pid,action_thread_parent_pid," \
             "action_thread_child_pid,action_process_username,auth_domain,dst_host_metadata_domain," \
             "host_metadata_domain,dst_action_url_category,action_registry_key_name,action_registry_value_name,mac," \
             "associated_mac,dst_associated_mac,dst_mac,actor_primary_user_sid,action_process_user_sid," \
             "actor_primary_username," \
             "actor_process_logon_id,action_file_info_company,action_file_extension,action_file_attributes," \
             "action_file_internal_zipped_files,action_file_last_writer_actor,action_file_signature_status," \
             "action_file_signature_vendor,action_file_signature_product,action_file_info_description," \
             "action_file_group,action_file_group_name,action_file_type,action_file_info_file_version," \
             "manifest_file_version,action_file_info_product_version,action_file_owner,action_file_owner_name," \
             "action_file_info_product_name,action_file_id,action_file_wildfire_verdict," \
             "action_file_hash_control_verdict,actor_process_instance_id,actor_process_causality_id," \
             "actor_process_auth_id,actor_process_container_id,actor_process_signature_vendor," \
             "actor_process_signature_status,actor_process_signature_product,actor_process_image_extension," \
             "action_process_termination_code,action_process_termination_date,action_remote_process_thread_id," \
             "action_process_instance_execution_time,actor_process_execution_time,action_process_handle_is_kernel," \
             "action_process_is_container_root,actor_process_is_native,agent_version,agent_hostname," \
             "agent_content_version,agent_session_start_time,agent_id,agent_os_type,agent_os_sub_type,agent_is_vdi," \
             "action_user_agent,http_req_user_agent_header,action_evtlog_data_fields,action_evtlog_description," \
             "action_evtlog_source,action_evtlog_event_id,action_evtlog_level,action_evtlog_tid,action_evtlog_uid," \
             "action_evtlog_pid,action_evtlog_message,action_evtlog_version,event_id,vpn_event_description," \
             "event_timestamp,event_version,event_rpc_interface_uuid,event_address_mapped_image_path,event_type," \
             "event_sub_type,action_network_creation_time,action_network_connection_id,action_network_packet_data," \
             "action_proxy,host_metadata_hostname,action_external_hostname"


class TestQueryTranslator(unittest.TestCase):
    if __name__ == "__main__":
        unittest.main()

    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(queries, list)
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        for index, each_query in enumerate(query.get('queries'), start=0):
            self.assertEqual(each_query, queries[index])

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '172.31.90.48']"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((action_local_ip = \"172.31.90.48\" or "
                   "action_remote_ip = \"172.31.90.48\" or agent_ip_addresses = \"172.31.90.48\")  and "
                   "(to_epoch(_time,\"millis\") >= 1645615464114 and to_epoch(_time,\"millis\") <= 1645615764114)) "
                   "| alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', 'timeframe': {"
                                                                                  "'from': 1645615464114, 'to': "
                                                                                  "1645615764114}}}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_traffic_query(self):
        stix_pattern = "[network-traffic:dst_port=53996]"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_remote_port = 53996  and "
                   "(to_epoch(_time,\"millis\") >= 1645615637334 and to_epoch(_time,\"millis\") <= 1645615937334))"
                   " | alter "
                   "dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', 'timeframe': {"
                                                                          "'from': 1645615637334, 'to': "
                                                                          "1645615937334}}}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_greater_than(self):
        stix_pattern = "[network-traffic:dst_port>53996]"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_remote_port > 53996  and "
                   "(to_epoch(_time,\"millis\") >= 1645615637334 and to_epoch(_time,\"millis\") <= 1645615937334))"
                   " | alter "
                   "dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', 'timeframe': {"
                                                                          "'from': 1645615637334, 'to': "
                                                                          "1645615937334}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_not_equals(self):
        stix_pattern = "[network-traffic:dst_port!=53996]"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_remote_port != 53996  and "
                   "(to_epoch(_time,\"millis\") >= 1645615637334 and to_epoch(_time,\"millis\") <= 1645615937334))"
                   " | alter "
                   "dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', 'timeframe': {"
                                                                          "'from': 1645615637334, 'to': "
                                                                          "1645615937334}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_enum_type(self):
        stix_pattern = "[network-traffic:protocols[*] IN ('TCP','udp')]"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_network_protocol in (ENUM.TCP,"
                   "ENUM.UDP)  and "
                   "(to_epoch(_time,\"millis\") >= 1645635857746 and to_epoch(_time,\"millis\") <= 1645636157746)) "
                   "| alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                                  "'timeframe': {'from': "
                                                                                  "1645635857746, "
                                                                                  "'to': 1645636157746}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_not_greater_than(self):
        stix_pattern = "[network-traffic:dst_port NOT > 53996]"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_remote_port <= 53996  and "
                   "(to_epoch(_time,\"millis\") >= 1645636616556 and to_epoch(_time,\"millis\") <= 1645636916556)) "
                   "| alter "
                   "dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                          "'timeframe': {'from': 1645636616556, 'to': "
                                                                          "1645636916556}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_less_than(self):
        stix_pattern = "[network-traffic:dst_port<53996]"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_remote_port < 53996  and "
                   "(to_epoch(_time,\"millis\") >= 1645636370847 and to_epoch(_time,\"millis\") <= 1645636670847)) "
                   "| alter "
                   "dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                          "'timeframe': {'from': 1645636370847, 'to': "
                                                                          "1645636670847}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_lessthan_or_equals(self):
        stix_pattern = "[network-traffic:dst_port<=53996]"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_remote_port <= 53996  and "
                   "(to_epoch(_time,\"millis\") >= 1645636370847 and to_epoch(_time,\"millis\") <= 1645636670847)) "
                   "| alter "
                   "dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                          "'timeframe': {'from': 1645636370847, 'to': "
                                                                          "1645636670847}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_query_greaterthan_or_equals(self):
        stix_pattern = "[network-traffic:dst_port>=53996]"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_remote_port >= 53996  and "
                   "(to_epoch(_time,\"millis\") >= 1645636370847 and to_epoch(_time,\"millis\") <= 1645636670847)) "
                   "| alter "
                   "dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                          "'timeframe': {'from': 1645636370847, 'to': "
                                                                          "1645636670847}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_file_like_operator(self):
        stix_pattern = "[file:name LIKE 'edr-2022-02-09_08-56-58-474-checksum.txt']"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])

        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((action_file_name contains "
                   "\"edr-2022-02-09_08-56-58-474-checksum.txt\" or action_process_image_name contains "
                   "\"edr-2022-02-09_08-56-58-474-checksum.txt\" or actor_process_image_name contains "
                   "\"edr-2022-02-09_08-56-58-474-checksum.txt\" or causality_actor_process_image_name contains "
                   "\"edr-2022-02-09_08-56-58-474-checksum.txt\" or os_actor_process_image_name contains "
                   "\"edr-2022-02-09_08-56-58-474-checksum.txt\")  and "
                   "(to_epoch(_time,\"millis\") >= 1645635327346 and to_epoch(_time,\"millis\") <= 1645635627346)) "
                   "| alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                                  "'timeframe': {'from': "
                                                                                  "1645635327346, "
                                                                                  "'to': 1645635627346}}}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_file_IN_operator(self):
        stix_pattern = "[file:name IN ('SentinelOne_1.binlog','edr-2022-02-09_08-56-58-47-checksum.txt')]"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((action_file_name in ("
                   "\"SentinelOne_1.binlog\",\"edr-2022-02-09_08-56-58-47-checksum.txt\") or "
                   "action_process_image_name in (\"SentinelOne_1.binlog\","
                   "\"edr-2022-02-09_08-56-58-47-checksum.txt\") or actor_process_image_name in ("
                   "\"SentinelOne_1.binlog\",\"edr-2022-02-09_08-56-58-47-checksum.txt\") or "
                   "causality_actor_process_image_name in (\"SentinelOne_1.binlog\","
                   "\"edr-2022-02-09_08-56-58-47-checksum.txt\") or os_actor_process_image_name in ("
                   "\"SentinelOne_1.binlog\",\"edr-2022-02-09_08-56-58-47-checksum.txt\"))  and "
                   "(to_epoch(_time,\"millis\") >= 1645635327346 and to_epoch(_time,\"millis\") <= 1645635627346)) "
                   "| alter "
                   "dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                          "'timeframe': {'from': 1645635327346, 'to': "
                                                                          "1645635627346}}}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_file_matches_operator(self):
        stix_pattern = "[file:name MATCHES '^g.{2}.exe']"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((action_file_name ~= \"^g.{2}.exe\" or "
                   "action_process_image_name ~= \"^g.{2}.exe\" or actor_process_image_name ~= \"^g.{2}.exe\" or "
                   "causality_actor_process_image_name ~= \"^g.{2}.exe\" or os_actor_process_image_name ~= \"^g.{"
                   "2}.exe\")  and "
                   "(to_epoch(_time,\"millis\") >= 1645635327346 and to_epoch(_time,\"millis\") <= 1645635627346)) "
                   "| alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                                  "'timeframe': {'from': "
                                                                                  "1645635327346, "
                                                                                  "'to': 1645635627346}}}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_mac_address_query(self):
        stix_pattern = "[mac-addr:value ='12:83:0e:be:f3:1d']"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((mac = \"12:83:0e:be:f3:1d\" or "
                   "associated_mac = \"12:83:0e:be:f3:1d\" or dst_associated_mac = \"12:83:0e:be:f3:1d\" or dst_mac "
                   "= \"12:83:0e:be:f3:1d\")  and "
                   "(to_epoch(_time,\"millis\") >= 1645635857746 and to_epoch(_time,\"millis\") <= 1645636157746)) "
                   "| alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                                  "'timeframe': {'from': "
                                                                                  "1645635857746, "
                                                                                  "'to': 1645636157746}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_not_matches_operator(self):
        stix_pattern = "[file:name NOT MATCHES '^g.{2}.exe']"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((action_file_name !~= \"^g.{2}.exe\" or "
                   "action_process_image_name !~= \"^g.{2}.exe\" or actor_process_image_name !~= \"^g.{2}.exe\" or "
                   "causality_actor_process_image_name !~= \"^g.{2}.exe\" or os_actor_process_image_name !~= \"^g.{"
                   "2}.exe\")  and "
                   "(to_epoch(_time,\"millis\") >= 1645636692740 and to_epoch(_time,\"millis\") <= 1645636992740)) "
                   "| alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                                  "'timeframe': {'from': "
                                                                                  "1645636692740, "
                                                                                  "'to': 1645636992740}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_process_not_in_operator(self):
        stix_pattern = "[process:name NOT IN('conhost.exe','AtBroker.exe')]"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((action_process_image_name not in ("
                   "\"conhost.exe\",\"AtBroker.exe\") or actor_process_image_name not in (\"conhost.exe\","
                   "\"AtBroker.exe\") or causality_actor_process_image_name not in (\"conhost.exe\",\"AtBroker.exe\") "
                   "or os_actor_process_image_name not in (\"conhost.exe\",\"AtBroker.exe\"))  and "
                   "(to_epoch(_time,\"millis\") >= 1645636692740 and to_epoch(_time,\"millis\") <= 1645636992740)) "
                   "| alter "
                   "dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                          "'timeframe': {'from': 1645636692740, 'to': "
                                                                          "1645636992740}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_windows_regkey_not_like_operator(self):
        stix_pattern = "[windows-registry-key:values[*] NOT LIKE 'DeltaUpdateFailure']"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_registry_value_name not contains "
                   "\"DeltaUpdateFailure\"  and "
                   "(to_epoch(_time,\"millis\") >= 1645638324427 and to_epoch(_time,\"millis\") <= 1645638624427)) "
                   "| alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                                  "'timeframe': {'from': "
                                                                                  "1645638324427, "
                                                                                  "'to': 1645638624427}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_multiple_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[file:name LIKE 'arp_cache.py' AND windows-registry-key:values[*] NOT LIKE 'SlotPerRow']"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_registry_value_name not contains "
                   "\"SlotPerRow\" and (action_file_name contains \"arp_cache.py\" or action_process_image_name "
                   "contains \"arp_cache.py\" or actor_process_image_name contains \"arp_cache.py\" or "
                   "causality_actor_process_image_name contains \"arp_cache.py\" or os_actor_process_image_name "
                   "contains \"arp_cache.py\")  and "
                   "(to_epoch(_time,\"millis\") >= 1645638324427 and to_epoch(_time,\"millis\") <= 1645638624427)) "
                   "| alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                                  "'timeframe': {'from': "
                                                                                  "1645638324427, "
                                                                                  "'to': 1645638624427}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_from_multiple_comparison_expressions_joined_by_OR(self):
        stix_pattern = "[network-traffic:dst_port!=53996 OR process:name NOT MATCHES '^G.{5}U.{5}.exe']"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((action_process_image_name !~= \"^G.{5}U.{"
                   "5}.exe\" or actor_process_image_name !~= \"^G.{5}U.{5}.exe\" or "
                   "causality_actor_process_image_name !~= \"^G.{5}U.{5}.exe\" or os_actor_process_image_name !~= "
                   "\"^G.{5}U.{5}.exe\") or action_remote_port != 53996  and "
                   "(to_epoch(_time,\"millis\") >= 1645635761271 and to_epoch(_time,\"millis\") <= 1645636061271)) "
                   "| alter dataset_name = "
                   "\"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                           "'timeframe': {'from': 1645635761271,"
                                                           " 'to': 1645636061271}}}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_for_morethan_two_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[file:name NOT LIKE 'arp_cache.py' AND windows-registry-key:values[*] IN" \
                       "('SlotPerRow','DeltaUpdateFailure') AND network-traffic:dst_port!=53996]"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)

        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_remote_port != 53996 and "
                   "action_registry_value_name in (\"SlotPerRow\",\"DeltaUpdateFailure\") and (action_file_name not "
                   "contains \"arp_cache.py\" or action_process_image_name not contains \"arp_cache.py\" or "
                   "actor_process_image_name not contains \"arp_cache.py\" or causality_actor_process_image_name not "
                   "contains \"arp_cache.py\" or os_actor_process_image_name not contains \"arp_cache.py\")  and "
                   "(to_epoch(_time,\"millis\") >= 1645636692740 and to_epoch(_time,\"millis\") <= 1645636992740)) | "
                   "alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                                "'timeframe': {'from': 1645636692740, "
                                                                                "'to': 1645636992740}}}"]
        queries = _remove_timestamp_from_query(queries)

        self._test_query_assertions(query, queries)

    def test_query_for_morethan_two_comparison_expressions_joined_by_OR(self):
        stix_pattern = "[network-traffic:dst_port!=53996 OR process:name NOT MATCHES '^G.{5}U.{5}.exe' OR " \
                       "mac-addr:value ='12:83:0e:be:f3:1d']"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((mac = \"12:83:0e:be:f3:1d\" or "
                   "associated_mac = \"12:83:0e:be:f3:1d\" or dst_associated_mac = \"12:83:0e:be:f3:1d\" or dst_mac "
                   "= \"12:83:0e:be:f3:1d\") or (action_process_image_name !~= \"^G.{5}U.{5}.exe\" or "
                   "actor_process_image_name !~= \"^G.{5}U.{5}.exe\" or causality_actor_process_image_name !~= \"^G.{"
                   "5}U.{5}.exe\" or os_actor_process_image_name !~= \"^G.{5}U.{5}.exe\") or action_remote_port != "
                   "53996  and "
                   "(to_epoch(_time,\"millis\") >= 1645636966650 and to_epoch(_time,\"millis\") <= 1645637266650)) "
                   "| alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                                  "'timeframe': {'from': "
                                                                                  "1645636966650, "
                                                                                  "'to': 1645637266650}}}"]

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_and_without_qualifier_query(self):
        stix_pattern = "[file:name LIKE 'metadata']START t'2022-01-01T00:00:00.030Z' STOP t'2022-02-07T00:00:00.030Z'" \
                       " AND[windows-registry-key:values[*] NOT LIKE 'SlotPerRow'OR " \
                       "process:name MATCHES '^G.{5}U.{5}.exe']"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((action_file_name contains \"metadata\" or "
                   "action_process_image_name contains \"metadata\" or actor_process_image_name contains \"metadata\" "
                   "or causality_actor_process_image_name contains \"metadata\" or os_actor_process_image_name "
                   "contains \"metadata\")  and (to_epoch(_time,\"millis\") >= 1640995200030 and to_epoch(_time,"
                   "\"millis\") <= 1644192000030)) or ((action_process_image_name ~= \"^G.{5}U.{5}.exe\" or "
                   "actor_process_image_name ~= \"^G.{5}U.{5}.exe\" or causality_actor_process_image_name ~= \"^G.{"
                   "5}U.{5}.exe\" or os_actor_process_image_name ~= \"^G.{5}U.{5}.exe\") or "
                   "action_registry_value_name not contains \"SlotPerRow\"  and "
                   "(to_epoch(_time,\"millis\") >= 1645635857746 and to_epoch(_time,\"millis\") <= 1645636157746)) "
                   "| alter dataset_name = "
                   "\"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                           "'timeframe': {'from': 1640995200030, "
                                                           "'to': 1645636157746}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_observation_with_invalid_operator(self):
        stix_pattern = "[network-traffic:dst_port LIKE '53996']"
        result = translation.translate('paloalto', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'LIKE operator is supported only for string type input' in result['error']

    def test_invalid_mac_address(self):
        stix_pattern = "[mac-addr:value = '00:00:00']"
        result = translation.translate('paloalto', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'Invalid mac address' in result['error']

    def test_invalid_stix_pattern(self):
        stix_pattern = "[not_a_valid_pattern]"
        result = translation.translate('paloalto', 'query', '{}', stix_pattern, {'validate_pattern': 'true'})
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_STIX_VALIDATION.value == result['code']
        assert stix_pattern[1:-1] in result['error']

    def test_combined_observation_AND(self):
        stix_pattern = "([process:pid = '868' OR  process:name = 'svchost.exe'] AND " \
                       "[network-traffic:dst_port = '53996' AND ipv4-addr:value = '172.31.31.67']) " \
                       "START t'2022-01-19T11:00:00.000Z' STOP t'2022-02-07T11:00:00.003Z'"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((action_process_image_name = \"svchost.exe\" "
                   "or actor_process_image_name = \"svchost.exe\" or causality_actor_process_image_name = "
                   "\"svchost.exe\" or os_actor_process_image_name = \"svchost.exe\") or ("
                   "action_module_process_os_pid = 868 or action_process_os_pid = 868 or actor_process_os_pid = 868 "
                   "or causality_actor_process_os_pid = 868 or os_actor_process_os_pid = 868 or "
                   "action_process_requested_parent_pid = 868 or action_thread_parent_pid = 868 or "
                   "action_thread_child_pid = 868)  and "
                   "(to_epoch(_time,\"millis\") >= 1642590000000 and to_epoch(_time,\"millis\") <= 1644231600003)) "
                   "or ((action_local_ip = \"172.31.31.67\" or action_remote_ip "
                   "= \"172.31.31.67\" or agent_ip_addresses = \"172.31.31.67\") and action_remote_port = 53996  and "
                   "(to_epoch(_time,\"millis\") >= 1642590000000 and to_epoch(_time,\"millis\") <= 1644231600003)) "
                   "| alter dataset_name = "
                   "\"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                           "'timeframe': {'from': 1642590000000, "
                                                           "'to': 1644231600003}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_combined_observation_OR(self):
        stix_pattern = "([file:name NOT MATCHES '^g.{2}.exe' AND network-traffic:dst_port <= 137]OR " \
                       "[mac-addr:value = '12:83:0e:be:f3:1d' OR process:name LIKE 'svchost.exe']) " \
                       "START t'2022-01-10T11:00:00.000Z' STOP t'2022-02-05T11:00:00.003Z'"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter (action_remote_port <= 137 and ("
                   "action_file_name !~= \"^g.{2}.exe\" or action_process_image_name !~= \"^g.{2}.exe\" or "
                   "actor_process_image_name !~= \"^g.{2}.exe\" or causality_actor_process_image_name !~= \"^g.{"
                   "2}.exe\" or os_actor_process_image_name !~= \"^g.{2}.exe\")  and "
                   "(to_epoch(_time,\"millis\") >= 1641812400000 and to_epoch(_time,\"millis\") <= 1644058800003)) "
                   "or ((action_process_image_name "
                   "contains \"svchost.exe\" or actor_process_image_name contains \"svchost.exe\" or "
                   "causality_actor_process_image_name contains \"svchost.exe\" or os_actor_process_image_name "
                   "contains \"svchost.exe\") or (mac = \"12:83:0e:be:f3:1d\" or associated_mac = "
                   "\"12:83:0e:be:f3:1d\" or dst_associated_mac = \"12:83:0e:be:f3:1d\" or dst_mac = "
                   "\"12:83:0e:be:f3:1d\")  and "
                   "(to_epoch(_time,\"millis\") >= 1641812400000 and to_epoch(_time,\"millis\") <= 1644058800003)) "
                   "| alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                                  "'timeframe': {'from': "
                                                                                  "1641812400000, "
                                                                                  "'to': 1644058800003}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_data_for_matches(self):
        stix_pattern = "[process:pid MATCHES '53996']"
        result = translation.translate('paloalto', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'MATCHES operators is supported only for string type input' in result['error']

    def test_invalid_regex_for_matches(self):
        stix_pattern = "[process:name MATCHES 'wild^fire$']"
        result = translation.translate('paloalto', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert '^ symbol should be at the starting position of the expression' in result['error']

    def test_invalid_enum_values(self):
        stix_pattern = "[network-traffic:protocols[*] = 'idp']"
        result = translation.translate('paloalto', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'Unsupported ENUM values provided' in result['error']

    def test_matches_operator_for_enum(self):
        stix_pattern = "[network-traffic:protocols[*] MATCHES 'tcp']"
        result = translation.translate('paloalto', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'MATCHES operators is supported only for string type input' in result['error']

    def test_invalid_operator_for_enum(self):
        stix_pattern = "[network-traffic:protocols[*] < 'tcp']"
        result = translation.translate('paloalto', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'operator is not supported for Enum type input' in result['error']

    def test_invalid_operator_for_string_input(self):
        stix_pattern = "[process:name < 'conhost.exe' ]"
        result = translation.translate('paloalto', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'operator is not supported for string type input' in result['error']

    def test_invalid_qualifier(self):
        stix_pattern = "[process:pid < '53996'] START " \
                       "t'2022-02-01T08:43:10.003Z' STOP t'2022-01-07T10:43:10.005Z' "
        result = translation.translate('paloalto', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert 'Start time should be lesser than Stop time' in result['error']

    def test_invalid_dollar_regexp(self):
        stix_pattern = "[process:name MATCHES '^wildfire$s']"
        result = translation.translate('paloalto', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert '$ symbol should be at the ending position of the expression' in result['error']

    def test_invalid_value_for_timestamp_field(self):
        stix_pattern = "[process:created = '2022-02-0108:43:10.003Z']"
        result = translation.translate('paloalto', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert ErrorCode.TRANSLATION_NOTIMPLEMENTED_MODE.value == result['code']
        assert 'cannot convert the timestamp' in result['error']

    def test_format_timestamp_fields(self):
        stix_pattern = "[process:created = '2022-02-01T08:43:10.003Z']"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        query['queries'] = _remove_timestamp_from_query(query['queries'])
        queries = ["{'xdr_data': {'query': 'dataset = xdr_data | filter ((action_process_file_create_time = "
                   "1643704990003 or actor_process_file_create_time = 1643704990003 or "
                   "causality_actor_process_file_create_time = 1643704990003 or os_actor_process_file_create_time = "
                   "1643704990003)  and "
                   "(to_epoch(_time,\"millis\") >= 1645635857746 and to_epoch(_time,\"millis\") <= 1645636157746)) "
                   "| alter dataset_name = \"xdr_data\" | fields " + all_fields + " | limit 10000 ', "
                                                                                  "'timeframe': {'from': "
                                                                                  "1645635857746, "
                                                                                  "'to': 1645636157746}}}"]
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_qualifier_without_milliseconds(self):
        stix_pattern = "[ipv4-addr:value = '10.0.1.4' AND network-traffic:src_port = 52221] " \
                       "START t'2022-02-01T08:43:10Z' STOP t'2022-04-07T10:43:10Z'"
        query = translation.translate('paloalto', 'query', '{}', stix_pattern)
        queries = [{'xdr_data': {'query': 'dataset = xdr_data | filter (action_local_port = 52221 '
                                          'and (action_local_ip = "10.0.1.4" or action_remote_ip = "10.0.1.4"'
                                          ' or agent_ip_addresses = "10.0.1.4")  and '
                                          '(to_epoch(_time,"millis") >= 1643704990000 and '
                                          'to_epoch(_time,"millis") <= 1649328190000)) | alter dataset_name = '
                                          '"xdr_data" | fields ' + all_fields + ' | limit 10000 ',
                                 'timeframe': {'from': 1643704990000, 'to': 1649328190000}}}]

        self._test_query_assertions(query, queries)
