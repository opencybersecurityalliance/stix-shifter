##### Updated on 05/15/23
## Splunk Enterprise Security
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

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
| AND (Comparision) | AND |
| OR (Comparision) | OR |
| ISSUBSET | encoders.subset |
| AND (Observation) | {expr1} OR {expr2} |
| OR (Observation) | {expr1} OR {expr2} |
| FOLLOWEDBY | latest=[search {expr2} | append [makeresults 1 | eval _time=0] | head 1 | return $_time] | where {expr1} |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **x-oca-event**:code | signature_id |
| **x-oca-event**:action | signature |
| **x-oca-event**:outcome | result |
| **x-oca-event**:module | source |
| **x-oca-event**:created | _time |
| **x-oca-event**:process_ref.command_line | process |
| **x-oca-event**:process_ref.binary_ref.name | process_exec |
| **x-oca-event**:process_ref.parent_ref.command_line | parent_process |
| **x-oca-event**:process_ref.creator_user_ref.user_id | process_user |
| **x-oca-event**:process_ref.name | process_name |
| **x-oca-event**:process_ref.pid | process_id |
| **x-oca-event**:parent_process_ref.command_line | parent_process |
| **x-oca-event**:parent_process_ref.binary_ref.name | parent_process_exec |
| **x-oca-event**:parent_process_ref.pid | parent_process_id |
| **x-oca-event**:parent_process_ref.name | parent_process_name |
| **x-oca-event**:domain_ref.value | url, url_domain |
| **x-oca-event**:file_ref.name | file_name |
| **x-oca-event**:host_ref.hostname | host |
| **x-oca-event**:host_ref.ip_refs[*].value | src_ip |
| **x-oca-event**:registry_ref.key | ObjectName, RegistryKey |
| **x-oca-event**:user_ref.user_id | user |
| **x-oca-event**:url_ref.value | url |
| **x-oca-asset**:hostname | host |
| **directory**:path | file_path, process_path, parent_process_path |
| **directory**:created | file_create_time |
| **directory**:modified | file_modify_time |
| **domain-name**:value | host, url |
| **x-readable-payload**:value | _raw |
| **email-addr**:value | src_user, recipient |
| **email-message**:body_multipart.[*].'mime-part-type'.body_raw_ref.hashes.MD5 | file_hash |
| **email-message**:body_multipart.[*].'mime-part-type'.body_raw_ref.hashes.'SHA-1' | file_hash |
| **email-message**:body_multipart.[*].'mime-part-type'.body_raw_ref.hashes.'SHA-256' | file_hash |
| **email-message**:body_multipart.[*].'mime-part-type'.body_raw_ref.name | file_name |
| **email-message**:body_multipart.[*].'mime-part-type'.body_raw_ref.size | file_size |
| **email-message**:to_refs.[*].value | recipient |
| **email-message**:cc_refs.[*].value | recipient |
| **email-message**:bcc_refs.[*].value | recipient |
| **email-message**:subject | subject |
| **email-message**:sender_ref.value | src_user |
| **email-message**:from_ref.value | src_user |
| **file**:hashes.MD5 | file_hash |
| **file**:hashes.'SHA-1' | file_hash |
| **file**:hashes.'SHA-256' | file_hash |
| **file**:name | file_name |
| **file**:created | file_create_time |
| **file**:modified | file_modify_time |
| **file**:parent_directory_ref.path | file_path |
| **file**:size | file_size |
| **ipv4-addr**:value | src_ip, dest_ip |
| **ipv6-addr**:value | src_ipv6, dest_ipv6 |
| **mac-addr**:value | src_mac, dest_mac |
| **network-traffic**:src_ref.value | src_ip |
| **network-traffic**:src_port | src_port |
| **network-traffic**:dst_ref.value | dest_ip |
| **network-traffic**:dst_port | dest_port |
| **network-traffic**:protocols[*] | protocol |
| **network-traffic**:start | earliest |
| **network-traffic**:end | latest |
| **process**:name | process_name, parent_process_name |
| **process**:command_line | process, parent_process |
| **process**:pid | process_id, parent_process_id |
| **process**:creator_user_ref.account_login | user |
| **process**:creator_user_ref.user_login | user |
| **process**:binary_ref.parent_directory_ref.path | process_path |
| **process**:binary_ref.name | process_exec |
| **process**:x_unique_id | process_guid |
| **url**:value | url |
| **user-account**:user_id | user |
| **user-account**:account_login | user |
| **windows-registry-key**:key | object |
| **windows-registry-key**:values[*] | result |
| **windows-registry-key**:creator_user_ref.account_login | user |
| **x509-certificate**:hashes.'SHA-256' | ssl_hash |
| **x509-certificate**:hashes.'SHA-1' | ssl_hash |
| **x509-certificate**:version | ssl_version |
| **x509-certificate**:serial_number | ssl_serial |
| **x509-certificate**:signature_algorithm | ssl_signature_algorithm |
| **x509-certificate**:issuer | ssl_issuer |
| **x509-certificate**:subject | ssl_subject |
| **x509-certificate**:subject_public_key_algorithm | ssl_publickey_algorithm |
| **x-splunk**:log_source | source |
| **x-splunk**:log_source_type | _sourcetype |
| **x-splunk**:direction | Direction |
| **x-splunk**:event_id | EventID |
| **x-splunk**:event_name | EventName |
| **x-splunk**:mitre_tactic_id | TacticId |
| **x-splunk**:mitre_tactic | Tactic |
| **x-splunk**:mitre_technique_id | TechniqueId |
| **x-splunk**:mitre_technique | Technique |
| **x-ibm-finding**:name | ss_name |
| **x-ibm-finding**:src_device | DeviceType |
| **x-ibm-finding**:severity | severity |
| <br> | |
### Supported STIX Objects and Properties for Query Results
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
| process | x_unique_id | process_guid |
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
