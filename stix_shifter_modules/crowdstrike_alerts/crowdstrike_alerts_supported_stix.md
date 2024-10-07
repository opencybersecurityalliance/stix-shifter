##### Updated on 07/19/24
## CrowdStrike Falcon Alerts API
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparison) | %2B |
| OR (Comparison) | , |
| = | : |
| != | :! |
| > | :> |
| >= | :>= |
| < | :< |
| <= | :<= |
| IN | : |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **file**:name | filename, grandparent_details.filename, parent_details.filename, documents_accessed.filename, files_accessed.filename, executables_written.filename, files_written.filename, file_writes.name |
| **file**:hashes.'MD5' | md5, grandparent_details.md5, parent_details.md5 |
| **file**:hashes.'SHA-256' | sha256, grandparent_details.sha256, parent_details.sha256, file_writes.sha256 |
| **file**:accessed | timestamp, grandparent_details.timestamp, parent_details.timestamp, documents_accessed.timestamp, files_accessed.timestamp, executables_written.timestamp, files_written.timestamp |
| **file**:parent_directory_ref.path | filepath, grandparent_details.filepath, parent_details.filepath, documents_accessed.filepath, files_accessed.filepath, executables_written.filepath, files_written.filepath |
| **file**:parent_directory_ref.accessed | accessed, grandparent_details.accessed, parent_details.accessed, documents_accessed.timestamp, files_accessed.timestamp, executables_written.timestamp, files_written.timestamp |
| **directory**:path | filepath, grandparent_details.filepath, parent_details.filepath |
| **directory**:accessed | accessed, grandparent_details.accessed, parent_details.accessed, documents_accessed.timestamp, files_accessed.timestamp, executables_written.timestamp, files_written.timestamp |
| **process**:command_line | cmdline, grandparent_details.cmdline, parent_details.cmdline |
| **process**:pid | local_process_id, grandparent_details.local_process_id, parent_details.local_process_id |
| **process**:name | filename, grandparent_details.filename, parent_details.filename |
| **process**:cwd | filepath, grandparent_details.filepath, parent_details.filepath |
| **process**:created | timestamp, grandparent_details.timestamp, parent_details.timestamp |
| **process**:creator_user_ref.user_id | user_id, parent_details.user_id, grandparent_details.user_id |
| **process**:creator_user_ref.account_login | user_name, parent_details.user_name, grandparent_details.user_name |
| **process**:binary_ref.name | filename, grandparent_details.filename, parent_details.filename |
| **process**:binary_ref.accessed | timestamp, grandparent_details.timestamp, parent_details.timestamp |
| **process**:binary_ref.hashes.'MD5' | md5, grandparent_details.md5, parent_details.md5 |
| **process**:binary_ref.hashes.'SHA-256' | sha256, grandparent_details.sha256, parent_details.sha256 |
| **process**:binary_ref.parent_directory_ref.path | filepath, grandparent_details.filepath, parent_details.filepath |
| **process**:binary_ref.parent_directory_ref.accessed | accessed, grandparent_details.accessed, parent_details.accessed |
| **process**:parent_process_ref.command_line | grandparent_details.cmdline, parent_details.cmdline |
| **process**:parent_process_ref.pid | grandparent_details.local_process_id, parent_details.local_process_id |
| **process**:parent_process_ref.name | grandparent_details.filename, parent_details.filename |
| **process**:parent_process_ref.cwd | grandparent_details.filepath, parent_details.filepath |
| **process**:parent_process_ref.created | grandparent_details.timestamp, parent_details.timestamp |
| **process**:parent_process_ref.creator_user_ref.user_id | parent_details.user_id, grandparent_details.user_id |
| **process**:parent_process_ref.creator_user_ref.account_login | parent_details.user_name, grandparent_details.user_name |
| **process**:parent_process_ref.binary_ref.name | grandparent_details.filename, parent_details.filename |
| **process**:parent_process_ref.binary_ref.accessed | grandparent_details.timestamp, parent_details.timestamp |
| **process**:parent_process_ref.binary_ref.hashes.'MD5' | grandparent_details.md5, parent_details.md5 |
| **process**:parent_process_ref.binary_ref.hashes.'SHA-256' | grandparent_details.sha256, parent_details.sha256 |
| **process**:parent_process_ref.binary_ref.parent_directory_ref.path | grandparent_details.filepath, parent_details.filepath |
| **process**:parent_process_ref.binary_ref.parent_directory_ref.accessed | grandparent_details.accessed, parent_details.accessed |
| **process**:parent_process_ref.child_refs.command_line | cmdline |
| **process**:parent_process_ref.child_refs.pid | local_process_id |
| **process**:parent_process_ref.child_refs.name | filename |
| **process**:parent_process_ref.child_refs.cwd | filepath |
| **process**:parent_process_ref.child_refs.created | timestamp |
| **process**:parent_process_ref.child_refs.creator_user_ref.user_id | user_id |
| **process**:parent_process_ref.child_refs.creator_user_ref.account_login | user_name |
| **process**:parent_process_ref.child_refs.binary_ref.name | filename |
| **process**:parent_process_ref.child_refs.binary_ref.accessed | timestamp |
| **process**:parent_process_ref.child_refs.binary_ref.hashes.'MD5' | md5 |
| **process**:parent_process_ref.child_refs.binary_ref.hashes.'SHA-256' | sha256 |
| **process**:parent_process_ref.child_refs.binary_ref.parent_directory_ref.path | filepath |
| **process**:parent_process_ref.child_refs.binary_ref.parent_directory_ref.accessed | accessed |
| **process**:parent_process_ref.parent_process_ref.command_line | grandparent_details.cmdline |
| **process**:parent_process_ref.parent_process_ref.pid | grandparent_details.local_process_id |
| **process**:parent_process_ref.parent_process_ref.name | grandparent_details.filename |
| **process**:parent_process_ref.parent_process_ref.cwd | grandparent_details.filepath |
| **process**:parent_process_ref.parent_process_ref.created | grandparent_details.timestamp |
| **process**:parent_process_ref.parent_process_ref.creator_user_ref.user_id | parent_details.user_id |
| **process**:parent_process_ref.parent_process_ref.creator_user_ref.account_login | parent_details.user_name |
| **process**:parent_process_ref.parent_process_ref.binary_ref.name | grandparent_details.filename |
| **process**:parent_process_ref.parent_process_ref.binary_ref.accessed | grandparent_details.timestamp |
| **process**:parent_process_ref.parent_process_ref.binary_ref.hashes.'MD5' | grandparent_details.md5 |
| **process**:parent_process_ref.parent_process_ref.binary_ref.hashes.'SHA-256' | grandparent_details.sha256 |
| **process**:parent_process_ref.parent_process_ref.binary_ref.parent_directory_ref.path | grandparent_details.filepath |
| **process**:parent_process_ref.parent_process_ref.binary_ref.parent_directory_ref.accessed | grandparent_details.accessed |
| **user-account**:user_id | user_id, parent_details.user_id, grandparent_details.user_id |
| **user-account**:account_login | user_name, parent_details.user_name, grandparent_details.user_name |
| **url**:value | falcon_host_link, device.hostinfo.domain |
| **x-oca-event**:action | name |
| **x-oca-event**:description | description |
| **x-oca-event**:category | scenario |
| **x-oca-event**:severity | severity |
| **x-oca-event**:x_severity_name | severity_name |
| **x-oca-event**:created | created_timestamp |
| **x-oca-event**:start | process_start_time |
| **x-oca-event**:url_ref.value | falcon_host_link |
| **x-oca-event**:file_ref.name | filename, grandparent_details.filename, parent_details.filename |
| **x-oca-event**:file_ref.hashes.'MD5' | md5, grandparent_details.md5, parent_details.md5 |
| **x-oca-event**:file_ref.hashes.'SHA-256' | sha256, grandparent_details.sha256, parent_details.sha256 |
| **x-oca-event**:file_ref.accessed | timestamp, grandparent_details.timestamp, parent_details.timestamp |
| **x-oca-event**:file_ref.parent_directory_ref.path | filepath, grandparent_details.filepath, parent_details.filepath |
| **x-oca-event**:file_ref.parent_directory_ref.accessed | accessed, grandparent_details.accessed, parent_details.accessed |
| **x-oca-event**:domain_ref.value | logon_domain |
| **x-oca-event**:domain_ref.resolves_to_refs.value | device.external_ip, device.local_ip |
| **x-oca-event**:ip_refs.value | device.external_ip, device.local_ip |
| **x-oca-event**:user_ref.user_id | user_id, parent_details.user_id, grandparent_details.user_id |
| **x-oca-event**:user_ref.account_login | user_name, parent_details.user_name, grandparent_details.user_name |
| **x-oca-event**:process_ref.command_line | cmdline, grandparent_details.cmdline, parent_details.cmdline |
| **x-oca-event**:process_ref.pid | local_process_id, grandparent_details.local_process_id, parent_details.local_process_id |
| **x-oca-event**:process_ref.name | filename, grandparent_details.filename, parent_details.filename |
| **x-oca-event**:process_ref.cwd | filepath, grandparent_details.filepath, parent_details.filepath |
| **x-oca-event**:process_ref.created | timestamp, grandparent_details.timestamp, parent_details.timestamp |
| **x-oca-event**:process_ref.creator_user_ref.user_id | user_id, parent_details.user_id, grandparent_details.user_id |
| **x-oca-event**:process_ref.creator_user_ref.account_login | user_name, parent_details.user_name, grandparent_details.user_name |
| **x-oca-event**:process_ref.binary_ref.name | filename, grandparent_details.filename, parent_details.filename |
| **x-oca-event**:process_ref.binary_ref.accessed | timestamp, grandparent_details.timestamp, parent_details.timestamp |
| **x-oca-event**:process_ref.binary_ref.hashes.'MD5' | md5, grandparent_details.md5, parent_details.md5 |
| **x-oca-event**:process_ref.binary_ref.hashes.'SHA-256' | sha256, grandparent_details.sha256, parent_details.sha256 |
| **x-oca-event**:process_ref.binary_ref.parent_directory_ref.path | filepath, grandparent_details.filepath, parent_details.filepath |
| **x-oca-event**:process_ref.binary_ref.parent_directory_ref.accessed | accessed, grandparent_details.accessed, parent_details.accessed |
| **x-oca-event**:parent_process_ref.command_line | grandparent_details.cmdline, parent_details.cmdline |
| **x-oca-event**:parent_process_ref.pid | grandparent_details.local_process_id, parent_details.local_process_id |
| **x-oca-event**:parent_process_ref.name | grandparent_details.filename, parent_details.filename |
| **x-oca-event**:parent_process_ref.cwd | grandparent_details.filepath, parent_details.filepath |
| **x-oca-event**:parent_process_ref.created | grandparent_details.timestamp, parent_details.timestamp |
| **x-oca-event**:parent_process_ref.creator_user_ref.user_id | parent_details.user_id, grandparent_details.user_id |
| **x-oca-event**:parent_process_ref.creator_user_ref.account_login | parent_details.user_name, grandparent_details.user_name |
| **x-oca-event**:parent_process_ref.binary_ref.name | grandparent_details.filename, parent_details.filename |
| **x-oca-event**:parent_process_ref.binary_ref.accessed | grandparent_details.timestamp, parent_details.timestamp |
| **x-oca-event**:parent_process_ref.binary_ref.hashes.'MD5' | grandparent_details.md5, parent_details.md5 |
| **x-oca-event**:parent_process_ref.binary_ref.hashes.'SHA-256' | grandparent_details.sha256, parent_details.sha256 |
| **x-oca-event**:parent_process_ref.binary_ref.parent_directory_ref.path | grandparent_details.filepath, parent_details.filepath |
| **x-oca-event**:parent_process_ref.binary_ref.parent_directory_ref.accessed | grandparent_details.accessed, parent_details.accessed |
| **ipv4-addr**:value | device.external_ip, device.local_ip, network_accesses.local_address, network_accesses.remote_address |
| **ipv6-addr**:value | device.external_ip, device.local_ip, network_accesses.local_address, network_accesses.remote_address |
| **network-traffic**:start | network_accesses.access_timestamp |
| **network-traffic**:x_access_type | network_accesses.access_type |
| **network-traffic**:x_connection_direction | network_accesses.connection_direction |
| **network-traffic**:x_network_isIPV6 | network_accesses.isIPV6 |
| **network-traffic**:local_port | network_accesses.src_port |
| **network-traffic**:protocols | network_accesses.protocol |
| **network-traffic**:dst_port | network_accesses.remote_port |
| **mac-addr**:value | device.mac_address |
| **software**:version | device.os_version |
| **software**:name | device.platform_name, platform, os_name |
| **x-oca-asset**:device_id | device.device_id |
| **x-oca-asset**:hostname | device.hostname |
| **x-oca-asset**:ip_refs.value | device.external_ip, device.local_ip |
| **x-oca-asset**:mac_refs.value | device.mac_address |
| **x-oca-asset**:os_ref.version | device.os_version |
| **x-oca-asset**:os_ref.name | device.platform_name, platform |
| **x-oca-asset**:x_agent_load_flags | device.agent_load_flags |
| **x-oca-asset**:x_agent_local_time | device.agent_local_time |
| **x-oca-asset**:x_agent_version | device.agent_version |
| **x-oca-asset**:x_bios_manufacturer | device.bios_manufacturer |
| **x-oca-asset**:x_bios_version | device.bios_version |
| **x-oca-asset**:x_device_cid | device.cid |
| **x-oca-asset**:x_config_id_base | device.config_id_base |
| **x-oca-asset**:x_config_id_build | device.config_id_build |
| **x-oca-asset**:x_config_id_platform | device.config_id_platform |
| **x-oca-asset**:x_first_seen | device.first_seen |
| **x-oca-asset**:x_instance_id | device.instance_id |
| **x-oca-asset**:x_last_seen | device.last_seen |
| **x-oca-asset**:x_major_version | device.major_version |
| **x-oca-asset**:x_minor_version | device.minor_version |
| **x-oca-asset**:x_modified_timestamp | device.modified_timestamp |
| **x-oca-asset**:x_device_ou | device.ou |
| **x-oca-asset**:x_platform_id | device.platform_id |
| **x-oca-asset**:x_pod_labels | device.pod_labels |
| **x-oca-asset**:x_product_type | device.product_type |
| **x-oca-asset**:x_product_type_desc | device.product_type_desc |
| **x-oca-asset**:x_service_provider | device.service_provider |
| **x-oca-asset**:x_service_provider_account_id | device.service_provider_account_id |
| **x-oca-asset**:x_device_status | device.status |
| **x-oca-asset**:x_system_manufacturer | device.system_manufacturer |
| **x-oca-asset**:x_system_product_name | device.system_product_name |
| **x-crowdstrike**:agent_id | agent_id |
| **x-crowdstrike**:aggregate_id | aggregate_id |
| **x-crowdstrike**:alleged_filetype | alleged_filetype |
| **x-crowdstrike**:author | author |
| **x-crowdstrike**:child_process_ids | child_process_ids |
| **x-crowdstrike**:cid | cid |
| **x-crowdstrike**:cloud_indicator | cloud_indicator |
| **x-crowdstrike**:composite_id | composite_id |
| **x-crowdstrike**:confidence | confidence |
| **x-crowdstrike**:context_timestamp | context_timestamp |
| **x-crowdstrike**:control_graph_id | control_graph_id |
| **x-crowdstrike**:crawled_timestamp | crawled_timestamp |
| **x-crowdstrike**:data_domains | data_domains |
| **x-crowdstrike**:display_name | display_name |
| **x-crowdstrike**:email_sent | email_sent |
| **x-crowdstrike**:entity_values | entity_values |
| **x-crowdstrike**:event_status | status |
| **x-crowdstrike**:global_prevalence | global_prevalence |
| **x-crowdstrike**:grandparent_user_graph_id | grandparent_details.user_graph_id |
| **x-crowdstrike**:id | id |
| **x-crowdstrike**:incident_start_time | start_time, incident.start_time |
| **x-crowdstrike**:incident_start_time_epoch | start_time_epoch |
| **x-crowdstrike**:incident_end_time | end_time |
| **x-crowdstrike**:incident_end_time_epoch | end_time_epoch, incident.end_time |
| **x-crowdstrike**:indicator_id | indicator_id |
| **x-crowdstrike**:ioc_context | ioc_context |
| **x-crowdstrike**:ioc_description | ioc_description |
| **x-crowdstrike**:ioc_source | ioc_source |
| **x-crowdstrike**:ioc_type | ioc_type |
| **x-crowdstrike**:ioc_value | ioc_value |
| **x-crowdstrike**:ioc_values | ioc_values |
| **x-crowdstrike**:local_prevalence | local_prevalence |
| **x-crowdstrike**:logon_domain | logon_domain |
| **x-crowdstrike**:no_signal | no_signal |
| **x-crowdstrike**:objective | objective |
| **x-crowdstrike**:parent_process_id | parent_process_id, parent_details.process_id |
| **x-crowdstrike**:parent_user_graph_id | parent_details.user_graph_id |
| **x-crowdstrike**:pattern_disposition | pattern_disposition |
| **x-crowdstrike**:pattern_disposition_description | pattern_disposition_description |
| **x-crowdstrike**:pattern_id | pattern_id |
| **x-crowdstrike**:poly_id | poly_id |
| **x-crowdstrike**:parent_process_graph_id | parent_details.process_graph_id |
| **x-crowdstrike**:grandparent_process_graph_id | grandparent_details.process_graph_id |
| **x-crowdstrike**:process_id | process_id |
| **x-crowdstrike**:grandparent_process_id | grandparent_details.process_id |
| **x-crowdstrike**:scenario | scenario |
| **x-crowdstrike**:sha1 | sha1 |
| **x-crowdstrike**:seconds_to_resolved | seconds_to_resolved |
| **x-crowdstrike**:seconds_to_triaged | seconds_to_triaged |
| **x-crowdstrike**:show_in_ui | show_in_ui |
| **x-crowdstrike**:source_event_model | source_event_model |
| **x-crowdstrike**:source_products | source_products |
| **x-crowdstrike**:source_vendors | source_vendors |
| **x-crowdstrike**:source_vertex_id | references.source_vertex_id |
| **x-crowdstrike**:source_vertex_type | references.source_vertex_type |
| **x-crowdstrike**:template_instance_id | template_instance_id |
| **x-crowdstrike**:tactic | tactic |
| **x-crowdstrike**:tactic_id | tactic_id |
| **x-crowdstrike**:technique | technique |
| **x-crowdstrike**:technique_id | technique_id |
| **x-crowdstrike**:tree_id | tree_id |
| **x-crowdstrike**:tree_root | tree_root |
| **x-crowdstrike**:triggering_process_graph_id | triggering_process_graph_id |
| **x-crowdstrike**:type | type |
| **x-crowdstrike**:updated_timestamp | updated_timestamp |
| **x-crowdstrike**:xdr_detection_id | xdr_detection_id |
| **x-crowdstrike**:xdr_pattern_id | xdr_pattern_id |
| **x-crowdstrike**:xdr_rule_id | xdr_rule_id |
| **x-crowdstrike**:xdr_source_event_id | references.xdr_source_event_id |
| **x-crowdstrike**:xdr_type | xdr_type |
| **x-crowdstrike**:incident_classification | incident.classification |
| **x-crowdstrike**:incident_created_time | incident.created_time |
| **x-crowdstrike**:incident_highest_score | incident.highest_score |
| **x-crowdstrike**:incident_host_ids | incident.host_ids |
| **x-crowdstrike**:incident_score | incident.score |
| **x-crowdstrike**:incident_state | incident.state |
| **x-crowdstrike**:incident_type | incident.type |
| **x-crowdstrike**:incident_version | incident.version |
| **x-crowdstrike**:incident_created | incident.created |
| **x-crowdstrike**:incident_end | incident.end |
| **x-crowdstrike**:incident_id | incident.id |
| **x-crowdstrike**:incident_start | incident.start |
| **x-crowdstrike**:has_script_or_module_ioc | has_script_or_module_ioc |
| **x-crowdstrike**:process_end_time | process_end_time |
| **x-crowdstrike**:agent_scan_id | agent_scan_id |
| **x-crowdstrike**:event_id | event_id |
| **x-crowdstrike**:quarantined | quarantined |
| **x-crowdstrike**:scan_id | scan_id |
| **x-crowdstrike**:list_of_agent_ids | entities.agent_ids |
| **x-crowdstrike**:list_of_alert_ids | refereneces.indicator_alert_ids |
| **x-crowdstrike**:list_of_detection_ids | refereneces.indicator_detection_ids |
| **x-crowdstrike**:list_of_vertex_ids | refereneces.indicator_vertex_ids |
| **x-crowdstrike**:list_of_indicator_ids | refereneces.xdr_indicator_ids |
| **x-crowdstrike**:list_of_tactic_ids | tactic_ids |
| **x-crowdstrike**:list_of_tactics | tactics |
| **x-crowdstrike**:list_of_technique_ids | technique_ids |
| **x-crowdstrike**:list_of_techniques | techniques |
| **x-crowdstrike**:list_of_domains | entities.domain |
| **x-crowdstrike**:list_of_file_names | entities.file_name |
| **x-crowdstrike**:list_of_image_file_names | entities.image_file_name |
| **x-crowdstrike**:list_of_ipv4 | entities.ipv4 |
| **x-crowdstrike**:list_of_processes | entities.process |
| **x-crowdstrike**:list_of_sha256 | entities.sha256 |
| **x-crowdstrike**:blocking_unsupported_or_disabled | pattern_disposition_details.blocking_unsupported_or_disabled |
| **x-crowdstrike**:bootup_safeguard_enabled | pattern_disposition_details.bootup_safeguard_enabled |
| **x-crowdstrike**:critical_process_disabled | pattern_disposition_details.critical_process_disabled |
| **x-crowdstrike**:detect | pattern_disposition_details.detect |
| **x-crowdstrike**:handle_operation_downgraded | pattern_disposition_details.handle_operation_downgraded |
| **x-crowdstrike**:inddet_mask | pattern_disposition_details.inddet_mask |
| **x-crowdstrike**:indicator | pattern_disposition_details.indicator |
| **x-crowdstrike**:fs_operation_blocked | pattern_disposition_details.fs_operation_blocked |
| **x-crowdstrike**:kill_action_failed | pattern_disposition_details.kill_action_failed |
| **x-crowdstrike**:kill_parent | pattern_disposition_details.kill_parent |
| **x-crowdstrike**:kill_process | pattern_disposition_details.kill_process |
| **x-crowdstrike**:kill_subprocess | pattern_disposition_details.kill_subprocess |
| **x-crowdstrike**:operation_blocked | pattern_disposition_details.operation_blocked |
| **x-crowdstrike**:policy_disabled | pattern_disposition_details.policy_disabled |
| **x-crowdstrike**:process_blocked | pattern_disposition_details.process_blocked |
| **x-crowdstrike**:quarantine_file | pattern_disposition_details.quarantine_file |
| **x-crowdstrike**:quarantine_machine | pattern_disposition_details.quarantine_machine |
| **x-crowdstrike**:registry_operation_blocked | pattern_disposition_details.registry_operation_blocked |
| **x-crowdstrike**:rooting | pattern_disposition_details.rooting |
| **x-crowdstrike**:sensor_only | pattern_disposition_details.sensor_only |
| **x-crowdstrike**:suspend_parent | pattern_disposition_details.suspend_parent |
| **x-crowdstrike**:suspend_process | pattern_disposition_details.suspend_process |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | filepath |
| directory | accessed | timestamp |
| <br> | | |
| file | filename | filename |
| file | parent_directory_ref | filepath |
| file | hashes.'MD5' | md5 |
| file | hashes.'SHA-256' | sha256 |
| file | accessed | timestamp |
| file | hashes'.SHA-256' | sha256 |
| file | filename | name |
| <br> | | |
| ipv4-addr | value | external_ip |
| ipv4-addr | value | local_ip |
| ipv4-addr | value | local_address |
| ipv4-addr | value | remote_address |
| <br> | | |
| mac-addr | value | mac_address |
| <br> | | |
| network-traffic | start | access_timestamp |
| network-traffic | x_access_type | access_type |
| network-traffic | x_connection_direction | connection_direction |
| network-traffic | x_network_isIPV6 | isIPV6 |
| network-traffic | src_ref | local_address |
| network-traffic | src_port | local_port |
| network-traffic | protocols | protocol |
| network-traffic | dst_ref | remote_address |
| network-traffic | dst_port | remote_port |
| <br> | | |
| process | command_line | cmdline |
| process | name | filename |
| process | binary_ref | filename |
| process | parent_process_ref | cmdline |
| process | child_refs | cmdline |
| process | pid | local_process_id |
| process | created | timestamp |
| process | creator_user_ref | user_id |
| <br> | | |
| software | version | os_version |
| software | name | platform_name |
| software | name | platform |
| software | name | os_name |
| <br> | | |
| url | value | domain |
| url | value | falcon_host_link |
| <br> | | |
| user-account | user_id | user_id |
| user-account | account_login | user_name |
| <br> | | |
| x-crowdstrike | agent_id | agent_id |
| x-crowdstrike | aggregate_id | aggregate_id |
| x-crowdstrike | alleged_filetype | alleged_filetype |
| x-crowdstrike | child_process_ids | child_process_ids |
| x-crowdstrike | cid | cid |
| x-crowdstrike | cloud_indicator | cloud_indicator |
| x-crowdstrike | composite_id | composite_id |
| x-crowdstrike | confidence | confidence |
| x-crowdstrike | context_timestamp | context_timestamp |
| x-crowdstrike | control_graph_id | control_graph_id |
| x-crowdstrike | crawled_timestamp | crawled_timestamp |
| x-crowdstrike | data_domains | data_domains |
| x-crowdstrike | display_name | display_name |
| x-crowdstrike | email_sent | email_sent |
| x-crowdstrike | global_prevalence | global_prevalence |
| x-crowdstrike | grandparent_process_graph_id | process_graph_id |
| x-crowdstrike | grandparent_process_id | process_id |
| x-crowdstrike | grandparent_user_graph_id | user_graph_id |
| x-crowdstrike | id | id |
| x-crowdstrike | indicator_id | indicator_id |
| x-crowdstrike | ioc_context | ioc_context |
| x-crowdstrike | ioc_values | ioc_values |
| x-crowdstrike | local_prevalence | local_prevalence |
| x-crowdstrike | logon_domain | logon_domain |
| x-crowdstrike | objective | objective |
| x-crowdstrike | parent_process_graph_id | process_graph_id |
| x-crowdstrike | process_id | process_id |
| x-crowdstrike | parent_user_graph_id | user_graph_id |
| x-crowdstrike | parent_process_id | parent_process_id |
| x-crowdstrike | pattern_disposition | pattern_disposition |
| x-crowdstrike | pattern_disposition_description | pattern_disposition_description |
| x-crowdstrike | blocking_unsupported_or_disabled | blocking_unsupported_or_disabled |
| x-crowdstrike | bootup_safeguard_enabled | bootup_safeguard_enabled |
| x-crowdstrike | critical_process_disabled | critical_process_disabled |
| x-crowdstrike | detect | detect |
| x-crowdstrike | fs_operation_blocked | fs_operation_blocked |
| x-crowdstrike | handle_operation_downgraded | handle_operation_downgraded |
| x-crowdstrike | inddet_mask | inddet_mask |
| x-crowdstrike | indicator | indicator |
| x-crowdstrike | kill_action_failed | kill_action_failed |
| x-crowdstrike | kill_parent | kill_parent |
| x-crowdstrike | kill_process | kill_process |
| x-crowdstrike | kill_subprocess | kill_subprocess |
| x-crowdstrike | operation_blocked | operation_blocked |
| x-crowdstrike | policy_disabled | policy_disabled |
| x-crowdstrike | process_blocked | process_blocked |
| x-crowdstrike | quarantine_file | quarantine_file |
| x-crowdstrike | quarantine_machine | quarantine_machine |
| x-crowdstrike | registry_operation_blocked | registry_operation_blocked |
| x-crowdstrike | rooting | rooting |
| x-crowdstrike | sensor_only | sensor_only |
| x-crowdstrike | suspend_parent | suspend_parent |
| x-crowdstrike | suspend_process | suspend_process |
| x-crowdstrike | pattern_id | pattern_id |
| x-crowdstrike | poly_id | poly_id |
| x-crowdstrike | seconds_to_resolved | seconds_to_resolved |
| x-crowdstrike | seconds_to_triaged | seconds_to_triaged |
| x-crowdstrike | sha1 | sha1 |
| x-crowdstrike | show_in_ui | show_in_ui |
| x-crowdstrike | source_products | source_products |
| x-crowdstrike | source_vendors | source_vendors |
| x-crowdstrike | event_status | status |
| x-crowdstrike | tactic | tactic |
| x-crowdstrike | tactic_id | tactic_id |
| x-crowdstrike | technique | technique |
| x-crowdstrike | technique_id | technique_id |
| x-crowdstrike | template_instance_id | template_instance_id |
| x-crowdstrike | tree_id | tree_id |
| x-crowdstrike | tree_root | tree_root |
| x-crowdstrike | triggering_process_graph_id | triggering_process_graph_id |
| x-crowdstrike | type | type |
| x-crowdstrike | updated_timestamp | updated_timestamp |
| x-crowdstrike | incident_start_time_epoch | start_time_epoch |
| x-crowdstrike | incident_end_time_epoch | end_time_epoch |
| x-crowdstrike | xdr_detection_id | xdr_detection_id |
| x-crowdstrike | xdr_pattern_id | xdr_pattern_id |
| x-crowdstrike | xdr_rule_id | xdr_rule_id |
| x-crowdstrike | xdr_type | xdr_type |
| x-crowdstrike | no_signal | no_signal |
| x-crowdstrike | entity_values | entity_values |
| x-crowdstrike | source_event_model | source_event_model |
| x-crowdstrike | has_script_or_module_ioc | has_script_or_module_ioc |
| x-crowdstrike | ioc_description | ioc_description |
| x-crowdstrike | ioc_source | ioc_source |
| x-crowdstrike | ioc_type | ioc_type |
| x-crowdstrike | ioc_value | ioc_value |
| x-crowdstrike | process_end_time | process_end_time |
| x-crowdstrike | agent_scan_id | agent_scan_id |
| x-crowdstrike | event_id | event_id |
| x-crowdstrike | quarantined | quarantined |
| x-crowdstrike | scan_id | scan_id |
| x-crowdstrike | incident | classification |
| x-crowdstrike | incident_created_time | created_time |
| x-crowdstrike | incident_highest_score | highest_score |
| x-crowdstrike | incident_host_ids | host_ids |
| x-crowdstrike | incident_score | score |
| x-crowdstrike | incident_state | state |
| x-crowdstrike | incident_type | type |
| x-crowdstrike | incident_version | version |
| x-crowdstrike | incident_start_time | start_time |
| x-crowdstrike | incident_end_time | end_time |
| x-crowdstrike | incident_created | created |
| x-crowdstrike | incident_end | end |
| x-crowdstrike | incident_id | id |
| x-crowdstrike | incident_start | start |
| x-crowdstrike | author | author |
| x-crowdstrike | source_vertex_id | source_vertex_id |
| x-crowdstrike | source_vertex_type | source_vertex_type |
| x-crowdstrike | xdr_source_event_id | xdr_source_event_id |
| x-crowdstrike | list_of_alert_ids | indicator_alert_ids |
| x-crowdstrike | list_of_detection_ids | indicator_detection_ids |
| x-crowdstrike | list_of_vertex_ids | indicator_vertex_ids |
| x-crowdstrike | list_of_indicator_ids | xdr_indicator_ids |
| x-crowdstrike | list_of_agent_ids | agent_ids |
| x-crowdstrike | list_of_domains | domain |
| x-crowdstrike | list_of_file_names | file_name |
| x-crowdstrike | list_of_image_file_names | image_file_name |
| x-crowdstrike | list_of_ipv4 | ipv4 |
| x-crowdstrike | list_of_processes | process |
| x-crowdstrike | list_of_sha256 | sha256 |
| x-crowdstrike | list_of_tactic_ids | tactic_ids |
| x-crowdstrike | list_of_tactics | tactics |
| x-crowdstrike | list_of_technique_ids | technique_ids |
| x-crowdstrike | list_of_techniques | techniques |
| x-crowdstrike | documents_accessed | groupReference |
| x-crowdstrike | files_accessed | groupReference |
| x-crowdstrike | executables_written | groupReference |
| x-crowdstrike | files_written | groupReference |
| x-crowdstrike | file_writes | groupReference |
| x-crowdstrike | network_objects | groupReference |
| <br> | | |
| x-oca-asset | x_agent_load_flags | agent_load_flags |
| x-oca-asset | x_agent_local_time | agent_local_time |
| x-oca-asset | x_agent_version | agent_version |
| x-oca-asset | x_bios_manufacturer | bios_manufacturer |
| x-oca-asset | x_bios_version | bios_version |
| x-oca-asset | x_device_cid | cid |
| x-oca-asset | x_config_id_base | config_id_base |
| x-oca-asset | x_config_id_build | config_id_build |
| x-oca-asset | x_config_id_platform | config_id_platform |
| x-oca-asset | device_id | device_id |
| x-oca-asset | ip_refs | external_ip |
| x-oca-asset | x_first_seen | first_seen |
| x-oca-asset | hostname | hostname |
| x-oca-asset | x_instance_id | instance_id |
| x-oca-asset | x_last_seen | last_seen |
| x-oca-asset | ip_refs | local_ip |
| x-oca-asset | mac_refs | mac_address |
| x-oca-asset | x_major_version | major_version |
| x-oca-asset | x_minor_version | minor_version |
| x-oca-asset | x_modified_timestamp | modified_timestamp |
| x-oca-asset | os_ref | os_version |
| x-oca-asset | x_device_ou | ou |
| x-oca-asset | x_platform_id | platform_id |
| x-oca-asset | x_pod_labels | pod_labels |
| x-oca-asset | x_product_type | product_type |
| x-oca-asset | x_product_type_desc | product_type_desc |
| x-oca-asset | x_service_provider | service_provider |
| x-oca-asset | x_service_provider_account_id | service_provider_account_id |
| x-oca-asset | x_device_status | status |
| x-oca-asset | x_system_manufacturer | system_manufacturer |
| x-oca-asset | x_system_product_name | system_product_name |
| x-oca-asset | os_ref | os_name |
| <br> | | |
| x-oca-event | process_ref | cmdline |
| x-oca-event | created | created_timestamp |
| x-oca-event | description | description |
| x-oca-event | ip_refs | external_ip |
| x-oca-event | ip_refs | local_ip |
| x-oca-event | url_ref | falcon_host_link |
| x-oca-event | file_ref | filename |
| x-oca-event | action | name |
| x-oca-event | start | process_start_time |
| x-oca-event | category | scenario |
| x-oca-event | severity | severity |
| x-oca-event | x_severity_name | severity_name |
| x-oca-event | user_ref | user_id |
| <br> | | |
