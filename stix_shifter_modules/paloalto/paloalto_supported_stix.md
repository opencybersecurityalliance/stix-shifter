##### Updated on 05/15/23
## PaloAlto Cortex XDR
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparision) | and |
| OR (Comparision) | or |
| = | = |
| != | != |
| LIKE | contains |
| MATCHES | ~= |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| IN | in |
| OR (Observation) | or |
| AND (Observation) | or |
| <br> | |
### Searchable STIX objects and properties for Xdr_data dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | action_local_ip, action_remote_ip, agent_ip_addresses |
| **ipv6-addr**:value | agent_ip_addresses_v6, dst_agent_ip_addresses_v6 |
| **network-traffic**:src_port | action_local_port |
| **network-traffic**:dst_port | action_remote_port |
| **network-traffic**:protocols[*] | action_network_protocol |
| **network-traffic**:src_ref.value | action_local_ip, agent_ip_addresses |
| **network-traffic**:dst_ref.value | action_remote_ip |
| **network-traffic**:src_packets | action_pkts_sent |
| **network-traffic**:dst_packets | action_pkts_received |
| **file**:name | action_file_name, action_process_image_name, actor_process_image_name, causality_actor_process_image_name, os_actor_process_image_name |
| **file**:size | action_file_size |
| **file**:hashes.MD5 | action_file_md5, action_module_md5, action_process_image_md5 |
| **file**:hashes.'SHA-1' | action_file_authenticode_sha1 |
| **file**:hashes.'SHA-2' | action_file_authenticode_sha2 |
| **file**:hashes.'SHA-256' | action_file_sha256, action_module_sha256, action_process_image_sha256 |
| **file**:accessed | action_file_access_time, actor_process_file_access_time, os_actor_process_file_access_time |
| **file**:modified | action_file_mod_time, actor_process_file_mod_time, os_actor_process_file_mod_time |
| **file**:created | action_file_create_time |
| **file**:parent_directory_ref.path | action_file_path, action_process_image_path, action_registry_file_path, actor_process_image_path, causality_actor_process_image_path, os_actor_process_image_path |
| **directory**:path | action_file_path, action_process_image_path, action_registry_file_path, actor_process_image_path, causality_actor_process_image_path, os_actor_process_image_path |
| **process**:command_line | action_process_image_command_line, actor_process_command_line, causality_actor_process_command_line, os_actor_process_command_line |
| **process**:created | action_process_file_create_time, actor_process_file_create_time, causality_actor_process_file_create_time, os_actor_process_file_create_time |
| **process**:name | action_process_image_name, actor_process_image_name, causality_actor_process_image_name, os_actor_process_image_name |
| **process**:pid | action_module_process_os_pid, action_process_os_pid, actor_process_os_pid, causality_actor_process_os_pid, os_actor_process_os_pid, action_process_requested_parent_pid, action_thread_parent_pid, action_thread_child_pid |
| **process**:parent_ref.pid | action_process_requested_parent_pid, action_thread_parent_pid |
| **process**:child_refs.pid | action_thread_child_pid |
| **process**:creator_user_ref.user_id | action_process_username |
| **process**:parent_ref.name | causality_actor_process_image_name, os_actor_process_image_name |
| **process**:binary_ref.name | action_process_image_name, actor_process_image_name |
| **process**:binary_ref.hashes.MD5 | action_process_image_md5 |
| **process**:binary_ref.hashes.'SHA-256' | action_process_image_sha256 |
| **process**:binary_ref.parent_directory_ref.path | action_process_image_path, actor_process_image_path, causality_actor_process_image_path, os_actor_process_image_path |
| **process**:x_unique_id | actor_process_instance_id |
| **domain-name**:value | auth_domain, dst_host_metadata_domain, host_metadata_domain |
| **url**:value | dst_action_url_category |
| **windows-registry-key**:key | action_registry_key_name |
| **windows-registry-key**:values[*] | action_registry_value_name |
| **mac-addr**:value | mac, associated_mac, dst_associated_mac, dst_mac |
| **user-account**:user_id | actor_primary_user_sid, action_process_user_sid |
| **user-account**:display_name | actor_primary_username, action_process_username |
| **user-account**:account_login | actor_process_logon_id |
| **x-paloalto-file**:extension | action_file_extension |
| **x-paloalto-file**:file_description | action_file_info_description |
| **x-paloalto-process**:extension | actor_process_image_extension |
| **x-paloalto-process**:execution_time | action_process_instance_execution_time, actor_process_execution_time |
| **x-oca-asset**:hostname | agent_hostname |
| **x-oca-asset**:ip_refs[*].value | action_local_ip, action_remote_ip, agent_ip_addresses_v6, agent_ip_addresses, dst_agent_ip_addresses_v6 |
| **x-oca-asset**:mac_refs[*].value | mac, associated_mac, dst_associated_mac, dst_mac |
| **x-paloalto-evtlog**:description | action_evtlog_description |
| **x-paloalto-evtlog**:message | action_evtlog_message |
| **x-oca-event**:code | event_id |
| **x-oca-event**:category[*] | event_type |
| **x-oca-event**:action | event_sub_type |
| **x-oca-event**:created | event_timestamp |
| **x-oca-event**:agent | agent_hostname |
| **x-oca-event**:url_ref.value | dst_action_url_category |
| **x-oca-event**:file_ref.name | action_file_name |
| **x-oca-event**:process_ref.pid | action_module_process_os_pid, action_process_os_pid, actor_process_os_pid, causality_actor_process_os_pid, os_actor_process_os_pid |
| **x-oca-event**:process_ref.name | action_process_image_name, actor_process_image_name |
| **x-oca-event**:process_ref.command_line | action_process_image_command_line, actor_process_command_line |
| **x-oca-event**:process_ref.binary_ref.name | action_process_image_name, actor_process_image_name |
| **x-oca-event**:process_ref.parent_ref.name | causality_actor_process_command_line, os_actor_process_command_line |
| **x-oca-event**:process_ref.parent_ref.pid | action_process_requested_parent_pid, action_thread_parent_pid |
| **x-oca-event**:process_ref.parent_ref.command_line | causality_actor_process_command_line, os_actor_process_command_line |
| **x-oca-event**:parent_process_ref.name | causality_actor_process_image_name, os_actor_process_image_name |
| **x-oca-event**:parent_process_ref.pid | action_process_requested_parent_pid, action_thread_parent_pid |
| **x-oca-event**:parent_process_ref.command_line | causality_actor_process_command_line, os_actor_process_command_line |
| **x-oca-event**:process_ref.creator_user_ref.user_id | action_process_username |
| **x-oca-event**:process_ref.binary_ref.hashes.MD5 | action_process_image_md5 |
| **x-oca-event**:process_ref.binary_ref.hashes.'SHA-256' | action_process_image_sha256 |
| **x-oca-event**:domain_ref.value | auth_domain, dst_host_metadata_domain, host_metadata_domain |
| **x-oca-event**:registry_ref.key | action_registry_key_name |
| **x-oca-event**:registry_ref.values[*] | action_registry_value_name |
| **x-paloalto-network**:creation_time | action_network_creation_time |
| **x-paloalto-network**:hostname | host_metadata_hostname, action_external_hostname |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | action_file_path |
| directory | path | action_registry_file_path |
| directory | path | action_process_image_path |
| directory | path | actor_process_image_path |
| directory | path | causality_actor_process_image_path |
| directory | path | os_actor_process_image_path |
| <br> | | |
| domain-name | value | auth_domain |
| domain-name | value | dst_host_metadata_domain |
| domain-name | value | host_metadata_domain |
| <br> | | |
| file | name | action_file_name |
| file | name | action_process_image_name |
| file | name | actor_process_image_name |
| file | name | causality_actor_process_image_name |
| file | name | os_actor_process_image_name |
| file | size | action_file_size |
| file | hashes.SHA-1 | action_file_authenticode_sha1 |
| file | hashes.SHA-2 | action_file_authenticode_sha2 |
| file | hashes.MD5 | action_file_md5 |
| file | hashes.MD5 | action_module_md5 |
| file | hashes.MD5 | action_process_image_md5 |
| file | hashes.SHA-256 | action_file_sha256 |
| file | hashes.SHA-256 | action_module_sha256 |
| file | hashes.SHA-256 | action_process_image_sha256 |
| file | accessed | action_file_access_time |
| file | accessed | actor_process_file_access_time |
| file | accessed | os_actor_process_file_access_time |
| file | modified | action_file_mod_time |
| file | modified | actor_process_file_mod_time |
| file | modified | os_actor_process_file_mod_time |
| file | created | action_file_create_time |
| file | parent_directory_ref | action_file_path |
| file | parent_directory_ref | action_registry_file_path |
| file | parent_directory_ref | action_process_image_path |
| file | parent_directory_ref | actor_process_image_path |
| file | parent_directory_ref | causality_actor_process_image_path |
| file | parent_directory_ref | os_actor_process_image_path |
| file | extensions.x-paloalto-file.company | action_file_info_company |
| file | extensions.x-paloalto-file.extension | action_file_extension |
| file | extensions.x-paloalto-file.attributes | action_file_attributes |
| file | extensions.x-paloalto-file.zipped_files | action_file_internal_zipped_files |
| file | extensions.x-paloalto-file.writer | action_file_last_writer_actor |
| file | extensions.x-paloalto-file.mode | action_file_mode |
| file | extensions.x-paloalto-file.signature_status | action_file_signature_status |
| file | extensions.x-paloalto-file.signature_vendor | action_file_signature_vendor |
| file | extensions.x-paloalto-file.signature_product | action_file_signature_product |
| file | extensions.x-paloalto-file.file_description | action_file_info_description |
| file | extensions.x-paloalto-file.group | action_file_group |
| file | extensions.x-paloalto-file.group_name | action_file_group_name |
| file | extensions.x-paloalto-file.type | action_file_type |
| file | extensions.x-paloalto-file.version | action_file_info_file_version |
| file | extensions.x-paloalto-file.manifest_version | manifest_file_version |
| file | extensions.x-paloalto-file.product_version | action_file_info_product_version |
| file | extensions.x-paloalto-file.owner | action_file_owner |
| file | extensions.x-paloalto-file.owner_name | action_file_owner_name |
| file | extensions.x-paloalto-file.product_name | action_file_info_product_name |
| file | extensions.x-paloalto-file.id | action_file_id |
| file | extensions.x-paloalto-file.wildfire_verdict | action_file_wildfire_verdict |
| file | extensions.x-paloalto-file.control_verdict | action_file_hash_control_verdict |
| <br> | | |
| ipv4-addr | value | action_local_ip |
| ipv4-addr | value | action_remote_ip |
| ipv4-addr | value | agent_ip_addresses |
| <br> | | |
| ipv6-addr | value | agent_ip_addresses_v6 |
| ipv6-addr | value | dst_agent_ip_addresses_v6 |
| <br> | | |
| mac-addr | value | mac |
| mac-addr | value | associated_mac |
| mac-addr | value | dst_associated_mac |
| mac-addr | value | dst_mac |
| <br> | | |
| network-traffic | src_ref | action_local_ip |
| network-traffic | dst_ref | action_remote_ip |
| network-traffic | src_ref | agent_ip_addresses |
| network-traffic | src_port | action_local_port |
| network-traffic | dst_port | action_remote_port |
| network-traffic | protocols | action_network_protocol |
| network-traffic | src_packets | action_pkts_sent |
| network-traffic | dst_packets | action_pkts_received |
| network-traffic | extensions.x-paloalto-network.creation_time | action_network_creation_time |
| network-traffic | extensions.x-paloalto-network.connection_id | action_network_connection_id |
| network-traffic | extensions.x-paloalto-network.packet_data | action_network_packet_data |
| network-traffic | extensions.x-paloalto-network.is_proxy | action_proxy |
| network-traffic | extensions.x-paloalto-network.metadata_hostname | host_metadata_hostname |
| network-traffic | extensions.x-paloalto-network.external_hostname | action_external_hostname |
| <br> | | |
| process | name | action_process_image_name |
| process | binary_ref | action_process_image_name |
| process | name | actor_process_image_name |
| process | binary_ref | actor_process_image_name |
| process | name | causality_actor_process_image_name |
| process | parent_ref | causality_actor_process_image_name |
| process | name | os_actor_process_image_name |
| process | parent_ref | os_actor_process_image_name |
| process | binary_ref | action_process_image_md5 |
| process | binary_ref | action_process_image_sha256 |
| process | binary_ref | action_process_image_path |
| process | binary_ref | actor_process_image_path |
| process | binary_ref | causality_actor_process_image_path |
| process | binary_ref | os_actor_process_image_path |
| process | command_line | action_process_image_command_line |
| process | command_line | actor_process_command_line |
| process | command_line | causality_actor_process_command_line |
| process | command_line | os_actor_process_command_line |
| process | created | action_process_file_create_time |
| process | created | actor_process_file_create_time |
| process | created | causality_actor_process_file_create_time |
| process | created | os_actor_process_file_create_time |
| process | pid | action_module_process_os_pid |
| process | pid | action_process_os_pid |
| process | pid | actor_process_os_pid |
| process | pid | causality_actor_process_os_pid |
| process | pid | os_actor_process_os_pid |
| process | pid | action_process_requested_parent_pid |
| process | parent_ref | action_process_requested_parent_pid |
| process | pid | action_thread_parent_pid |
| process | parent_ref | action_thread_parent_pid |
| process | pid | action_thread_child_pid |
| process | child_refs | action_thread_child_pid |
| process | creator_user_ref | action_process_username |
| process | extensions.x-paloalto-process.causality_id | actor_process_causality_id |
| process | extensions.x-paloalto-process.auth_id | actor_process_auth_id |
| process | extensions.x-paloalto-process.container_id | actor_process_container_id |
| process | extensions.x-paloalto-process.signature_vendor | actor_process_signature_vendor |
| process | extensions.x-paloalto-process.signature_status | actor_process_signature_status |
| process | extensions.x-paloalto-process.signature_product | actor_process_signature_product |
| process | extensions.x-paloalto-process.extension | actor_process_image_extension |
| process | extensions.x-paloalto-process.termination_code | action_process_termination_code |
| process | extensions.x-paloalto-process.termination_date | action_process_termination_date |
| process | extensions.x-paloalto-process.tid | action_remote_process_thread_id |
| process | extensions.x-paloalto-process.instance_exec_time | action_process_instance_execution_time |
| process | extensions.x-paloalto-process.execution_time | actor_process_execution_time |
| process | extensions.x-paloalto-process.is_kernel | action_process_handle_is_kernel |
| process | extensions.x-paloalto-process.is_root | action_process_is_container_root |
| process | extensions.x-paloalto-process.is_native | actor_process_is_native |
| process | x_unique_id | actor_process_instance_id |
| <br> | | |
| url | value | dst_action_url_category |
| <br> | | |
| user-account | user_id | actor_primary_user_sid |
| user-account | extensions.x-paloalto-user.process_user_id | action_process_user_sid |
| user-account | display_name | actor_primary_username |
| user-account | extensions.x-paloalto-user.process_user_name | action_process_username |
| user-account | account_login | actor_process_logon_id |
| <br> | | |
| windows-registry-key | key | action_registry_key_name |
| windows-registry-key | values | action_registry_value_name |
| <br> | | |
| x-oca-asset | ip_refs | action_local_ip |
| x-oca-asset | ip_refs | action_remote_ip |
| x-oca-asset | ip_refs | agent_ip_addresses |
| x-oca-asset | ip_refs | agent_ip_addresses_v6 |
| x-oca-asset | ip_refs | dst_agent_ip_addresses_v6 |
| x-oca-asset | mac_refs | mac |
| x-oca-asset | mac_refs | associated_mac |
| x-oca-asset | mac_refs | dst_associated_mac |
| x-oca-asset | mac_refs | dst_mac |
| x-oca-asset | extensions.x-paloalto-agent.agent_version | agent_version |
| x-oca-asset | hostname | agent_hostname |
| x-oca-asset | extensions.x-paloalto-agent.content_version | agent_content_version |
| x-oca-asset | extensions.x-paloalto-agent.start_time | agent_session_start_time |
| x-oca-asset | extensions.x-paloalto-agent.asset_id | agent_id |
| x-oca-asset | extensions.x-paloalto-agent.os_type | agent_os_type |
| x-oca-asset | extensions.x-paloalto-agent.os_sub_type | agent_os_sub_type |
| x-oca-asset | extensions.x-paloalto-agent.is_vdi | agent_is_vdi |
| x-oca-asset | extensions.x-paloalto-agent.user_agent | action_user_agent |
| x-oca-asset | extensions.x-paloalto-agent.agent_header | http_req_user_agent_header |
| <br> | | |
| x-oca-event | network_ref | action_network_protocol |
| x-oca-event | file_ref | action_file_name |
| x-oca-event | process_ref | action_process_image_name |
| x-oca-event | process_ref | actor_process_image_name |
| x-oca-event | parent_process_ref | causality_actor_process_image_name |
| x-oca-event | parent_process_ref | os_actor_process_image_name |
| x-oca-event | process_ref | action_process_image_command_line |
| x-oca-event | process_ref | actor_process_command_line |
| x-oca-event | parent_process_ref | causality_actor_process_command_line |
| x-oca-event | parent_process_ref | os_actor_process_command_line |
| x-oca-event | process_ref | action_module_process_os_pid |
| x-oca-event | process_ref | action_process_os_pid |
| x-oca-event | process_ref | actor_process_os_pid |
| x-oca-event | process_ref | causality_actor_process_os_pid |
| x-oca-event | process_ref | os_actor_process_os_pid |
| x-oca-event | parent_process_ref | action_process_requested_parent_pid |
| x-oca-event | parent_process_ref | action_thread_parent_pid |
| x-oca-event | domain_ref | auth_domain |
| x-oca-event | domain_ref | dst_host_metadata_domain |
| x-oca-event | domain_ref | host_metadata_domain |
| x-oca-event | url_ref | dst_action_url_category |
| x-oca-event | registry_ref | action_registry_key_name |
| x-oca-event | registry_ref | action_registry_value_name |
| x-oca-event | agent | agent_hostname |
| x-oca-event | code | event_id |
| x-oca-event | extensions.x-paloalto-event.event_description | vpn_event_description |
| x-oca-event | created | event_timestamp |
| x-oca-event | extensions.x-paloalto-event.version | event_version |
| x-oca-event | extensions.x-paloalto-event.uuid | event_rpc_interface_uuid |
| x-oca-event | extensions.x-paloalto-event.path | event_address_mapped_image_path |
| x-oca-event | category | event_type |
| x-oca-event | action | event_sub_type |
| x-oca-event | process_ref | actor_process_instance_id |
| <br> | | |
| x-paloalto-evtlog | data_fields | action_evtlog_data_fields |
| x-paloalto-evtlog | description | action_evtlog_description |
| x-paloalto-evtlog | source | action_evtlog_source |
| x-paloalto-evtlog | evtlog_id | action_evtlog_event_id |
| x-paloalto-evtlog | level | action_evtlog_level |
| x-paloalto-evtlog | tid | action_evtlog_tid |
| x-paloalto-evtlog | uid | action_evtlog_uid |
| x-paloalto-evtlog | pid | action_evtlog_pid |
| x-paloalto-evtlog | message | action_evtlog_message |
| x-paloalto-evtlog | version | action_evtlog_version |
| <br> | | |
