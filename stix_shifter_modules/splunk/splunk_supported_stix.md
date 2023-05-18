##### Updated on 05/18/23
## Splunk Enterprise Security
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparision) | AND |
| OR (Comparision) | OR |
| = | = |
| != | != |
| LIKE | like({field}, {value}) |
| MATCHES | match({field}, {value}) |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| IN | IN |
| OR (Observation) | OR |
| AND (Observation) | OR |
| ISSUBSET | cidrmatch({field}, {value}) |
| FOLLOWEDBY | latest=[search {expr2} | append [makeresults 1 | eval _time=0] | head 1 | return $_time] | where {expr1} |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | src_ip, dest_ip |
| **ipv4-addr**:resolves_to_refs[*].value | src_mac, dest_mac |
| **ipv6-addr**:value | src_ip, dest_ip |
| **ipv6-addr**:resolves_to_refs[*].value | src_mac, dest_mac |
| **mac-addr**:value | src_mac, dest_mac |
| **network-traffic**:dst_port | dest_port |
| **network-traffic**:src_port | src_port |
| **network-traffic**:protocols[*] | protocol, transport |
| **network-traffic**:src_ref.value | src_ip |
| **network-traffic**:dst_ref.value | dest_ip |
| **network-traffic**:dst_ref.value | dest_ip |
| **network-traffic**:dst_byte_count | bytes_in |
| **network-traffic**:src_byte_count | bytes_out |
| **network-traffic**:dst_packets | packets_in |
| **network-traffic**:src_packets | packets_out |
| **network-traffic**:x_direction | direction |
| **network-traffic**:extensions.'dns-ext'.name | name |
| **network-traffic**:extensions.'dns-ext'.question.name_ref.value | query |
| **network-traffic**:extensions.'dns-ext'.resolved_ip_refs[*].value | answer |
| **network-traffic**:extensions.'dns-ext'.message_type | message_type |
| **network-traffic**:extensions.'dns-ext'.query_count | query_count |
| **network-traffic**:extensions.'dns-ext'.query_type | query_type |
| **network-traffic**:extensions.'dns-ext'.record_type | record_type |
| **network-traffic**:extensions.'dns-ext'.reply_code | reply_code |
| **network-traffic**:extensions.'dns-ext'.reply_code_id | reply_code_id |
| **network-traffic**:extensions.'dns-ext'.transaction_id | transaction_id |
| **network-traffic**:extensions.'http-request-ext'.request_method | http_method |
| **network-traffic**:extensions.'http-request-ext'.request_value | uri_path |
| **network-traffic**:extensions.'http-request-ext'.request_header.Referer | http_referrer |
| **network-traffic**:extensions.'http-request-ext'.request_header.'User-Agent' | http_user_agent |
| **network-traffic**:extensions.'http-request-ext'.x_uri_query | uri_query |
| **domain-name**:value | query, recipient_domain, src_user_domain, ssl_issuer_email_domain, ssl_subject_email_domain |
| **url**:value | url |
| **process**:command_line | process, parent_process |
| **process**:pid | process_id, parent_process_id |
| **process**:name | process_name, parent_process_name |
| **process**:cwd | process_current_directory |
| **process**:binary_ref.name | process_name, parent_process_name |
| **process**:x_original_file_name | original_file_name |
| **process**:x_memory_used | mem_used |
| **process**:x_unique_id | process_guid, parent_process_guid |
| **file**:name | file_name, process_name, parent_process_name, process_exec, parent_process_exec |
| **file**:size | file_size |
| **file**:hashes.MD5 | file_hash |
| **file**:hashes.'SHA-1' | file_hash |
| **file**:hashes.'SHA-256' | file_hash |
| **file**:parent_directory_ref.path | file_path, process_path, parent_process_path |
| **file**:created | file_create_time |
| **file**:modified | file_modify_time |
| **file**:accessed | file_access_time |
| **file**:x_acl | file_acl |
| **directory**:path | file_path, process_path, parent_process_path |
| **user-account**:user_id | user |
| **user-account**:account_login | user_id |
| **user-account**:x_user_name | user_name |
| **windows-registry-key**:key | registry_key_name |
| **windows-registry-key**:values[*].name | registry_value_name |
| **windows-registry-key**:values[*].data | registry_value_data |
| **windows-registry-key**:x_hive | registry_hive |
| **windows-registry-key**:x_path | registry_path |
| **windows-registry-key**:x_value_text | registry_value_text |
| **x-oca-asset**:hostname | host |
| **x-oca-asset**:x_operating_system | os |
| **x-oca-event**:code | signature_id |
| **x-oca-event**:action | signature |
| **x-oca-event**:outcome | action |
| **x-oca-event**:module | source |
| **x-oca-event**:created | _time |
| **x-oca-event**:duration | duration |
| **x-oca-event**:provider | vendor_product |
| **x-oca-event**:severity | severity |
| **x-oca-event**:file_ref.name | file_name |
| **x-oca-event**:process_ref.binary_ref.name | process_exec |
| **x-oca-event**:process_ref.name | process_name |
| **x-oca-event**:parent_process_ref.pid | parent_process_id |
| **x-oca-event**:parent_process_ref.name | parent_process_name |
| **x-oca-event**:domain_ref.value | query |
| **x-oca-event**:host_ref.hostname | host |
| **x-oca-event**:ip_refs[*].value | src_ip, dest_ip |
| **x-oca-event**:registry_ref.key | registry_key_name |
| **x-oca-event**:user_ref.user_id | user |
| **x-oca-event**:url_ref.value | url |
| **x-oca-event**:network_ref.src_port | src_port |
| **x-oca-event**:network_ref.dst_port | dest_port |
| **x-oca-event**:x_dest | dest |
| **x-oca-event**:x_src | src |
| **x-oca-event**:x_application | app |
| **x-oca-event**:x_status | status |
| **x-oca-event**:x_event_id | event_id |
| **x-readable-payload**:value | _raw |
| **email-addr**:value | src_user, recipient, ssl_issuer_email, ssl_subject_email |
| **email-addr**:x_recipient_domain_ref.value | recipient_domain |
| **email-message**:to_refs[*].value | recipient |
| **email-message**:subject | subject |
| **email-message**:from_ref.value | src_user |
| **email-message**:x_url_ref.value | url |
| **email-message**:x_internal_message_id | internal_message_id |
| **email-message**:x_message_id | message_id |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.technique_id | mitre_technique_id |
| **x-splunk-vulnerability**:msft | msft |
| **x-splunk-vulnerability**:cve | cve |
| **x-splunk-vulnerability**:cvss | cvss |
| **x-splunk-vulnerability**:mskb | mskb |
| **x-splunk-authentication**:user_type | user_type |
| **x-splunk-authentication**:user_agent | user_agent |
| **x-splunk-authentication**:method | authentication_method |
| **x-splunk-authentication**:service | authentication_service |
| **x-splunk-data**:log_source | source |
| **x-splunk-data**:log_source_type | _sourcetype |
| **x-splunk-data**:event_type | eventtype |
| **x-ibm-finding**:severity | severity |
| **x-ibm-finding**:finding_type | type |
| **x-ibm-finding**:name | signature |
| **x-ibm-finding**:alert_id | id |
| **x-ibm-finding**:description | description |
| **x-ibm-finding**:src_ip_ref.value | src_ip |
| **x-ibm-finding**:dst_ip_ref.value | dest_ip |
| **x-ibm-finding**:ttp_tagging_refs[*].extensions.'mitre-attack-ext'.technique_id | mitre_technique_id |
| **x509-certificate**:hashes.'SHA-256' | ssl_hash |
| **x509-certificate**:hashes.'SHA-1' | ssl_hash |
| **x509-certificate**:version | ssl_version |
| **x509-certificate**:serial_number | ssl_serial |
| **x509-certificate**:signature_algorithm | ssl_signature_algorithm |
| **x509-certificate**:issuer | ssl_issuer |
| **x509-certificate**:subject | ssl_subject |
| **x509-certificate**:subject_public_key_algorithm | ssl_publickey_algorithm |
| **x509-certificate**:validity_not_before | ssl_start_time |
| **x509-certificate**:validity_not_after | ssl_end_time |
| **x509-certificate**:x_ssl_is_valid | ssl_is_valid |
| **x509-certificate**:x_ssl_issuer_common_name | ssl_issuer_common_name |
| **x509-certificate**:x_ssl_subject_common_name | ssl_subject_common_name |
| **x509-certificate**:x_ssl_name | ssl_name |
| **x509-certificate**:x_ssl_publickey | ssl_publickey |
| **x509-certificate**:x_ssl_issuer_email_ref.value | ssl_issuer_email |
| **x509-certificate**:x_ssl_subject_email_ref.value | ssl_subject_email |
| **x509-certificate**:x_ssl_issuer_domain_ref.value | ssl_issuer_email_domain |
| **x509-certificate**:x_ssl_subject_domain_ref.value | ssl_subject_email_domain |
| **x509-certificate**:x_ssl_issuer_organization | ssl_issuer_organization |
| **x509-certificate**:x_ssl_subject_organization | ssl_subject_organization |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | process_path |
| directory | path | parent_process_path |
| directory | path | file_path |
| <br> | | |
| domain-name | value | query |
| domain-name | value | ssl_issuer_email_domain |
| domain-name | value | ssl_subject_email_domain |
| domain-name | value | recipient_domain |
| domain-name | value | src_user_domain |
| <br> | | |
| file | name | file_name |
| file | name | process_name |
| file | name | process_exec |
| file | name | parent_process_name |
| file | name | parent_process_exec |
| file | size | file_size |
| file | hashes | process_hash |
| file | hashes.MD5 | file_md5 |
| file | hashes.SHA-1 | file_sha1 |
| file | hashes.SHA-256 | file_sha256 |
| file | parent_directory_ref | process_path |
| file | parent_directory_ref | parent_process_path |
| file | parent_directory_ref | file_path |
| file | created | file_create_time |
| file | modified | file_modify_time |
| file | accessed | file_access_time |
| file | x_acl | file_acl |
| <br> | | |
| ipv4-addr | value | dest_ip |
| ipv4-addr | value | src_ip |
| ipv4-addr | value | answer |
| ipv4-addr | resolves_to_refs | src_mac |
| ipv4-addr | resolves_to_refs | dest_mac |
| <br> | | |
| ipv6-addr | value | dest_ip |
| ipv6-addr | value | answer |
| ipv6-addr | value | src_ip |
| <br> | | |
| mac-addr | value | src_mac |
| mac-addr | value | dest_mac |
| <br> | | |
| network-traffic | src_ref | src_ip |
| network-traffic | protocols | protocol |
| network-traffic | protocols | transport |
| network-traffic | dst_ref | dest_ip |
| network-traffic | dst_port | dest_port |
| network-traffic | src_port | src_port |
| network-traffic | x_direction | direction |
| network-traffic | dst_byte_count | bytes_in |
| network-traffic | src_byte_count | bytes_out |
| network-traffic | dst_packets | packets_in |
| network-traffic | src_packets | packets_out |
| network-traffic | extensions.dns-ext.name | name |
| network-traffic | extensions.dns-ext.message_type | message_type |
| network-traffic | extensions.dns-ext.query_count | query_count |
| network-traffic | extensions.dns-ext.query_type | query_type |
| network-traffic | extensions.dns-ext.record_type | record_type |
| network-traffic | extensions.dns-ext.reply_code | reply_code |
| network-traffic | extensions.dns-ext.reply_code_id | reply_code_id |
| network-traffic | extensions.dns-ext.question.name_ref | query |
| network-traffic | extensions.dns-ext.resolved_ip_refs | answer |
| network-traffic | extensions.dns-ext.transaction_id | transaction_id |
| network-traffic | extensions.http-request-ext.request_method | http_method |
| network-traffic | extensions.http-request-ext.request_header.Referer | http_referrer |
| network-traffic | extensions.http-request-ext.request_header.User-Agent | http_user_agent |
| network-traffic | extensions.http-request-ext.request_value | uri_path |
| network-traffic | extensions.http-request-ext.x_uri_query | uri_query |
| <br> | | |
| process | binary_ref | process_name |
| process | binary_ref | process_exec |
| process | binary_ref | parent_process_exec |
| process | x_unique_id | process_guid |
| process | x_unique_id | parent_process_guid |
| process | cwd | process_current_directory |
| process | command_line | process |
| process | command_line | parent_process |
| process | x_original_file_name | original_file_name |
| process | x_memory_used | mem_used |
| process | pid | process_id |
| process | pid | parent_process_id |
| process | name | process_name |
| process | parent_ref | parent_process_id |
| process | name | parent_process_name |
| process | opened_connection_refs | protocol |
| process | opened_connection_refs | transport |
| process | parent_ref | parent_process_name |
| <br> | | |
| url | value | url |
| <br> | | |
| user-account | user_id | user |
| user-account | x_user_name | user_name |
| user-account | account_login | user_id |
| <br> | | |
| windows-registry-key | key | registry_key_name |
| windows-registry-key | values | registry_value |
| windows-registry-key | x_hive | registry_hive |
| windows-registry-key | x_path | registry_path |
| windows-registry-key | x_value_text | registry_value_text |
| <br> | | |
| x-oca-asset | x_operating_system | os |
| x-oca-asset | hostname | host |
| <br> | | |
| x-oca-event | original_ref | _raw |
| x-oca-event | ip_refs | dest_ip |
| x-oca-event | ip_refs | src_ip |
| x-oca-event | network_ref | dest_port |
| x-oca-event | network_ref | src_port |
| x-oca-event | network_ref | transport |
| x-oca-event | domain_ref | query |
| x-oca-event | user_ref | user |
| x-oca-event | process_ref | process_id |
| x-oca-event | process_ref | process_name |
| x-oca-event | process_ref | process |
| x-oca-event | parent_process_ref | parent_process_id |
| x-oca-event | parent_process_ref | parent_process_name |
| x-oca-event | process_ref | parent_process |
| x-oca-event | parent_process_ref | parent_process |
| x-oca-event | file_ref | file_name |
| x-oca-event | registry_ref | registry_key_name |
| x-oca-event | url_ref | url |
| x-oca-event | host_ref | host |
| x-oca-event | module | source |
| x-oca-event | x_status | status |
| x-oca-event | provider | vendor_product |
| x-oca-event | outcome | action |
| x-oca-event | duration | duration |
| x-oca-event | severity | severity |
| x-oca-event | created | _time |
| x-oca-event | action | signature |
| x-oca-event | code | signature_id |
| x-oca-event | x_application | app |
| x-oca-event | x_dest | dest |
| x-oca-event | x_src | src |
| x-oca-event | x_event_id | event_id |
| <br> | | |
| x-splunk-authentication | method | authentication_method |
| x-splunk-authentication | service | authentication_service |
| x-splunk-authentication | user_agent | user_agent |
| x-splunk-authentication | user_type | user_type |
| <br> | | |
| x-splunk-vulnerability | msft | msft |
| x-splunk-vulnerability | cve | cve |
| x-splunk-vulnerability | cvss | cvss |
| x-splunk-vulnerability | mskb | mskb |
| <br> | | |
| x-ibm-ttp-tagging | extensions.mitre-attack-ext.technique_id | mitre_technique_id |
| <br> | | |
| artifact | payload_bin | _raw |
| <br> | | |
| x-splunk-data | log_source_type | _sourcetype |
| x-splunk-data | event_type | eventtype |
| x-splunk-data | log_source | source |
| <br> | | |
| x-ibm-finding | dst_ip_ref | dest_ip |
| x-ibm-finding | src_ip_ref | src_ip |
| x-ibm-finding | finding_type | finding_type |
| x-ibm-finding | severity | alert_severity |
| x-ibm-finding | name | alert_signature |
| x-ibm-finding | alert_id | alert_id |
| x-ibm-finding | description | alert_description |
| x-ibm-finding | ttp_tagging_refs | mitre_technique_id |
| <br> | | |
| email-addr | value | src_user |
| email-addr | value | recipient |
| email-addr | value | ssl_issuer_email |
| email-addr | value | ssl_subject_email |
| email-addr | x_recipient_domain_ref | recipient_domain |
| email-addr | x_src_user_domain_ref | src_user_domain |
| <br> | | |
| email-message | from_ref | src_user |
| email-message | to_refs | recipient |
| email-message | subject | subject |
| email-message | is_multipart | is_multipart |
| email-message | x_internal_message_id | internal_message_id |
| email-message | x_message_id | message_id |
| email-message | x_message_info | message_info |
| <br> | | |
| x509-certificate | hashes.SHA-256 | ssl_hash |
| x509-certificate | version | ssl_version |
| x509-certificate | serial_number | ssl_serial |
| x509-certificate | signature_algorithm | ssl_signature_algorithm |
| x509-certificate | ssl_issuer | issuer |
| x509-certificate | subject | ssl_subject |
| x509-certificate | subject_public_key_algorithm | ssl_publickey_algorithm |
| x509-certificate | validity_not_before | ssl_start_time |
| x509-certificate | validity_not_after | ssl_end_time |
| x509-certificate | x_ssl_is_valid | ssl_is_valid |
| x509-certificate | x_ssl_issuer_common_name | ssl_issuer_common_name |
| x509-certificate | x_ssl_subject_common_name | ssl_subject_common_name |
| x509-certificate | x_ssl_name | ssl_name |
| x509-certificate | x_ssl_publickey | ssl_publickey |
| x509-certificate | x_ssl_issuer_domain_ref | ssl_issuer_email_domain |
| x509-certificate | x_ssl_subject_domain_ref | ssl_subject_email_domain |
| x509-certificate | x_ssl_issuer_organization | ssl_issuer_organization |
| x509-certificate | x_ssl_subject_organization | ssl_subject_organization |
| x509-certificate | x_ssl_issuer_email_ref | ssl_issuer_email |
| x509-certificate | x_ssl_subject_email_ref | ssl_subject_email |
| <br> | | |