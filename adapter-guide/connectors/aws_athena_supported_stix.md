##### Updated on 02/04/22
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
### Supported STIX Objects and Properties
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
| software | name | resource_instancedetails_platform |
| <br> | | |
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
| x-ibm-finding | name | title |
| x-ibm-finding | finding_type | type |
| x-ibm-finding | description | description |
| x-ibm-finding | src_os_ref | resource_instancedetails_platform |
| x-ibm-finding | start | service_eventfirstseen |
| x-ibm-finding | end | service_eventlastseen |
| <br> | | |
