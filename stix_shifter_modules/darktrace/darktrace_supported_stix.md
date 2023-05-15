##### Updated on 05/15/23
## Darktrace
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
| > | :> |
| < | :< |
| >= | :> |
| <= | :< |
| = | : |
| LIKE | : |
| IN | : |
| MATCHES | : |
| != | NOT |
| OR (Observation) | OR |
| AND (Observation) | OR |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | source_ip, dest_ip, src, dst, ip, subnet_mask, released_ip, requested_ip, assigned_ip |
| **ipv6-addr**:value | source_ip, dest_ip, src, dst, ip, subnet_mask, released_ip, requested_ip, assigned_ip |
| **mac-addr**:value | mac |
| **domain-name**:value | domain_name, query |
| **network-traffic**:src_port | source_port, src_p |
| **network-traffic**:dst_port | dest_port, dst_p |
| **network-traffic**:src_ref.value | source_ip, src, mac |
| **network-traffic**:dst_ref.value | dest_ip, dst |
| **network-traffic**:protocols[*] | proto, protocol |
| **network-traffic**:src_packets | pkts_recv, orig_pkts |
| **network-traffic**:dst_packets | pkts_dropped, resp_pkts |
| **network-traffic**:src_byte_count | orig_bytes, orig_ip_bytes |
| **network-traffic**:dst_byte_count | megabytes_recv, resp_bytes, resp_ip_bytes |
| **network-traffic**:extensions.'x-darktrace-conn'.app_protocol | service |
| **network-traffic**:extensions.'x-darktrace-conn'.start_ts | start_ts |
| **network-traffic**:extensions.'x-darktrace-conn'.oss_start_ts | oss_start_ts |
| **network-traffic**:extensions.'x-darktrace-conn'.connection_length | duration |
| **network-traffic**:extensions.'x-darktrace-conn'.conn_state | conn_state |
| **network-traffic**:extensions.'x-darktrace-conn'.connection_state_desc | conn_state_full |
| **network-traffic**:extensions.'x-darktrace-conn'.is_locally_originated | local_orig |
| **network-traffic**:extensions.'x-darktrace-conn'.is_locally_responded | local_resp |
| **network-traffic**:extensions.'x-darktrace-conn'.missed_bytes_orig | missed_bytes_orig |
| **network-traffic**:extensions.'x-darktrace-conn'.missed_bytes_resp | missed_bytes_resp |
| **network-traffic**:extensions.'x-darktrace-conn'.history | history |
| **network-traffic**:extensions.'x-darktrace-conn'.originator_ttl | orig_ttl |
| **network-traffic**:extensions.'x-darktrace-conn'.responder_ttl | resp_ttl |
| **network-traffic**:extensions.'x-darktrace-conn'.tunnel_parents | tunnel_parents |
| **network-traffic**:extensions.'x-darktrace-conn'.orig_percent_invalid_checksum | orig_percent_invalid_checksum |
| **network-traffic**:extensions.'x-darktrace-conn'.resp_percent_invalid_checksum | resp_percent_invalid_checksum |
| **network-traffic**:extensions.'x-darktrace-conn'.outer_vlan | outer_vlan |
| **network-traffic**:extensions.'x-darktrace-conn'.vlan_id | vlan |
| **network-traffic**:extensions.'x-darktrace-conn'.orig_country_code | orig_cc |
| **network-traffic**:extensions.'x-darktrace-conn'.resp_country_code | resp_cc |
| **network-traffic**:extensions.'x-darktrace-conn'.originator_asn | orig_asn |
| **network-traffic**:extensions.'x-darktrace-conn'.responder_asn | resp_asn |
| **network-traffic**:extensions.'x-darktrace-ssh'.ssh_version | version |
| **network-traffic**:extensions.'x-darktrace-ssh'.status | status_guess |
| **network-traffic**:extensions.'x-darktrace-ssh'.auth_result | auth_success |
| **network-traffic**:extensions.'x-darktrace-ssh'.auth_attempts | auth_attempts |
| **network-traffic**:extensions.'x-darktrace-ssh'.connection_direction | direction |
| **network-traffic**:extensions.'x-darktrace-ssh'.client_version | client |
| **network-traffic**:extensions.'x-darktrace-ssh'.server_version | server |
| **network-traffic**:extensions.'x-darktrace-ssh'.encrypt_algo | cipher_alg |
| **network-traffic**:extensions.'x-darktrace-ssh'.signing_algo | mac_alg |
| **network-traffic**:extensions.'x-darktrace-ssh'.compression_algo | compression_alg |
| **network-traffic**:extensions.'x-darktrace-ssh'.key_exchange_algo | kex_alg |
| **network-traffic**:extensions.'x-darktrace-ssh'.server_key_algo | host_key_alg |
| **network-traffic**:extensions.'x-darktrace-ssh'.server_key | host_key |
| **network-traffic**:extensions.'x-darktrace-http'.orginator_ip | xorig_ip |
| **network-traffic**:extensions.'x-darktrace-http'.transaction_depth | trans_depth |
| **network-traffic**:extensions.'http-request-ext'.request_method | method |
| **network-traffic**:extensions.'x-darktrace-http'.server_host | host |
| **network-traffic**:extensions.'http-request-ext'.request_value | uri |
| **network-traffic**:extensions.'x-darktrace-http'.referrer | referrer |
| **network-traffic**:extensions.'http-request-ext'.request_version | version |
| **network-traffic**:extensions.'x-darktrace-http'.user_agent | user_agent |
| **network-traffic**:extensions.'http-request-ext'.message_body_length | request_body_len |
| **network-traffic**:extensions.'x-darktrace-http'.response_body_len | response_body_len |
| **network-traffic**:extensions.'x-darktrace-http'.status_code | status_code |
| **network-traffic**:extensions.'x-darktrace-http'.status_msg | status_msg |
| **network-traffic**:extensions.'x-darktrace-http'.informational_code | info_code |
| **network-traffic**:extensions.'x-darktrace-http'.informational_msg | info_msg |
| **network-traffic**:extensions.'x-darktrace-http'.content_type | content_type |
| **network-traffic**:extensions.'x-darktrace-http'.tags[*] | tags |
| **network-traffic**:extensions.'x-darktrace-http'.unencrypted_password | unencrypted_password |
| **network-traffic**:extensions.'x-darktrace-http'.is_proxied | proxied |
| **network-traffic**:extensions.'x-darktrace-http'.outside_timestamp | oss_ts |
| **network-traffic**:extensions.'x-darktrace-http'.client_ids[*] | orig_fuids |
| **network-traffic**:extensions.'x-darktrace-http'.client_filenames[*] | orig_filenames |
| **network-traffic**:extensions.'x-darktrace-http'.client_mime_types[*] | orig_mime_types |
| **network-traffic**:extensions.'x-darktrace-http'.server_file_ids[*] | resp_fuids |
| **network-traffic**:extensions.'x-darktrace-http'.server_file_names[*] | resp_filenames |
| **network-traffic**:extensions.'x-darktrace-http'.server_mime_types[*] | resp_mime_types |
| **network-traffic**:extensions.'x-darktrace-http'.client_header_names[*] | client_header_names |
| **network-traffic**:extensions.'x-darktrace-http'.server_header_names[*] | server_header_names |
| **network-traffic**:extensions.'x-darktrace-http'.redirect_location | redirect_location |
| **network-traffic**:extensions.'x-darktrace-http'.flash_version | flash_version |
| **network-traffic**:extensions.'x-darktrace-ftp'.client_command | command |
| **network-traffic**:extensions.'x-darktrace-ftp'.argument | arg |
| **network-traffic**:extensions.'x-darktrace-ftp'.file_msg | file_msg |
| **network-traffic**:extensions.'x-darktrace-ftp'.reply_code | reply_code |
| **network-traffic**:extensions.'x-darktrace-ftp'.reply_msg | reply_msg |
| **network-traffic**:extensions.'x-darktrace-ftp'.data_channel | data_channel |
| **network-traffic**:extensions.'x-darktrace-ftp'.data_channel_passive | data_channel_passive |
| **network-traffic**:extensions.'x-darktrace-ftp'.data_channel_originator | data_channel_orig_h |
| **network-traffic**:extensions.'x-darktrace-ftp'.data_channel_responder | data_channel_resp_h |
| **network-traffic**:extensions.'x-darktrace-ftp'.data_channel_responder_port | data_channel_resp_p |
| **network-traffic**:extensions.'x-darktrace-ftp'.file_uid | fuid |
| **network-traffic**:extensions.'x-darktrace-dns'.transaction_id | trans_id |
| **network-traffic**:extensions.'x-darktrace-dns'.query_class | query_class |
| **network-traffic**:extensions.'x-darktrace-dns'.query_type | query_type |
| **network-traffic**:extensions.'x-darktrace-dns'.additional_queries | other_queries |
| **network-traffic**:extensions.'x-darktrace-dns'.response_code | err_code |
| **network-traffic**:extensions.'x-darktrace-dns'.recognised_answers[*] | answers |
| **network-traffic**:extensions.'x-darktrace-dns'.answer_types[*] | atypes |
| **network-traffic**:extensions.'x-darktrace-dns'.pay_load[*] | a_load |
| **network-traffic**:extensions.'x-darktrace-dns'.ttls[*] | TTLs |
| **network-traffic**:extensions.'x-darktrace-dns'.unprocessed_atypes[*] | unprocessed_atypes |
| **network-traffic**:extensions.'x-darktrace-dns'.unprocessed_payload_size | unprocessed_payload_size |
| **network-traffic**:extensions.'x-darktrace-dns'.unprocessed_ttls[*] | unprocessed_TTLs |
| **network-traffic**:extensions.'x-darktrace-dns'.multicast_responder | multicast_responder |
| **network-traffic**:extensions.'x-darktrace-dns'.details | details |
| **network-traffic**:extensions.'x-darktrace-dns'.is_rejected | rejected |
| **network-traffic**:extensions.'x-darktrace-ldap'.operation | operation |
| **network-traffic**:extensions.'x-darktrace-ldap'.services[*] | services |
| **network-traffic**:extensions.'x-darktrace-ldap'.bind_version | version |
| **network-traffic**:extensions.'x-darktrace-ldap'.authentication | authentication |
| **network-traffic**:extensions.'x-darktrace-ldap'.bind_name | bind_name |
| **network-traffic**:extensions.'x-darktrace-ldap'.is_password_seen | password_seen |
| **network-traffic**:extensions.'x-darktrace-ldap'.search_root | search_root |
| **network-traffic**:extensions.'x-darktrace-ldap'.search_scope | search_scope |
| **network-traffic**:extensions.'x-darktrace-ldap'.dereference_aliases | dereference_aliases |
| **network-traffic**:extensions.'x-darktrace-ldap'.search_filter | filter |
| **network-traffic**:extensions.'x-darktrace-ldap'.Requested_attributes | attributes |
| **network-traffic**:extensions.'x-darktrace-ldap'.entry | entry |
| **network-traffic**:extensions.'x-darktrace-ldap'.comparison | comparison |
| **network-traffic**:extensions.'x-darktrace-ldap'.response | response |
| **network-traffic**:extensions.'x-darktrace-ldap'.issue_details | issue |
| **network-traffic**:extensions.'x-darktrace-dhcp'.dhcp_type | dhcp_type |
| **network-traffic**:extensions.'x-darktrace-dhcp'.host_name | host_name |
| **network-traffic**:extensions.'x-darktrace-dhcp'.lease_time | lease_time |
| **network-traffic**:extensions.'x-darktrace-rdp'.cookie | cookie |
| **network-traffic**:extensions.'x-darktrace-rdp'.security_protocol | security_protocol |
| **network-traffic**:extensions.'x-darktrace-rdp'.client_channels[*] | client_channels |
| **network-traffic**:extensions.'x-darktrace-rdp'.client_name | client_name |
| **network-traffic**:extensions.'x-darktrace-rdp'.client_build | client_build |
| **network-traffic**:extensions.'x-darktrace-rdp'.cert_type | cert_type |
| **network-traffic**:extensions.'x-darktrace-rdp'.cert_count | cert_count |
| **network-traffic**:extensions.'x-darktrace-rdp'.is_cert_permanent | cert_permanent |
| **network-traffic**:extensions.'x-darktrace-rdp'.encryption_level | encryption_level |
| **network-traffic**:extensions.'x-darktrace-rdp'.encryption_method | encryption_method |
| **network-traffic**:extensions.'x-darktrace-pop3'.is_login_success | login_success |
| **network-traffic**:extensions.'x-darktrace-pop3'.commands_used | commands_used |
| **network-traffic**:extensions.'x-darktrace-pop3'.file_uids[*] | fuids |
| **network-traffic**:extensions.'x-darktrace-files-identified'.src_hosts[*].value | tx_hosts |
| **network-traffic**:extensions.'x-darktrace-files-identified'.dest_hosts[*].value | rx_hosts |
| **network-traffic**:extensions.'x-darktrace-files-identified'.source | source |
| **network-traffic**:extensions.'x-darktrace-files-identified'.seen_bytes | seen_bytes |
| **network-traffic**:extensions.'x-darktrace-files-identified'.file_ident_descr | file_ident_descr |
| **network-traffic**:extensions.'x-darktrace-files-identified'.file_ident_ports[*] | file_ident_ports |
| **network-traffic**:extensions.'x-darktrace-files-identified'.file_identifier | fuid |
| **network-traffic**:extensions.'x-darktrace-device-details'.connection_method | method |
| **network-traffic**:extensions.'x-darktrace-device-details'.lease_time | lease_time |
| **network-traffic**:extensions.'x-darktrace-device-details'.released_ip | released_ip |
| **network-traffic**:extensions.'x-darktrace-device-details'.outer_vlan_tag | outer_vlan |
| **network-traffic**:extensions.'x-darktrace-device-details'.vlan_tag | vlan |
| **user-account**:account_login | user, username |
| **file**:name | filename |
| **file**:hashes.'SHA-1' | sha1_file_hash, sha1 |
| **file**:hashes.MD5 | md5_file_hash, md5 |
| **file**:hashes.'SHA-256' | sha256_file_hash, sha256 |
| **file**:mime_type | mime, file_mime_type, mime_type, dcc_mime_type |
| **file**:size | total_bytes, file_msg, read_size, write_size, dcc_file_size |
| **file**:created | epochdate |
| **email-addr**:value | mailfrom, rcptto, from, to, cc |
| **email-message**:date | date |
| **email-message**:from_ref.value | mailfrom |
| **email-message**:sender_ref.value | from |
| **email-message**:to_refs.value | rcptto |
| **email-message**:cc_refs.value | cc |
| **email-message**:subject | subject |
| **email-message**:received_lines | last_reply |
| **email-message**:extensions.'x-darktrace-smtp'.transaction_depth | trans_depth |
| **email-message**:extensions.'x-darktrace-smtp'.helo_header | helo |
| **email-message**:extensions.'x-darktrace-smtp'.reply_to_header | reply_to |
| **email-message**:extensions.'x-darktrace-smtp'.msg_id_header | msg_id |
| **email-message**:extensions.'x-darktrace-smtp'.in_reply_to_header | in_reply_to |
| **email-message**:extensions.'x-darktrace-smtp'.x_originating_ip_h | x_originating_ip |
| **email-message**:extensions.'x-darktrace-smtp'.first_received | first_received |
| **email-message**:extensions.'x-darktrace-smtp'.second_received | second_received |
| **email-message**:extensions.'x-darktrace-smtp'.message_path | path |
| **email-message**:extensions.'x-darktrace-smtp'.user_agent | user_agent |
| **email-message**:extensions.'x-darktrace-smtp'.is_tls | tls |
| **email-message**:extensions.'x-darktrace-smtp'.file_ids[*] | fuids |
| **email-message**:extensions.'x-darktrace-smtp'.decoded_subject | decoded_subject |
| **software**:name | name |
| **software**:version | version |
| **software**:extensions.'x-darktrace-software'.software_type | software_type |
| **software**:extensions.'x-darktrace-software'.version_major | version_major |
| **software**:extensions.'x-darktrace-software'.version_minor | version_minor |
| **software**:extensions.'x-darktrace-software'.version_minor3 | version_minor3 |
| **software**:extensions.'x-darktrace-software'.host | host |
| **software**:extensions.'x-darktrace-software'.host_port | host_p |
| **x509-certificate**:version | certificate_version |
| **x509-certificate**:serial_number | certificate_serial |
| **x509-certificate**:signature_algorithm | certificate_sig_alg |
| **x509-certificate**:issuer | certificate_issuer, issuer |
| **x509-certificate**:validity_not_before | certificate_not_valid_before |
| **x509-certificate**:validity_not_after | certificate_not_valid_after |
| **x509-certificate**:subject | certificate_subject |
| **x509-certificate**:subject_public_key_algorithm | certificate_key_alg |
| **x509-certificate**:subject_public_key_exponent | certificate_exponent |
| **x509-certificate**:extensions.'x509_v3_extensions'.basic_constraints | basic_constraints |
| **x509-certificate**:extensions.'x509_v3_extensions'.subject_alternative_name | san |
| **x509-certificate**:extensions.'x-darktrace-x509'.certificate_key_type | certificate_key_type |
| **x509-certificate**:extensions.'x-darktrace-x509'.certificate_key_length | certificate_key_length |
| **x509-certificate**:extensions.'x-darktrace-x509'.certificate_curve | certificate_curve |
| **x509-certificate**:extensions.'x-darktrace-x509'.is_basic_constraints_ca | basic_constraints_ca |
| **x509-certificate**:extensions.'x-darktrace-x509'.basic_constraints_path_len | basic_constraints_path_len |
| **x509-certificate**:extensions.'x-darktrace-x509'.certificate_basic_info | certificate |
| **x509-certificate**:extensions.'x-darktrace-x509'.file_id | fid |
| **x509-certificate**:extensions.'x-darktrace-ssl'.client_subject | client_subject |
| **x509-certificate**:extensions.'x-darktrace-ssl'.client_issuer | client_issuer |
| **x509-certificate**:extensions.'x-darktrace-ssl'.ssl_version | version |
| **x509-certificate**:extensions.'x-darktrace-ssl'.cipher_suite | cipher |
| **x509-certificate**:extensions.'x-darktrace-ssl'.cipher_list[*] | client_ciphers |
| **x509-certificate**:extensions.'x-darktrace-ssl'.total_ciphers | total_client_ciphers |
| **x509-certificate**:extensions.'x-darktrace-ssl'.elliptic_curve | curve |
| **x509-certificate**:extensions.'x-darktrace-ssl'.server_name | server_name |
| **x509-certificate**:extensions.'x-darktrace-ssl'.is_resumed | resumed |
| **x509-certificate**:extensions.'x-darktrace-ssl'.last_alert | last_alert |
| **x509-certificate**:extensions.'x-darktrace-ssl'.next_protocol | next_protocol |
| **x509-certificate**:extensions.'x-darktrace-ssl'.is_established | established |
| **x509-certificate**:extensions.'x-darktrace-ssl'.is_client_hello_seen | client_hello_seen |
| **x509-certificate**:extensions.'x-darktrace-ssl'.cert_file_uids[*] | cert_chain_fuids |
| **x509-certificate**:extensions.'x-darktrace-ssl'.cert_chainfile_uids[*] | client_cert_chain_fuids |
| **x509-certificate**:extensions.'x-darktrace-ssl'.ocsp_status | ocsp_status |
| **x509-certificate**:extensions.'x-darktrace-ssl'.validation_status | validation_status |
| **x509-certificate**:extensions.'x-darktrace-ssl'.ja3_client_fingerprint | ja3_client_fingerprint |
| **x509-certificate**:extensions.'x-darktrace-ssl'.ja3s_server_fingerprint | ja3s_server_fingerprint |
| **x509-certificate**:extensions.'x-darktrace-ssl'.application_guess | application_guess |
| **x-oca-asset**:hostname | host |
| **x-oca-asset**:ip_refs[*].value | source_ip, dest_ip, src, dst, ip |
| **x-oca-asset**:mac_refs[*].value | mac |
| **x-oca-asset**:extensions.'x-darktrace-conn'.asset_id | id_hUUID |
| **x-oca-asset**:extensions.'x-darktrace-endpoint'.host_uuid | hUUID |
| **x-oca-event**:created | epochdate |
| **x-oca-event**:code | uid |
| **x-oca-event**:host_ref | host |
| **x-oca-event**:file_ref | filename |
| **x-oca-event**:user_ref | user, username |
| **x-oca-event**:domain_ref | domain_name, query |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| domain-name | value | query |
| domain-name | value | domain_name |
| <br> | | |
| email-addr | value | mailfrom |
| email-addr | value | rcptto |
| email-addr | value | from |
| email-addr | value | cc |
| <br> | | |
| email-message | extensions.x-darktrace-smtp.transaction_depth | trans_depth |
| email-message | additional_header_fields.helo_header | helo |
| email-message | is_multipart | helo |
| email-message | from_ref | mailfrom |
| email-message | is_multipart | mailfrom |
| email-message | to_refs | rcptto |
| email-message | is_multipart | rcptto |
| email-message | date | date |
| email-message | is_multipart | is_multipart |
| email-message | sender_ref | from |
| email-message | additional_header_fields.to_header | to |
| email-message | cc_refs | cc |
| email-message | additional_header_fields.reply_to_header | reply_to |
| email-message | additional_header_fields.msg_id_header | msg_id |
| email-message | additional_header_fields.in_reply_to_header | in_reply_to |
| email-message | subject  | subject |
| email-message | additional_header_fields.x_originating_ip | x_originating_ip |
| email-message | additional_header_fields.first_received | first_received |
| email-message | additional_header_fields.second_received | second_received |
| email-message | extensions.x-darktrace-smtp.last_reply | last_reply |
| email-message | additional_header_fields.message_path | path |
| email-message | additional_header_fields.user_agent | user_agent |
| email-message | extensions.x-darktrace-smtp.is_tls | tls |
| email-message | extensions.x-darktrace-smtp.file_ids | fuids |
| email-message | additional_header_fields.decoded_subject | decoded_subject |
| <br> | | |
| file | mime_type | mime_type |
| file | name | filename |
| file | size | total_bytes |
| file | hashes.MD5 | md5 |
| file | hashes.SHA-1 | sha1 |
| file | hashes.SHA-256 | sha256 |
| <br> | | |
| ipv4-addr | value | source_ip |
| ipv4-addr | value | dest_ip |
| ipv4-addr | value | subnet_mask |
| ipv4-addr | value | released_ip |
| ipv4-addr | value | requested_ip |
| ipv4-addr | value | assigned_ip |
| ipv4-addr | value | tx_hosts |
| ipv4-addr | value | rx_hosts |
| ipv4-addr | value | host |
| ipv4-addr | value | ip |
| <br> | | |
| ipv6-addr | value | source_ip |
| ipv6-addr | value | dest_ip |
| ipv6-addr | value | ip |
| <br> | | |
| mac-addr | value | mac |
| <br> | | |
| network-traffic | src_ref | source_ip |
| network-traffic | dst_ref | dest_ip |
| network-traffic | src_port | source_port |
| network-traffic | dst_port | dest_port |
| network-traffic | protocols | proto |
| network-traffic | extensions.x-darktrace-conn.app_protocol | service |
| network-traffic | extensions.x-darktrace-conn.start_ts | start_ts |
| network-traffic | extensions.x-darktrace-conn.oss_start_ts | oss_start_ts |
| network-traffic | extensions.x-darktrace-conn.connection_length | duration |
| network-traffic | src_byte_count | orig_bytes |
| network-traffic | dst_byte_count | resp_bytes |
| network-traffic | extensions.x-darktrace-conn.conn_state | conn_state |
| network-traffic | extensions.x-darktrace-conn.connection_state_desc | conn_state_full |
| network-traffic | extensions.x-darktrace-conn.is_locally_originated | local_orig |
| network-traffic | extensions.x-darktrace-conn.is_locally_responded | local_resp |
| network-traffic | extensions.x-darktrace-conn.missed_bytes_orig | missed_bytes_orig |
| network-traffic | extensions.x-darktrace-conn.missed_bytes_resp | missed_bytes_resp |
| network-traffic | extensions.x-darktrace-conn.history | history |
| network-traffic | src_packets | orig_pkts |
| network-traffic | src_byte_count | orig_ip_bytes |
| network-traffic | dst_packets | resp_pkts |
| network-traffic | dst_byte_count | resp_ip_bytes |
| network-traffic | extensions.x-darktrace-conn.originator_ttl | orig_ttl |
| network-traffic | extensions.x-darktrace-conn.responder_ttl | resp_ttl |
| network-traffic | extensions.x-darktrace-conn.tunnel_parents | tunnel_parents |
| network-traffic | extensions.x-darktrace-conn.orig_percent_invalid_checksum | orig_percent_invalid_checksum |
| network-traffic | extensions.x-darktrace-conn.resp_percent_invalid_checksum | resp_percent_invalid_checksum |
| network-traffic | extensions.x-darktrace-conn.outer_vlan | outer_vlan |
| network-traffic | extensions.x-darktrace-conn.vlan_id | vlan |
| network-traffic | extensions.x-darktrace-conn.orig_country_code | orig_cc |
| network-traffic | extensions.x-darktrace-conn.resp_country_code | resp_cc |
| network-traffic | extensions.x-darktrace-conn.originator_asn | orig_asn |
| network-traffic | extensions.x-darktrace-conn.responder_asn | resp_asn |
| network-traffic | extensions.x-darktrace-ssh.ssh_version | version |
| network-traffic | extensions.x-darktrace-ssh.status | status_guess |
| network-traffic | extensions.x-darktrace-ssh.auth_result | auth_success |
| network-traffic | extensions.x-darktrace-ssh.auth_attempts | auth_attempts |
| network-traffic | extensions.x-darktrace-ssh.connection_direction | direction |
| network-traffic | extensions.x-darktrace-ssh.client_version | client |
| network-traffic | extensions.x-darktrace-ssh.server_version | server |
| network-traffic | extensions.x-darktrace-ssh.encrypt_algo | cipher_alg |
| network-traffic | extensions.x-darktrace-ssh.signing_algo | mac_alg |
| network-traffic | extensions.x-darktrace-ssh.compression_algo | compression_alg |
| network-traffic | extensions.x-darktrace-ssh.key_exchange_algo | kex_alg |
| network-traffic | extensions.x-darktrace-ssh.server_key_algo | host_key_alg |
| network-traffic | extensions.x-darktrace-ssh.server_key | host_key |
| network-traffic | extensions.x-darktrace-http.orginator_ip | xorig_ip |
| network-traffic | extensions.x-darktrace-http.transaction_depth | trans_depth |
| network-traffic | extensions.http-request-ext.request_method | method |
| network-traffic | extensions.x-darktrace-http.server_host | host |
| network-traffic | extensions.http-request-ext.request_value | uri |
| network-traffic | extensions.x-darktrace-http.referrer | referrer |
| network-traffic | extensions.http-request-ext.request_version | version |
| network-traffic | extensions.x-darktrace-http.user_agent | user_agent |
| network-traffic | extensions.http-request-ext.message_body_length | request_body_len |
| network-traffic | extensions.x-darktrace-http.response_body_len | response_body_len |
| network-traffic | extensions.x-darktrace-http.status_code | status_code |
| network-traffic | extensions.x-darktrace-http.status_msg | status_msg |
| network-traffic | extensions.x-darktrace-http.informational_code | info_code |
| network-traffic | extensions.x-darktrace-http.informational_msg | info_msg |
| network-traffic | extensions.x-darktrace-http.content_type | content_type |
| network-traffic | extensions.x-darktrace-http.tags | tags |
| network-traffic | extensions.x-darktrace-http.unencrypted_password | unencrypted_password |
| network-traffic | extensions.x-darktrace-http.is_proxied | proxied |
| network-traffic | extensions.x-darktrace-http.outside_timestamp | oss_ts |
| network-traffic | extensions.x-darktrace-http.client_ids | orig_fuids |
| network-traffic | extensions.x-darktrace-http.client_filenames | orig_filenames |
| network-traffic | extensions.x-darktrace-http.client_mime_types | orig_mime_types |
| network-traffic | extensions.x-darktrace-http.server_file_ids | resp_fuids |
| network-traffic | extensions.x-darktrace-http.server_file_names | resp_filenames |
| network-traffic | extensions.x-darktrace-http.server_mime_types | resp_mime_types |
| network-traffic | extensions.x-darktrace-http.client_header_names | client_header_names |
| network-traffic | extensions.x-darktrace-http.server_header_names | server_header_names |
| network-traffic | extensions.x-darktrace-http.redirect_location | redirect_location |
| network-traffic | extensions.x-darktrace-http.flash_version | flash_version |
| network-traffic | extensions.x-darktrace-ftp.client_command | command |
| network-traffic | extensions.x-darktrace-ftp.argument | arg |
| network-traffic | extensions.x-darktrace-ftp.file_msg | file_msg |
| network-traffic | extensions.x-darktrace-ftp.reply_code | reply_code |
| network-traffic | extensions.x-darktrace-ftp.reply_msg | reply_msg |
| network-traffic | extensions.x-darktrace-ftp.data_channel | data_channel |
| network-traffic | extensions.x-darktrace-ftp.data_channel_passive | data_channel_passive |
| network-traffic | extensions.x-darktrace-ftp.data_channel_originator | data_channel_orig_h |
| network-traffic | extensions.x-darktrace-ftp.data_channel_responder | data_channel_resp_h |
| network-traffic | extensions.x-darktrace-ftp.data_channel_responder_port | data_channel_resp_p |
| network-traffic | extensions.x-darktrace-ftp.file_uid | fuid |
| network-traffic | extensions.x-darktrace-dns.transaction_id | trans_id |
| network-traffic | extensions.x-darktrace-dns.query_class | query_class |
| network-traffic | extensions.x-darktrace-dns.query_type | query_type |
| network-traffic | extensions.x-darktrace-dns.additional_queries | other_queries |
| network-traffic | extensions.x-darktrace-dns.response_code | err_code |
| network-traffic | extensions.x-darktrace-dns.recognised_answers | answers |
| network-traffic | extensions.x-darktrace-dns.answer_types | atypes |
| network-traffic | extensions.x-darktrace-dns.pay_load | a_load |
| network-traffic | extensions.x-darktrace-dns.ttls | TTLs |
| network-traffic | extensions.x-darktrace-dns.unprocessed_atypes | unprocessed_atypes |
| network-traffic | extensions.x-darktrace-dns.unprocessed_payload_size | unprocessed_payload_size |
| network-traffic | extensions.x-darktrace-dns.unprocessed_ttls | unprocessed_TTLs |
| network-traffic | extensions.x-darktrace-dns.multicast_responder | multicast_responder |
| network-traffic | extensions.x-darktrace-dns.details | details |
| network-traffic | extensions.x-darktrace-dns.is_rejected | rejected |
| network-traffic | extensions.x-darktrace-ldap.operation | operation |
| network-traffic | extensions.x-darktrace-ldap.services | services |
| network-traffic | extensions.x-darktrace-ldap.bind_version | version |
| network-traffic | extensions.x-darktrace-ldap.authentication | authentication |
| network-traffic | extensions.x-darktrace-ldap.bind_name | bind_name |
| network-traffic | extensions.x-darktrace-ldap.is_password_seen | password_seen |
| network-traffic | extensions.x-darktrace-ldap.search_root | search_root |
| network-traffic | extensions.x-darktrace-ldap.search_scope | search_scope |
| network-traffic | extensions.x-darktrace-ldap.dereference_aliases | dereference_aliases |
| network-traffic | extensions.x-darktrace-ldap.search_filter | filter |
| network-traffic | extensions.x-darktrace-ldap.requested_attributes | attributes |
| network-traffic | extensions.x-darktrace-ldap.entry | entry |
| network-traffic | extensions.x-darktrace-ldap.comparison | comparison |
| network-traffic | extensions.x-darktrace-ldap.response | response |
| network-traffic | extensions.x-darktrace-ldap.issue_details | issue |
| network-traffic | extensions.x-darktrace-dhcp.dhcp_type | dhcp_type |
| network-traffic | extensions.x-darktrace-dhcp.host_name | host_name |
| network-traffic | extensions.x-darktrace-dhcp.subnet_mask_ref | subnet_mask |
| network-traffic | extensions.x-darktrace-dhcp.released_ip_ref | released_ip |
| network-traffic | extensions.x-darktrace-dhcp.requested_ip_ref | requested_ip |
| network-traffic | extensions.x-darktrace-dhcp.lease_time | lease_time |
| network-traffic | extensions.x-darktrace-dhcp.assigned_ip_ref | assigned_ip |
| network-traffic | extensions.x-darktrace-rdp.cookie | cookie |
| network-traffic | extensions.x-darktrace-rdp.security_protocol | security_protocol |
| network-traffic | extensions.x-darktrace-rdp.client_channels | client_channels |
| network-traffic | extensions.x-darktrace-rdp.client_name | client_name |
| network-traffic | extensions.x-darktrace-rdp.client_build | client_build |
| network-traffic | extensions.x-darktrace-rdp.cert_type | cert_type |
| network-traffic | extensions.x-darktrace-rdp.cert_count | cert_count |
| network-traffic | extensions.x-darktrace-rdp.is_cert_permanent | cert_permanent |
| network-traffic | extensions.x-darktrace-rdp.encryption_level | encryption_level |
| network-traffic | extensions.x-darktrace-rdp.encryption_method | encryption_method |
| network-traffic | extensions.x-darktrace-pop3.is_login_success | login_success |
| network-traffic | extensions.x-darktrace-pop3.commands_used | commands_used |
| network-traffic | extensions.x-darktrace-pop3.file_uids | fuids |
| network-traffic | extensions.x-darktrace-files-identified.src_host_refs | tx_hosts |
| network-traffic | extensions.x-darktrace-files-identified.dest_host_refs | rx_hosts |
| network-traffic | extensions.x-darktrace-files-identified.source | source |
| network-traffic | extensions.x-darktrace-files-identified.seen_bytes | seen_bytes |
| network-traffic | extensions.x-darktrace-files-identified.file_ident_descr | file_ident_descr |
| network-traffic | extensions.x-darktrace-files-identified.file_ident_ports | file_ident_ports |
| network-traffic | extensions.x-darktrace-files-identified.file_identifier | fuid |
| network-traffic | extensions.x-darktrace-device-details.connection_method | method |
| network-traffic | src_port | src_p |
| network-traffic | dst_port | dst_p |
| network-traffic | extensions.x-darktrace-device-details.event_ip_ref | ip |
| network-traffic | extensions.x-darktrace-device-details.subnet_mask_ref | subnet_mask |
| network-traffic | extensions.x-darktrace-device-details.lease_time | lease_time |
| network-traffic | extensions.x-darktrace-device-details.released_ip_ref | released_ip |
| network-traffic | extensions.x-darktrace-device-details.outer_vlan_tag | outer_vlan |
| network-traffic | extensions.x-darktrace-device-details.vlan_tag | vlan |
| <br> | | |
| software | name | name |
| software | version | version |
| software | extensions.x-darktrace-software.software_type | software_type |
| software | extensions.x-darktrace-software.version_major | version_major |
| software | extensions.x-darktrace-software.version_minor | version_minor |
| software | extensions.x-darktrace-software.version_minor2 | version_minor2 |
| software | extensions.x-darktrace-software.version_minor3 | version_minor3 |
| software | extensions.x-darktrace-software.host_ref | host |
| software | extensions.x-darktrace-software.host_port | host_p |
| <br> | | |
| user-account | user_id | username |
| user-account | user_id | user |
| <br> | | |
| x-oca-asset | extensions.x-darktrace-connection.asset_id | id_hUUID |
| x-oca-asset | ip_refs | source_ip |
| x-oca-asset | ip_refs | dest_ip |
| x-oca-asset | mac_refs | mac |
| x-oca-asset | ip_refs | subnet_mask |
| x-oca-asset | ip_refs | released_ip |
| x-oca-asset | ip_refs | requested_ip |
| x-oca-asset | ip_refs | assigned_ip |
| x-oca-asset | ip_refs | tx_hosts |
| x-oca-asset | ip_refs | rx_hosts |
| x-oca-asset | ip_refs | host |
| x-oca-asset | ip_refs | ip |
| x-oca-asset | hostname | host |
| x-oca-asset | extensions.x-darktrace-endpoint.host_uuid | hUUID |
| <br> | | |
| x-oca-event | created | epochdate |
| x-oca-event | code | uid |
| x-oca-event | user_ref | username |
| x-oca-event | user_ref | user |
| x-oca-event | domain_ref | query |
| x-oca-event | domain_ref | domain_name |
| x-oca-event | file_ref | filename |
| x-oca-event | host_ref | host |
| <br> | | |
| x509-certificate | version | version |
| x509-certificate | extensions.x-darktrace-ssl.cipher_suite | cipher |
| x509-certificate | extensions.x-darktrace-ssl.cipher_list | client_ciphers |
| x509-certificate | extensions.x-darktrace-ssl.total_ciphers | total_client_ciphers |
| x509-certificate | extensions.x-darktrace-ssl.elliptic_curve | curve |
| x509-certificate | extensions.x-darktrace-ssl.server_name | server_name |
| x509-certificate | extensions.x-darktrace-ssl.is_resumed | resumed |
| x509-certificate | extensions.x-darktrace-ssl.last_alert | last_alert |
| x509-certificate | extensions.x-darktrace-ssl.next_protocol | next_protocol |
| x509-certificate | extensions.x-darktrace-ssl.is_established | established |
| x509-certificate | extensions.x-darktrace-ssl.is_client_hello_seen | client_hello_seen |
| x509-certificate | extensions.x-darktrace-ssl.cert_file_uids | cert_chain_fuids |
| x509-certificate | extensions.x-darktrace-ssl.cert_chainfile_uids | client_cert_chain_fuids |
| x509-certificate | subject | subject |
| x509-certificate | issuer | issuer |
| x509-certificate | subject | client_subject |
| x509-certificate | issuer | client_issuer |
| x509-certificate | extensions.x-darktrace-ssl.ocsp_status | ocsp_status |
| x509-certificate | extensions.x-darktrace-ssl.validation_status | validation_status |
| x509-certificate | extensions.x-darktrace-ssl.ja3_client_fingerprint | ja3_client_fingerprint |
| x509-certificate | extensions.x-darktrace-ssl.ja3s_server_fingerprint | ja3s_server_fingerprint |
| x509-certificate | extensions.x-darktrace-ssl.application_guess | application_guess |
| x509-certificate | version | certificate_version |
| x509-certificate | serial_number | certificate_serial |
| x509-certificate | signature_algorithm | certificate_sig_alg |
| x509-certificate | issuer | certificate_issuer |
| x509-certificate | validity_not_after | certificate_not_valid_before |
| x509-certificate | validity_not_before | certificate_not_valid_after |
| x509-certificate | subject | certificate_subject |
| x509-certificate | subject_public_key_algorithm | certificate_key_alg |
| x509-certificate | subject_public_key_exponent | certificate_exponent |
| x509-certificate | extensions.x509_v3_extensions.basic_constraints | basic_constraints |
| x509-certificate | extensions.x509_v3_extensions.subject_alternative_name | san |
| x509-certificate | extensions.x-darktrace-x509.certificate_key_type | certificate_key_type |
| x509-certificate | extensions.x-darktrace-x509.certificate_key_length | certificate_key_length |
| x509-certificate | extensions.x-darktrace-x509.certificate_curve | certificate_curve |
| x509-certificate | extensions.x-darktrace-x509.is_basic_constraints_ca | basic_constraints_ca |
| x509-certificate | extensions.x-darktrace-x509.basic_constraints_path_len | basic_constraints_path_len |
| x509-certificate | extensions.x-darktrace-x509.certificate_basic_info | certificate |
| x509-certificate | extensions.x-darktrace-x509.file_id | fid |
| <br> | | |
