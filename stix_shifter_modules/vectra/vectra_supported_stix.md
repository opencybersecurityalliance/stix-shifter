##### Updated on 05/23/24
## Vectra NDR
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparison) | AND |
| OR (Comparison) | OR |
| > | :> |
| < | :< |
| >= | :>= |
| <= | :<= |
| = | : |
| LIKE | : |
| IN | : |
| MATCHES | :* |
| != | : |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | detection.src_ip, detection.grouped_details.dst_ips, detection.grouped_details.dst_hosts.dst_ip, detection.grouped_details.normal_admin_hosts.ip, detection.grouped_details.dst_hosts.ip, detection.grouped_details.origin_ip, detection.grouped_details.sessions.dst_ip, detection.grouped_details.events.dst_ip, detection.grouped_details.events.dst_ips, detection.grouped_details.events.sessions.dst_ip, detection.grouped_details.connection_events.target_host.ip |
| **ipv6-addr**:value | detection.src_ip, detection.grouped_details.dst_ips, detection.grouped_details.dst_hosts.dst_ip, detection.grouped_details.normal_admin_hosts.ip, detection.grouped_details.dst_hosts.ip, detection.grouped_details.origin_ip, detection.grouped_details.sessions.dst_ip, detection.grouped_details.events.dst_ip, detection.grouped_details.events.dst_ips, detection.grouped_details.events.sessions.dst_ip, detection.grouped_details.connection_events.target_host.ip |
| **domain-name**:value | detection.grouped_details.target_domains, detection.grouped_details.origin_domain, detection.grouped_details.events.target_domains, detection.grouped_details.connection_events.target_host.dst_dns |
| **network-traffic**:dst_port | detection.grouped_details.dst_ports, detection.grouped_details.dst_hosts.dst_port, detection.grouped_details.origin_port, detection.grouped_details.sessions.dst_port, detection.grouped_details.events.dst_ports, detection.grouped_details.events.sessions.dst_port, detection.grouped_details.events.target_summary.dst_port, detection.grouped_details.connection_events.dst_port |
| **network-traffic**:src_port | detection.grouped_details.src_port |
| **network-traffic**:src_ref.value | detection.src_ip |
| **network-traffic**:dst_ref.value | detection.grouped_details.dst_ips, detection.grouped_details.dst_hosts.dst_ip, detection.grouped_details.sessions.dst_ip, detection.grouped_details.origin_ip, detection.grouped_details.events.sessions.dst_ip, detection.grouped_details.connection_events.target_host.ip |
| **network-traffic**:protocols[*] | detection.grouped_details.protocol, detection.grouped_details.app_protocol, detection.grouped_details.dst_protocol, detection.grouped_details.origin_protocol, detection.grouped_details.sessions.protocol, detection.grouped_details.sessions.app_protocol, detection.grouped_details.events.protocol, detection.grouped_details.events.sessions.app_protocol, detection.grouped_details.events.sessions.protocol, detection.grouped_details.events.target_summary.app_protocol, detection.grouped_details.events.target_summary.protocol, detection.grouped_details.connection_events.protocol |
| **network-traffic**:src_byte_count | detection.grouped_details.bytes_sent, detection.grouped_details.sessions.bytes_sent, detection.grouped_details.events.bytes_sent, detection.grouped_details.connection_events.total_bytes_sent |
| **network-traffic**:dst_byte_count | detection.grouped_details.bytes_received, detection.grouped_details.sessions.bytes_received, detection.grouped_details.events.bytes_received, detection.grouped_details.events.sessions.bytes_received, detection.grouped_details.connection_events.total_bytes_rcvd |
| **network-traffic**:start | detection.first_timestamp, detection.grouped_details.first_timestamp, detection.grouped_details.sessions.first_timestamp, detection.grouped_details.events.first_timestamp, detection.grouped_details.events.sessions.first_timestamp, detection.grouped_details.events.target_summary.first_timestamp, detection.grouped_details.connection_events.first_timestamp |
| **network-traffic**:end | detection.last_timestamp, detection.grouped_details.last_timestamp, detection.grouped_details.dst_hosts.last_timestamp, detection.grouped_details.sessions.last_timestamp, detection.grouped_details.events.last_seen, detection.grouped_details.events.last_timestamp, detection.grouped_details.events.target_summary.last_timestamp, detection.grouped_details.connection_events.last_timestamp |
| **network-traffic**:x_count | detection.grouped_details.events.count |
| **network-traffic**:x_dst_country | detection.grouped_details.events.dst_country |
| **network-traffic**:x_num_accounts | detection.grouped_details.num_accounts |
| **network-traffic**:x_reason | detection.grouped_details.reason |
| **network-traffic**:x_num_attempts | detection.grouped_details.num_attempts |
| **network-traffic**:x_tunnel_type | detection.grouped_details.sessions.tunnel_type |
| **network-traffic**:x_num_sessions | detection.grouped_details.num_sessions |
| **network-traffic**:x_user_agent | detection.grouped_details.user_agent |
| **network-traffic**:x_dst_geo_latitude | detection.grouped_details.dst_geo_lat, detection.grouped_details.origin_geo_lat |
| **network-traffic**:x_dst_geo_longitude | detection.grouped_details.dst_geo_lon, detection.grouped_details.origin_geo_lon |
| **network-traffic**:x_dst_geo | detection.grouped_details.dst_geo, detection.grouped_details.origin_geo |
| **network-traffic**:x_num_response_objects | detection.grouped_details.num_response_objects |
| **network-traffic**:x_client_name | detection.grouped_details.client_name |
| **network-traffic**:x_client_token | detection.grouped_details.client_token |
| **network-traffic**:x_is_normally_accessed_by_rdp | detection.grouped_details.events.is_normally_accessed_by_rdp |
| **network-traffic**:x_rpc_uuid | detection.grouped_details.uuid |
| **network-traffic**:x_nt_referrer | detection.grouped_details.events.referrer |
| **network-traffic**:x_num_events | detection.grouped_details.num_events |
| **network-traffic**:x_time_duration | detection.grouped_details.duration, detection.grouped_details.events.duration, detection.grouped_details.events.sessions.duration, detection.grouped_details.connection_events.duration_int |
| **network-traffic**:x_status_code | detection.grouped_details.status_code |
| **network-traffic**:x_named_pipe | detection.grouped_details.named_pipe |
| **network-traffic**:x_uri | detection.grouped_details.uri |
| **network-traffic**:x_src_session_uid | detection.grouped_details.metadata.orig_sluid |
| **network-traffic**:x_executed_functions | detection.grouped_details.executed_functions |
| **network-traffic**:x_event_type | detection.grouped_details.events.event_type |
| **network-traffic**:x_error_code | detection.grouped_details.events.error_code |
| **network-traffic**:x_target_domain_refs[*].value | detection.grouped_details.events.target_domains |
| **network-traffic**:x_is_external | detection.grouped_details.connection_events.is_external |
| **network-traffic**:x_request_uri | detection.grouped_details.uri |
| **network-traffic**:x_period_identified | detection.grouped_details.period_identified |
| **network-traffic**:x_smb_share | detection.grouped_details.share |
| **network-traffic**:x_account_uid | detection.grouped_details.account_uid |
| **network-traffic**:extensions.'http-request-ext'.request_method | detection.grouped_details.events.http_method |
| **network-traffic**:extensions.'http-request-ext'.x_response_code | detection.grouped_details.events.response_code |
| **network-traffic**:extensions.'http-request-ext'.request_header.'User-Agent' | detection.grouped_details.user_agent |
| **user-account**:user_id | detection.grouped_details.dst_accounts.uid, detection.grouped_details.src_account.name, detection.grouped_details.normal_users, detection.summary.accounts |
| **user-account**:account_login | detection.grouped_details.src_account.name |
| **user-account**:x_privilege_category | detection.grouped_details.src_account.privilege_category |
| **user-account**:x_privilege_level | detection.grouped_details.src_account.privilege_level |
| **x-ibm-finding**:name | detection.detection_type |
| **x-ibm-finding**:alert_id | detection.id |
| **x-ibm-finding**:description | detection.description, detection.summary.description |
| **x-ibm-finding**:x_num_sessions | detection.grouped_details.num_sessions |
| **x-ibm-finding**:severity | detection.threat |
| **x-ibm-finding**:confidence | detection.certainty |
| **x-ibm-finding**:start | detection.first_timestamp |
| **x-ibm-finding**:end | detection.last_timestamp |
| **x-ibm-finding**:time_observed | detection.created_timestamp |
| **x-ibm-finding**:event_count | detection.summary.num_sessions, detection.summary.num_attempts |
| **x-ibm-finding**:x_state | detection.state |
| **x-ibm-finding**:x_num_successes | detection.summary.num_successes |
| **x-ibm-finding**:x_assigned_to | detection.assigned_to |
| **x-ibm-finding**:x_assigned_date | detection.assigned_date |
| **x-ibm-finding**:x_sensor_name | detection.sensor_name |
| **x-ibm-finding**:x_is_triaged | detection.is_triaged |
| **x-ibm-finding**:src_ip_ref | detection.src_ip |
| **x-ibm-finding**:x_dst_ports | detection.summary.dst_ports |
| **x-ibm-finding**:x_account_refs.user_id | detection.summary.accounts |
| **x-ibm-finding**:x_shares | detection.summary.shares |
| **x-ibm-finding**:x_probable_owner | detection.summary.probable_owner |
| **x-ibm-finding**:x_matches | detection.summary.matches |
| **x-ibm-ttp-tagging**:name | detection.detection_type |
| **x-ibm-ttp-tagging**:confidence | detection.certainty |
| **x-ibm-ttp-tagging**:kill_chain_phases.phase_name | detection.detection_category |
| **x-oca-asset**:hostname | detection.src_host.name |
| **x-oca-asset**:device_id | detection.src_host.id |
| **x-oca-asset**:x_is_key_asset | detection.src_host.is_key_asset |
| **x-oca-asset**:ip_refs[*].value | detection.src_ip |
| **x-oca-asset**:x_threat | detection.src_host.threat |
| **x-oca-asset**:x_certainty | detection.src_host.certainty |
| **x-oca-asset**:x_privilege_category | detection.grouped_details.src_host.privilege_category |
| **x-oca-asset**:x_privilege_level | detection.grouped_details.src_host.privilege_level |
| **x-grouped-details**:first_seen | detection.grouped_details.first_seen |
| **x-grouped-details**:last_seen | detection.grouped_details.last_seen |
| **x-grouped-details**:detection_source | detection.grouped_details.detection_source |
| **x-grouped-details**:detection_slug | detection.grouped_details.detection_slug |
| **x-grouped-details**:account_ref.user_id | detection.grouped_details.src_account.name |
| **x-grouped-details**:ja3_hashes | detection.grouped_details.ja3_hashes |
| **x-grouped-details**:ja3s_hashes | detection.grouped_details.ja3s_hashes |
| **x-grouped-details**:x_num_sessions | detection.grouped_details.num_sessions |
| **x-grouped-details**:start | detection.grouped_details.first_timestamp |
| **x-grouped-details**:end | detection.grouped_details.last_timestamp |
| **x-grouped-details**:count | detection.grouped_details.count |
| **x-grouped-details**:client_name | detection.grouped_details.client_name |
| **x-grouped-details**:client_token | detection.grouped_details.client_token |
| **x-grouped-details**:dst_byte_count | detection.grouped_details.bytes_received |
| **x-grouped-details**:src_byte_count | detection.grouped_details.bytes_sent |
| **x-grouped-details**:subnet | detection.grouped_details.subnet |
| **x-grouped-details**:rpc_function_uuid | detection.grouped_details.uuid |
| **x-grouped-details**:num_services_requested | detection.grouped_details.num_services_requested |
| **x-grouped-details**:num_services_high_privilege | detection.grouped_details.num_services_high_privilege |
| **x-grouped-details**:service_privilege | detection.grouped_details.service_privilege |
| **x-service-accessed-info**:name | detection.grouped_details.service_accessed.name |
| **x-service-accessed-info**:privilege_category | detection.grouped_details.service_accessed.privilege_category |
| **x-service-accessed-info**:privilege_level | detection.grouped_details.service_accessed.privilege_level |
| **x-ldap-event**:base_object | detection.grouped_details.events.base_object |
| **x-ldap-event**:request | detection.grouped_details.events.request |
| **x-ldap-event**:response_code | detection.grouped_details.events.response_code |
| **x-ldap-event**:num_response_objects | detection.grouped_details.events.num_response_objects |
| **x-ldap-event**:last_timestamp | detection.grouped_details.events.last_timestamp |
| **x-sql-request-info**:http_segment | detection.grouped_details.targets.events.http_segment |
| **x-sql-request-info**:user_agent | detection.grouped_details.targets.events.user_agent |
| **x-sql-request-info**:sql_fragment | detection.grouped_details.targets.events.sql_fragment |
| **x-sql-request-info**:response_code | detection.grouped_details.targets.events.response_code |
| **x-sql-request-info**:bytes_received | detection.grouped_details.targets.events.bytes_received |
| **x-sql-request-info**:last_seen | detection.grouped_details.targets.events.last_seen |
| **x-anomalous-rpc**:function_call | detection.grouped_details.anomalous_profiles.function_call |
| **x-anomalous-rpc**:rpc_function_uuid | detection.grouped_details.anomalous_profiles.function_uuid |
| **x-anomalous-rpc**:count | detection.grouped_details.anomalous_profiles.count |
| **x-anomalous-rpc**:start | detection.grouped_details.anomalous_profiles.first_timestamp |
| **x-anomalous-rpc**:end | detection.grouped_details.anomalous_profiles.last_timestamp |
| **x-services-requested**:service | detection.grouped_details.services_requested.service |
| **x-new-host-info**:artifact | detection.grouped_details.artifact |
| **x-new-host-info**:via | detection.grouped_details.via |
| **x-new-host-info**:role | detection.grouped_details.role |
| **x-new-host-info**:end | detection.grouped_details.last_timestamp |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| domain-name | value | target_domains |
| domain-name | value | origin_domain |
| domain-name | resolves_to_refs | origin_ip |
| domain-name | value | dst_dns |
| domain-name | resolves_to_refs | dst_dns |
| <br> | | |
| ipv4-addr | value | src_ip |
| ipv4-addr | value | dst_ips |
| ipv4-addr | value | ip |
| ipv4-addr | value | origin_ip |
| ipv4-addr | value | dst_ip |
| <br> | | |
| ipv6-addr | value | src_ip |
| ipv6-addr | value | dst_ips |
| ipv6-addr | value | ip |
| ipv6-addr | value | origin_ip |
| ipv6-addr | value | dst_ip |
| <br> | | |
| network-traffic | protocols | protocol |
| network-traffic | protocols | app_protocol |
| network-traffic | protocols | dst_protocol |
| network-traffic | dst_port | dst_ports |
| network-traffic | dst_ref | dst_ips |
| network-traffic | dst_ref | groupdstReference |
| network-traffic | x_normal_admin_host_refs | groupNormalHostReference |
| network-traffic | src_port | src_port |
| network-traffic | dst_byte_count | bytes_received |
| network-traffic | src_byte_count | bytes_sent |
| network-traffic | start | first_timestamp |
| network-traffic | end | last_timestamp |
| network-traffic | src_ref | last_timestamp |
| network-traffic | x_time_duration | duration |
| network-traffic | x_dst_geo | dst_geo |
| network-traffic | x_dst_geo_latitude | dst_geo_lat |
| network-traffic | x_dst_geo_longitude | dst_geo_lon |
| network-traffic | x_reason_message | reason |
| network-traffic | x_num_attempts | num_attempts |
| network-traffic | x_num_successes | num_successes |
| network-traffic | x_user_agent | user_agent |
| network-traffic | x_status_code | status_code |
| network-traffic | x_request_uri | uri |
| network-traffic | x_src_session_uid | orig_sluid |
| network-traffic | dst_ref | origin_ip |
| network-traffic | src_ref | origin_ip |
| network-traffic | dst_port | origin_port |
| network-traffic | protocols | origin_protocol |
| network-traffic | x_dst_geo_latitude | origin_geo_lat |
| network-traffic | x_dst_geo_longitude | origin_geo_lon |
| network-traffic | x_dst_geo | origin_geo |
| network-traffic | x_num_accounts | num_accounts |
| network-traffic | x_num_response_objects | num_response_objects |
| network-traffic | x_client_name | client_name |
| network-traffic | x_client_token | client_token |
| network-traffic | x_rpc_uuid | uuid |
| network-traffic | x_named_pipe | named_pipe |
| network-traffic | x_executed_functions | executed_functions |
| network-traffic | x_normal_user_refs | normal_users |
| network-traffic | x_num_events | num_events |
| network-traffic | x_num_sessions | num_sessions |
| network-traffic | x_period_identified | period_identified |
| network-traffic | x_smb_share | share |
| network-traffic | x_account_uid | account_uid |
| network-traffic | x_anomalous_rpc_refs | groupProfileReference |
| network-traffic | x_ldap_event_refs | groupEventReference |
| network-traffic | x_sql_request_info_refs | groupSQLReferences |
| network-traffic | dst_port | dst_port |
| network-traffic | dst_ref | dst_ip |
| network-traffic | x_count | count |
| network-traffic | x_dst_country | dst_country |
| network-traffic | x_error_code | error_code |
| network-traffic | x_event_type | event_type |
| network-traffic | src_ref | first_timestamp |
| network-traffic | extensions.http-request-ext.request_method | http_method |
| network-traffic | x_is_normally_accessed_by_rdp | is_normally_accessed_by_rdp |
| network-traffic | end | last_seen |
| network-traffic | x_nt_referrer | referrer |
| network-traffic | extensions.http-request-ext.request_value | request |
| network-traffic | extensions.http-request-ext.x_response_code | response_code |
| network-traffic | x_target_domain_refs | target_domains |
| network-traffic | x_session_refs | groupSessionReference |
| network-traffic | extensions.http-request-ext.request_header.User-Agent | user_agent |
| network-traffic | x_tunnel_type | tunnel_type |
| network-traffic | x_time_duration | duration_int |
| network-traffic | x_is_external | is_external |
| network-traffic | dst_ref | ip |
| network-traffic | dst_byte_count | total_bytes_rcvd |
| network-traffic | src_byte_count | total_bytes_sent |
| <br> | | |
| url | value | url |
| <br> | | |
| user-account | user_id | accounts |
| user-account | user_id | normal_users |
| user-account | user_id | name |
| user-account | account_login | name |
| user-account | x_privilege_category | privilege_category |
| user-account | x_privilege_level | privilege_level |
| user-account | user_id | uid |
| <br> | | |
| x-anomalous-rpc | function_call | function_call |
| x-anomalous-rpc | rpc_function_uuid | function_uuid |
| x-anomalous-rpc | count | count |
| x-anomalous-rpc | start | first_timestamp |
| x-anomalous-rpc | end | last_timestamp |
| <br> | | |
| x-grouped-details | first_seen | first_seen |
| x-grouped-details | last_seen | last_seen |
| x-grouped-details | detection_source | detection_source |
| x-grouped-details | detection_slug | detection_slug |
| x-grouped-details | account_ref | name |
| x-grouped-details | service_accessed_info_ref | name |
| x-grouped-details | num_sessions | num_sessions |
| x-grouped-details | ja3_hashes | ja3_hashes |
| x-grouped-details | ja3s_hashes | ja3s_hashes |
| x-grouped-details | start | first_timestamp |
| x-grouped-details | end | last_timestamp |
| x-grouped-details | count | count |
| x-grouped-details | client_name | client_name |
| x-grouped-details | client_token | client_token |
| x-grouped-details | dst_byte_count | bytes_received |
| x-grouped-details | src_byte_count | bytes_sent |
| x-grouped-details | subnet | subnet |
| x-grouped-details | rpc_function_uuid | uuid |
| x-grouped-details | num_services_requested | num_services_requested |
| x-grouped-details | num_services_high_privilege | num_services_high_privilege |
| x-grouped-details | service_privilege | service_privilege |
| x-grouped-details | service_refs | groupServiceReference |
| x-grouped-details | dst_account_refs | groupServiceReference |
| x-grouped-details | host_network_refs | group_nt_Reference |
| x-grouped-details | event_refs | groupEventReference |
| x-grouped-details | session_refs | groupSessionReference |
| x-grouped-details | connection_event_refs | groupConEventsReference |
| <br> | | |
| x-ibm-finding | src_ip_ref | src_ip |
| x-ibm-finding | name | detection_type |
| x-ibm-finding | finding_type | detection_type |
| x-ibm-finding | alert_id | id |
| x-ibm-finding | description | description |
| x-ibm-finding | event_count | num_sessions |
| x-ibm-finding | event_count | num_attempts |
| x-ibm-finding | x_num_successes | num_successes |
| x-ibm-finding | x_dst_ports | dst_ports |
| x-ibm-finding | x_account_refs | accounts |
| x-ibm-finding | x_shares | shares |
| x-ibm-finding | x_probable_owner | probable_owner |
| x-ibm-finding | x_matches | matches |
| x-ibm-finding | severity | threat |
| x-ibm-finding | confidence | certainty |
| x-ibm-finding | start | first_timestamp |
| x-ibm-finding | end | last_timestamp |
| x-ibm-finding | time_observed | created_timestamp |
| x-ibm-finding | x_state | state |
| x-ibm-finding | x_assigned_to | assigned_to |
| x-ibm-finding | x_assigned_date | assigned_date |
| x-ibm-finding | ttp_tagging_refs | detection_category |
| x-ibm-finding | x_sensor_name | sensor_name |
| x-ibm-finding | x_is_triaged | is_triaged |
| x-ibm-finding | src_os_user_ref | name |
| x-ibm-finding | ioc_refs | groupIocReference |
| x-ibm-finding | ioc_refs | groupIOCReference |
| x-ibm-finding | x_new_host_info_refs | groupNewHostReferences |
| <br> | | |
| x-ibm-ttp-tagging | name | detection_type |
| x-ibm-ttp-tagging | confidence | certainty |
| x-ibm-ttp-tagging | kill_chain_phases | detection_category |
| <br> | | |
| x-ldap-event | base_object | base_object |
| x-ldap-event | request | request |
| x-ldap-event | response_code | response_code |
| x-ldap-event | num_response_objects | num_response_objects |
| x-ldap-event | last_timestamp | last_timestamp |
| <br> | | |
| x-new-host-info | artifact | artifact |
| x-new-host-info | via | via |
| x-new-host-info | role | role |
| x-new-host-info | end | last_timestamp |
| <br> | | |
| x-oca-asset | ip_refs | src_ip |
| x-oca-asset | hostname | name |
| x-oca-asset | device_id | id |
| x-oca-asset | x_is_key_asset | is_key_asset |
| x-oca-asset | x_threat | threat |
| x-oca-asset | x_certainty | certainty |
| x-oca-asset | x_privilege_category | privilege_category |
| x-oca-asset | x_privilege_level | privilege_level |
| <br> | | |
| x-service-accessed-info | name | name |
| x-service-accessed-info | privilege_category | privilege_category |
| x-service-accessed-info | privilege_level | privilege_level |
| <br> | | |
| x-services-requested | service | service |
| x-services-requested | privilege | privilege |
| <br> | | |
| x-sql-request-info | http_segment | http_segment |
| x-sql-request-info | user_agent | user_agent |
| x-sql-request-info | sql_fragment | sql_fragment |
| x-sql-request-info | response_code | response_code |
| x-sql-request-info | bytes_received | bytes_received |
| x-sql-request-info | last_seen | last_seen |
| <br> | | |
