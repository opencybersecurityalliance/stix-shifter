##### Updated on 05/15/23
## GCP Chronicle
### Results STIX Domain Objects
* Identity
* Observed Data
<br>
### Supported STIX Operators
*Comparison AND/OR operators are inside the observation while observation AND/OR operators are between observations (square brackets).*

| STIX Operator | Data Source Operator |
|--|--|
| AND (Comparision) | and |
| OR (Comparision) | or |
| = | = |
| != | != |
| LIKE | = |
| MATCHES | = |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| IN | = |
| OR (Observation) | or |
| AND (Observation) | or |
| <br> | |
### Searchable STIX objects and properties
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | src.ip, target.ip, principal.ip |
| **ipv4-addr**:resolves_to_refs[*].value | src.mac, target.mac, principal.mac |
| **ipv6-addr**:value | src.ip, target.ip, principal.ip |
| **ipv6-addr**:resolves_to_refs[*].value | src.mac, target.mac, principal.mac |
| **url**:value | src.url, target.url, principal.url, network.http.referral_url, security_result.about.url |
| **network-traffic**:src_port | src.port, principal.port |
| **network-traffic**:dst_port | target.port |
| **network-traffic**:protocols[*] | network.ip_protocol, network.application_protocol |
| **network-traffic**:src_ref.value | src.ip, principal.ip |
| **network-traffic**:dst_ref.value | target.ip |
| **network-traffic**:src_byte_count | network.sent_bytes |
| **network-traffic**:dst_byte_count | network.received_bytes |
| **network-traffic**:extensions.'x-gcp-chronicle-network'.session_duration | network.session_duration.seconds |
| **network-traffic**:extensions.'x-gcp-chronicle-network'.session_id | network.session_id |
| **network-traffic**:extensions.'x-gcp-chronicle-network'.direction | network.direction |
| **network-traffic**:extensions.'ftp-ext'.command | network.ftp.command |
| **network-traffic**:extensions.'dns-ext'.query_id | network.dns.id |
| **network-traffic**:extensions.'dns-ext'.opcode | network.dns.opcode |
| **network-traffic**:extensions.'dns-ext'.response_code | network.dns.response_code |
| **network-traffic**:extensions.'dns-ext'.query_class | network.dns.questions.class |
| **network-traffic**:extensions.'dns-ext'.query_type | network.dns.questions.type |
| **network-traffic**:extensions.'dns-ext'.questions_domain_name | network.dns.questions.name |
| **network-traffic**:extensions.'dhcp-ext'.client_hostname | network.dhcp.client_hostname |
| **network-traffic**:extensions.'dhcp-ext'.opcode | network.dhcp.opcode |
| **network-traffic**:extensions.'dhcp-ext'.server_name | network.dhcp.sname |
| **network-traffic**:extensions.'dhcp-ext'.transaction_id | network.dhcp.transaction_id |
| **network-traffic**:extensions.'dhcp-ext'.message_type | network.dhcp.type |
| **network-traffic**:extensions.'http-ext'.request_method | network.http.method |
| **network-traffic**:extensions.'http-ext'.response_code | network.http.response_code |
| **network-traffic**:extensions.'http-ext'.user_agent | network.http.user_agent |
| **network-traffic**:extensions.'smtp-ext'.server_response[*] | network.smtp.server_response |
| **network-traffic**:extensions.'tls-ext'.cipher | network.tls.cipher |
| **network-traffic**:extensions.'tls-ext'.version | network.tls.version |
| **network-traffic**:extensions.'tls-ext'.version_protocol | network.tls.version_protocol |
| **network-traffic**:extensions.'tls-ext'.elliptical_curve | network.tls.curve |
| **network-traffic**:extensions.'tls-ext'.next_protocol | network.tls.next_protocol |
| **network-traffic**:extensions.'tls-ext'.server_ja3_hash | network.tls.server.ja3s |
| **network-traffic**:extensions.'tls-ext'.client_ja3_hash | network.tls.client.ja3 |
| **network-traffic**:extensions.'tls-ext'.server_host_name | network.tls.client.server_name |
| **network-traffic**:extensions.'tls-ext'.server_certificate_ref.subject | network.tls.server.certificate.subject |
| **network-traffic**:extensions.'tls-ext'.client_certificate_ref.subject | network.tls.client.certificate.subject |
| **mac-addr**:value | src.mac, target.mac, principal.mac |
| **autonomous-system**:number | network.asn |
| **domain-name**:value | src.domain.name, target.domain.name, principal.domain.name, network.dns_domain |
| **domain-name**:extensions.'x-gcp-chronicle-domain'.status | src.domain.status, target.domain.status, principal.domain.status |
| **email-addr**:value | principal.user.email_addresses, src.user.email_addresses, target.user.email_addresses, network.email.from, network.email.to, network.email.cc, network.email.bcc, security_result.about.email |
| **email-message**:subject | network.email.subject |
| **email-message**:to_refs[*] | network.email.to |
| **email-message**:from_ref | network.email.from |
| **email-message**:cc_refs[*] | network.email.cc |
| **email-message**:bcc_refs[*] | network.email.bcc |
| **email-message**:extensions.'x-gcp-chronicle-email-message'.file_ref.name | about.file.full_path |
| **user-account**:user_id | src.user.userid, target.user.userid, principal.user.userid |
| **user-account**:display_name | src.user.user_display_name, target.user.user_display_name, principal.user.user_display_name |
| **user-account**:extensions.'x-gcp-chronicle-user'.type | src.user.account_type, target.user.account_type, principal.user.account_type |
| **user-account**:extensions.'windows-account-ext'.sid | src.user.windows_sid, target.user.windows_sid, principal.user.windows_sid |
| **file**:name | src.file.full_path, target.file.full_path, src.process.file.full_path, target.process.file.full_path, principal.process.file.full_path, target.process.parent_process.file.full_path, principal.process.parent_process.file.full_path, about.file.full_path |
| **file**:size | src.file.size, target.file.size, src.process.file.size, target.process.file.size, principal.process.file.size, about.file.size |
| **file**:hashes.MD5 | src.file.md5, target.file.md5, src.process.file.md5, target.process.file.md5, principal.process.file.md5, about.file.md5 |
| **file**:hashes.'SHA-1' | src.file.sha1, target.file.sha1, src.process.file.sha1, target.process.file.sha1, principal.process.file.sha1, about.file.sha1 |
| **file**:hashes.'SHA-256' | src.file.sha256, target.file.sha256, src.process.file.sha256, target.process.file.sha256, principal.process.file.sha256, about.file.sha256 |
| **file**:modified | src.file.last_modification_time.seconds, target.file.last_modification_time.seconds, src.process.file.last_modification_time.seconds, target.process.file.last_modification_time.seconds, principal.process.file.last_modification_time.seconds, about.file.last_modification_time.seconds |
| **file**:parent_directory_ref.path | src.file.full_path, target.file.full_path, src.process.file.full_path, target.process.file.full_path, principal.process.file.full_path, target.process.parent_process.file.full_path, principal.process.parent_process.file.full_path, about.file.full_path |
| **file**:extensions.'x-gcp-chronicle-file'.mime_type | src.file.mime_type, target.file.mime_type, src.process.file.mime_type, target.process.file.mime_type, principal.process.file.mime_type, about.file.mime_type |
| **file**:extensions.'x-gcp-chronicle-file'.file_type | src.file.file_type, target.file.file_type, src.process.file.file_type, target.process.file.file_type, principal.process.file.file_type, about.file.file_type |
| **directory**:path | src.file.full_path, target.file.full_path, about.file.full_path, src.process.file.full_path, target.process.file.full_path, principal.process.file.full_path, target.process.parent_process.file.full_path, principal.process.parent_process.file.full_path |
| **process**:command_line | src.process.command_line, target.process.command_line, principal.process.command_line, target.process.parent_process.command_line, principal.process.parent_process.command_line |
| **process**:name | src.process.file.full_path, target.process.file.full_path, principal.process.file.full_path, target.process.parent_process.file.full_path, principal.process.parent_process.file.full_path |
| **process**:pid | src.process.pid, target.process.pid, principal.process.pid, target.process.parent_process.pid, principal.process.parent_process.pid |
| **process**:parent_ref.pid | target.process.parent_process.pid, principal.process.parent_process.pid |
| **process**:creator_user_ref.user_id | src.user.userid, target.user.userid, principal.user.userid |
| **process**:parent_ref.name | target.process.parent_process.file.full_path, principal.process.parent_process.file.full_path |
| **process**:binary_ref.name | src.process.file.full_path, target.process.file.full_path, principal.process.file.full_path, target.process.parent_process.file.full_path, principal.process.parent_process.file.full_path |
| **process**:binary_ref.hashes.MD5 | src.process.file.md5, target.process.file.md5, principal.process.file.md5 |
| **process**:binary_ref.hashes.'SHA-256' | src.process.file.sha256, target.process.file.sha256, principal.process.file.sha256 |
| **process**:binary_ref.parent_directory_ref.path | src.process.file.full_path, target.process.file.full_path, principal.process.file.full_path |
| **software**:name | src.asset.software.name, target.asset.software.name, principal.asset.software.name, principal.asset.platform_software.platform, target.asset.platform_software.platform, src.asset.platform_software.platform |
| **software**:version | src.asset.software.version, target.asset.software.version, principal.asset.software.version, principal.asset.platform_software.platform_version, src.asset.platform_software.platform_version, target.asset.platform_software.platform_version |
| **windows-registry-key**:key | src.registry.registry_key, target.registry.registry_key |
| **windows-registry-key**:values[*] | src.registry.registry_value_data, target.registry.registry_value_data |
| **x509-certificate**:version | network.tls.client.certificate.version, network.tls.server.certificate.version |
| **x509-certificate**:serial_number | network.tls.client.certificate.serial, network.tls.server.certificate.serial |
| **x509-certificate**:issuer | network.tls.client.certificate.issuer, network.tls.server.certificate.issuer |
| **x509-certificate**:validity_not_before | network.tls.server.certificate.not_before.seconds, network.tls.client.certificate.not_before.seconds |
| **x509-certificate**:validity_not_after | network.tls.server.certificate.not_after.seconds, network.tls.client.certificate.not_after.seconds |
| **x509-certificate**:subject | network.tls.client.certificate.subject, network.tls.server.certificate.subject |
| **x509-certificate**:hashes.MD5 | network.tls.client.certificate.md5, network.tls.server.certificate.md5 |
| **x509-certificate**:hashes.'SHA-1' | network.tls.client.certificate.sha1, network.tls.server.certificate.sha1 |
| **x509-certificate**:hashes.'SHA-256' | network.tls.client.certificate.sha256, network.tls.server.certificate.sha256 |
| **x-ibm-finding**:name | security_result.summary |
| **x-ibm-finding**:finding_type | security_result.category |
| **x-ibm-finding**:rule_names[*] | security_result.rule_name |
| **x-ibm-finding**:severity | security_result.severity |
| **x-ibm-finding**:src_ip_ref.value | principal.ip |
| **x-ibm-finding**:dst_ip_ref.value | target.ip |
| **x-ibm-finding**:src_os_ref | principal.asset.platform_software.platform |
| **x-ibm-finding**:dst_os_ref | target.asset.platform_software.platform |
| **x-ibm-finding**:src_application_ref.name | principal.asset.software.name |
| **x-ibm-finding**:dst_application_ref.name | target.asset.software.name |
| **x-ibm-finding**:extensions.'x-gcp-chronicle-security-result'.url_ref.value | security_result.about.url |
| **x-ibm-finding**:extensions.'x-gcp-chronicle-security-result'.alert_state | security_result.alert_state |
| **x-ibm-finding**:extensions.'x-gcp-chronicle-security-result'.threat_id | security_result.threat_id |
| **x-ibm-finding**:extensions.'x-gcp-chronicle-security-result'.threat_status | security_result.threat_status |
| **x-ibm-finding**:extensions.'x-gcp-chronicle-security-result'.threat_name | security_result.threat_name |
| **x-ibm-finding**:extensions.'x-gcp-chronicle-security-result'.description | security_result.description |
| **x-ibm-finding**:extensions.'x-gcp-chronicle-security-result'.actions_taken[*] | security_result.action |
| **x-oca-event**:action | metadata.event_type |
| **x-oca-event**:code | metadata.product_log_id |
| **x-oca-event**:created | metadata.event_timestamp.seconds |
| **x-oca-event**:agent | metadata.product_name |
| **x-oca-event**:provider | metadata.vendor_name |
| **x-oca-event**:outcome | metadata.product_event_type |
| **x-oca-event**:host_ref.hostname | principal.hostname |
| **x-oca-event**:url_ref.value | principal.url |
| **x-oca-event**:file_ref.name | principal.process.file.full_path |
| **x-oca-event**:process_ref.name | principal.process.file.full_path |
| **x-oca-event**:parent_process_ref.name | principal.process.parent_process.file.full_path |
| **x-oca-event**:domain_ref.value | principal.domain.name |
| **x-oca-event**:ip_refs[*].value | src.ip, principal.ip, target.ip |
| **x-oca-event**:network_ref.src_port | principal.port |
| **x-oca-event**:network_ref.dst_port | target.port |
| **x-oca-event**:user_ref.user_id | principal.user.userid |
| **x-oca-event**:registry_ref.key | target.registry.registry_key |
| **x-oca-event**:cross_process_target_ref.name | target.process.file.full_path |
| **x-oca-event**:extensions.'x-gcp-chronicle-event'.src_location | principal.location.name |
| **x-oca-event**:extensions.'x-gcp-chronicle-event'.target_location | target.location.name |
| **x-oca-event**:extensions.'x-gcp-chronicle-event'.target_hostname | target.hostname |
| **x-oca-event**:extensions.'x-gcp-chronicle-event'.email_message_ref.value | network.email.from |
| **x-oca-event**:extensions.'x-gcp-chronicle-event'.src_appservice | principal.application |
| **x-oca-event**:extensions.'x-gcp-chronicle-event'.target_appservice | target.application |
| **x-oca-event**:extensions.'x-gcp-chronicle-event'.src_resource_ref.name | principal.resource.name |
| **x-oca-event**:extensions.'x-gcp-chronicle-event'.target_resource_ref.name | target.resource.name |
| **x-oca-event**:extensions.'x-gcp-chronicle-event'.description | metadata.description |
| **x-oca-asset**:hostname | principal.hostname |
| **x-oca-asset**:ip_refs[*].value | principal.ip |
| **x-oca-asset**:mac_refs[*].value | principal.mac |
| **x-oca-asset**:extensions.'x-gcp-chronicle-asset'.cloud_environment | principal.asset.attribute.cloud.environment |
| **x-oca-asset**:extensions.'x-gcp-chronicle-asset'.cloud_availability_zone | principal.asset.attribute.cloud.availability_zone |
| **x-oca-asset**:extensions.'x-gcp-chronicle-asset'.city | principal.location.city |
| **x-oca-asset**:extensions.'x-gcp-chronicle-asset'.country_or_region | principal.location.country_or_region |
| **x-oca-asset**:extensions.'x-gcp-chronicle-asset'.asset_id | principal.asset_id |
| **x-oca-asset**:extensions.'x-gcp-chronicle-asset'.category | principal.asset.category |
| **x-oca-asset**:extensions.'x-gcp-chronicle-asset'.type | principal.asset.type |
| **x-oca-asset**:extensions.'x-gcp-chronicle-asset'.hw_cpu_platform | principal.asset.hardware.cpu_platform |
| **x-oca-asset**:extensions.'x-gcp-chronicle-asset'.hw_manufacturer | principal.asset.hardware.manufacturer |
| **x-oca-asset**:extensions.'x-gcp-chronicle-asset'.hw_serial_number | principal.asset.hardware.serial_number |
| **x-gcp-chronicle-resource**:name | src.resource.name, target.resource.name, principal.resource.name |
| **x-gcp-chronicle-resource**:resource_type | src.resource.resource_type, target.resource.resource_type, principal.resource.resource_type |
| **x-gcp-chronicle-resource**:resource_subtype | src.resource.resource_subtype, target.resource.resource_subtype, principal.resource.resource_subtype |
| **x-gcp-chronicle-resource**:availability_zone | src.resource.attribute.cloud.availability_zone, target.resource.attribute.cloud.availability_zone, principal.resource.attribute.cloud.availability_zone |
| **x-gcp-chronicle-resource**:environment | src.resource.attribute.cloud.environment, target.resource.attribute.cloud.environment, principal.resource.attribute.cloud.environment |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| autonomous-system | number | asn |
| <br> | | |
| directory | path | fullPath |
| <br> | | |
| domain-name | value | name |
| domain-name | extensions.x-gcp-chronicle-domain.status | status |
| domain-name | value | dnsDomain |
| <br> | | |
| email-addr | value | emailAddresses |
| email-addr | value | from |
| email-addr | value | to |
| email-addr | value | cc |
| email-addr | value | bcc |
| email-addr | value | email |
| <br> | | |
| email-message | subject | subject |
| email-message | is_multipart | isMultipart |
| email-message | from_ref | from |
| email-message | to_refs | to |
| email-message | cc_refs | cc |
| email-message | bcc_refs | bcc |
| email-message | extensions.x-gcp-chronicle-email-message.file_ref | fullPath |
| <br> | | |
| file | name | fullPath |
| file | parent_directory_ref | fullPath |
| file | size | size |
| file | hashes.MD5 | md5 |
| file | hashes.SHA-1 | sha1 |
| file | hashes.SHA-256 | sha256 |
| file | modified | lastModificationTime |
| file | extensions.x-gcp-chronicle-file.mime_type | mimeType |
| file | extensions.x-gcp-chronicle-file.file_type | fileType |
| <br> | | |
| ipv4-addr | value | ip |
| ipv4-addr | resolves_to_refs | mac |
| <br> | | |
| ipv6-addr | value | ip |
| ipv6-addr | resolves_to_refs | mac |
| <br> | | |
| mac-addr | value | mac |
| <br> | | |
| network-traffic | src_ref | ip |
| network-traffic | src_port | port |
| network-traffic | dst_ref | ip |
| network-traffic | dst_port | port |
| network-traffic | protocols | ipProtocol |
| network-traffic | protocols | applicationProtocol |
| network-traffic | src_byte_count | sentBytes |
| network-traffic | dst_byte_count | receivedBytes |
| network-traffic | extensions.x-gcp-chronicle-network.session_duration | sessionDuration |
| network-traffic | extensions.x-gcp-chronicle-network.session_id | sessionId |
| network-traffic | extensions.x-gcp-chronicle-network.direction | direction |
| network-traffic | extensions.ftp-ext.command | command |
| network-traffic | extensions.dns-ext.query_id | id |
| network-traffic | extensions.dns-ext.opcode | opcode |
| network-traffic | extensions.dns-ext.response_code | responseCode |
| network-traffic | extensions.dns-ext.questions | questions |
| network-traffic | extensions.dhcp-ext.client_hostname | clientHostname |
| network-traffic | extensions.dhcp-ext.opcode | opcode |
| network-traffic | extensions.dhcp-ext.server_name | sname |
| network-traffic | extensions.dhcp-ext.transaction_id | transactionId |
| network-traffic | extensions.dhcp-ext.message_type | type |
| network-traffic | extensions.http-ext.request_method | method |
| network-traffic | extensions.http-ext.response_code | responseCode |
| network-traffic | extensions.http-ext.user_agent | userAgent |
| network-traffic | extensions.tls-ext.cipher | cipher |
| network-traffic | extensions.tls-ext.version | version |
| network-traffic | extensions.tls-ext.version_protocol | versionProtocol |
| network-traffic | extensions.tls-ext.elliptical_curve | curve |
| network-traffic | extensions.tls-ext.next_protocol | nextProtocol |
| network-traffic | extensions.tls-ext.server_ja3_hash | ja3s |
| network-traffic | extensions.tls-ext.server_certificate_ref | version |
| network-traffic | extensions.tls-ext.server_certificate_ref | serial |
| network-traffic | extensions.tls-ext.server_certificate_ref | issuer |
| network-traffic | extensions.tls-ext.server_certificate_ref | subject |
| network-traffic | extensions.tls-ext.client_ja3_hash | ja3 |
| network-traffic | extensions.tls-ext.server_host_name | serverName |
| network-traffic | extensions.tls-ext.client_certificate_ref | version |
| network-traffic | extensions.tls-ext.client_certificate_ref | serial |
| network-traffic | extensions.tls-ext.client_certificate_ref | issuer |
| network-traffic | extensions.tls-ext.client_certificate_ref | subject |
| network-traffic | extensions.smtp-ext.server_response | serverResponse |
| <br> | | |
| process | creator_user_ref | userid |
| process | name | fullPath |
| process | binary_ref | fullPath |
| process | binary_ref | md5 |
| process | binary_ref | sha256 |
| process | command_line | commandLine |
| process | parent_ref | fullPath |
| process | pid | pid |
| process | parent_ref | pid |
| <br> | | |
| software | name | platform |
| software | version | platformVersion |
| software | name | name |
| software | version | version |
| <br> | | |
| url | value | url |
| url | value | referralUrl |
| <br> | | |
| user-account | user_id | userid |
| user-account | display_name | userDisplayName |
| user-account | extensions.x-gcp-chronicle-user.type | accountType |
| user-account | extensions.windows-account-ext.sid | windowsSid |
| <br> | | |
| windows-registry-key | key | registryKey |
| windows-registry-key | values | registryValues |
| <br> | | |
| x-gcp-chronicle-resource | resource_type | resourceType |
| x-gcp-chronicle-resource | resource_subtype | resourceSubtype |
| x-gcp-chronicle-resource | name | name |
| x-gcp-chronicle-resource | availability_zone | availabilityZone |
| x-gcp-chronicle-resource | environment | environment |
| <br> | | |
| x-ibm-finding | src_ip_ref | ip |
| x-ibm-finding | src_os_ref | platform |
| x-ibm-finding | src_application_ref | name |
| x-ibm-finding | dst_ip_ref | ip |
| x-ibm-finding | dst_os_ref | platform |
| x-ibm-finding | dst_application_ref | name |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.url_ref | url |
| x-ibm-finding | finding_type | findingType |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.threat_name | threatName |
| x-ibm-finding | rule_names | ruleName |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.alert_state | alertState |
| x-ibm-finding | severity | severity |
| x-ibm-finding | finding_type | category |
| x-ibm-finding | name | summary |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.threat_id | threatId |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.threat_status | threatStatus |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.description | description |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.actions_taken | action |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.aws_detector_id | detectorId |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.aws_archived | archived |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.aws_count | count |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.aws_image_id | imageId |
| x-ibm-finding | extensions.x-gcp-chronicle-security-result.aws_resource_role | resourceRole |
| <br> | | |
| x-oca-asset | ip_refs | ip |
| x-oca-asset | mac_refs | mac |
| x-oca-asset | hostname | hostname |
| x-oca-asset | extensions.x-gcp-chronicle-asset.asset_id | assetId |
| x-oca-asset | extensions.x-gcp-chronicle-asset.city | city |
| x-oca-asset | extensions.x-gcp-chronicle-asset.country_or_region | countryOrRegion |
| x-oca-asset | extensions.x-gcp-chronicle-asset.category | category |
| x-oca-asset | extensions.x-gcp-chronicle-asset.type | type |
| x-oca-asset | extensions.x-gcp-chronicle-asset.hw_cpu_platform | cpuPlatform |
| x-oca-asset | extensions.x-gcp-chronicle-asset.hw_manufacturer | manufacturer |
| x-oca-asset | extensions.x-gcp-chronicle-asset.hw_serial_number | serialNumber |
| x-oca-asset | extensions.x-gcp-chronicle-asset.cloud_environment | environment |
| x-oca-asset | extensions.x-gcp-chronicle-asset.cloud_availability_zone | availabilityZone |
| <br> | | |
| x-oca-event | network_ref | ip |
| x-oca-event | ip_refs | ip |
| x-oca-event | network_ref | port |
| x-oca-event | url_ref | url |
| x-oca-event | domain_ref | name |
| x-oca-event | extensions.x-gcp-chronicle-event.src_appservice | application |
| x-oca-event | host_ref | hostname |
| x-oca-event | extensions.x-gcp-chronicle-event.src_location | name |
| x-oca-event | user_ref | userid |
| x-oca-event | file_ref | fullPath |
| x-oca-event | process_ref | fullPath |
| x-oca-event | parent_process_ref | fullPath |
| x-oca-event | extensions.x-gcp-chronicle-event-ext.src_resource_ref | name |
| x-oca-event | registry_ref | registryKey |
| x-oca-event | extensions.x-gcp-chronicle-event.target_appservice | application |
| x-oca-event | extensions.x-gcp-chronicle-event.target_hostname | hostname |
| x-oca-event | extensions.x-gcp-chronicle-event.target_location | name |
| x-oca-event | cross_process_target_ref | fullPath |
| x-oca-event | extensions.x-gcp-chronicle-event.target_resource_ref | name |
| x-oca-event | extensions.x-gcp-chronicle-event.email_message_ref | from |
| x-oca-event | action | eventType |
| x-oca-event | code | productLogId |
| x-oca-event | created | eventTimestamp |
| x-oca-event | extensions.x-gcp-chronicle-event.description | description |
| x-oca-event | agent | productName |
| x-oca-event | provider | vendorName |
| x-oca-event | outcome | productEventType |
| <br> | | |
| x509-certificate | version | version |
| x509-certificate | serial_number | serial |
| x509-certificate | issuer | issuer |
| x509-certificate | validity_not_before | notBefore |
| x509-certificate | validity_not_after | notAfter |
| x509-certificate | subject | subject |
| x509-certificate | hashes.MD5 | md5 |
| x509-certificate | hashes.SHA-1 | sha1 |
| x509-certificate | hashes.SHA-256 | sha256 |
| <br> | | |
