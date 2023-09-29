##### Updated on 19/07/23
## Vectra NDR
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Vectra Operator |
|--|--|
| AND (Comparision) | AND |
| OR (Comparision) | OR |
| = | : |
| != | : |
| IN | : |
| MATCHES | :* |
| > | :> |
| >= | :>= |
| < | :< |
| <= | :<= |
| LIKE | : |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | detection.src_ip, detection.grouped_details.dst_ips, detection.grouped_details.dst_hosts.dst_ip, detection.grouped_details.normal_admin_hosts.ip, detection.grouped_details.dst_hosts.ip, detection.grouped_details.origin_ip, detection.grouped_details.sessions.dst_ip, detection.grouped_details.events.dst_ip, detection.grouped_details.events.dst_ips, detection.grouped_details.events.sessions.dst_ip, detection.grouped_details.connection_events.target_host.ip |
| **ipv6-addr**:value | detection.src_ip, detection.grouped_details.dst_ips, detection.grouped_details.dst_hosts.dst_ip, detection.grouped_details.normal_admin_hosts.ip, detection.grouped_details.origin_ip, detection.grouped_details.sessions.dst_ip, detection.grouped_details.events.dst_ip, detection.grouped_details.events.dst_ips, detection.grouped_details.events.sessions.dst_ip, detection.grouped_details.connection_events.target_host.ip |
| **domain-name**:value | detection.grouped_details.target_domains, detection.grouped_details.origin_domain, detection.grouped_details.events.target_domains, detection.grouped_details.connection_events.target_host.dst_dns |
| **network-traffic**:dst_port | detection.grouped_details.dst_ports, detection.grouped_details.dst_hosts.dst_port, detection.grouped_details.origin_port, detection.grouped_details.sessions.dst_port, detection.grouped_details.events.dst_port, detection.grouped_details.events.sessions.dst_port, detection.grouped_details.events.target_summary.dst_port, detection.grouped_details.connection_events.dst_port |
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
| **network-traffic**:x_dst_geo_latitude | detection.grouped_details.dst_geo_lat, detection.grouped_details.origin_geo_lat, detection.grouped_details.sessions.dst_geo_lat |
| **network-traffic**:x_dst_geo_longitude | detection.grouped_details.dst_geo_lon, detection.grouped_details.origin_geo_lon, detection.grouped_details.sessions.dst_geo_lon |
| **network-traffic**:x_dst_geo | detection.grouped_details.dst_geo, detection.grouped_details.origin_geo, detection.grouped_details.sessions.dst_geo |
| **network-traffic**:x_num_response_objects | detection.grouped_details.num_response_objects |
| **network-traffic**:x_client_name | detection.grouped_details.client_name |
| **network-traffic**:x_client_token | detection.grouped_details.client_token |
| **network-traffic**:x_is_normally_accessed_by_rdp | detection.grouped_details.events.is_normally_accessed_by_rdp |
| **network-traffic**:x_rpc_uuid | detection.grouped_details.uuid |
| **network-traffic**:x_nt_referrer | detection.grouped_details.events.referrer |
| **network-traffic**:x_num_events | detection.grouped_details.num_events |
| **network-traffic**:x_time_duration | detection.grouped_details.duration, detection.grouped_details.events.duration, detection.grouped_details.events.sessions.duration, detection.grouped_details.connection_events.duration |
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
| **x-ibm-finding**:x_state | detection.state |
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
| **x-ibm-ttp-tagging**:name | detection.detection_category |
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
| **x-grouped-details**:account_ref.user_id | detection.grouped_details.src_account.id |
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
| **x-services-requested**:privilege | detection.grouped_details.services_requested.privilege |
| **x-new-host-info**:artifact | detection.grouped_details.artifact |
| **x-new-host-info**:via | detection.grouped_details.via |
| **x-new-host-info**:role | detection.grouped_details.role |
| **x-new-host-info**:end | detection.grouped_details.last_timestamp |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| ipv4-addr | value | detection.src_ip |
| ipv4-addr | value | detection.grouped_details.dst_ips |
| ipv4-addr | value | detection.grouped_details.dst_hosts.dst_ip |
| ipv4-addr | value | detection.grouped_details.normal_admin_hosts.ip |
| ipv4-addr | value | detection.grouped_details.dst_hosts.ip |
| ipv4-addr | value | detection.grouped_details.origin_ip |
| ipv4-addr | value | detection.grouped_details.sessions.dst_ip |
| ipv4-addr | value | detection.grouped_details.events.dst_ip |
| ipv4-addr | value | detection.grouped_details.events.dst_ips |
| ipv4-addr | value | detection.grouped_details.events.sessions.dst_ip |
| ipv4-addr | value | detection.grouped_details.connection_events.target_host.ip |
| <br> | | |
| ipv6-addr | value | detection.src_ip |
| ipv6-addr | value | detection.grouped_details.dst_ips |
| ipv6-addr | value | detection.grouped_details.dst_hosts.dst_ip |
| ipv6-addr | value | detection.grouped_details.normal_admin_hosts.ip |
| ipv6-addr | value | detection.grouped_details.dst_hosts.ip |
| ipv6-addr | value | detection.grouped_details.origin_ip |
| ipv6-addr | value | detection.grouped_details.sessions.dst_ip |
| ipv6-addr | value | detection.grouped_details.events.dst_ip |
| ipv6-addr | value | detection.grouped_details.events.dst_ips |
| ipv6-addr | value | detection.grouped_details.events.sessions.dst_ip |
| ipv6-addr | value | detection.grouped_details.connection_events.target_host.ip |
| <br> | | |
| domain-name | value | detection.grouped_details.target_domains |
| domain-name | value | detection.grouped_details.origin_domain |
| domain-name | value | detection.grouped_details.events.target_domains |
| domain-name | value | detection.grouped_details.connection_events.target_host.dst_dns |
| <br> | | |
| network-traffic | dst_port | detection.grouped_details.dst_ports |
| network-traffic | dst_port | detection.grouped_details.dst_hosts.dst_port |
| network-traffic | dst_port | detection.grouped_details.origin_port |
| network-traffic | dst_port | detection.grouped_details.sessions.dst_port |
| network-traffic | dst_port | detection.grouped_details.events.dst_port |
| network-traffic | dst_port | detection.grouped_details.events.sessions.dst_port |
| network-traffic | dst_port | detection.grouped_details.events.target_summary.dst_port |
| network-traffic | dst_port | detection.grouped_details.connection_events.dst_port |
| network-traffic | src_port | detection.grouped_details.src_port |
| network-traffic | src_ref.value | detection.src_ip |
| network-traffic | dst_ref.value | detection.grouped_details.dst_ips |
| network-traffic | dst_ref.value | detection.grouped_details.dst_hosts.dst_ip |
| network-traffic | dst_ref.value | detection.grouped_details.sessions.dst_ip |
| network-traffic | dst_ref.value | detection.grouped_details.origin_ip |
| network-traffic | dst_ref.value | detection.grouped_details.events.sessions.dst_ip |
| network-traffic | dst_ref.value | detection.grouped_details.connection_events.target_host.ip |
| network-traffic | protocols[*] | detection.grouped_details.protocol |
| network-traffic | protocols[*] | detection.grouped_details.app_protocol |
| network-traffic | protocols[*] | detection.grouped_details.dst_protocol |
| network-traffic | protocols[*] | detection.grouped_details.origin_protocol |
| network-traffic | protocols[*] | detection.grouped_details.sessions.protocol |
| network-traffic | protocols[*] | detection.grouped_details.sessions.app_protocol |
| network-traffic | protocols[*] | detection.grouped_details.events.protocol |
| network-traffic | protocols[*] | detection.grouped_details.events.sessions.app_protocol |
| network-traffic | protocols[*] | detection.grouped_details.events.sessions.protocol |
| network-traffic | protocols[*] | detection.grouped_details.events.target_summary.app_protocol |
| network-traffic | protocols[*] | detection.grouped_details.events.target_summary.protocol |
| network-traffic | protocols[*] | detection.grouped_details.connection_events.protocol |
| network-traffic | src_byte_count | detection.grouped_details.bytes_sent |
| network-traffic | src_byte_count | detection.grouped_details.sessions.bytes_sent |
| network-traffic | src_byte_count | detection.grouped_details.events.bytes_sent |
| network-traffic | src_byte_count | detection.grouped_details.connection_events.total_bytes_sent |
| network-traffic | dst_byte_count | detection.grouped_details.bytes_received |
| network-traffic | dst_byte_count | detection.grouped_details.sessions.bytes_received |
| network-traffic | dst_byte_count | detection.grouped_details.events.bytes_received |
| network-traffic | dst_byte_count | detection.grouped_details.events.sessions.bytes_received |
| network-traffic | dst_byte_count | detection.grouped_details.connection_events.total_bytes_rcvd |
| network-traffic | start | detection.first_timestamp |
| network-traffic | start | detection.grouped_details.first_timestamp |
| network-traffic | start | detection.grouped_details.sessions.first_timestamp |
| network-traffic | start | detection.grouped_details.events.first_timestamp |
| network-traffic | start | detection.grouped_details.events.sessions.first_timestamp |
| network-traffic | start | detection.grouped_details.events.target_summary.first_timestamp |
| network-traffic | start | detection.grouped_details.connection_events.first_timestamp |
| network-traffic | end | detection.last_timestamp |
| network-traffic | end | detection.grouped_details.last_timestamp |
| network-traffic | end | detection.grouped_details.dst_hosts.last_timestamp |
| network-traffic | end | detection.grouped_details.sessions.last_timestamp |
| network-traffic | end | detection.grouped_details.events.last_seen |
| network-traffic | end | detection.grouped_details.events.last_timestamp |
| network-traffic | end | detection.grouped_details.events.target_summary.last_timestamp |
| network-traffic | end | detection.grouped_details.connection_events.last_timestamp |
| network-traffic | x_count | detection.grouped_details.events.count |
| network-traffic | x_dst_country | detection.grouped_details.events.dst_country |
| network-traffic | x_num_accounts | detection.grouped_details.num_accounts |
| network-traffic | x_reason | detection.grouped_details.reason |
| network-traffic | x_num_attempts | detection.grouped_details.num_attempts |
| network-traffic | x_tunnel_type | detection.grouped_details.sessions.tunnel_type |
| network-traffic | x_num_sessions | detection.grouped_details.num_sessions |
| network-traffic | x_user_agent | detection.grouped_details.user_agent |
| network-traffic | x_dst_geo_latitude | detection.grouped_details.dst_geo_lat |
| network-traffic | x_dst_geo_latitude | detection.grouped_details.origin_geo_lat |
| network-traffic | x_dst_geo_latitude | detection.grouped_details.sessions.dst_geo_lat |
| network-traffic | x_dst_geo_longitude | detection.grouped_details.dst_geo_lon |
| network-traffic | x_dst_geo_longitude | detection.grouped_details.origin_geo_lon |
| network-traffic | x_dst_geo_longitude | detection.grouped_details.sessions.dst_geo_lon |
| network-traffic | x_dst_geo | detection.grouped_details.dst_geo |
| network-traffic | x_dst_geo | detection.grouped_details.origin_geo |
| network-traffic | x_dst_geo | detection.grouped_details.sessions.dst_geo |
| network-traffic | x_num_response_objects | detection.grouped_details.num_response_objects |
| network-traffic | x_client_name | detection.grouped_details.client_name |
| network-traffic | x_client_token | detection.grouped_details.client_token |
| network-traffic | x_is_normally_accessed_by_rdp | detection.grouped_details.events.is_normally_accessed_by_rdp |
| network-traffic | x_rpc_uuid | detection.grouped_details.uuid |
| network-traffic | x_nt_referrer | detection.grouped_details.events.referrer |
| network-traffic | x_num_events | detection.grouped_details.num_events |
| network-traffic | x_time_duration | detection.grouped_details.duration |
| network-traffic | x_time_duration | detection.grouped_details.events.duration |
| network-traffic | x_time_duration | detection.grouped_details.events.sessions.duration |
| network-traffic | x_time_duration | detection.grouped_details.connection_events.duration |
| network-traffic | x_status_code | detection.grouped_details.status_code |
| network-traffic | x_named_pipe | detection.grouped_details.named_pipe |
| network-traffic | x_uri | detection.grouped_details.uri |
| network-traffic | x_src_session_uid | detection.grouped_details.metadata.orig_sluid |
| network-traffic | x_executed_functions | detection.grouped_details.executed_functions |
| network-traffic | x_event_type | detection.grouped_details.events.event_type |
| network-traffic | x_error_code | detection.grouped_details.events.error_code |
| network-traffic | x_target_domain_refs[*].value | detection.grouped_details.events.target_domains |
| network-traffic | x_is_external | detection.grouped_details.connection_events.is_external |
| network-traffic | x_request_uri | detection.grouped_details.uri |
| network-traffic | x_period_identified | detection.grouped_details.period_identified |
| network-traffic | x_smb_share | detection.grouped_details.share |
| network-traffic | x_account_uid | detection.grouped_details.account_uid |
| network-traffic | extensions.'http-request-ext'.request_method | detection.grouped_details.events.http_method |
| network-traffic | extensions.'http-request-ext'.x_response_code | detection.grouped_details.events.response_code |
| network-traffic | extensions.'http-request-ext'.request_header.'User-Agent' | detection.grouped_details.user_agent |
| <br> | | |
| user-account | user_id | detection.grouped_details.dst_accounts.uid |
| user-account | user_id | detection.grouped_details.src_account.name |
| user-account | user_id | detection.grouped_details.normal_users |
| user-account | user_id | detection.summary.accounts |
| user-account | account_login | detection.grouped_details.src_account.name |
| user-account | x_privilege_category | detection.grouped_details.src_account.privilege_category |
| user-account | x_privilege_level | detection.grouped_details.src_account.privilege_level |
| <br> | | |
| x-ibm-finding | name | detection.detection_type |
| x-ibm-finding | alert_id | detection.id |
| x-ibm-finding | description | detection.description |
| x-ibm-finding | description | detection.summary.description |
| x-ibm-finding | x_num_sessions | detection.grouped_details.num_sessions |
| x-ibm-finding | severity | detection.threat |
| x-ibm-finding | confidence | detection.certainty |
| x-ibm-finding | start | detection.first_timestamp |
| x-ibm-finding | end | detection.last_timestamp |
| x-ibm-finding | time_observed | detection.created_timestamp |
| x-ibm-finding | x_state | detection.state |
| x-ibm-finding | x_assigned_to | detection.assigned_to |
| x-ibm-finding | x_assigned_date | detection.assigned_date |
| x-ibm-finding | x_sensor_name | detection.sensor_name |
| x-ibm-finding | x_is_triaged | detection.is_triaged |
| x-ibm-finding | src_ip_ref | detection.src_ip |
| x-ibm-finding | x_dst_ports | detection.summary.dst_ports |
| x-ibm-finding | x_account_refs.user_id | detection.summary.accounts |
| x-ibm-finding | x_shares | detection.summary.shares |
| x-ibm-finding | x_probable_owner | detection.summary.probable_owner |
| x-ibm-finding | x_matches | detection.summary.matches |
| <br> | | |
| x-ibm-ttp-tagging | name | detection.detection_category |
| x-ibm-ttp-tagging | confidence | detection.certainty |
| x-ibm-ttp-tagging | kill_chain_phases.phase_name | detection.detection_category |
| <br> | | |
| x-oca-asset | hostname | detection.src_host.name |
| x-oca-asset | device_id | detection.src_host.id |
| x-oca-asset | x_is_key_asset | detection.src_host.is_key_asset |
| x-oca-asset | ip_refs[*].value | detection.src_ip |
| x-oca-asset | x_threat | detection.src_host.threat |
| x-oca-asset | x_certainty | detection.src_host.certainty |
| x-oca-asset | x_privilege_category | detection.grouped_details.src_host.privilege_category |
| x-oca-asset | x_privilege_level | detection.grouped_details.src_host.privilege_level |
| <br> | | |
| x-grouped-details | first_seen | detection.grouped_details.first_seen |
| x-grouped-details | last_seen | detection.grouped_details.last_seen |
| x-grouped-details | detection_source | detection.grouped_details.detection_source |
| x-grouped-details | detection_slug | detection.grouped_details.detection_slug |
| x-grouped-details | account_ref.user_id | detection.grouped_details.src_account.id |
| x-grouped-details | ja3_hashes | detection.grouped_details.ja3_hashes |
| x-grouped-details | ja3s_hashes | detection.grouped_details.ja3s_hashes |
| x-grouped-details | x_num_sessions | detection.grouped_details.num_sessions |
| x-grouped-details | start | detection.grouped_details.first_timestamp |
| x-grouped-details | end | detection.grouped_details.last_timestamp |
| x-grouped-details | count | detection.grouped_details.count |
| x-grouped-details | client_name | detection.grouped_details.client_name |
| x-grouped-details | client_token | detection.grouped_details.client_token |
| x-grouped-details | dst_byte_count | detection.grouped_details.bytes_received |
| x-grouped-details | src_byte_count | detection.grouped_details.bytes_sent |
| x-grouped-details | subnet | detection.grouped_details.subnet |
| x-grouped-details | rpc_function_uuid | detection.grouped_details.uuid |
| x-grouped-details | num_services_requested | detection.grouped_details.num_services_requested |
| x-grouped-details | num_services_high_privilege | detection.grouped_details.num_services_high_privilege |
| x-grouped-details | service_privilege | detection.grouped_details.service_privilege |
| <br> | | |
| x-service-accessed-info | name | detection.grouped_details.service_accessed.name |
| x-service-accessed-info | privilege_category | detection.grouped_details.service_accessed.privilege_category |
| x-service-accessed-info | privilege_level | detection.grouped_details.service_accessed.privilege_level |
| <br> | | |
| x-ldap-event | base_object | detection.grouped_details.events.base_object |
| x-ldap-event | request | detection.grouped_details.events.request |
| x-ldap-event | response_code | detection.grouped_details.events.response_code |
| x-ldap-event | num_response_objects | detection.grouped_details.events.num_response_objects |
| x-ldap-event | last_timestamp | detection.grouped_details.events.last_timestamp |
| <br> | | |
| x-sql-request-info | http_segment | detection.grouped_details.targets.events.http_segment |
| x-sql-request-info | user_agent | detection.grouped_details.targets.events.user_agent |
| x-sql-request-info | sql_fragment | detection.grouped_details.targets.events.sql_fragment |
| x-sql-request-info | response_code | detection.grouped_details.targets.events.response_code |
| x-sql-request-info | bytes_received | detection.grouped_details.targets.events.bytes_received |
| x-sql-request-info | last_seen | detection.grouped_details.targets.events.last_seen |
| <br> | | |
| x-anomalous-rpc | function_call | detection.grouped_details.anomalous_profiles.function_call |
| x-anomalous-rpc | rpc_function_uuid | detection.grouped_details.anomalous_profiles.function_uuid |
| x-anomalous-rpc | count | detection.grouped_details.anomalous_profiles.count |
| x-anomalous-rpc | start | detection.grouped_details.anomalous_profiles.first_timestamp |
| x-anomalous-rpc | end | detection.grouped_details.anomalous_profiles.last_timestamp |
| <br> | | |
| x-services-requested | service | detection.grouped_details.services_requested.service |
| x-services-requested | privilege | detection.grouped_details.services_requested.privilege |
| <br> | | |
| x-new-host-info | artifact | detection.grouped_details.artifact |
| x-new-host-info | via | detection.grouped_details.via |
| x-new-host-info | role | detection.grouped_details.role |
| x-new-host-info | end | detection.grouped_details.last_timestamp |
| <br> | | |
