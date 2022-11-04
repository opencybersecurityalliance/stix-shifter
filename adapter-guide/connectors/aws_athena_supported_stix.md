##### Updated on 11/04/22
## Amazon Athena
### Supported STIX Operators
| STIX Operator | Data Source Operator |
|--|--|
| AND | INTERSECT |
| OR | UNION |
| > | > |
| >= | >= |
| < | < |
| <= | <= |
| = | = |
| != | != |
| LIKE | LIKE |
| IN | IN |
| MATCHES | REGEXP_LIKE |
| <br> | |
### Searchable STIX objects and properties for Guardduty
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
### Searchable STIX objects and properties for Ocsf
| STIX Object and Property | Mapped Data Source Fields |
|--|--|
| **email-addr**:value | identity.user.email_addr |
| **ipv4-addr**:value | src_endpoint.intermediate_ips |
| **ipv6-addr**:value | src_endpoint.intermediate_ips |
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
| **x-ibm-finding**:alert_id | observables.type_id |
| **x-ibm-finding**:description | observables.value |
| **x-ibm-finding**:end | end_time |
| **x-ibm-finding**:event_count | count |
| **x-ibm-finding**:finding_type | observables.type |
| **x-ibm-finding**:name | observables.name |
| **x-ibm-finding**:severity | severity_id |
| **x-ibm-finding**:start | start_time |
| **x-oca-asset**:extensions.'x-oca-endpoint-ext'.port | src_endpoint.port |
| **x-oca-asset**:extensions.'x-oca-endpoint-ext'.svc_name | src_endpoint.svc_name |
| **x-oca-asset**:ip_refs[*].value | src_endpoint.intermediate_ips |
| **x-oca-asset**:name | src_endpoint.name |
| **x-oca-event**:action | activity, category_name |
| **x-oca-event**:code | activity_id, category_uid |
| **x-oca-event**:created | time |
| **x-oca-event**:duration | duration |
| **x-oca-event**:extensions.'x-cloud-api'.class_uid | class_uid |
| **x-oca-event**:module | class_name |
| **x-oca-event**:timezone | timezone_offset |
| **x-ocsf-cloud**:account_type | cloud.account_type |
| **x-ocsf-cloud**:account_type_id | cloud.account_type_id |
| **x-ocsf-cloud**:account_uid | cloud.account_uid |
| **x-ocsf-cloud**:api_version | api.version |
| **x-ocsf-cloud**:http_request.user_agent | http_request.user_agent |
| **x-ocsf-cloud**:message | message |
| **x-ocsf-cloud**:operation | api.operation |
| **x-ocsf-cloud**:org_uid | cloud.org_uid |
| **x-ocsf-cloud**:profiles | profiles, unmapped.profiles |
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
### Searchable STIX objects and properties for Vpcflow
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
| ipv6-addr | value | intermediate_ips |
| ipv6-addr | value | sourceaddress |
| ipv6-addr | x_aws_interface_id | sourceaddress |
| ipv6-addr | value | destinationaddress |
| ipv6-addr | value | resource_instancedetails_networkinterfaces_0_ipv6addresses_0 |
| ipv6-addr | x_aws_interface_id | resource_instancedetails_networkinterfaces_0_ipv6addresses_0 |
| <br> | | |
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
| software | extension.product.feature_name | name |
| software | extension.product.feature_uid | uid |
| software | extension.product.feature_version | version |
| software | languages | lang |
| software | name | name |
| software | extension.product.path | path |
| software | extension.product.uid | uid |
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
| x-ibm-finding | event_count | count |
| x-ibm-finding | end | end_time |
| x-ibm-finding | name | name |
| x-ibm-finding | finding_type | type |
| x-ibm-finding | alert_id | type_id |
| x-ibm-finding | description | value |
| x-ibm-finding | severity | severity_id |
| x-ibm-finding | start | start_time |
| x-ibm-finding | src_ip_ref | sourceaddress |
| x-ibm-finding | dst_ip_ref | destinationaddress |
| x-ibm-finding | start | starttime |
| x-ibm-finding | end | endtime |
| x-ibm-finding | finding_type | action |
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
| x-ibm-finding | name | title |
| x-ibm-finding | description | description |
| x-ibm-finding | src_os_ref | resource_instancedetails_platform |
| x-ibm-finding | start | service_eventfirstseen |
| x-ibm-finding | end | service_eventlastseen |
| <br> | | |
| x-oca-asset | ip_refs | intermediate_ips |
| x-oca-asset | name | name |
| x-oca-asset | extensions.x-oca-endpoint-ext.port | port |
| x-oca-asset | extensions.x-oca-endpoint-ext.svc_name | svc_name |
| <br> | | |
| x-oca-event | action | activity |
| x-oca-event | code | activity_id |
| x-oca-event | action | category_name |
| x-oca-event | code | category_uid |
| x-oca-event | module | class_name |
| x-oca-event | extensions.x-cloud-api.class_uid | class_uid |
| x-oca-event | duration | duration |
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
