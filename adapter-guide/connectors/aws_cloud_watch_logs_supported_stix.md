## Amazon CloudWatch Logs
| STIX Object | STIX Property | Data Source Field |
|--|--|--|
| domain-name | resolves_to_refs | detail_resource_instanceDetails_networkInterfaces_0_privateIpAddress |
| domain-name | resolves_to_refs | detail_resource_instanceDetails_networkInterfaces_0_publicIp |
| domain-name | value | detail_resource_instanceDetails_networkInterfaces_0_privateDnsName |
| domain-name | value | detail_resource_instanceDetails_networkInterfaces_0_publicDnsName |
| domain-name | resolves_to_refs | detail_resource_instanceDetails_networkInterfaces_1_privateIpAddress |
| domain-name | value | detail_resource_instanceDetails_networkInterfaces_1_privateDnsName |
| domain-name | value | detail_service_action_dnsRequestAction_domain |
| <br> | | |
| ipv4-addr | value | srcAddr |
| ipv4-addr | x_aws_interface_id | srcAddr |
| ipv4-addr | value | dstAddr |
| ipv4-addr | value | detail_resource_instanceDetails_networkInterfaces_0_privateIpAddress |
| ipv4-addr | x_aws_interface_id | detail_resource_instanceDetails_networkInterfaces_0_privateIpAddress |
| ipv4-addr | x_aws_ip_type | detail_resource_instanceDetails_networkInterfaces_0_privateIpAddress |
| ipv4-addr | value | detail_resource_instanceDetails_networkInterfaces_0_publicIp |
| ipv4-addr | x_aws_interface_id | detail_resource_instanceDetails_networkInterfaces_0_publicIp |
| ipv4-addr | x_aws_ip_type | detail_resource_instanceDetails_networkInterfaces_0_publicIp |
| ipv4-addr | value | detail_resource_instanceDetails_networkInterfaces_1_privateIpAddress |
| ipv4-addr | x_aws_interface_id | detail_resource_instanceDetails_networkInterfaces_1_privateIpAddress |
| ipv4-addr | x_aws_ip_type | detail_resource_instanceDetails_networkInterfaces_1_privateIpAddress |
| ipv4-addr | value | detail_service_action_networkConnectionAction_remoteIpDetails_ipAddressV4 |
| ipv4-addr | x_aws_remote_city_name | detail_service_action_networkConnectionAction_remoteIpDetails_ipAddressV4 |
| ipv4-addr | x_aws_remote_country_name | detail_service_action_networkConnectionAction_remoteIpDetails_ipAddressV4 |
| ipv4-addr | value | detail_service_action_portProbeAction_portProbeDetails_0_remoteIpDetails_ipAddressV4 |
| ipv4-addr | x_aws_remote_city_name | detail_service_action_portProbeAction_portProbeDetails_0_remoteIpDetails_ipAddressV4 |
| ipv4-addr | x_aws_remote_country_name | detail_service_action_portProbeAction_portProbeDetails_0_remoteIpDetails_ipAddressV4 |
| ipv4-addr | value | detail_service_action_awsApiCallAction_remoteIpDetails_ipAddressV4 |
| ipv4-addr | x_aws_remote_city_name | detail_service_action_awsApiCallAction_remoteIpDetails_ipAddressV4 |
| ipv4-addr | x_aws_remote_country_name | detail_service_action_awsApiCallAction_remoteIpDetails_ipAddressV4 |
| <br> | | |
| ipv6-addr | value | srcAddr |
| ipv6-addr | x_aws_interface_id | srcAddr |
| ipv6-addr | value | dstAddr |
| ipv6-addr | value | detail_resource_instanceDetails_networkInterfaces_0_ipv6Addresses_0 |
| ipv6-addr | x_aws_interface_id | detail_resource_instanceDetails_networkInterfaces_0_ipv6Addresses_0 |
| <br> | | |
| network-traffic | src_ref | srcAddr |
| network-traffic | dst_ref | dstAddr |
| network-traffic | src_port | srcPort |
| network-traffic | dst_port | dstPort |
| network-traffic | protocols | protocol |
| network-traffic | start | start |
| network-traffic | end | end |
| network-traffic | src_ref | detail_resource_instanceDetails_networkInterfaces_0_privateIpAddress |
| network-traffic | dst_ref | detail_service_action_networkConnectionAction_remoteIpDetails_ipAddressV4 |
| network-traffic | src_port | detail_service_action_networkConnectionAction_localPortDetails_port |
| network-traffic | dst_port | detail_service_action_networkConnectionAction_remotePortDetails_port |
| network-traffic | protocols | detail_service_action_networkConnectionAction_protocol |
| <br> | | |
| user-account | user_id | detail_resource_accessKeyDetails_principalId |
| user-account | account_login | detail_resource_accessKeyDetails_userName |
| <br> | | |
| x_aws | account_id | accountId |
| x_aws | account_id | account |
| x_aws | region | detail_region |
| <br> | | |
| x_aws_api | access_key_id | detail_resource_accessKeyDetails_accessKeyId |
| x_aws_api | api | detail_service_action_awsApiCallAction_api |
| x_aws_api | service_name | detail_service_action_awsApiCallAction_serviceName |
| <br> | | |
| x_aws_guardduty_finding | probe_port | detail_service_action_portProbeAction_portProbeDetails_0_localPortDetails_port |
| x_aws_guardduty_finding | timestamp | @timestamp |
| x_aws_guardduty_finding | id | detail_id |
| x_aws_guardduty_finding | severity | detail_severity |
| x_aws_guardduty_finding | type | detail_type |
| x_aws_guardduty_finding | title | detail_title |
| <br> | | |
| x_aws_instance | image_id | detail_resource_instanceDetails_imageId |
| x_aws_instance | instance_id | detail_resource_instanceDetails_instanceId |
| x_aws_instance | availability_zone | detail_resource_instanceDetails_availabilityZone |
| <br> | | |
| x_aws_vpc | subnet_id | detail_resource_instanceDetails_networkInterfaces_0_subnetId |
| x_aws_vpc | vpc_id | detail_resource_instanceDetails_networkInterfaces_0_vpcId |
| x_aws_vpc | security_group_id | detail_resource_instanceDetails_networkInterfaces_0_securityGroups_0_groupId |
| x_aws_vpc | security_group_name | detail_resource_instanceDetails_networkInterfaces_0_securityGroups_0_groupName |
| <br> | | |
