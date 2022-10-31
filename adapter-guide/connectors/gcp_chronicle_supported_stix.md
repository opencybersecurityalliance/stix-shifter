##### Updated on 10/28/22
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
