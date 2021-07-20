## Splunk Enterprise Security
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| artifact | payload_bin | _raw |
| <br> | | |
| directory | path | file_path |
| directory | created | file_create_time |
| directory | modified | file_modify_time |
| <br> | | |
| domain-name | value | url |
| domain-name | value | host |
| <br> | | |
| email-addr | value | src_user |
| <br> | | |
| email-message | sender_ref | src_user |
| email-message | from_ref | src_user |
| email-message | subject | subject |
| email-message | is_multipart | is_multipart |
| <br> | | |
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
| <br> | | |
| process | creator_user_ref | process_user |
| process | name | process_name |
| process | pid | process_id |
| process | binary_ref | file_path |
| <br> | | |
| url | value | url |
| <br> | | |
| user-account | account_login | user |
| user-account | user_id | user |
| <br> | | |
| windows-registry-key | creator_user_ref | process_user |
| windows-registry-key | key | object_path |
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
| x-splunk | log_source | source |
| x-splunk | provider | _sourcetype |
| x-splunk | device_type | DeviceType |
| x-splunk | direction | Direction |
| x-splunk | severity | severity |
| x-splunk | EventID | EventID |
| x-splunk | event_name | EventName |
| x-splunk | Mitre_TacticId | TacticId |
| x-splunk | Mitre_Tactic | Tactic |
| x-splunk | Mitre_TechniqueId | TechniqueId |
| x-splunk | Mitre_Technique | Technique |
| <br> | | |
| x-ibm-finding | ss_name | ss_name |
| x-ibm-finding | severity | severity |
| <br> | | |
