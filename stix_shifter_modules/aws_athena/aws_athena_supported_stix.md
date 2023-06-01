##### Updated on 05/15/23
## Amazon Athena
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
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| = | = |
| != | != |
| LIKE | LIKE |
| IN | IN |
| MATCHES | REGEXP_LIKE |
| OR (Observation) | UNION |
| AND (Observation) | INTERSECT |
| <br> | |
### Searchable STIX objects and properties for Guardduty dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | eth0_private_ip, eth1_private_ip, public_ip, remote_ip |
| **ipv4-addr**:x_aws_interface_id | interface_id |
| **ipv4-addr**:x_aws_remote_city_name | city_name |
| **ipv4-addr**:x_aws_remote_country_name | country_name |
| **ipv6-addr**:value | ipv6_address |
| **ipv6-addr**:x_aws_interface_id | interface_id |
| **network-traffic**:src_port | local_port |
| **network-traffic**:dst_port | remote_port |
| **network-traffic**:src_ref.value | eth0_private_ip |
| **network-traffic**:dst_ref.value | remote_ip |
| **network-traffic**:protocols[*] | protocol |
| **domain-name**:value | eth0_private_dns_name, eth1_private_dns_name, public_dns_name, dns_domain |
| **user-account**:user_id | principal_id |
| **user-account**:account_login | user_name |
| **x-aws-details**:account_id | accountid |
| **x-aws-details**:region | region |
| **x-aws-instance**:instance_id | instance_id |
| **x-aws-instance**:image_id | image_id |
| **x-aws-instance**:availability_zone | availability_zone |
| **x-aws-vpc**:vpc_id | vpc_id |
| **x-aws-vpc**:subnet_id | subnet_id |
| **x-aws-vpc**:security_group_name | security_group_name |
| **x-aws-vpc**:security_group_id | security_group_id |
| **x-aws-api**:access_key_id | access_key_id |
| **x-aws-api**:api | api |
| **x-aws-api**:api_service_name | api_service_name |
| **x-ibm-finding**:name | title |
| **x-ibm-finding**:finding_type | type |
| **x-ibm-finding**:description | description |
| **x-ibm-finding**:src_ip_ref.value | eth0_private_ip |
| **x-ibm-finding**:dst_ip_ref.value | remote_ip |
| **x-ibm-finding**:start | event_firstseen |
| **x-ibm-finding**:end | event_lastseen |
| **x-ibm-finding**:src_os_ref.value | platform |
| **x-ibm-finding**:dst_geolocation | country_name |
| <br> | |
### Searchable STIX objects and properties for Ocsf dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **email-addr**:value | identity.user.email_addr |
| **file**:accessed | file.accessed_time |
| **file**:created | file.created_time |
| **file**:extensions.'x-ocsf-file-ext'.algorithm | file.fingerprints.algorithm |
| **file**:extensions.'x-ocsf-file-ext'.algorithm_id | file.fingerprints.algorithm_id |
| **file**:extensions.'x-ocsf-file-ext'.algorithm_value | file.fingerprints.value |
| **file**:extensions.'x-ocsf-file-ext'.attributes | file.attributes |
| **file**:extensions.'x-ocsf-file-ext'.company_name | file.company_name |
| **file**:extensions.'x-ocsf-file-ext'.confidentiality | file.confidentiality |
| **file**:extensions.'x-ocsf-file-ext'.confidentiality_id | file.confidentiality_id |
| **file**:extensions.'x-ocsf-file-ext'.description | file.desc |
| **file**:extensions.'x-ocsf-file-ext'.feature_name | file.product.feature.name |
| **file**:extensions.'x-ocsf-file-ext'.feature_uid | file.product.feature.uid |
| **file**:extensions.'x-ocsf-file-ext'.feature_version | file.product.feature.version |
| **file**:extensions.'x-ocsf-file-ext'.installed_path | file.product.path |
| **file**:extensions.'x-ocsf-file-ext'.product_lang | file.product.lang |
| **file**:extensions.'x-ocsf-file-ext'.product_name | file.product.name |
| **file**:extensions.'x-ocsf-file-ext'.product_uid | file.product.uid |
| **file**:extensions.'x-ocsf-file-ext'.product_vendor | file.product.vendor_name |
| **file**:extensions.'x-ocsf-file-ext'.product_version | file.product.version |
| **file**:extensions.'x-ocsf-file-ext'.security_descriptor | file.security_descriptor |
| **file**:extensions.'x-ocsf-file-ext'.signature | file.signature |
| **file**:extensions.'x-ocsf-file-ext'.type | file.type |
| **file**:extensions.'x-ocsf-file-ext'.type_id | file.type_id |
| **file**:extensions.'x-ocsf-file-ext'.uid | file.uid |
| **file**:extensions.'x-ocsf-file-ext'.version | file.version |
| **file**:name | file.name |
| **file**:size | file.size |
| **ipv4-addr**:value | dst_endpoint.ip, src_endpoint.ip |
| **ipv6-addr**:value | dst_endpoint.ip, src_endpoint.ip |
| **network-traffic**:dst_byte_count | traffic.bytes_in |
| **network-traffic**:dst_packets | traffic.packets_in |
| **network-traffic**:dst_port | dst_endpoint.port |
| **network-traffic**:dst_ref.value | dst_endpoint.ip |
| **network-traffic**:extensions.'x-network-ext'.boundary | connection_info.boundary |
| **network-traffic**:extensions.'x-network-ext'.boundary_id | connection_info.boundary_id |
| **network-traffic**:extensions.'x-network-ext'.bytes | traffic.bytes |
| **network-traffic**:extensions.'x-network-ext'.direction | connection_info.direction |
| **network-traffic**:extensions.'x-network-ext'.direction_id | connection_info.direction_id |
| **network-traffic**:extensions.'x-network-ext'.packets | traffic.packets |
| **network-traffic**:extensions.'x-network-ext'.protocol_ver | connection_info.protocol_ver |
| **network-traffic**:extensions.'tcp-ext'.src_flags_hex | connection_info.tcp_flags |
| **network-traffic**:protocols[*] | connection_info.protocol_num, connection_info.protocol_ver_id |
| **network-traffic**:src_byte_count | traffic.bytes_out |
| **network-traffic**:src_packets | traffic.packets_out |
| **network-traffic**:src_port | src_endpoint.port |
| **network-traffic**:src_ref.value | src_endpoint.ip |
| **process**:binary_ref.name | file.name |
| **process**:command_line | process.cmd_line |
| **process**:created | process.created_time |
| **process**:extensions.'x-ocsf-process-ext'.integrity | process.integrity |
| **process**:extensions.'x-ocsf-process-ext'.integrity_id | process.integrity_id |
| **process**:extensions.'x-ocsf-process-ext'.is_system | process.is_system |
| **process**:extensions.'x-ocsf-process-ext'.lineage | process.lineage |
| **process**:extensions.'x-ocsf-process-ext'.loaded_modules | process.sandbox |
| **process**:extensions.'x-ocsf-process-ext'.terminated_time | terminated_time |
| **process**:extensions.'x-ocsf-process-ext'.tid | process.tid |
| **process**:x_unique_id | process.uid |
| **process**:extensions.'x-ocsf-process-ext'.xattributes | process.xattributes |
| **process**:mime_type | mime_type |
| **process**:extensions.'x-ocsf-process-ext'.modified_time | process.modified_time |
| **process**:name | process.name |
| **process**:pid | process.pid |
| **software**:extension.product.feature_name | metadata.product.feature.name |
| **software**:extension.product.feature_uid | metadata.product.feature.uid |
| **software**:extension.product.feature_version | metadata.product.feature.version |
| **software**:extension.product.path | metadata.product.path |
| **software**:extension.product.uid | metadata.product.uid |
| **software**:languages | metadata.product.lang |
| **software**:name | metadata.product.name |
| **software**:vendor | metadata.product.vendor_name |
| **software**:version | metadata.product.version |
| **url**:value | http_request.url |
| **user-account**:account_type | identity.user.account_type |
| **user-account**:display_name | identity.user.name |
| **user-account**:extensions.'aws-account-ext'.account_type_id | identity.user.account_type_id |
| **user-account**:extensions.'aws-account-ext'.credential_uid | identity.user.credential_uid |
| **user-account**:extensions.'aws-account-ext'.domain | identity.user.domain |
| **user-account**:extensions.'aws-account-ext'.group_desc | identity.user.groups.desc |
| **user-account**:extensions.'aws-account-ext'.group_name | identity.user.groups.name |
| **user-account**:extensions.'aws-account-ext'.group_privileges | identity.user.groups.privileges |
| **user-account**:extensions.'aws-account-ext'.group_type | identity.user.groups.type |
| **user-account**:extensions.'aws-account-ext'.group_uid | identity.user.groups.uid |
| **user-account**:extensions.'aws-account-ext'.org_uid | identity.user.org_uid |
| **user-account**:extensions.'aws-account-ext'.session_uid | identity.user.session_uid |
| **user-account**:extensions.'aws-account-ext'.session_uuid | identity.user.session_uuid |
| **user-account**:extensions.'aws-account-ext'.type | identity.user.type |
| **user-account**:extensions.'aws-account-ext'.type_id | identity.user.type_id |
| **user-account**:extensions.'aws-account-ext'.uid | identity.user.uid |
| **user-account**:extensions.'aws-account-ext'.uuid | identity.user.uuid |
| **user-account**:user_id | identity.user.account_uid |
| **x-ibm-finding**:alert_id | observables.type_id, finding.uid |
| **x-ibm-finding**:description | observables.value |
| **x-ibm-finding**:dst_ip_ref.value | dst_endpoint.ip |
| **x-ibm-finding**:end | end_time |
| **x-ibm-finding**:event_count | count |
| **x-ibm-finding**:finding_type | observables.type |
| **x-ibm-finding**:name | observables.name, finding.title |
| **x-ibm-finding**:types | finding.types |
| **x-ibm-finding**:severity | severity_id |
| **x-ibm-finding**:src_ip_ref.value | src_endpoint.ip |
| **x-ibm-finding**:start | finding.created_time |
| **x-ibm-finding**:time_observed | finding.first_seen_time |
| **x-oca-asset**:extensions.'x-dst-endpoint'.instance_uid | dst_endpoint.instance_uid |
| **x-oca-asset**:extensions.'x-dst-endpoint'.interface_uid | dst_endpoint.interface_uid |
| **x-oca-asset**:extensions.'x-dst-endpoint'.subnet_uid | dst_endpoint.subnet_uid |
| **x-oca-asset**:extensions.'x-dst-endpoint'.svc_name | dst_endpoint.svc_name |
| **x-oca-asset**:extensions.'x-dst-endpoint'.vpc_uid | dst_endpoint.vpc_uid |
| **x-oca-asset**:extensions.'x-src-endpoint'.instance_uid | src_endpoint.instance_uid |
| **x-oca-asset**:extensions.'x-src-endpoint'.interface_uid | src_endpoint.interface_uid |
| **x-oca-asset**:extensions.'x-src-endpoint'.subnet_uid | src_endpoint.subnet_uid |
| **x-oca-asset**:extensions.'x-src-endpoint'.svc_name | src_endpoint.svc_name |
| **x-oca-asset**:extensions.'x-src-endpoint'.vpc_uid | src_endpoint.vpc_uid |
| **x-oca-asset**:name | dst_endpoint.name, src_endpoint.name |
| **x-oca-event**:action | activity, activity_name |
| **x-oca-event**:category | category_name |
| **x-oca-event**:code | activity_id, category_uid |
| **x-oca-event**:confidence | confidence |
| **x-oca-event**:created | time |
| **x-oca-event**:duration | duration |
| **x-oca-event**:extensions.'x-cloud-api'.class_uid | class_uid |
| **x-oca-event**:module | class_name |
| **x-oca-event**:network_ref.dst_ref.value | dst_endpoint.ip |
| **x-oca-event**:network_ref.src_ref.value | dst_endpoint.ip |
| **x-oca-event**:timezone | timezone_offset |
| **x-ocsf-cloud**:account_type | cloud.account_type |
| **x-ocsf-cloud**:account_type_id | cloud.account_type_id |
| **x-ocsf-cloud**:account_uid | cloud.account_uid |
| **x-ocsf-cloud**:api_version | api.version |
| **x-ocsf-cloud**:message | message |
| **x-ocsf-cloud**:operation | api.operation |
| **x-ocsf-cloud**:org_uid | cloud.org_uid |
| **x-ocsf-cloud**:profiles | profiles |
| **x-ocsf-cloud**:project_uid | cloud.project_uid |
| **x-ocsf-cloud**:provider | cloud.provider |
| **x-ocsf-cloud**:raw_data | raw_data |
| **x-ocsf-cloud**:ref_event_code | ref_event_code |
| **x-ocsf-cloud**:ref_event_name | ref_event_name |
| **x-ocsf-cloud**:ref_event_uid | ref_event_uid |
| **x-ocsf-cloud**:ref_time | ref_time |
| **x-ocsf-cloud**:region | cloud.region |
| **x-ocsf-cloud**:request_flags | api.request.flags |
| **x-ocsf-cloud**:request_uid | api.request.uid |
| **x-ocsf-cloud**:resource_uid | cloud.resource_uid |
| **x-ocsf-cloud**:response_code | api.response.code |
| **x-ocsf-cloud**:response_error | api.response.error |
| **x-ocsf-cloud**:response_error_message | api.response.error_message |
| **x-ocsf-cloud**:response_flags | api.response.flags |
| **x-ocsf-cloud**:response_message | api.response.message |
| **x-ocsf-cloud**:service_labels | api.service.labels |
| **x-ocsf-cloud**:service_name | api.service.name |
| **x-ocsf-cloud**:service_uid | api.service.uid, api.service.version |
| **x-ocsf-cloud**:severity | severity |
| **x-ocsf-cloud**:status | status |
| **x-ocsf-cloud**:status_code | status_code |
| **x-ocsf-cloud**:status_detail | status_detail |
| **x-ocsf-cloud**:status_id | status_id |
| **x-ocsf-cloud**:type_name | type_name |
| **x-ocsf-cloud**:type_uid | type_uid |
| **x-ocsf-cloud**:zone | cloud.zone |
| **x-ibm-ttp-tagging**:name | attack.technique.name |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.tactic_name | attack.tactics.name |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.tactic_id | attack.tactics.uid |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.technique_id | attack.technique.uid |
| **x-ibm-ttp-tagging**:extensions.'mitre-attack-ext'.version | attack.version |
| **x-ocsf-compliance**:requirements | compliance.requirements |
| **x-ocsf-compliance**:status | compliance.status |
| **x-ocsf-compliance**:status_detail | compliance.status_detail |
| **x-ocsf-enrichments**:data | enrichments.data |
| **x-ocsf-enrichments**:name | enrichments.name |
| **x-ocsf-enrichments**:provider | enrichments.provider |
| **x-ocsf-enrichments**:type | enrichments.type |
| **x-ocsf-enrichments**:value | enrichments.value |
| **x-ocsf-http-request**:http_headers_name | http_request.http_headers.name |
| **x-ocsf-http-request**:http_headers_value | http_request.http_headers.value |
| **x-ocsf-http-request**:http_method | http_request.http_method |
| **x-ocsf-http-request**:prefix | http_request.prefix |
| **x-ocsf-http-request**:referrer | http_request.referrer |
| **x-ocsf-http-request**:uid | http_request.uid |
| **x-ocsf-http-request**:user_agent | http_request.user_agent |
| **x-ocsf-http-request**:value | http_request.args |
| **x-ocsf-http-request**:version | http_request.version |
| **x-ocsf-http-request**:x_forwarded_for | http_request.x_forwarded_for |
| **x-ocsf-identity**:authorizations.decision | identity.authorizations.decision |
| **x-ocsf-identity**:authorizations.name | identity.authorizations.policy.name |
| **x-ocsf-identity**:authorizations.policy_desc | identity.authorizations.policy.desc |
| **x-ocsf-identity**:authorizations.policy_group_desc | identity.authorizations.policy.group.desc |
| **x-ocsf-identity**:authorizations.policy_group_namee | identity.authorizations.policy.group.name |
| **x-ocsf-identity**:authorizations.policy_group_privileges | identity.authorizations.policy.group.privileges |
| **x-ocsf-identity**:authorizations.policy_group_type | identity.authorizations.policy.group.type |
| **x-ocsf-identity**:authorizations.policy_group_uid | identity.authorizations.policy.group.uid |
| **x-ocsf-identity**:authorizations.uid | identity.authorizations.policy.uid |
| **x-ocsf-identity**:authorizations.version | identity.authorizations.policy.version |
| **x-ocsf-identity**:idp.name | identity.idp.name |
| **x-ocsf-identity**:idp.uid | identity.idp.uid |
| **x-ocsf-identity**:invoked_by | identity.invoked_by |
| **x-ocsf-identity**:message | identity.message |
| **x-ocsf-identity**:session.created_time | identity.session.created_time |
| **x-ocsf-identity**:session.credential_uid | identity.session.credential_uid |
| **x-ocsf-identity**:session.expiration_time | identity.session.expiration_time |
| **x-ocsf-identity**:session.issuer | identity.session.issuer |
| **x-ocsf-identity**:session.mfa | identity.session.mfa |
| **x-ocsf-identity**:session.uid | identity.session.uid |
| **x-ocsf-malware**:base_score | malware.cves.cvss.base_score |
| **x-ocsf-malware**:classification_ids | malware.classification_ids |
| **x-ocsf-malware**:classifications | malware.classifications |
| **x-ocsf-malware**:created_time | malware.cves.created_time |
| **x-ocsf-malware**:cwe_uid | malware.cves.cwe_uid |
| **x-ocsf-malware**:cwe_url | malware.cves.cwe_url |
| **x-ocsf-malware**:depth | malware.cves.cvss.depth |
| **x-ocsf-malware**:lang | malware.cves.product.lang |
| **x-ocsf-malware**:modified_time | malware.cves.modified_time |
| **x-ocsf-malware**:name | malware.name |
| **x-ocsf-malware**:overall_score | malware.cves.cvss.overall_score |
| **x-ocsf-malware**:path | malware.path |
| **x-ocsf-malware**:provider | malware.provider |
| **x-ocsf-malware**:severity | malware.cves.cvss.severity |
| **x-ocsf-malware**:type | malware.cves.type |
| **x-ocsf-malware**:uid | malware.uid |
| **x-ocsf-malware**:value | malware.cves.product.value |
| **x-ocsf-malware**:vector_string | malware.cves.cvss.vector_string |
| **x-ocsf-malware**:vendor_name | malware.cves.product.vendor_name |
| **x-ocsf-malware**:version | malware.cves.cvss.version |
| **x-ocsf-metadata**:correlation_uid | metadata.correlation_uid |
| **x-ocsf-metadata**:labels | metadata.labels |
| **x-ocsf-metadata**:logged_time | metadata.logged_time |
| **x-ocsf-metadata**:modified_time | metadata.modified_time |
| **x-ocsf-metadata**:processed_time | metadata.processed_time |
| **x-ocsf-metadata**:sequence | metadata.sequence |
| **x-ocsf-metadata**:uid | metadata.uid |
| **x-ocsf-metadata**:version | metadata.version |
| **x-ocsf-resources**:account_uid | resources.account_uid |
| **x-ocsf-resources**:cloud_partition | resources.cloud_partition |
| **x-ocsf-resources**:criticality | resources.criticality |
| **x-ocsf-resources**:details | resources.details |
| **x-ocsf-resources**:group_name | resources.group_name |
| **x-ocsf-resources**:labels | resources.labels |
| **x-ocsf-resources**:name | resources.name |
| **x-ocsf-resources**:owner | resources.owner |
| **x-ocsf-resources**:region | resources.region |
| **x-ocsf-resources**:type | resources.type |
| **x-ocsf-resources**:uid | resources.uid |
| <br> | |
### Searchable STIX objects and properties for Vpcflow dialect
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **ipv4-addr**:value | sourceaddress, destinationaddress |
| **ipv4-addr**:x_aws_interface_id | interfaceId |
| **ipv6-addr**:value | sourceaddress, destinationaddress |
| **ipv6-addr**:x_aws_interface_id | interfaceid |
| **network-traffic**:src_port | sourceport |
| **network-traffic**:dst_port | destinationport |
| **network-traffic**:src_ref.value | sourceaddress |
| **network-traffic**:dst_ref.value | destinationaddress |
| **network-traffic**:protocols[*] | protocol |
| **network-traffic**:start | starttime |
| **network-traffic**:end | endtime |
| **x-aws-details**:account_id | account |
| **x-ibm-finding**:finding_type | action |
| **x-ibm-finding**:src_ip_ref.value | sourceaddress |
| **x-ibm-finding**:dst_ip_ref.value | destinationaddress |
| **x-ibm-finding**:start | starttime |
| **x-ibm-finding**:end | endtime |
| <br> | |
### Supported STIX Objects and Properties for Query Results
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| directory | path | parent_folder |
| <br> | | |
| domain-name | resolves_to_refs | resource_instancedetails_networkinterfaces_0_privateipaddress |
| domain-name | resolves_to_refs | resource_instancedetails_networkinterfaces_0_publicip |
| domain-name | value | resource_instancedetails_networkinterfaces_0_privatednsname |
| domain-name | value | resource_instancedetails_networkinterfaces_0_publicdnsname |
| domain-name | resolves_to_refs | resource_instancedetails_networkinterfaces_1_privateipaddress |
| domain-name | value | resource_instancedetails_networkinterfaces_1_privatednsname |
| domain-name | resolves_to_refs | portprobe_resource_instancedetails_networkinterfaces_0_privateipaddress |
| domain-name | resolves_to_refs | dnsrequest_resource_instancedetails_networkinterfaces_0_privateipaddress |
| domain-name | value | service_action_dnsrequestaction_domain |
| <br> | | |
| email-addr | value | email_addr |
| <br> | | |
| file | accessed | accessed_time |
| file | extensions.x-ocsf-file-ext.attributes | attributes |
| file | extensions.x-ocsf-file-ext.company_name | company_name |
| file | extensions.x-ocsf-file-ext.confidentiality | confidentiality |
| file | extensions.x-ocsf-file-ext.confidentiality_id | confidentiality_id |
| file | created | created_time |
| file | extensions.x-ocsf-file-ext.description | desc |
| file | hashes.Unknown | Unknown |
| file | hashes.MD5 | MD5 |
| file | hashes.SHA-1 | SHA-1 |
| file | hashes.SHA-256 | SHA-256 |
| file | hashes.SHA-512 | SHA-512 |
| file | hashes.CTPH | CTPH |
| file | hashes.Other | Other |
| file | name | name |
| file | parent_directory_ref | parent_folder |
| file | extensions.x-ocsf-file-ext.path | path |
| file | extensions.x-ocsf-file-ext.security_descriptor | security_descriptor |
| file | extensions.x-ocsf-file-ext.signature | signature |
| file | size | size |
| file | extensions.x-ocsf-file-ext.type | type |
| file | extensions.x-ocsf-file-ext.type_id | type_id |
| file | extensions.x-ocsf-file-ext.uid | uid |
| file | extensions.x-ocsf-file-ext.version | version |
| <br> | | |
| ipv4-addr | value | ip |
| ipv4-addr | value | intermediate_ips |
| ipv4-addr | value | sourceaddress |
| ipv4-addr | x_aws_interface_id | sourceaddress |
| ipv4-addr | value | destinationaddress |
| ipv4-addr | value | resource_instancedetails_networkinterfaces_0_privateipaddress |
| ipv4-addr | x_aws_interface_id | resource_instancedetails_networkinterfaces_0_privateipaddress |
| ipv4-addr | x_aws_ip_type | resource_instancedetails_networkinterfaces_0_privateipaddress |
| ipv4-addr | value | resource_instancedetails_networkinterfaces_0_publicip |
| ipv4-addr | x_aws_interface_id | resource_instancedetails_networkinterfaces_0_publicip |
| ipv4-addr | x_aws_ip_type | resource_instancedetails_networkinterfaces_0_publicip |
| ipv4-addr | value | resource_instancedetails_networkinterfaces_1_privateipaddress |
| ipv4-addr | x_aws_interface_id | resource_instancedetails_networkinterfaces_1_privateipaddress |
| ipv4-addr | x_aws_ip_type | resource_instancedetails_networkinterfaces_1_privateipaddress |
| ipv4-addr | value | service_action_networkconnectionaction_remoteipdetails_ipaddressv4 |
| ipv4-addr | x_aws_remote_city_name | service_action_networkconnectionaction_remoteipdetails_ipaddressv4 |
| ipv4-addr | x_aws_remote_country_name | service_action_networkconnectionaction_remoteipdetails_ipaddressv4 |
| ipv4-addr | value | portprobe_resource_instancedetails_networkinterfaces_0_privateipaddress |
| ipv4-addr | x_aws_interface_id | portprobe_resource_instancedetails_networkinterfaces_0_privateipaddress |
| ipv4-addr | x_aws_ip_type | portprobe_resource_instancedetails_networkinterfaces_0_privateipaddress |
| ipv4-addr | value | service_action_portprobeaction_portprobedetails_0_remoteipdetails_ipaddressv4 |
| ipv4-addr | x_aws_remote_city_name | service_action_portprobeaction_portprobedetails_0_remoteipdetails_ipaddressv4 |
| ipv4-addr | x_aws_remote_country_name | service_action_portprobeaction_portprobedetails_0_remoteipdetails_ipaddressv4 |
| ipv4-addr | value | service_action_awsapicallaction_remoteipdetails_ipaddressv4 |
| ipv4-addr | x_aws_remote_city_name | service_action_awsapicallaction_remoteipdetails_ipaddressv4 |
| ipv4-addr | x_aws_remote_country_name | service_action_awsapicallaction_remoteipdetails_ipaddressv4 |
| ipv4-addr | value | dnsrequest_resource_instancedetails_networkinterfaces_0_privateipaddress |
| ipv4-addr | x_aws_interface_id | dnsrequest_resource_instancedetails_networkinterfaces_0_privateipaddress |
| ipv4-addr | x_aws_ip_type | dnsrequest_resource_instancedetails_networkinterfaces_0_privateipaddress |
| <br> | | |
| ipv6-addr | value | ip |
| ipv6-addr | value | intermediate_ips |
| ipv6-addr | value | sourceaddress |
| ipv6-addr | x_aws_interface_id | sourceaddress |
| ipv6-addr | value | destinationaddress |
| ipv6-addr | value | resource_instancedetails_networkinterfaces_0_ipv6addresses_0 |
| ipv6-addr | x_aws_interface_id | resource_instancedetails_networkinterfaces_0_ipv6addresses_0 |
| <br> | | |
| network-traffic | src_port | port |
| network-traffic | src_ref | ip |
| network-traffic | dst_port | port |
| network-traffic | dst_ref | ip |
| network-traffic | protocols | protocol_num |
| network-traffic | extensions.x-network-ext.protocol_name | protocol_name |
| network-traffic | extensions.tcp-ext.src_flags_hex | tcp_flags |
| network-traffic | protocols | protocol_ver |
| network-traffic | extensions.x-network-ext.protocol_ver_id | protocol_ver_id |
| network-traffic | extensions.x-network-ext.direction | direction |
| network-traffic | extensions.x-network-ext.boundary_id | boundary_id |
| network-traffic | extensions.x-network-ext.boundary | boundary |
| network-traffic | extensions.x-network-ext.direction_id | direction_id |
| network-traffic | dst_packets | packets_in |
| network-traffic | src_packets | packets_out |
| network-traffic | extensions.x-network-ext.packets | packets |
| network-traffic | dst_byte_count | bytes_in |
| network-traffic | src_byte_count | bytes_out |
| network-traffic | extensions.x-network-ext.bytes | bytes |
| network-traffic | src_ref | sourceaddress |
| network-traffic | dst_ref | destinationaddress |
| network-traffic | src_port | sourceport |
| network-traffic | dst_port | destinationport |
| network-traffic | protocols | protocol |
| network-traffic | start | starttime |
| network-traffic | end | endtime |
| network-traffic | src_ref | resource_instancedetails_networkinterfaces_0_privateipaddress |
| network-traffic | dst_ref | service_action_networkconnectionaction_remoteipdetails_ipaddressv4 |
| network-traffic | src_port | service_action_networkconnectionaction_localportdetails_port |
| network-traffic | dst_port | service_action_networkconnectionaction_remoteportdetails_port |
| network-traffic | protocols | service_action_networkconnectionaction_protocol |
| <br> | | |
| process | command_line | cmd_line |
| process | created | created_time |
| process | extensions.x-ocsf-process-ext.is_system | is_system |
| process | mime_type | mime_type |
| process | extensions.x-ocsf-process-ext.modified_time | modified_time |
| process | binary_ref | name |
| process | extensions.x-ocsf-process-ext.xattributes | xattributes |
| process | extensions.x-ocsf-process-ext.integrity | integrity |
| process | extensions.x-ocsf-process-ext.integrity_id | integrity_id |
| process | extensions.x-ocsf-process-ext.lineage | lineage |
| process | extensions.x-ocsf-process-ext.loaded_modules | loaded_modules |
| process | name | name |
| process | pid | pid |
| process | child_refs | pid |
| process | extensions.x-ocsf-process-ext.loaded_modules | sandbox |
| process | extensions.x-ocsf-process-ext.terminated_time | terminated_time |
| process | extensions.x-ocsf-process-ext.tid | tid |
| process | x_unique_id | uid |
| process | parent_ref | pid |
| <br> | | |
| software | extensions.x-ocsf-product-ext.feature_name | name |
| software | extensions.x-ocsf-product-ext.feature_uid | uid |
| software | extensions.x-ocsf-product-ext.feature_version | version |
| software | languages | lang |
| software | name | name |
| software | extensions.x-ocsf-product-ext.installed_path | path |
| software | extensions.x-ocsf-product-ext.product_uid | uid |
| software | vendor | vendor_name |
| software | version | version |
| software | name | resource_instancedetails_platform |
| <br> | | |
| url | value | url |
| <br> | | |
| user-account | account_type | account_type |
| user-account | extensions.aws-account-ext.account_type_id | account_type_id |
| user-account | user_id | account_uid |
| user-account | extensions.aws-account-ext.credential_uid | credential_uid |
| user-account | extensions.aws-account-ext.domain | domain |
| user-account | extensions.aws-account-ext.group_desc | desc |
| user-account | extensions.aws-account-ext.group_name | name |
| user-account | extensions.aws-account-ext.group_privileges | privileges |
| user-account | extensions.aws-account-ext.group_type | type |
| user-account | extensions.aws-account-ext.group_uid | uid |
| user-account | display_name | name |
| user-account | extensions.aws-account-ext.org_uid | org_uid |
| user-account | extensions.aws-account-ext.session_uid | session_uid |
| user-account | extensions.aws-account-ext.session_uuid | session_uuid |
| user-account | extensions.aws-account-ext.type | type |
| user-account | extensions.aws-account-ext.type_id | type_id |
| user-account | extensions.aws-account-ext.uid | uid |
| user-account | extensions.aws-account-ext.uuid | uuid |
| user-account | extensions.x-accessor-ext.account_type_id | account_type_id |
| user-account | extensions.x-accessor-ext.account_uid | account_uid |
| user-account | extensions.x-accessor-ext.credential_uid | credential_uid |
| user-account | extensions.x-accessor-ext.domain | domain |
| user-account | extensions.x-accessor-ext.group_desc | desc |
| user-account | extensions.x-accessor-ext.group_name | name |
| user-account | extensions.x-accessor-ext.group_privileges | privileges |
| user-account | extensions.x-accessor-ext.group_type | type |
| user-account | extensions.x-accessor-ext.group_uid | uid |
| user-account | extensions.x-accessor-ext.org_uid | org_uid |
| user-account | extensions.x-accessor-ext.session_uid | session_uid |
| user-account | extensions.x-accessor-ext.session_uuid | session_uuid |
| user-account | extensions.x-accessor-ext.type | type |
| user-account | extensions.x-accessor-ext.type_id | type_id |
| user-account | user_id | uid |
| user-account | extensions.x-accessor-ext.uuid | uuid |
| user-account | creator_user_ref | uid |
| user-account | user_id | resource_accesskeydetails_principalid |
| user-account | account_login | resource_accesskeydetails_username |
| <br> | | |
| x-aws-api | access_key_id | resource_accesskeydetails_accesskeyid |
| x-aws-api | api | service_action_awsapicallaction_api |
| x-aws-api | service_name | service_action_awsapicallaction_servicename |
| <br> | | |
| x-aws-details | account_id | account |
| x-aws-details | account_id | accountid |
| x-aws-details | region | region |
| <br> | | |
| x-aws-instance | image_id | resource_instancedetails_imageid |
| x-aws-instance | instance_id | resource_instancedetails_instanceid |
| x-aws-instance | availability_zone | resource_instancedetails_availabilityzone |
| <br> | | |
| x-aws-vpc | subnet_id | resource_instancedetails_networkinterfaces_0_subnetid |
| x-aws-vpc | vpc_id | resource_instancedetails_networkinterfaces_0_vpcid |
| x-aws-vpc | security_group_id | resource_instancedetails_networkinterfaces_0_securitygroups_0_groupid |
| x-aws-vpc | security_group_name | resource_instancedetails_networkinterfaces_0_securitygroups_0_groupname |
| <br> | | |
| x-ibm-finding | time_observed | _time |
| x-ibm-finding | ttp_tagging_refs | name |
| x-ibm-finding | event_count | count |
| x-ibm-finding | end | end_time |
| x-ibm-finding | start | created_time |
| x-ibm-finding | description | desc |
| x-ibm-finding | time_observed | first_seen_time |
| x-ibm-finding | extensions.x-ocsf-findings.last_seen_time | last_seen_time |
| x-ibm-finding | extensions.x-ocsf-findings.modified_time | modified_time |
| x-ibm-finding | extensions.x-ocsf-findings.product_uid | product_uid |
| x-ibm-finding | extensions.x-ocsf-findings.type | type |
| x-ibm-finding | extensions.x-ocsf-findings.type_uid | type_uid |
| x-ibm-finding | extensions.x-ocsf-findings.uid | uid |
| x-ibm-finding | extensions.x-ocsf-findings.remediation_desc | desc |
| x-ibm-finding | extensions.x-ocsf-findings.remediation_kb_articles | kb_articles |
| x-ibm-finding | extensions.x-ocsf-findings.src_url | src_url |
| x-ibm-finding | extensions.x-ocsf-findings.upporting_data | supporting_data |
| x-ibm-finding | name | title |
| x-ibm-finding | types | types |
| x-ibm-finding | alert_id | uid |
| x-ibm-finding | ioc_refs | name |
| x-ibm-finding | severity | severity_id |
| x-ibm-finding | src_ip_ref | ip |
| x-ibm-finding | dst_ip_ref | ip |
| x-ibm-finding | src_ip_ref | sourceaddress |
| x-ibm-finding | dst_ip_ref | destinationaddress |
| x-ibm-finding | start | starttime |
| x-ibm-finding | end | endtime |
| x-ibm-finding | finding_type | action |
| x-ibm-finding | name | name |
| x-ibm-finding | src_ip_ref | resource_instancedetails_networkinterfaces_0_privateipaddress |
| x-ibm-finding | dst_ip_ref | service_action_networkconnectionaction_remoteipdetails_ipaddressv4 |
| x-ibm-finding | dst_geolocation | service_action_networkconnectionaction_remoteipdetails_ipaddressv4 |
| x-ibm-finding | src_ip_ref | portprobe_resource_instancedetails_networkinterfaces_0_privateipaddress |
| x-ibm-finding | dst_ip_ref | service_action_portprobeaction_portprobedetails_0_remoteipdetails_ipaddressv4 |
| x-ibm-finding | dst_geolocation | service_action_portprobeaction_portprobedetails_0_remoteipdetails_ipaddressv4 |
| x-ibm-finding | probe_port | service_action_portprobeaction_portprobedetails_0_localportdetails_port |
| x-ibm-finding | dst_ip_ref | service_action_awsapicallaction_remoteipdetails_ipaddressv4 |
| x-ibm-finding | dst_geolocation | service_action_awsapicallaction_remoteipdetails_ipaddressv4 |
| x-ibm-finding | src_ip_ref | dnsrequest_resource_instancedetails_networkinterfaces_0_privateipaddress |
| x-ibm-finding | severity | severity |
| x-ibm-finding | finding_type | type |
| x-ibm-finding | description | description |
| x-ibm-finding | src_os_ref | resource_instancedetails_platform |
| x-ibm-finding | start | service_eventfirstseen |
| x-ibm-finding | end | service_eventlastseen |
| <br> | | |
| x-ibm-observables | name | name |
| x-ibm-observables | finding_type | type |
| x-ibm-observables | alert_id | type_id |
| x-ibm-observables | description | value |
| <br> | | |
| x-ibm-ttp-tagging | extensions.mitre-attack-ext.tactic_name | name |
| x-ibm-ttp-tagging | extensions.mitre-attack-ext.tactic_id | uid |
| x-ibm-ttp-tagging | name | name |
| x-ibm-ttp-tagging | extensions.mitre-attack-ext.technique_name | name |
| x-ibm-ttp-tagging | extensions.mitre-attack-ext.technique_id | uid |
| x-ibm-ttp-tagging | extensions.mitre-attack-ext.versoin | version |
| <br> | | |
| x-oca-asset | extensions.x-src-endpoint.svc_name | svc_name |
| x-oca-asset | ip_refs | ip |
| x-oca-asset | ip_refs | intermediate_ips |
| x-oca-asset | extensions.x-src-endpoint.interface_uid | interface_uid |
| x-oca-asset | extensions.x-src-endpoint.vpc_uid | vpc_uid |
| x-oca-asset | extensions.x-src-endpoint.instance_uid | instance_uid |
| x-oca-asset | extensions.x-src-endpoint.subnet_uid | subnet_uid |
| x-oca-asset | name | name |
| x-oca-asset | extensions.x-dst-endpoint.svc_name | svc_name |
| x-oca-asset | extensions.x-dst-endpoint.interface_uid | interface_uid |
| x-oca-asset | extensions.x-dst-endpoint.vpc_uid | vpc_uid |
| x-oca-asset | extensions.x-dst-endpoint.instance_uid | instance_uid |
| x-oca-asset | extensions.x-dst-endpoint.subnet_uid | subnet_uid |
| <br> | | |
| x-oca-event | action | activity |
| x-oca-event | code | activity_id |
| x-oca-event | action | activity_name |
| x-oca-event | category | category_name |
| x-oca-event | code | category_uid |
| x-oca-event | module | class_name |
| x-oca-event | extensions.x-cloud-api.class_uid | class_uid |
| x-oca-event | confidence | confidence |
| x-oca-event | extensions.x-ocsf-data.data | data |
| x-oca-event | duration | duration |
| x-oca-event | network_ref | ip |
| x-oca-event | created | time |
| x-oca-event | timezone | timezone_offset |
| <br> | | |
| x-ocsf-cloud | operation | operation |
| x-ocsf-cloud | request_flags | flags |
| x-ocsf-cloud | request_uid | uid |
| x-ocsf-cloud | response_code | code |
| x-ocsf-cloud | response_error | error |
| x-ocsf-cloud | response_error_message | error_message |
| x-ocsf-cloud | response_flags | flags |
| x-ocsf-cloud | response_message | message |
| x-ocsf-cloud | service_labels | labels |
| x-ocsf-cloud | service_name | name |
| x-ocsf-cloud | service_uid | uid |
| x-ocsf-cloud | service_uid | version |
| x-ocsf-cloud | api_version | version |
| x-ocsf-cloud | account_type | account_type |
| x-ocsf-cloud | account_type_id | account_type_id |
| x-ocsf-cloud | account_uid | account_uid |
| x-ocsf-cloud | org_uid | org_uid |
| x-ocsf-cloud | project_uid | project_uid |
| x-ocsf-cloud | provider | provider |
| x-ocsf-cloud | region | region |
| x-ocsf-cloud | resource_uid | resource_uid |
| x-ocsf-cloud | zone | zone |
| x-ocsf-cloud | message | message |
| x-ocsf-cloud | profiles | profiles |
| x-ocsf-cloud | raw_data | raw_data |
| x-ocsf-cloud | ref_event_code | ref_event_code |
| x-ocsf-cloud | ref_event_name | ref_event_name |
| x-ocsf-cloud | ref_event_uid | ref_event_uid |
| x-ocsf-cloud | ref_time | ref_time |
| x-ocsf-cloud | severity | severity |
| x-ocsf-cloud | status | status |
| x-ocsf-cloud | status_code | status_code |
| x-ocsf-cloud | status_detail | status_detail |
| x-ocsf-cloud | status_id | status_id |
| x-ocsf-cloud | type_name | type_name |
| x-ocsf-cloud | type_uid | type_uid |
| <br> | | |
| x-ocsf-compliance | requirements | requirements |
| x-ocsf-compliance | status | status |
| x-ocsf-compliance | status_detail | status_detail |
| <br> | | |
| x-ocsf-enrichments | data | data |
| x-ocsf-enrichments | name | name |
| x-ocsf-enrichments | provider | provider |
| x-ocsf-enrichments | type | type |
| x-ocsf-enrichments | value | value |
| <br> | | |
| x-ocsf-http-request | value | args |
| x-ocsf-http-request | http_headers_name | name |
| x-ocsf-http-request | http_headers_value | value |
| x-ocsf-http-request | http_method | http_method |
| x-ocsf-http-request | prefix | prefix |
| x-ocsf-http-request | referrer | referrer |
| x-ocsf-http-request | uid | uid |
| x-ocsf-http-request | user_agent | user_agent |
| x-ocsf-http-request | version | version |
| x-ocsf-http-request | x_forwarded_for | x_forwarded_for |
| <br> | | |
| x-ocsf-identity | authorizations.decision | decision |
| x-ocsf-identity | authorizations.policy_desc | desc |
| x-ocsf-identity | authorizations.policy_group_desc | desc |
| x-ocsf-identity | authorizations.policy_group_namee | name |
| x-ocsf-identity | authorizations.policy_group_privileges | privileges |
| x-ocsf-identity | authorizations.policy_group_type | type |
| x-ocsf-identity | authorizations.policy_group_uid | uid |
| x-ocsf-identity | authorizations.name | name |
| x-ocsf-identity | authorizations.uid | uid |
| x-ocsf-identity | authorizations.version | version |
| x-ocsf-identity | idp.name | name |
| x-ocsf-identity | idp.uid | uid |
| x-ocsf-identity | invoked_by | invoked_by |
| x-ocsf-identity | message | message |
| x-ocsf-identity | session.created_time | created_time |
| x-ocsf-identity | session.credential_uid | credential_uid |
| x-ocsf-identity | session.expiration_time | expiration_time |
| x-ocsf-identity | session.issuer | issuer |
| x-ocsf-identity | session.mfa | mfa |
| x-ocsf-identity | session.uid | uid |
| <br> | | |
| x-ocsf-malware | classification_ids | classification_ids |
| x-ocsf-malware | classifications | classifications |
| x-ocsf-malware | created_time | created_time |
| x-ocsf-malware | base_score | base_score |
| x-ocsf-malware | depth | depth |
| x-ocsf-malware | name | name |
| x-ocsf-malware | value | value |
| x-ocsf-malware | overall_score | overall_score |
| x-ocsf-malware | severity | severity |
| x-ocsf-malware | vector_string | vector_string |
| x-ocsf-malware | version | version |
| x-ocsf-malware | cwe_uid | cwe_uid |
| x-ocsf-malware | cwe_url | cwe_url |
| x-ocsf-malware | modified_time | modified_time |
| x-ocsf-malware | type | type |
| x-ocsf-malware | uid | uid |
| x-ocsf-malware | path | path |
| x-ocsf-malware | provider | provider |
| <br> | | |
| x-ocsf-metadata | correlation_uid | correlation_uid |
| x-ocsf-metadata | labels | labels |
| x-ocsf-metadata | logged_time | logged_time |
| x-ocsf-metadata | modified_time | modified_time |
| x-ocsf-metadata | processed_time | processed_time |
| x-ocsf-metadata | sequence | sequence |
| x-ocsf-metadata | uid | uid |
| x-ocsf-metadata | version | version |
| <br> | | |
| x-ocsf-resources | account_uid | account_uid |
| x-ocsf-resources | cloud_api_ref | account_uid |
| x-ocsf-resources | cloud_partition | cloud_partition |
| x-ocsf-resources | criticality | criticality |
| x-ocsf-resources | details | details |
| x-ocsf-resources | group_name | group_name |
| x-ocsf-resources | labels | labels |
| x-ocsf-resources | name | name |
| x-ocsf-resources | owner | owner |
| x-ocsf-resources | region | region |
| x-ocsf-resources | type | type |
| x-ocsf-resources | uid | uid |
| <br> | | |
| x-ocsf-vulnerabilities | created_time | created_time |
| x-ocsf-vulnerabilities | base_score | base_score |
| x-ocsf-vulnerabilities | depth | depth |
| x-ocsf-vulnerabilities | name | name |
| x-ocsf-vulnerabilities | value | value |
| x-ocsf-vulnerabilities | overall_score | overall_score |
| x-ocsf-vulnerabilities | severity | severity |
| x-ocsf-vulnerabilities | vector_string | vector_string |
| x-ocsf-vulnerabilities | version | version |
| x-ocsf-vulnerabilities | cwe_uid | cwe_uid |
| x-ocsf-vulnerabilities | cwe_url | cwe_url |
| x-ocsf-vulnerabilities | modified_time | modified_time |
| x-ocsf-vulnerabilities | type | type |
| x-ocsf-vulnerabilities | uid | uid |
| x-ocsf-vulnerabilities | desc | desc |
| x-ocsf-vulnerabilities | kb_articles | kb_articles |
| x-ocsf-vulnerabilities | packages_architecture | architecture |
| x-ocsf-vulnerabilities | packages_epoch | epoch |
| x-ocsf-vulnerabilities | packages_license | license |
| x-ocsf-vulnerabilities | packages_name | name |
| x-ocsf-vulnerabilities | packages_release | release |
| x-ocsf-vulnerabilities | packages_version | version |
| x-ocsf-vulnerabilities | references | references |
| x-ocsf-vulnerabilities | related_vulnerabilities | related_vulnerabilities |
| x-ocsf-vulnerabilities | title | title |
| x-ocsf-vulnerabilities | vendor_name | vendor_name |
| <br> | | |
