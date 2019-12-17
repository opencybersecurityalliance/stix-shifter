# AWS CloudWatchLogs UDS Connector

## This connector supports two types of datasource authentication:

   1. Using user's security credentials (Access and Secret keys)
       #### Sample Input:
        ```
        transmit
        "aws_cloud_watch_logs"
        "{\"host\":\"xxxxxxx.xxxx.xxxxx\",\"port\": \"xxx\",\"cert_verify\":\"xxxx\"}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
        query <translated_query>
        ``` 
   
   2. Using user's security credentials (Access and Secret keys) and IAM role (ARN value of the IAM role)
       #### Sample Input:
        ```
        transmit
        "aws_cloud_watch_logs"
        "{\"host\":\"xxxxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\"}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxxxxxx\", \"aws_secret_access_key\": 
        \"xxxxxxxxx\",\"aws_iam_role\":\"xxxxxxxxx\"}}"
        query <translated_query>
        ```
    
## This connector supports two types of data search 

   1. Collect data from specific loggroups if "log_group_names" is given.
   Provide logtype (guarduty or vpcflow) and loggroups as input
        #### Sample Input:
        ```
        transmit
        "aws_cloud_watch_logs"
        "{\"host\":\"xxxxxxx.xxxx.xxxxx\",\"port\": \"xxx\",\"cert_verify\":\"xxxx\"}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"},\"log_group_names\":{\"guardduty\":[\"CloudTrail/DefaultLogGroup\",\"/aws/events/guardduty\"], \"vpcflow\":[\"USEast1_FlowLogs\"}}"
        query <translated_query>
        ```
    
   2. Collect data from all available loggroups if no "log_group_names" is given.
        #### Sample Input:
        ```
        transmit
        "aws_cloud_watch_logs"
        "{\"host\":\"xxxxxxx.xxxx.xxxxx\",\"port\": \"xxx\",\"cert_verify\":\"xxxx\"}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
        query <translated_query>
        ```

## Sample 1:

#### STIX patterns:

```
([domain-name:value = 'guarddutyc2activityb.com' OR x_com_aws_cwl:imageId = 'ami-00068cd7555f543d']) START t'2019-12-01T08:43:10.003Z' STOP t'2019-12-06T10:43:10.003Z'
```

#### Translated query:

```
{"logType": "guardduty", "limit": 1000, "queryString": "fields @timestamp, source, @message  | parse detail.resource.instanceDetails.imageId \\"\\" as image_id | parse detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateDnsName\\":\\"*\\"\' as private_dns_name | parse detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicDnsName\\":\\"*\\"\' as public_dns_name | parse detail.service.action.dnsRequestAction.domain \\"\\" as dns_domain | filter source = \'aws.guardduty\' or strlen (image_id) > 0 or strlen (private_dns_name) > 0 or strlen (public_dns_name) > 0 or strlen (dns_domain) > 0  | filter ((image_id =~ /^(?i)ami-00068cd7555f543d$/) OR ((private_dns_name =~ /^(?i)guarddutyc2activityb.com$/ OR public_dns_name =~ /^(?i)guarddutyc2activityb.com$/ OR dns_domain =~ /^(?i)guarddutyc2activityb.com$/)))", "startTime": 1575189790, "endTime": 1575628990}
```

