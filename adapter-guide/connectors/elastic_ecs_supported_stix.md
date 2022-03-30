##### Updated on 02/04/22
## Elasticsearch ECS
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | OR |
| OR | OR |
| > | :> |
| >= | :>= |
| < | :< |
| <= | :<= |
| = | : |
| != | NOT |
| LIKE | : |
| IN | : |
| MATCHES | : |
| ISSUBSET | : |
| ISSUPERSET | : |
| <br> | |
### Supported STIX Objects and Properties
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| artifact | payload_bin | original |
| artifact | mime_type | mime_type_event |
| <br> | | |
| autonomous-system | number | number |
| autonomous-system | name | name |
| <br> | | |
| directory | path | executable |
| directory | path | directory |
| <br> | | |
| domain-name | value | url |
| domain-name | value | domain |
| domain-name | value | name |
| domain-name | value | registered_domain |
| <br> | | |
| email-addr | value | email |
| email-addr | belongs_to_ref | email |
| <br> | | |
| file | name | executable |
| file | parent_directory_ref | executable |
| file | name | name |
| file | created | created |
| file | parent_directory_ref | directory |
| file | size | size |
| file | hashes.SHA-256 | sha256 |
| file | hashes.SHA-1 | sha1 |
| file | hashes.MD5 | md5 |
| file | hashes.SHA-512 | sha512 |
| <br> | | |
| ipv4-addr | value | ip |
| ipv4-addr | resolves_to_refs | mac |
| ipv4-addr | belongs_to_refs | number |
| ipv4-addr | value | resolved_ip |
| <br> | | |
| ipv6-addr | value | ip |
| ipv6-addr | resolves_to_refs | mac |
| ipv6-addr | value | resolved_ip |
| <br> | | |
| mac-addr | value | mac |
| <br> | | |
| network-traffic | src_ref | ip |
| network-traffic | src_port | port |
| network-traffic | src_byte_count | bytes |
| network-traffic | src_packets | packets |
| network-traffic | dst_ref | ip |
| network-traffic | dst_port | port |
| network-traffic | dst_byte_count | bytes |
| network-traffic | dst_packets | packets |
| network-traffic | protocols | transport |
| network-traffic | protocols | type |
| network-traffic | protocols | protocol |
| network-traffic | extensions.dns-ext.answers | answers |
| network-traffic | extensions.dns-ext.header_flags | header_flags |
| network-traffic | extensions.dns-ext.dns_id | id |
| network-traffic | extensions.dns-ext.op_code | op_code |
| network-traffic | extensions.dns-ext.question.class | class |
| network-traffic | extensions.dns-ext.question.domain_ref | name |
| network-traffic | extensions.dns-ext.question.registered_domain_ref | registered_domain |
| network-traffic | extensions.dns-ext.question.subdomain | subdomain |
| network-traffic | extensions.dns-ext.question.top_level_domain | top_level_domain |
| network-traffic | extensions.dns-ext.question.type | type |
| network-traffic | extensions.dns-ext.resolved_ip_refs | resolved_ip |
| network-traffic | extensions.dns-ext.response_code | response_code |
| network-traffic | extensions.dns-ext.type | type |
| <br> | | |
| process | opened_connection_refs | transport |
| process | opened_connection_refs | type |
| process | opened_connection_refs | protocol |
| process | created | start |
| process | pid | pid |
| process | name | name |
| process | pid | ppid |
| process | parent_ref | ppid |
| process | command_line | command_line |
| process | binary_ref | executable |
| process | parent_ref | name |
| process | parent_ref | pid |
| process | creator_user_ref | name |
| process | creator_user_ref | id |
| process | x_ttp_tags | tags |
| <br> | | |
| software | name | name |
| software | vendor | type |
| software | version | version |
| <br> | | |
| url | value | original |
| <br> | | |
| user-account | user_id | name |
| user-account | account_login | name |
| user-account | user_id | id |
| <br> | | |
| windows-registry-key | key | registry |
| windows-registry-key | values | registry |
| <br> | | |
| x-ecs | version | version |
| <br> | | |
| x-ecs-client | address | address |
| x-ecs-client | domain | domain |
| x-ecs-client | nat_ip | ip |
| x-ecs-client | nat_port | port |
| x-ecs-client | registered_domain | registered_domain |
| x-ecs-client | top_level_domain | top_level_domain |
| x-ecs-client | geo_city_name | city_name |
| x-ecs-client | geo_continent_name | continent_name |
| x-ecs-client | geo_country_iso_code | country_iso_code |
| x-ecs-client | geo_country_name | country_name |
| x-ecs-client | geo_location | location |
| x-ecs-client | geo_name | name |
| x-ecs-client | geo_region_iso_code | region_iso_code |
| x-ecs-client | geo_region_name | region_name |
| <br> | | |
| x-ecs-cloud | account_id | id |
| x-ecs-cloud | availability_zone | availability_zone |
| x-ecs-cloud | instance_id | id |
| x-ecs-cloud | instance_name | name |
| x-ecs-cloud | machine_type | type |
| x-ecs-cloud | provider | provider |
| x-ecs-cloud | region | region |
| <br> | | |
| x-ecs-container | id | id |
| x-ecs-container | image_name | name |
| x-ecs-container | image_tag | tag |
| x-ecs-container | labels | labels |
| x-ecs-container | name | name |
| x-ecs-container | runtime | runtime |
| <br> | | |
| x-ecs-destination | address | address |
| x-ecs-destination | domain | domain |
| x-ecs-destination | nat_ip | ip |
| x-ecs-destination | nat_port | port |
| x-ecs-destination | registered_domain | registered_domain |
| x-ecs-destination | top_level_domain | top_level_domain |
| x-ecs-destination | geo_city_name | city_name |
| x-ecs-destination | geo_continent_name | continent_name |
| x-ecs-destination | geo_country_iso_code | country_iso_code |
| x-ecs-destination | geo_country_name | country_name |
| x-ecs-destination | geo_location | location |
| x-ecs-destination | geo_name | name |
| x-ecs-destination | geo_region_iso_code | region_iso_code |
| x-ecs-destination | geo_region_name | region_name |
| <br> | | |
| x-ecs-dll | name | name |
| x-ecs-dll | path | path |
| x-ecs-dll | pe_company | company |
| x-ecs-dll | pe_description | description |
| x-ecs-dll | pe_file_version | file_version |
| x-ecs-dll | pe_original_file_name | original_file_name |
| x-ecs-dll | pe_product | product |
| x-ecs-dll | code_signature_exists | exists |
| x-ecs-dll | code_signature_subject_name | subject_name |
| x-ecs-dll | hashes.SHA-256 | sha256 |
| x-ecs-dll | hashes.SHA-1 | sha1 |
| x-ecs-dll | hashes.MD5 | md5 |
| x-ecs-dll | hashes.SHA-512 | sha512 |
| <br> | | |
| x-ecs-error | code | code |
| x-ecs-error | id | id |
| x-ecs-error | message | message |
| x-ecs-error | stack_trace | stack_trace |
| x-ecs-error | type | type |
| <br> | | |
| x-ecs-file | pe_company | company |
| x-ecs-file | pe_description | description |
| x-ecs-file | pe_file_version | file_version |
| x-ecs-file | pe_original_file_name | original_file_name |
| x-ecs-file | pe_product | product |
| x-ecs-file | code_signature_exists | exists |
| x-ecs-file | code_signature_subject_name | subject_name |
| x-ecs-file | accessed | accessed |
| x-ecs-file | attributes | attributes |
| x-ecs-file | ctime | ctime |
| x-ecs-file | device | device |
| x-ecs-file | drive_letter | drive_letter |
| x-ecs-file | extension | extension |
| x-ecs-file | gid | gid |
| x-ecs-file | group | group |
| x-ecs-file | inode | inode |
| x-ecs-file | mime_type | mime_type |
| x-ecs-file | mode | mode |
| x-ecs-file | mtime | mtime |
| x-ecs-file | owner | owner |
| x-ecs-file | path | path |
| x-ecs-file | target_path | target_path |
| x-ecs-file | type | type |
| x-ecs-file | uid | uid |
| <br> | | |
| x-ecs-group | domain | domain |
| x-ecs-group | id | id |
| x-ecs-group | name | name |
| <br> | | |
| x-ecs-http | request_body_bytes | bytes |
| x-ecs-http | request_body_content | content |
| x-ecs-http | request_bytes | bytes |
| x-ecs-http | request_method | method |
| x-ecs-http | request_referrer | referrer |
| x-ecs-http | response_body_bytes | bytes |
| x-ecs-http | response_body_content | content |
| x-ecs-http | response_bytes | bytes |
| x-ecs-http | response_status_code | status_code |
| x-ecs-http | version | version |
| <br> | | |
| x-ecs-log | level | level |
| x-ecs-log | logger | logger |
| x-ecs-log | origin_file_line | line |
| x-ecs-log | origin_file_name | name |
| x-ecs-log | origin_function | function |
| x-ecs-log | original | original |
| x-ecs-log | syslog_facility_code | code |
| x-ecs-log | syslog_facility_name | name |
| x-ecs-log | syslog_priority | priority |
| x-ecs-log | severity_syslog_code | code |
| x-ecs-log | severity_syslog_name | name |
| <br> | | |
| x-ecs-network | vlan_id | id |
| x-ecs-network | vlan_name | name |
| x-ecs-network | inner_vlan_id | id |
| x-ecs-network | inner_vlan_name | name |
| x-ecs-network | name | name |
| x-ecs-network | application | application |
| x-ecs-network | direction | direction |
| x-ecs-network | forwarded_ip | forwarded_ip |
| x-ecs-network | community_id | community_id |
| <br> | | |
| x-ecs-observer | egress_zone | zone |
| x-ecs-observer | egress_interface_alias | alias |
| x-ecs-observer | egress_interface_id | id |
| x-ecs-observer | egress_interface_name | name |
| x-ecs-observer | egress_vlan_id | id |
| x-ecs-observer | egress_vlan_name | name |
| x-ecs-observer | hostname | hostname |
| x-ecs-observer | ingress_zone | zone |
| x-ecs-observer | ingress_interface_alias | alias |
| x-ecs-observer | ingress_interface_id | id |
| x-ecs-observer | ingress_interface_name | name |
| x-ecs-observer | ingress_vlan_id | id |
| x-ecs-observer | ingress_vlan_name | name |
| x-ecs-observer | ip | ip |
| x-ecs-observer | mac | mac |
| x-ecs-observer | name | name |
| x-ecs-observer | product | product |
| x-ecs-observer | serial_number | serial_number |
| x-ecs-observer | type | type |
| x-ecs-observer | vendor | vendor |
| x-ecs-observer | version | version |
| x-ecs-observer | os_name | name |
| x-ecs-observer | os_platform | platform |
| x-ecs-observer | os_version | version |
| x-ecs-observer | geo_city_name | city_name |
| x-ecs-observer | geo_continent_name | continent_name |
| x-ecs-observer | geo_country_iso_code | country_iso_code |
| x-ecs-observer | geo_country_name | country_name |
| x-ecs-observer | geo_location | location |
| x-ecs-observer | geo_name | name |
| x-ecs-observer | geo_region_iso_code | region_iso_code |
| x-ecs-observer | geo_region_name | region_name |
| <br> | | |
| x-ecs-organization | id | id |
| x-ecs-organization | name | name |
| <br> | | |
| x-ecs-process | code_signature_exists | exists |
| x-ecs-process | code_signature_subject_name | subject_name |
| x-ecs-process | pe_company | company |
| x-ecs-process | pe_description | description |
| x-ecs-process | pe_file_version | file_version |
| x-ecs-process | pe_original_file_name | original_file_name |
| x-ecs-process | pe_product | product |
| x-ecs-process | args | args |
| x-ecs-process | args_count | args_count |
| x-ecs-process | entity_id | entity_id |
| x-ecs-process | exit_code | exit_code |
| x-ecs-process | parent_args | args |
| x-ecs-process | parent_args_count | args_count |
| x-ecs-process | parent_entity_id | entity_id |
| x-ecs-process | parent_exit_code | exit_code |
| x-ecs-process | parent_pgid | pgid |
| x-ecs-process | parent_ppid | ppid |
| x-ecs-process | parent_thread_id | id |
| x-ecs-process | parent_thread_name | name |
| x-ecs-process | parent_title | title |
| x-ecs-process | parent_uptime | uptime |
| x-ecs-process | parent_working_directory | working_directory |
| x-ecs-process | exit_code | pgid |
| x-ecs-process | thread_id | id |
| x-ecs-process | thread_name | name |
| x-ecs-process | title | title |
| x-ecs-process | uptime | uptime |
| x-ecs-process | working_directory | working_directory |
| <br> | | |
| x-ecs-registry | key | registry |
| x-ecs-registry | data_bytes | bytes |
| x-ecs-registry | data_strings | strings |
| x-ecs-registry | data_type | type |
| x-ecs-registry | hive | registry |
| x-ecs-registry | path | registry |
| x-ecs-registry | value | registry |
| <br> | | |
| x-ecs-related | hash | hash |
| x-ecs-related | ip | ip |
| x-ecs-related | user | user |
| <br> | | |
| x-ecs-rule | author | author |
| x-ecs-rule | category | category |
| x-ecs-rule | description | description |
| x-ecs-rule | id | id |
| x-ecs-rule | license | license |
| x-ecs-rule | name | name |
| x-ecs-rule | reference | reference |
| x-ecs-rule | ruleset | ruleset |
| x-ecs-rule | uuid | uuid |
| x-ecs-rule | version | version |
| <br> | | |
| x-ecs-server | address | address |
| x-ecs-server | domain | domain |
| x-ecs-server | nat_ip | ip |
| x-ecs-server | nat_port | port |
| x-ecs-server | registered_domain | registered_domain |
| x-ecs-server | top_level_domain | top_level_domain |
| x-ecs-server | geo_city_name | city_name |
| x-ecs-server | geo_continent_name | continent_name |
| x-ecs-server | geo_country_iso_code | country_iso_code |
| x-ecs-server | geo_country_name | country_name |
| x-ecs-server | geo_location | location |
| x-ecs-server | geo_name | name |
| x-ecs-server | geo_region_iso_code | region_iso_code |
| x-ecs-server | geo_region_name | region_name |
| <br> | | |
| x-ecs-service | id | id |
| x-ecs-service | name | name |
| x-ecs-service | state | state |
| x-ecs-service | type | type |
| x-ecs-service | version | version |
| x-ecs-service | ephemeral_id | ephemeral_id |
| x-ecs-service | node_name | name |
| <br> | | |
| x-ecs-source | address | address |
| x-ecs-source | domain | domain |
| x-ecs-source | nat_ip | ip |
| x-ecs-source | nat_port | port |
| x-ecs-source | registered_domain | registered_domain |
| x-ecs-source | top_level_domain | top_level_domain |
| x-ecs-source | geo_city_name | city_name |
| x-ecs-source | geo_continent_name | continent_name |
| x-ecs-source | geo_country_iso_code | country_iso_code |
| x-ecs-source | geo_country_name | country_name |
| x-ecs-source | geo_location | location |
| x-ecs-source | geo_name | name |
| x-ecs-source | geo_region_iso_code | region_iso_code |
| x-ecs-source | geo_region_name | region_name |
| <br> | | |
| x-ecs-threat | framework | framework |
| x-ecs-threat | tactic_id | id |
| x-ecs-threat | tactic_name | name |
| x-ecs-threat | tactic_reference | reference |
| x-ecs-threat | technique_id | id |
| x-ecs-threat | technique_name | name |
| x-ecs-threat | technique_reference | reference |
| <br> | | |
| x-ecs-tls | client_certificate | certificate |
| x-ecs-tls | client_certificate_chain | certificate_chain |
| x-ecs-tls | client_ja3 | ja3 |
| x-ecs-tls | client_supported_ciphers | supported_ciphers |
| x-ecs-tls | server_certificate | certificate |
| x-ecs-tls | server_certificate_chain | certificate_chain |
| x-ecs-tls | server_ja3s | ja3s |
| x-ecs-tls | cipher | cipher |
| x-ecs-tls | curve | curve |
| x-ecs-tls | established | established |
| x-ecs-tls | next_protocol | next_protocol |
| x-ecs-tls | resumed | resumed |
| x-ecs-tls | version | version |
| x-ecs-tls | version_protocol | version_protocol |
| <br> | | |
| x-ecs-trace | id | id |
| <br> | | |
| x-ecs-transaction | id | id |
| <br> | | |
| x-ecs-user | domain | domain |
| x-ecs-user | full_name | full_name |
| x-ecs-user | hash | hash |
| x-ecs-user | id | id |
| x-ecs-user | group_domain | domain |
| x-ecs-user | group_id | id |
| x-ecs-user | group_name | name |
| <br> | | |
| x-ecs-user_agent | name | name |
| x-ecs-user_agent | original | original |
| x-ecs-user_agent | version | version |
| x-ecs-user_agent | device_name | name |
| <br> | | |
| x-ecs-vulnerability | category | category |
| x-ecs-vulnerability | classification | classification |
| x-ecs-vulnerability | description | description |
| x-ecs-vulnerability | enumeration | enumeration |
| x-ecs-vulnerability | id | id |
| x-ecs-vulnerability | reference | reference |
| x-ecs-vulnerability | report_id | report_id |
| x-ecs-vulnerability | severity | severity |
| x-ecs-vulnerability | scanner_vendor | vendor |
| x-ecs-vulnerability | score_base | base |
| x-ecs-vulnerability | score_environmental | environmental |
| x-ecs-vulnerability | score_temporal | temporal |
| x-ecs-vulnerability | score_version | version |
| <br> | | |
| x-oca-asset | architecture | architecture |
| x-oca-asset | domain | domain |
| x-oca-asset | hostname | hostname |
| x-oca-asset | id | id |
| x-oca-asset | ip_refs | ip |
| x-oca-asset | mac_refs | mac |
| x-oca-asset | name | name |
| x-oca-asset | host_type | type |
| x-oca-asset | uptime | uptime |
| x-oca-asset | geo_city_name | city_name |
| x-oca-asset | geo_continent_name | continent_name |
| x-oca-asset | geo_country_iso_code | country_iso_code |
| x-oca-asset | geo_country_name | country_name |
| x-oca-asset | geo_location | location |
| x-oca-asset | geo_name | name |
| x-oca-asset | geo_region_iso_code | region_iso_code |
| x-oca-asset | geo_region_name | region_name |
| x-oca-asset | os_name | name |
| x-oca-asset | os_platform | platform |
| x-oca-asset | os_version | version |
| x-oca-asset | user_domain | domain |
| x-oca-asset | user_email | email |
| x-oca-asset | user_full_name | full_name |
| x-oca-asset | user_hash | hash |
| x-oca-asset | user_id | id |
| x-oca-asset | user_name | name |
| x-oca-asset | user_group_domain | domain |
| x-oca-asset | user_group_id | id |
| x-oca-asset | user_group_name | name |
| <br> | | |
| x-oca-event | network_ref | transport |
| x-oca-event | network_ref | type |
| x-oca-event | network_ref | protocol |
| x-oca-event | original_ref | original |
| x-oca-event | action | action |
| x-oca-event | id | id |
| x-oca-event | category | category |
| x-oca-event | code | code |
| x-oca-event | created | created |
| x-oca-event | dataset | dataset |
| x-oca-event | duration | duration |
| x-oca-event | end | end |
| x-oca-event | hash | hash |
| x-oca-event | ingested | ingested |
| x-oca-event | kind | kind |
| x-oca-event | module | module |
| x-oca-event | outcome | outcome |
| x-oca-event | provider | provider |
| x-oca-event | reference | reference |
| x-oca-event | risk_score | risk_score |
| x-oca-event | risk_score_norm | risk_score_norm |
| x-oca-event | sequence | sequence |
| x-oca-event | severity | severity |
| x-oca-event | start | start |
| x-oca-event | timezone | timezone |
| x-oca-event | event_type | type |
| x-oca-event | url | url |
| x-oca-event | domain_ref | url |
| x-oca-event | url_ref | original |
| x-oca-event | domain_ref | domain |
| x-oca-event | process_ref | pid |
| x-oca-event | process_ref | name |
| x-oca-event | process_ref | executable |
| x-oca-event | parent_process_ref | name |
| x-oca-event | parent_process_ref | pid |
| x-oca-event | parent_process_ref | executable |
| x-oca-event | user_ref | name |
| x-oca-event | user_ref | id |
| x-oca-event | agent | name |
| x-oca-event | domain_ref | name |
| x-oca-event | network_ref | name |
| x-oca-event | ip_refs | resolved_ip |
| x-oca-event | file_ref | name |
| x-oca-event | host_ref | hostname |
| x-oca-event | host_ref | name |
| x-oca-event | registry_ref | registry |
| <br> | | |
| x509-certificate | issuer | issuer |
| x509-certificate | hashes.SHA-256 | sha256 |
| x509-certificate | hashes.SHA-1 | sha1 |
| x509-certificate | hashes.MD5 | md5 |
| x509-certificate | validity_not_after | not_after |
| x509-certificate | validity_not_before | not_before |
| x509-certificate | subject | subject |
| <br> | | |
