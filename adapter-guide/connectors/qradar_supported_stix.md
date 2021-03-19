## IBM QRadar
### artifact
- payload_bin

___
### directory
- path

___
### domain-name
- value

___
### email-message
- content_type

___
### file
- name
- hashes.SHA-256
- hashes.SHA-1
- hashes.MD5
- hashes.UNKNOWN
- size
- parent_directory_ref
- mime_type

___
### ipv4-addr
- value
- resolves_to_refs

___
### ipv6-addr
- value
- resolves_to_refs

___
### mac-addr
- value

___
### network-traffic
- dst_ref
- src_ref
- extensions.dns-ext.question.domain_ref
- src_payload_ref
- dst_payload_ref
- dst_port
- src_port
- src_byte_count
- dst_byte_count
- src_packets
- dst_packets
- protocols
- extensions.http-request-ext.request_header.Host
- extensions.http-request-ext.request_header.Referer
- extensions.http-request-ext.request_header.Server
- extensions.http-request-ext.request_header.User-Agent
- extensions.http-request-ext.request_version
- ipfix.flowId
- extensions.http-request-ext.request_header.Content-Type

___
### process
- creator_user_ref
- binary_ref
- parent_ref
- command_line
- name
- pid
- extensions.windows-service-ext.service_dll_refs

___
### software
- name

___
### url
- value

___
### user-account
- user_id

___
### windows-registry-key
- key
- values

___
### x-ibm-finding
- src_application_user_ref
- dst_ip_ref
- event_count
- finding_type
- start
- end
- magnitude
- src_ip_ref
- src_geolocation
- dst_geolocation
- severity
- rule_names
- name
- description

___
### x-ibm-windows
- targetimage
- granted_access
- call_trace
- source_image
- pipe_name
- start_module
- start_function
- signed
- imphash

___
### x-oca-asset
- ip_refs
- hostname
- mac_refs

___
### x-oca-event
- user_ref
- outcome
- category
- host_ref
- action
- created
- network_ref
- agent
- provider
- url_ref
- domain_ref
- file_ref
- original_ref
- process_ref
- parent_process_ref
- code
- registry_ref
- original

___
### x-qradar
- category_id
- high_level_category_id
- relevance
- log_source_id
- direction
- qid
- domain_name
- flow_source
- flow_interface
- flow_interface_id
- geographic
- credibility
- severity
- first_packet_time
- last_packet_time
- application_id
- cre_event_list
- domain_id
- device_type
- flow_type
- file_entropy
- http_response_code
- tls_ja3_hash
- tls_ja3s_hash
- suspect_content_descriptions
- tls_server_name_indication
- registry_key

___
