##### Updated on 02/04/22
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
| directory | path | file_path |
| directory | created | file_create_time |
| directory | modified | file_modify_time |
| <br> | | |
| domain-name | value | url |
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
| x-ibm-finding | name | ss_name |
| x-ibm-finding | src_device | DeviceType |
| x-ibm-finding | severity | severity |
| <br> | | |
| x-splunk | log_source | source |
| x-splunk | log_source_type | _sourcetype |
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
