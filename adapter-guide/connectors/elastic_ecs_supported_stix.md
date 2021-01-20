## Elasticsearch ECS
### artifact
- payload_bin

___
### autonomous-system
- number
- name

___
### directory
- path

___
### domain-name
- value

___
### email-addr
- value
- belongs_to_ref

___
### file
- name
- parent_directory_ref
- created
- size
- hashes.SHA-256
- hashes.SHA-1
- hashes.MD5
- hashes.SHA-512

___
### ipv4-addr
- value
- resolves_to_refs
- belongs_to_refs

___
### ipv6-addr
- value
- resolves_to_refs

___
### mac-addr
- value

___
### network-traffic
- src_ref
- src_port
- src_byte_count
- src_packets
- dst_ref
- dst_port
- dst_byte_count
- dst_packets
- protocols
- extensions.dns-ext.answers
- extensions.dns-ext.header_flags
- extensions.dns-ext.dns_id
- extensions.dns-ext.op_code
- extensions.dns-ext.question.class
- extensions.dns-ext.question.domain_ref
- extensions.dns-ext.question.registered_domain_ref
- extensions.dns-ext.question.subdomain
- extensions.dns-ext.question.top_level_domain
- extensions.dns-ext.question.type
- extensions.dns-ext.resolved_ip_refs
- extensions.dns-ext.response_code
- extensions.dns-ext.type

___
### process
- opened_connection_refs
- created
- pid
- name
- parent_ref
- command_line
- binary_ref
- creator_user_ref

___
### software
- name
- vendor
- version

___
### url
- value

___
### user-account
- user_id
- account_login

___
### windows-registry-key
- key
- values

___
### x-ecs-client
- address
- domain
- nat_ip
- nat_port
- registered_domain
- top_level_domain
- geo_city_name
- geo_continent_name
- geo_country_iso_code
- geo_country_name
- geo_location
- geo_name
- geo_region_iso_code
- geo_region_name

___
### x-ecs-cloud
- account_id
- availability_zone
- instance_id
- instance_name
- machine_type
- provider
- region

___
### x-ecs-container
- id
- image_name
- image_tag
- labels
- name
- runtime

___
### x-ecs-destination
- address
- domain
- nat_ip
- nat_port
- registered_domain
- top_level_domain
- geo_city_name
- geo_continent_name
- geo_country_iso_code
- geo_country_name
- geo_location
- geo_name
- geo_region_iso_code
- geo_region_name

___
### x-ecs-dll
- name
- path
- pe_company
- pe_description
- pe_file_version
- pe_original_file_name
- pe_product
- code_signature_exists
- code_signature_subject_name
- hashes.SHA-256
- hashes.SHA-1
- hashes.MD5
- hashes.SHA-512

___
### x-ecs-error
- code
- id
- message
- stack_trace
- type

___
### x-ecs-file
- pe_company
- pe_description
- pe_file_version
- pe_original_file_name
- pe_product
- code_signature_exists
- code_signature_subject_name
- accessed
- attributes
- ctime
- device
- drive_letter
- extension
- gid
- group
- inode
- mime_type
- mode
- mtime
- owner
- path
- target_path
- type
- uid

___
### x-ecs-group
- domain
- id
- name

___
### x-ecs-http
- request_body_bytes
- request_body_content
- request_bytes
- request_method
- request_referrer
- response_body_bytes
- response_body_content
- response_bytes
- response_status_code
- version

___
### x-ecs-log
- level
- logger
- origin_file_line
- origin_file_name
- origin_function
- original
- syslog_facility_code
- syslog_facility_name
- syslog_priority
- severity_syslog_code
- severity_syslog_name

___
### x-ecs-network
- vlan_id
- vlan_name
- inner_vlan_id
- inner_vlan_name
- name
- application
- direction
- forwarded_ip
- community_id

