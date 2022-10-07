##### Updated on 10/07/22
## GCP Chronicle 
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | or |
| OR | or |
| = | = |
| != | != |
| LIKE | = |
| MATCHES | = |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| IN | = |
| <br> | |
### Supported STIX Objects and Properties
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| autonomous-system | number | network.asn |
| <br> | | |
| directory | path | src.file.full_path |
| directory | path | target.file.full_path |
| directory | path | about.file.full_path |
| directory | path | src.process.file.full_path |
| directory | path | target.process.file.full_path |
| directory | path | principal.process.file.full_path |
| directory | path | target.process.parent_process.file.full_path |
| directory | path | principal.process.parent_process.file.full_path |
| <br> | | |
| domain-name | value | src.domain.name |
| domain-name | value | target.domain.name |
| domain-name | value | principal.domain.name |
| domain-name | value | network.dns_domain |
| domain-name | extensions.x-gcp-chronicle-domain.status | src.domain.status |
| domain-name | extensions.x-gcp-chronicle-domain.status | target.domain.status |
| domain-name | extensions.x-gcp-chronicle-domain.status | principal.domain.status |
| <br> | | |
| email-addr | value | principal.user.email_addresses |
| email-addr | value | src.user.email_addresses |
| email-addr | value | target.user.email_addresses |
| email-addr | value | network.email.from |
| email-addr | value | network.email.to |
| email-addr | value | network.email.cc |
| email-addr | value | network.email.bcc |
| email-addr | value | security_result.about.email |
| <br> | | |
| email-message | subject | network.email.subject |
| email-message | to_refs | network.email.to |
| email-message | from_ref | network.email.from |
| email-message | cc_refs | network.email.cc |
| email-message | bcc_refs | network.email.bcc |
| email-message | extensions.x-gcp-chronicle-email-message.file_ref | about.file.full_path |
| <br> | | |
| file | name | src.file.full_path |
| file | name | target.file.full_path |
| file | name | src.process.file.full_path |
| file | name | target.process.file.full_path |
| file | name | principal.process.file.full_path |
| file | name | target.process.parent_process.file.full_path |
| file | name | principal.process.parent_process.file.full_path |
| file | name | about.file.full_path |
| file | size | src.file.size |
| file | size | target.file.size |
| file | size | src.process.file.size |
| file | size | target.process.file.size |
| file | size | principal.process.file.size |
| file | size | about.file.size |
| file | hashes.MD5 | src.file.md5 |
| file | hashes.MD5 | target.file.md5 |
| file | hashes.MD5 | src.process.file.md5 |
| file | hashes.MD5 | target.process.file.md5 |
| file | hashes.MD5 | principal.process.file.md5 |
| file | hashes.MD5 | about.file.md5 |
| file | hashes.SHA-1 | src.file.sha1 |
| file | hashes.SHA-1 | target.file.sha1 |
| file | hashes.SHA-1 | src.process.file.sha1 |
| file | hashes.SHA-1 | target.process.file.sha1 |
| file | hashes.SHA-1 | principal.process.file.sha1 |
| file | hashes.SHA-1 | about.file.sha1 |
| file | hashes.SHA-256 | src.file.sha256 |
| file | hashes.SHA-256 | target.file.sha256 |
| file | hashes.SHA-256 | src.process.file.sha256 |
| file | hashes.SHA-256 | target.process.file.sha256 |
| file | hashes.SHA-256 | principal.process.file.sha256 |
| file | hashes.SHA-256 | about.file.sha256 |
| file | modified | src.file.last_modification_time.seconds |
| file | modified | target.file.last_modification_time.seconds |
| file | modified | src.process.file.last_modification_time.seconds |
| file | modified | target.process.file.last_modification_time.seconds |
| file | modified | principal.process.file.last_modification_time.seconds |
| file | modified | about.file.last_modification_time.seconds |
| file | parent_directory_ref | src.file.full_path |
| file | parent_directory_ref | target.file.full_path |
| file | parent_directory_ref | src.process.file.full_path |
| file | parent_directory_ref | target.process.file.full_path |
| file | parent_directory_ref | principal.process.file.full_path |
| file | parent_directory_ref | target.process.parent_process.file.full_path |
| file | parent_directory_ref | principal.process.parent_process.file.full_path |
| file | parent_directory_ref | about.file.full_path |
| file | extensions.x-gcp-chronicle-file.mime_type | src.file.mime_type |
| file | extensions.x-gcp-chronicle-file.mime_type | target.file.mime_type |
| file | extensions.x-gcp-chronicle-file.mime_type | src.process.file.mime_type |
| file | extensions.x-gcp-chronicle-file.mime_type | target.process.file.mime_type |
| file | extensions.x-gcp-chronicle-file.mime_type | principal.process.file.mime_type |
| file | extensions.x-gcp-chronicle-file.mime_type | about.file.mime_type |
| file | extensions.x-gcp-chronicle-file.file_type | src.file.file_type |
| file | extensions.x-gcp-chronicle-file.file_type | target.file.file_type |
| file | extensions.x-gcp-chronicle-file.file_type | src.process.file.file_type |
| file | extensions.x-gcp-chronicle-file.file_type | target.process.file.file_type |
| file | extensions.x-gcp-chronicle-file.file_type | principal.process.file.file_type |
| file | extensions.x-gcp-chronicle-file.file_type | about.file.file_type |
| <br> | | |
| ipv4-addr | value | src.ip |
| ipv4-addr | value | target.ip |
| ipv4-addr | value | principal.ip |
| ipv4-addr | resolves_to_refs | src.mac |
| ipv4-addr | resolves_to_refs | target.mac |
| ipv4-addr | resolves_to_refs | principal.mac |
| <br> | | |
| ipv6-addr | value | src.ip |
| ipv6-addr | value | target.ip |
| ipv6-addr | value | principal.ip |
| ipv6-addr | resolves_to_refs | src.mac |
| ipv6-addr | resolves_to_refs | target.mac |
| ipv6-addr | resolves_to_refs | principal.mac |
| <br> | | |
| mac-addr | value | src.mac |
| mac-addr | value | target.mac |
| mac-addr | value | principal.mac |
| <br> | | |
| network-traffic | src_port | src.port |
| network-traffic | src_port | principal.port |
| network-traffic | dst_port | target.port |
| network-traffic | protocols | network.ip_protocol |
| network-traffic | protocols | network.application_protocol |
| network-traffic | src_ref | src.ip |
| network-traffic | src_ref | principal.ip |
| network-traffic | dst_ref | target.ip |
| network-traffic | src_byte_count | network.sent_bytes |
| network-traffic | dst_byte_count | network.received_bytes |
| network-traffic | extensions.x-gcp-chronicle-network.session_duration | network.session_duration.seconds |
| network-traffic | extensions.x-gcp-chronicle-network.session_id | network.session_id |
| network-traffic | extensions.x-gcp-chronicle-network.direction | network.direction |
| network-traffic | extensions.ftp-ext.command | network.ftp.command |
| network-traffic | extensions.dns-ext.query_id | network.dns.id |
| network-traffic | extensions.dns-ext.opcode | network.dns.opcode |
| network-traffic | extensions.dns-ext.response_code | network.dns.response_code |
| network-traffic | extensions.dns-ext.query_class | network.dns.questions.class |
| network-traffic | extensions.dns-ext.query_type | network.dns.questions.type |
| network-traffic | extensions.dns-ext.questions_domain_name | network.dns.questions.name |
| network-traffic | extensions.dhcp-ext.client_hostname | network.dhcp.client_hostname |
| network-traffic | extensions.dhcp-ext.opcode | network.dhcp.opcode |
| network-traffic | extensions.dhcp-ext.server_name | network.dhcp.sname |
| network-traffic | extensions.dhcp-ext.transaction_id | network.dhcp.transaction_id |
| network-traffic | extensions.dhcp-ext.message_type | network.dhcp.type |
| network-traffic | extensions.http-ext.request_method | network.http.method |
| network-traffic | extensions.http-ext.response_code | network.http.response_code |
| network-traffic | extensions.http-ext.user_agent | network.http.user_agent |
| network-traffic | extensions.smtp-ext.server_response | network.smtp.server_response |
| network-traffic | extensions.tls-ext.cipher | network.tls.cipher |
| network-traffic | extensions.tls-ext.version | network.tls.version |
| network-traffic | extensions.tls-ext.version_protocol | network.tls.version_protocol |
| network-traffic | extensions.tls-ext.elliptical_curve | network.tls.curve |
| network-traffic | extensions.tls-ext.next_protocol | network.tls.next_protocol |
| network-traffic | extensions.tls-ext.server_ja3_hash | network.tls.server.ja3s |
| network-traffic | extensions.tls-ext.client_ja3_hash | network.tls.client.ja3 |
| network-traffic | extensions.tls-ext.server_host_name | network.tls.client.server_name |
| network-traffic | extensions.tls-ext.server_certificate_ref | network.tls.server.certificate.subject |
| network-traffic | extensions.tls-ext.client_certificate_ref | network.tls.client.certificate.subject |
| <br> | | |
| process | command_line | src.process.command_line |
| process | command_line | target.process.command_line |
| process | command_line | principal.process.command_line |
| process | command_line | target.process.parent_process.command_line |
| process | command_line | principal.process.parent_process.command_line |
| process | name | src.process.file.full_path |
| process | name | target.process.file.full_path |
| process | name | principal.process.file.full_path |
| process | name | target.process.parent_process.file.full_path |
| process | name | principal.process.parent_process.file.full_path |
| process | pid | src.process.pid |
| process | pid | target.process.pid |
| process | pid | principal.process.pid |
| process | pid | target.process.parent_process.pid |
| process | pid | principal.process.parent_process.pid |
| process | parent_ref | target.process.parent_process.pid |
| process | parent_ref | principal.process.parent_process.pid |
| process | creator_user_ref | src.user.userid |
| process | creator_user_ref | target.user.userid |
| process | creator_user_ref | principal.user.userid |
| process | parent_ref | target.process.parent_process.file.full_path |
| process | parent_ref | principal.process.parent_process.file.full_path |
| process | binary_ref | src.process.file.full_path |
| process | binary_ref | target.process.file.full_path |
| process | binary_ref | principal.process.file.full_path |
| process | binary_ref | target.process.parent_process.file.full_path |
| process | binary_ref | principal.process.parent_process.file.full_path |
| process | binary_ref | src.process.file.md5 |
| process | binary_ref | target.process.file.md5 |
| process | binary_ref | principal.process.file.md5 |
| process | binary_ref | src.process.file.sha256 |
| process | binary_ref | target.process.file.sha256 |
| process | binary_ref | principal.process.file.sha256 |
| <br> | | |
| software | name | src.asset.software.name |
| software | name | target.asset.software.name |
| software | name | principal.asset.software.name |
| software | name | principal.asset.platform_software.platform |
| software | name | target.asset.platform_software.platform |
| software | name | src.asset.platform_software.platform |
| software | version | src.asset.software.version |
| software | version | target.asset.software.version |
| software | version | principal.asset.software.version |
| software | version | principal.asset.platform_software.platform_version |
| software | version | src.asset.platform_software.platform_version |
| software | version | target.asset.platform_software.platform_version |
| <br> | | |
| url | value | src.url |
| url | value | target.url |
| url | value | principal.url |
| url | value | network.http.referral_url |
| url | value | security_result.about.url |
| <br> | | |
| user-account | user_id | src.user.userid |
| user-account | user_id | target.user.userid |
| user-account | user_id | principal.user.userid |
| user-account | display_name | src.user.user_display_name |
| user-account | display_name | target.user.user_display_name |
| user-account | display_name | principal.user.user_display_name |
| user-account | extensions.x-gcp-chronicle-user.type | src.user.account_type |
| user-account | extensions.x-gcp-chronicle-user.type | target.user.account_type |
| user-account | extensions.x-gcp-chronicle-user.type | principal.user.account_type |
| user-account | extensions.windows-account-ext.sid | src.user.windows_sid |
| user-account | extensions.windows-account-ext.sid | target.user.windows_sid |
| user-account | extensions.windows-account-ext.sid | principal.user.windows_sid |
| <br> | | |
| windows-registry-key | key | src.registry.registry_key |
| windows-registry-key | key | target.registry.registry_key |
| windows-registry-key | values | src.registry.registry_value_data |
| windows-registry-key | values | target.registry.registry_value_data |
| <br> | | |
| x509-certificate | version | network.tls.client.certificate.version |
| x509-certificate | version | network.tls.server.certificate.version |
| x509-certificate | serial_number | network.tls.client.certificate.serial |
| x509-certificate | serial_number | network.tls.server.certificate.serial |
| x509-certificate | issuer | network.tls.client.certificate.issuer |
| x509-certificate | issuer | network.tls.server.certificate.issuer |
| x509-certificate | validity_not_before | network.tls.server.certificate.not_before.seconds |
| x509-certificate | validity_not_before | network.tls.client.certificate.not_before.seconds |
| x509-certificate | validity_not_after | network.tls.server.certificate.not_after.seconds |
| x509-certificate | validity_not_after | network.tls.client.certificate.not_after.seconds |
| x509-certificate | subject | network.tls.client.certificate.subject |
| x509-certificate | subject | network.tls.server.certificate.subject |
| x509-certificate | hashes.MD5 | network.tls.client.certificate.md5 |
| x509-certificate | hashes.MD5 | network.tls.server.certificate.md5 |
| x509-certificate | hashes.SHA-1 | network.tls.client.certificate.sha1 |
| x509-certificate | hashes.SHA-1  | network.tls.server.certificate.sha1 |
| x509-certificate | hashes.SHA-256  | network.tls.client.certificate.sha256 |
| x509-certificate | hashes.SHA-256  | network.tls.server.certificate.sha256 |
| <br> | | |
| x-ibm-finding | name | security_result.summary |
| x-ibm-finding | finding_type | security_result.category |
| x-ibm-finding | rule_names | security_result.rule_name |
| x-ibm-finding | severity | security_result.severity |
| x-ibm-finding | src_ip_ref | principal.ip |
| x-ibm-finding | dst_ip_ref | target.ip |
| x-ibm-finding | src_os_ref | principal.asset.platform_software.platform |
| x-ibm-finding | dst_os_ref | target.asset.platform_software.platform |
| x-ibm-finding | src_application_ref | principal.asset.software.name |
| x-ibm-finding | dst_application_ref | target.asset.software.name |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.url_ref | security_result.about.url |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.alert_state | security_result.alert_state |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.threat_id | security_result.threat_id |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.threat_status | security_result.threat_status |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.threat_name | security_result.threat_name |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.description | security_result.description |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.actions_taken | security_result.action |
| <br> | | |
| x-oca-event | action | metadata.event_type |
| x-oca-event | code | metadata.product_log_id |
| x-oca-event | created | metadata.event_timestamp.seconds |
| x-oca-event | agent | metadata.product_name |
| x-oca-event | provider | metadata.vendor_name |
| x-oca-event | outcome | metadata.product_event_type |
| x-oca-event | host_ref | principal.hostname |
| x-oca-event | url_ref | principal.url |
| x-oca-event | file_ref | principal.process.file.full_path |
| x-oca-event | process_ref | principal.process.file.full_path |
| x-oca-event | parent_process_ref | principal.process.parent_process.file.full_path |
| x-oca-event | domain_ref | principal.domain.name |
| x-oca-event | ip_refs | src.ip |
| x-oca-event | ip_refs | principal.ip |
| x-oca-event | ip_refs | target.ip |
| x-oca-event | network_ref | principal.port |
| x-oca-event | network_ref | target.port |
| x-oca-event | user_ref | principal.user.userid |
| x-oca-event | registry_ref | target.registry.registry_key |
| x-oca-event | cross_process_target_ref | target.process.file.full_path |
| x-oca-event | extensions.x-gcp-chronicle-event.src_location | principal.location.name |
| x-oca-event | extensions.x-gcp-chronicle-event.target_location | target.location.name |
| x-oca-event | extensions.x-gcp-chronicle-event.target_hostname | target.hostname |
| x-oca-event | extensions.x-gcp-chronicle-event.email_message_ref | network.email.from |
| x-oca-event | extensions.x-gcp-chronicle-event.src_appservice | principal.application |
| x-oca-event | extensions.x-gcp-chronicle-event.target_appservice | target.application |
| x-oca-event | extensions.x-gcp-chronicle-event.src_resource_ref | principal.resource.name |
| x-oca-event | extensions.x-gcp-chronicle-event.target_resource_ref | target.resource.name |
| x-oca-event | extensions.x-gcp-chronicle-event.description | metadata.description |
| <br> | | |
| x-oca-asset | hostname | principal.hostname |
| x-oca-asset | ip_refs | principal.ip |
| x-oca-asset | mac_refs | principal.mac |
| x-oca-asset | extensions.x-gcp-chronicle-asset.cloud_environment | principal.asset.attribute.cloud.environment |
| x-oca-asset | extensions.x-gcp-chronicle-asset.cloud_availability_zone | principal.asset.attribute.cloud.availability_zone |
| x-oca-asset | extensions.x-gcp-chronicle-asset.city | principal.location.city |
| x-oca-asset | extensions.x-gcp-chronicle-asset.country_or_region | principal.location.country_or_region |
| x-oca-asset | extensions.x-gcp-chronicle-asset.asset_id | principal.asset_id |
| x-oca-asset | extensions.x-gcp-chronicle-asset.category | principal.asset.category |
| x-oca-asset | extensions.x-gcp-chronicle-asset.type | principal.asset.type |
| x-oca-asset | extensions.x-gcp-chronicle-asset.hw_cpu_platform | principal.asset.hardware.cpu_platform |
| x-oca-asset | extensions.x-gcp-chronicle-asset.hw_manufacturer | principal.asset.hardware.manufacturer |
| x-oca-asset | extensions.x-gcp-chronicle-asset.hw_serial_number | principal.asset.hardware.serial_number |
| <br> | | |
| x-gcp-chronicle-resource | name | src.resource.name |
| x-gcp-chronicle-resource | name | target.resource.name |
| x-gcp-chronicle-resource | name | principal.resource.name |
| x-gcp-chronicle-resource | resource_type | src.resource.resource_type |
| x-gcp-chronicle-resource | resource_type | target.resource.resource_type |
| x-gcp-chronicle-resource | resource_type | principal.resource.resource_type |
| x-gcp-chronicle-resource | resource_subtype | src.resource.resource_subtype |
| x-gcp-chronicle-resource | resource_subtype | target.resource.resource_subtype |
| x-gcp-chronicle-resource | resource_subtype | principal.resource.resource_subtype |
| x-gcp-chronicle-resource | availability_zone | src.resource.attribute.cloud.availability_zone |
| x-gcp-chronicle-resource | availability_zone | target.resource.attribute.cloud.availability_zone |
| x-gcp-chronicle-resource | availability_zone | principal.resource.attribute.cloud.availability_zone |
| x-gcp-chronicle-resource | environment | src.resource.attribute.cloud.environment |
| x-gcp-chronicle-resource | environment | target.resource.attribute.cloud.environment |
| x-gcp-chronicle-resource | environment | principal.resource.attribute.cloud.environment |
| <br> | | |