#### Transmit query:

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxxxxx.xxxx.xxxxx\",\"port\": \"xxx\",\"cert_verify\":\"xxxx\"}"
"{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"},\"log_group_names\":{\"xxxx\": 
[\"xxxxxx\"]}}"
query
"{\"logType\": \"guardduty\", \"limit\": 1000, \"queryString\": \"fields @timestamp, source, @message  | parse detail
.resource.instanceDetails.imageId \\\"\\\" as image_id | parse detail.resource.instanceDetails.networkInterfaces.0 
'\\\"privateDnsName\\\":\\\"*\\\"' as private_dns_name | parse detail.resource.instanceDetails.networkInterfaces.0 
'\\\"publicDnsName\\\":\\\"*\\\"' as public_dns_name | parse detail.service.action.dnsRequestAction.domain \\\"\\\" as 
dns_domain | filter source = 'aws.guardduty' or strlen (image_id) > 0 or strlen (private_dns_name) > 0 or strlen 
(public_dns_name) > 0 or strlen (dns_domain) > 0  | filter ((image_id =~ /^(?i)ami-00068cd7555f543d$/) OR (
(private_dns_name =~ /^(?i)guarddutyc2activityb.com$/ OR public_dns_name =~ /^(?i)guarddutyc2activityb.com$/ OR 
dns_domain =~ /^(?i)guarddutyc2activityb.com$/)))\", \"startTime\": 1575189790, \"endTime\": 1575628990}"
```

#### Search id:

```
{'success': True, 'search_id': 'ca48ecec-09d1-4745-bbf3-ee2743586f7f'}
```

#### For Transmit result:

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxxxxx.xxxx.xxxxx\",\"port\": \"xxx\",\"cert_verify\":\"xxxx\"}"
"{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
results
ca48ecec-09d1-4745-bbf3-ee2743586f7f
0
2
```

#### STIX observable output:

```
{
    "type": "bundle",
    "id": "bundle--8b5f8064-4e2a-436f-8657-c68d8d9c32ea",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "aws_cloud_watch_logs",
            "identity_class": "events"
        },
        {
            "id": "observed-data--af00bbea-5f76-481a-a44e-f98835a9fc44",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-12-12T06:40:39.465Z",
            "modified": "2019-12-12T06:40:39.465Z",
            "objects": {
                "0": {
                    "type": "ipv6-addr",
                    "value": "2600:1f18:4036:e6fe:1ad2:4170:395a:da9a"
                },
                "1": {
                    "type": "domain-name",
                    "value": "ip-172-31-13-238.ec2.internal",
                    "resolves_to_refs": [
                        "2"
                    ]
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "172.31.13.238"
                },
                "3": {
                    "type": "domain-name",
                    "value": "ec2-3-231-163-216.compute-1.amazonaws.com",
                    "resolves_to_refs": [
                        "4"
                    ]
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "3.231.163.216"
                },
                "5": {
                    "type": "domain-name",
                    "value": "guarddutyc2activityb.com"
                }
            },
            "x_com_guardduty_findings": {
                "resource": {
                    "instance_details": {
                        "instance_id": "i-091501e21e01d0602",
                        "network_interfaces_0": {
                            "ipv6_addresses_0_ref": "0",
                            "network_interface_id": "eni-0a70b0fa1a9cd3dbe",
                            "private_dns_name_ref": "1",
                            "private_ip_address_ref": "2",
                            "subnet_id": "subnet-b9a994de",
                            "vpc_id": "vpc-10db926a",
                            "security_groups": {
                                "group_name": "launch-wizard-1",
                                "group_id": "sg-0aa89ff4646f71594"
                            },
                            "public_dns_name_ref": "3",
                            "public_ip_ref": "4"
                        },
                        "tags_0": {
                            "key": "stack",
                            "value": "test"
                        },
                        "image_id": "ami-00068cd7555f543d5"
                    },
                    "resource_type": "Instance"
                },
                "service": {
                    "action": {
                        "dns_request_action": {
                            "domain_ref": "5"
                        },
                        "action_type": "DNS_REQUEST"
                    },
                    "resource_role": "TARGET"
                },
                "source": "aws.guardduty",
                "account_id": "979326520502",
                "region": "us-east-1",
                "id": "0ab76a9742c56179c3cfbc9d0616ff49",
                "type": "Backdoor:EC2/C&CActivity.B!DNS",
                "severity": 8,
                "updated_at": "2019-12-05T10:03:15.926Z",
                "title": "Command and Control server domain name queried by EC2 instance i-091501e21e01d0602."
            },
            "first_observed": "2019-12-05T08:16:04Z",
            "last_observed": "2019-12-05T08:16:18Z",
            "x_com_cwl_timestamp": "2019-12-05T10:15:01.000Z",
            "number_observed": 1
        }
}
```

## Sample 2:

#### STIX patterns:

```
[ipv4-addr:value = '172.31.88.63'] START t'2019-12-01T08:43:10.003Z' STOP t'2019-12-06T10:43:10.003Z'
```

#### Translated query:

```
{"logType": "guardduty", "limit": 1000, "queryString": "fields @timestamp, source, @message  | parse detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as private_ip_address | parse detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicIp\\":\\"*\\"\' as public_ip | parse @message /(?:\\"ipAddressV4\\"\\\\:\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\")/ | filter source = \'aws.guardduty\' or strlen (private_ip_address) > 0 or strlen (public_ip) > 0 or strlen (remote_ip) > 0  | filter ((private_ip_address =~ /^(?i)172.31.88.63$/ OR public_ip =~ /^(?i)172.31.88.63$/ OR remote_ip =~ /^(?i)172.31.88.63$/))", "startTime": 1575189790, "endTime": 1575628990}', '{"logType": "vpcflow", "limit": 1000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, dstPort, protocol, start, end, accountId, interfaceId, bytes, packets   | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or strlen(protocol) > 0 | filter ((srcAddr =~ /^(?i)172.31.88.63$/ OR dstAddr =~ /^(?i)172.31.88.63$/))", "startTime": 1575189790, "endTime": 1575628990}
```

#### Transmit query for vpcflow:

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\"}"
"{\"auth\":{\"aws_access_key_id\": \"xxxxxxxx\", \"aws_secret_access_key\": 
\"xxxxxxxxx\",\"aws_iam_role\":\"xxxxxxxxx\"},\"log_group_names\":{\"vpcflow\": 
[\"USEast1_FlowLogs\"]}}"
query
"{\"logType\": \"vpcflow\", \"limit\": 1000, \"queryString\": \"fields @timestamp, srcAddr, dstAddr, srcPort, dstPort, protocol, start, end, accountId, interfaceId, bytes, packets   | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or strlen(protocol) > 0 | filter ((srcAddr =~ /^(?i)172.31.88.63$/ OR dstAddr =~ /^(?i)172.31.88.63$/))\", \"startTime\": 1575189790, \"endTime\": 1575628990}"
```

#### Transmit query for guardduty:

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\"}"
"{\"auth\":{\"aws_access_key_id\": \"xxxxxxxx\", \"aws_secret_access_key\": 
\"xxxxxxxxx\",\"aws_iam_role\":\"xxxxxxxxx\"},\"log_group_names\":{\"vpcflow\": 
[\"USEast1_FlowLogs\"]}}"
query
"{\"logType\": \"guardduty\", \"limit\": 1000, \"queryString\": \"fields @timestamp, source, @message  | parse detail
.resource.instanceDetails.networkInterfaces.0 '\\\"privateIpAddress\\\":\\\"*\\\"' as private_ip_address | parse detail
.resource.instanceDetails.networkInterfaces.0 '\\\"publicIp\\\":\\\"*\\\"' as public_ip | parse @message /
(?:\\\"ipAddressV4\\\"\\\\:\\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\\\.){3}
(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\\")/ | filter source = 'aws.guardduty' or strlen (private_ip_address) > 0
 or strlen (public_ip) > 0 or strlen (remote_ip) > 0  | filter ((private_ip_address =~ /^(?i)172.31.88.63$/ OR public_ip =~ /^(?i)172.31.88.63$/ OR remote_ip =~ /^(?i)172.31.88.63$/))\", \"startTime\": 1575189790, \"endTime\": 1575628990}"
```

#### Search id for guardduty and vpcflow:

```
{'success': True, 'search_id': '8c816cdd-51ac-4e55-a335-59179fa817b1'}
```
```
{'success': True, 'search_id': '947b9ac3-4653-4846-8472-d25d17e72349'}
```

#### For guardduty Transmit result:

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\"}"
"{\"auth\":{\"aws_access_key_id\": \"xxxxxxxx\", \"aws_secret_access_key\": 
\"xxxxxxxxx\",\"aws_iam_role\":\"xxxxxxxxx\"}}"
results
8c816cdd-51ac-4e55-a335-59179fa817b1
0
2
```

#### For vpcflow Transmit result:

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\"}"
"{\"auth\":{\"aws_access_key_id\": \"xxxxxxxx\", \"aws_secret_access_key\": 
\"xxxxxxxxx\",\"aws_iam_role\":\"xxxxxxxxx\"}}"
results
947b9ac3-4653-4846-8472-d25d17e72349
0
2
```
#### STIX observable output for guardduty:

```
{
    "type": "bundle",
    "id": "bundle--dc36b68c-4ffc-40d6-a848-ca5ffe179fd1",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "aws_cloud_watch_logs",
            "identity_class": "events"
        },
        {
            "id": "observed-data--eb288544-b02c-4680-9bb3-dd087f33d5ee",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-12-12T06:58:18.993Z",
            "modified": "2019-12-12T06:58:18.993Z",
            "objects": {
                "0": {
                    "type": "domain-name",
                    "value": "ip-172-31-88-63.ec2.internal",
                    "resolves_to_refs": [
                        "1"
                    ]
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "172.31.88.63"
                },
                "2": {
                    "type": "domain-name",
                    "value": "ec2-54-211-223-78.compute-1.amazonaws.com",
                    "resolves_to_refs": [
                        "3"
                    ]
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "54.211.223.78"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "115.213.134.162"
                }
            },
            "x_com_guardduty_findings": {
                "resource": {
                    "instance_details": {
                        "instance_id": "i-0b8fd03ade35c681d",
                        "iam_instance_profile": {
                            "id": "AIPA6IBDIZS3ES3TI5TNQ"
                        },
                        "network_interfaces_0": {
                            "network_interface_id": "eni-02e70b8e842c70a2f",
                            "private_dns_name_ref": "0",
                            "private_ip_address_ref": "1",
                            "public_dns_name_ref": "2",
                            "public_ip_ref": "3"
                        },
                        "image_id": "ami-04763b3055de4860b"
                    },
                    "resource_type": "Instance"
                },
                "service": {
                    "action": {
                        "port_probe_action": {
                            "port_probe_details_0": {
                                "port": 22,
                                "port_name": "SSH",
                                "remote_ip_ref": "4",
                                "remote_ip_details": {
                                    "organization": {
                                        "asn": "4134",
                                        "asn_org": "No.31,Jin-rong Street",
                                        "isp": "China Telecom"
                                    },
                                    "country": {
                                        "country_name": "China"
                                    },
                                    "city": {
                                        "city_name": "Lishui"
                                    }
                                }
                            }
                        },
                        "action_type": "PORT_PROBE"
                    },
                    "additional_info": {
                        "threat_list_name": "ProofPoint"
                    },
                    "resource_role": "TARGET"
                },
                "source": "aws.guardduty",
                "account_id": "979326520502",
                "region": "us-east-1",
                "id": "9ab6e702ba673b8f1f3323956f0759d9",
                "type": "Recon:EC2/PortProbeUnprotectedPort",
                "severity": 2,
                "updated_at": "2019-10-18T09:37:44.346Z",
                "title": "Unprotected port on EC2 instance i-0b8fd03ade35c681d is being probed."
            },
            "first_observed": "2019-10-15T05:50:08Z",
            "last_observed": "2019-10-18T09:20:16Z",
            "x_com_cwl_timestamp": "2019-10-18T09:45:05.000Z",
            "number_observed": 1
        }
}
```

#### STIX observable output for vpcflow:

```
{
            "id": "observed-data--a4348702-f095-4393-bf56-0b17e1c09500",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-12-12T06:58:20.431Z",
            "modified": "2019-12-12T06:58:20.431Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "120.192.217.102"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "dst_ref": "2",
                    "src_port": 12041,
                    "dst_port": 1433,
                    "protocols": [
                        "tcp"
                    ],
                    "start": "2019-10-20T10:43:09.000Z",
                    "end": "2019-10-20T10:44:08.000Z"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "172.31.88.63"
                }
            },
            "first_observed": "2019-10-20T10:43:09.000Z",
            "last_observed": "2019-10-20T10:43:09.000Z",
            "x_com_vpc_flow": {
                "account_id": "979326520502",
                "interface_id": "eni-02e70b8e842c70a2f"
            },
            "number_observed": 1
        },
        {
            "id": "observed-data--d516f912-36f1-44d2-8c06-bbe4e21b6c16",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-12-12T06:58:20.517Z",
            "modified": "2019-12-12T06:58:20.517Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "172.31.88.63"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "dst_ref": "2",
                    "src_port": 53866,
                    "dst_port": 443,
                    "protocols": [
                        "tcp"
                    ],
                    "start": "2019-10-20T10:43:09.000Z",
                    "end": "2019-10-20T10:44:08.000Z"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "54.239.29.61"
                }
            },
            "first_observed": "2019-10-20T10:43:09.000Z",
            "last_observed": "2019-10-20T10:43:09.000Z",
            "x_com_vpc_flow": {
                "account_id": "979326520502",
                "interface_id": "eni-02e70b8e842c70a2f"
            },
            "number_observed": 1
        }
}
```