___
### x-ecs-observer
- egress_zone
- egress_interface_alias
- egress_interface_id
- egress_interface_name
- egress_vlan_id
- egress_vlan_name
- hostname
- ingress_zone
- ingress_interface_alias
- ingress_interface_id
- ingress_interface_name
- ingress_vlan_id
- ingress_vlan_name
- ip
- mac
- name
- product
- serial_number
- type
- vendor
- version
- os_name
- os_platform
- os_version
- geo_city_name
- geo_continent_name
- geo_country_iso_code
- geo_country_name
- geo_location
- geo_name
- geo_region_iso_code
- geo_region_name

___
### x-ecs-organization
- id
- name

___
### x-ecs-process
- code_signature_exists
- code_signature_subject_name
- pe_company
- pe_description
- pe_file_version
- pe_original_file_name
- pe_product
- args
- args_count
- entity_id
- exit_code
- parent_args
- parent_args_count
- parent_entity_id
- parent_exit_code
- parent_pgid
- parent_ppid
- parent_thread_id
- parent_thread_name
- parent_title
- parent_uptime
- parent_working_directory
- thread_id
- thread_name
- title
- uptime
- working_directory

___
### x-ecs-registry
- key
- data_bytes
- data_strings
- data_type
- hive
- path
- value

___
### x-ecs-related
- hash
- ip
- user

___
### x-ecs-rule
- author
- category
- description
- id
- license
- name
- reference
- ruleset
- uuid
- version

___
### x-ecs-server
- address
- domain
- nat_ip
- nat_port
- registered_domain
- top_level_domain
- geo_city_name
- geo_continent_name
- geo_country_iso_code
- geo_country_name
- geo_location
- geo_name
- geo_region_iso_code
- geo_region_name

___
### x-ecs-service
- id
- name
- state
- type
- version
- ephemeral_id
- node_name

___
### x-ecs-source
- address
- domain
- nat_ip
- nat_port
- registered_domain
- top_level_domain
- geo_city_name
- geo_continent_name
- geo_country_iso_code
- geo_country_name
- geo_location
- geo_name
- geo_region_iso_code
- geo_region_name

___
### x-ecs-threat
- framework
- tactic_id
- tactic_name
- tactic_reference
- technique_id
- technique_name
- technique_reference

___
### x-ecs-tls
- client_certificate
- client_certificate_chain
- client_ja3
- client_supported_ciphers
- server_certificate
- server_certificate_chain
- server_ja3s
- cipher
- curve
- established
- next_protocol
- resumed
- version
- version_protocol

___
### x-ecs-trace
- id

___
### x-ecs-transaction
- id

___
### x-ecs-user
- domain
- full_name
- hash
- id
- group_domain
- group_id
- group_name

___
### x-ecs-user_agent
- name
- original
- version
- device_name

___
### x-ecs-vulnerability
- category
- classification
- description
- enumeration
- id
- reference
- report_id
- severity
- scanner_vendor
- score_base
- score_environmental
- score_temporal
- score_version

___
### x-oca-asset
- architecture
- domain
- hostname
- id
- ip_refs
- mac_refs
- name
- host_type
- uptime
- geo_city_name
- geo_continent_name
- geo_country_iso_code
- geo_country_name
- geo_location
- geo_name
- geo_region_iso_code
- geo_region_name
- os_name
- os_platform
- os_version
- user_domain
- user_email
- user_full_name
- user_hash
- user_id
- user_name
- user_group_domain
- user_group_id
- user_group_name

___
### x-oca-event
- network_ref
- original_ref
- action
- id
- category
- code
- created
- dataset
- duration
- end
- hash
- ingested
- kind
- module
- outcome
- provider
- reference
- risk_score
- risk_score_norm
- sequence
- severity
- start
- timezone
- event_type
- url
- domain_ref
- url_ref
- process_ref
- parent_process_ref
- user_ref
- agent
- ip_refs
- file_ref
- host_ref
- registry_ref

___
### x509-certificate
- issuer
- hashes.SHA-256
- hashes.SHA-1
- hashes.MD5
- validity_not_after
- validity_not_before
- subject

___
### x_ecs
- version

___
