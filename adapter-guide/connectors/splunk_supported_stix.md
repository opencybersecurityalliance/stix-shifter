##### Updated on 06/01/22
## Splunk Enterprise Security
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| = | = |
| != | != |
| LIKE | encoders.like |
| IN | encoders.set |
| MATCHES | encoders.matches |
| AND | {expr1} OR {expr2} |
| OR | {expr1} OR {expr2} |
| ISSUBSET | = |
| FOLLOWEDBY | latest=[search {expr2} | append [makeresults 1 | eval _time=0] | head 1 | return $_time] | where {expr1} |
| <br> | |
### Supported STIX Objects and Properties
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| artifact | payload_bin | _raw |
| artifact | mime_type | mime_type_raw |
| <br> | | |
| directory | path | process_path |
| directory | path | parent_process_path |
| directory | path | file_path |
| directory | created | file_create_time |
| directory | modified | file_modify_time |
| <br> | | |
| domain-name | value | url |
| domain-name | value | query |
| <br> | | |
| email-addr | value | src_user |
| <br> | | |
| email-message | sender_ref | src_user |
| email-message | from_ref | src_user |
| email-message | subject | subject |
| email-message | is_multipart | is_multipart |
| <br> | | |
| file | name | process_exec |
| file | hashes | process_hash |
| file | parent_directory_ref | process_path |
| file | name | parent_process_exec |
| file | parent_directory_ref | parent_process_path |
| file | parent_directory_ref | file_path |
| file | created | file_create_time |
| file | modified | file_modify_time |
| file | hashes.UNKNOWN | file_hash |
| file | name | file_name |
| file | size | file_size |
| <br> | | |
| ipv4-addr | value | dest_ip |
| ipv4-addr | value | src_ip |
| ipv4-addr | resolves_to_refs | src_mac |
| ipv4-addr | resolves_to_refs | dest_mac |
| ipv4-addr | value | answer |
| <br> | | |
| ipv6-addr | value | dest_ip |
| ipv6-addr | value | src_ip |
| ipv6-addr | resolves_to_refs | src_mac |
| ipv6-addr | resolves_to_refs | dest_mac |
| <br> | | |
| mac-addr | value | src_mac |
| mac-addr | value | dest_mac |
| <br> | | |
| network-traffic | dst_ref | dest_ip |
| network-traffic | src_ref | src_ip |
| network-traffic | dst_port | dest_port |
| network-traffic | src_port | src_port |
| network-traffic | protocols | protocol |
| network-traffic | extensions.dns-ext.question.domain_ref | query |
| network-traffic | extensions.dns-ext.resolved_ip_refs | answer |
| <br> | | |
| process | opened_connection_refs | dest_ip |
| process | opened_connection_refs | src_ip |
| process | opened_connection_refs | dest_port |
| process | opened_connection_refs | src_port |
| process | opened_connection_refs | protocol |
| process | creator_user_ref | process_user |
| process | pid | process_id |
| process | name | process_name |
| process | command_line | process |
| process | binary_ref | process_exec |
| process | pid | parent_process_id |
| process | parent_ref | parent_process_id |
| process | name | parent_process_name |
| process | parent_ref | parent_process_name |
| process | command_line | parent_process |
| process | binary_ref | parent_process_exec |
| process | opened_connection_refs | query |
| process | opened_connection_refs | answer |
| <br> | | |
| url | value | url |
| <br> | | |
| user-account | account_login | user |
| user-account | user_id | user |
| <br> | | |
| windows-registry-key | key | object_path |
| <br> | | |
| x-ibm-finding | name | ss_name |
| x-ibm-finding | src_device | DeviceType |
| x-ibm-finding | severity | severity |
| <br> | | |
| x-oca-asset | hostname | host |
| <br> | | |
| x-oca-event | original_ref | _raw |
| x-oca-event | ip_refs | dest_ip |
| x-oca-event | network_ref | dest_ip |
| x-oca-event | ip_refs | src_ip |
| x-oca-event | network_ref | src_ip |
| x-oca-event | network_ref | dest_port |
| x-oca-event | network_ref | src_port |
| x-oca-event | network_ref | protocol |
| x-oca-event | created | _time |
| x-oca-event | user_ref | user |
| x-oca-event | process_ref | process_id |
| x-oca-event | process_ref | process_name |
| x-oca-event | file_ref | process_exec |
| x-oca-event | parent_process_ref | parent_process_id |
| x-oca-event | parent_process_ref | parent_process_name |
| x-oca-event | file_ref | file_name |
| x-oca-event | registry_ref | object_path |
| x-oca-event | host_ref | host |
| x-oca-event | module | source |
| x-oca-event | action | description |
| x-oca-event | action | signature |
| x-oca-event | code | signature_id |
| x-oca-event | outcome | result |
| x-oca-event | domain_ref | query |
| x-oca-event | network_ref | query |
| x-oca-event | network_ref | answer |
| <br> | | |
| x-splunk | direction | Direction |
| x-splunk | event_id | EventID |
| x-splunk | mitre_tactic_id | TacticId |
| x-splunk | mitre_tactic | Tactic |
| x-splunk | mitre_technique_id | TechniqueId |
| x-splunk | mitre_technique | Technique |
| x-splunk | event_name | EventName |
| <br> | | |
| x509-certificate | hashes.SHA-256 | ssl_hash |
| x509-certificate | version | ssl_version |
| x509-certificate | serial_number | ssl_serial |
| x509-certificate | signature_algorithm | ssl_signature_algorithm |
| x509-certificate | issuer | ssl_issuer |
| x509-certificate | subject | ssl_subject |
| x509-certificate | subject_public_key_algorithm | ssl_publickey_algorithm |
| <br> | | |
| x_splunk_spl | user | user |
| x_splunk_spl | bytes | bytes |
| <br> | | |
