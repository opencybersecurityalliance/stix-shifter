# Amazon CloudWatch Logs

## Supported STIX Mappings

See the [table of mappings](aws_cloud_watch_logs_supported_stix.md) for the STIX objects and operators supported by this connector.

## This connector supports two types of datasource authentication:

   1. Using user's security credentials (Access and Secret keys)
       #### Sample Input:
        ```
        transmit
        "aws_cloud_watch_logs"
        "{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"xxxx\"}}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxx\"}}"
        query <translated_query>
        ``` 
   
   2. Using user's security credentials (Access and Secret keys) and IAM role (ARN value of the IAM role)
       #### Sample Input:
        ```
        transmit
        "aws_cloud_watch_logs"
        "{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"xxxx\"}}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxxxxxx\", \"aws_secret_access_key\": 
        \"xxxxxxxxx\",\"aws_iam_role\":\"xxxxxxxxx\"}}"
        query <translated_query>
        ```
    
## This connector supports following ways of data search 

   1. No log groups given
       #### Sample Input:
        ```
        transmit
        "aws_cloud_watch_logs"
        "{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"xxxx\"}}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
        query <translated_query>
        ```

   2. Log groups given without logtype specification
        #### Sample Input:
        ```
        transmit
        "aws_cloud_watch_logs"
        "{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"us-east-1\", 
        \"log_group_names\": {\"default\":[\"/aws/events/guardduty\", \"USEast1_FlowLogs\"]}}}" "{\"auth\":{\"aws_access_key_id\": \"xxxx\", 
        \"aws_secret_access_key\": \"xxxx\"}}"
        query <translated_query>
        ```

   3. Log groups given with logtype specification
        #### Sample Input:
        ```
        transmit
        "aws_cloud_watch_logs"
        "{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"us-east-1\", 
        \"log_group_names\": {\"guardduty\": [\"/aws/events/guardduty\"], \"vpcflow\":\"USEast1_FlowLogs\"}}}" "{\"auth\":{\"aws_access_key_id\": \"xxxx\", 
        \"aws_secret_access_key\": \"xxxx\"}}"
        query <translated_query>
        ```

   4. Log groups given with logtype and default specification
        #### Sample Input:
        ```
        transmit
        "aws_cloud_watch_logs"
        "{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"xxxx\", 
        \"log_group_names\": {\"guardduty\": [\"/aws/events/guardduty\"], \"vpcflow\":\"USEast1_FlowLogs\", \"default\":[\"/aws/events/guardduty\", \"USEast1_FlowLogs\"]}}}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
        query <translated_query>
        ```  

## Sample 1:(STIX pattern with resultSizeLimit)

#### STIX patterns:

```
"([domain-name:value = 'guarddutyc2activityb.com' OR x-aws-instance:image_id = 'ami-00068cd7555f543d']) START 
t'2019-12-01T08:43:10.003Z' STOP t'2019-12-06T10:43:10.003Z'" "{\"resultSizeLimit\":500}"
```

#### Translated query:

```
{"logType": "guardduty", "limit": 500, "queryString": "fields @timestamp, source, @message | parse detail.resource
.instanceDetails.imageId \\"\\" as image_id | parse detail.resource.instanceDetails.networkInterfaces.0 \'\\"privateDnsName\\":\\"*\\"\' as eth0_private_dns_name | parse detail.resource.instanceDetails.networkInterfaces.1 \'\\"privateDnsName\\":\\"*\\"\' as eth1_private_dns_name | parse detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicDnsName\\":\\"*\\"\' as public_dns_name | parse detail.service.action.dnsRequestAction.domain \\"\\" as dns_domain | filter source = \'aws.guardduty\' or strlen(image_id) > 0 or strlen(eth0_private_dns_name) > 0 or strlen(eth1_private_dns_name) > 0 or strlen(public_dns_name) > 0 or strlen(dns_domain) > 0 | filter ((tolower(image_id) = tolower(\'ami-00068cd7555f543d\')) OR ((tolower(eth0_private_dns_name) = tolower(\'guarddutyc2activityb.com\') OR tolower(eth1_private_dns_name) = tolower(\'guarddutyc2activityb.com\') OR tolower(public_dns_name) = tolower(\'guarddutyc2activityb.com\') OR tolower(dns_domain) = tolower(\'guarddutyc2activityb.com\'))))", "startTime": 1575189790, "endTime": 1575628990}
```

#### Transmit query:

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"xxxx\",\"log_group_names\":{\"guardduty\":[\"CloudTrail/DefaultLogGroup\",\"/aws/events/guardduty\"], \"vpcflow\":\"USEast1_FlowLogs\"}}}"
"{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
query
"{\"logType\": \"guardduty\", \"limit\": 500, \"queryString\": \"fields @timestamp, source, @message | parse detail
.resource.instanceDetails.imageId \\\"\\\" as image_id | parse detail.resource.instanceDetails.networkInterfaces.0 '\\\"privateDnsName\\\":\\\"*\\\"' as eth0_private_dns_name | parse detail.resource.instanceDetails.networkInterfaces.1 '\\\"privateDnsName\\\":\\\"*\\"' as eth1_private_dns_name | parse detail.resource.instanceDetails.networkInterfaces.0 '\\\"publicDnsName\\\":\\\"*\\\"' as public_dns_name | parse detail.service.action.dnsRequestAction.domain \\"\\" as dns_domain | filter source = 'aws.guardduty' or strlen(image_id) > 0 or strlen(eth0_private_dns_name) > 0 or strlen(eth1_private_dns_name) > 0 or strlen(public_dns_name) > 0 or strlen(dns_domain) > 0 | filter ((tolower(image_id) = tolower('ami-00068cd7555f543d')) OR ((tolower(eth0_private_dns_name) = tolower('guarddutyc2activityb.com') OR tolower(eth1_private_dns_name) = tolower('guarddutyc2activityb.com') OR tolower(public_dns_name) = tolower('guarddutyc2activityb.com') OR tolower(dns_domain) = tolower('guarddutyc2activityb.com'))))\", \"startTime\": 1575189790, \"endTime\": 1575628990}"
```

#### Search id:

```
{'success': True, 'search_id': '3c4d5934-aa47-4a4f-be16-ef963d73b502:500'}
```

#### Transmit result:

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"xxxx\"}}"
"{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
results
3c4d5934-aa47-4a4f-be16-ef963d73b502:500
0
50
```

#### STIX observable output:

```
{
    "type": "bundle",
    "id": "bundle--d74ec163-7d77-4cbd-8503-f7d353ed96f8",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "aws_cloud_watch_logs",
            "identity_class": "events"
        },
        {
            "id": "observed-data--0bcbbf16-b5c2-4479-98e0-da080bf08f87",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-12-23T10:25:07.536Z",
            "modified": "2019-12-23T10:25:07.536Z",
            "objects": {
                "0": {
                    "type": "ipv6-addr",
                    "value": "2600:1f18:4036:e6fe:1ad2:4170:395a:da9a",
                    "x_aws_interface_id": "eni-0a70b0fa1a9cd3dbe"
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
                    "value": "172.31.13.238",
                    "x_aws_interface_id": "eni-0a70b0fa1a9cd3dbe",
                    "x_aws_ip_type": "private"
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
                    "value": "3.231.163.216",
                    "x_aws_interface_id": "eni-0a70b0fa1a9cd3dbe",
                    "x_aws_ip_type": "public"
                },
                "5": {
                    "type": "domain-name",
                    "value": "guarddutyc2activityb.com"
                }
            },
            "x_aws_instance": {
                "instance_id": "i-091501e21e01d0602",
                "availability_zone": "us-east-1a",
                "image_id": "ami-00068cd7555f543d5"
            },
            "x_aws_vpc": {
                "subnet_id": "subnet-b9a994de",
                "vpc_id": "vpc-10db926a",
                "security_group_name": "launch-wizard-1",
                "security_group_id": "sg-0aa89ff4646f71594"
            },
            "x_aws": {
                "account_id": "979326520502",
                "region": "us-east-1"
            },
            "x_aws_guardduty_finding": {
                "id": "0ab76a9742c56179c3cfbc9d0616ff49",
                "type": "Backdoor:EC2/C&CActivity.B!DNS",
                "severity": 8,
                "title": "Command and Control server domain name queried by EC2 instance i-091501e21e01d0602.",
                "timestamp": "2019-12-05T10:15:01.000Z"
            },
            "first_observed": "2019-12-05T08:16:04Z",
            "last_observed": "2019-12-05T08:16:18Z",
            "number_observed": 1
    }   
}
```

## Sample 2:

#### STIX patterns:(STIX pattern without resultSizeLimit)

```
[ipv4-addr:value = '172.31.88.63'] START t'2019-10-01T08:43:10.003Z' STOP t'2019-10-20T10:43:10.003Z'
```

#### Translated query:

```
{"logType": "guardduty", "limit": 10000, "queryString": "fields @timestamp, source, @message | parse detail.resource
.instanceDetails.networkInterfaces.0 \'\\"privateIpAddress\\":\\"*\\"\' as eth0_private_ip | parse detail.resource
.instanceDetails.networkInterfaces.1 \'\\"privateIpAddress\\":\\"*\\"\' as eth1_private_ip | parse detail.resource.instanceDetails.networkInterfaces.0 \'\\"publicIp\\":\\"*\\"\' as public_ip | parse @message /(?:\\"ipAddressV4\\"\\\\:\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\")/ | filter source = \'aws.guardduty\' or strlen(eth0_private_ip) > 0 or strlen(eth1_private_ip) > 0 or strlen(public_ip) > 0 or strlen(remote_ip) > 0 | filter ((tolower(eth0_private_ip) = tolower(\'172.31.88.63\') OR tolower(eth1_private_ip) = tolower(\'172.31.88.63\') OR tolower(public_ip) = tolower(\'172.31.88.63\') OR tolower(remote_ip) = tolower(\'172.31.88.63\')))", "startTime": 1569919390, "endTime": 1571568190}', '{"logType": "vpcflow", "limit": 10000, "queryString": "fields @timestamp, srcAddr, dstAddr, srcPort, dstPort, protocol, start, end, accountId, interfaceId | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or strlen(protocol) > 0 | filter ((tolower(srcAddr) = tolower(\'172.31.88.63\') OR tolower(dstAddr) = tolower(\'172.31.88.63\')))", "startTime": 1569919390, "endTime": 1571568190}
```

#### GuardDuty Transmit query :

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"xxxx\",\"log_group_names\":{\"guardduty\":[\"CloudTrail/DefaultLogGroup\",\"/aws/events/guardduty\"], \"vpcflow\":\"USEast1_FlowLogs\"}}}"
"{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
query
"{\"logType\": \"guardduty\", \"limit\": 10000, \"queryString\": \"fields @timestamp, source, @message | parse detail
.resource.instanceDetails.networkInterfaces.0 '\\\"privateIpAddress\\\":\\\"*\\\"' as eth0_private_ip | parse detail.resource.instanceDetails.networkInterfaces.1 '\\\"privateIpAddress\\\":\\\"*\\\"' as eth1_private_ip | parse detail.resource.instanceDetails.networkInterfaces.0 '\\\"publicIp\\\":\\\"*\\\"' as public_ip | parse @message /(?:\\\"ipAddressV4\\\"\\\\:\\\")(?<remote_ip>((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?:\\\")/ | filter source = 'aws.guardduty' or strlen(eth0_private_ip) > 0 or strlen(eth1_private_ip) > 0 or strlen(public_ip) > 0 or strlen(remote_ip) > 0 | filter ((tolower(eth0_private_ip) = tolower('172.31.88.63') OR tolower(eth1_private_ip) = tolower('172.31.88.63') OR tolower(public_ip) = tolower('172.31.88.63') OR tolower(remote_ip) = tolower('172.31.88.63')))\", \"startTime\": 1569919390, \"endTime\": 1571568190}"
```

#### VPCFlow Transmit query:

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"xxxx\",\"log_group_names\":{\"guardduty\":[\"CloudTrail/DefaultLogGroup\",\"/aws/events/guardduty\"], \"vpcflow\":\"USEast1_FlowLogs\"}}}"
"{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
query
"{\"logType\": \"vpcflow\", \"limit\": 10000, \"queryString\": \"fields @timestamp, srcAddr, dstAddr, srcPort, 
dstPort, protocol, start, end, accountId, interfaceId | filter strlen(srcAddr) > 0 or strlen(dstAddr) > 0 or strlen(protocol) > 0 | filter ((tolower(srcAddr) = tolower('172.31.88.63') OR tolower(dstAddr) = tolower('172.31.88.63')))\", \"startTime\": 1569919390, \"endTime\": 1571568190}"
```

#### GuardDuty Search id:

```
{'success': True, 'search_id': '713bd4e2-1e9c-4919-bdb4-72baceed3ba7:10000'}
```

#### VPCFlow Search id:

```
{'success': True, 'search_id': 'c3be3246-8b2b-4be7-b2de-d5d475c0ed8a:10000'}
```

#### GuardDuty Transmit result :

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"xxxx\"}}"
"{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
results
713bd4e2-1e9c-4919-bdb4-72baceed3ba7:10000
0
2
```

#### VPCFlow Transmit result :

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"xxxx\"}}"
"{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
results
c3be3246-8b2b-4be7-b2de-d5d475c0ed8a:10000
0
2
```

#### GuardDuty STIX observable output:

```
{
    "type": "bundle",
    "id": "bundle--2e3adffd-2694-4e89-848a-a70bd58dece0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "aws_cloud_watch_logs",
            "identity_class": "events"
        },
        {
            "id": "observed-data--2542d92e-0662-4cac-878e-a183198b33ee",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-12-23T10:40:15.840Z",
            "modified": "2019-12-23T10:40:15.840Z",
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
                    "value": "172.31.88.63",
                    "x_aws_interface_id": "eni-02e70b8e842c70a2f",
                    "x_aws_ip_type": "private"
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
                    "value": "54.211.223.78",
                    "x_aws_interface_id": "eni-02e70b8e842c70a2f",
                    "x_aws_ip_type": "public"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "115.213.134.162",
                    "x_aws_remote_city_name": "Lishui",
                    "x_aws_remote_country_name": "China"
                }
            },
            "x_aws_instance": {
                "instance_id": "i-0b8fd03ade35c681d",
                "availability_zone": "us-east-1b",
                "image_id": "ami-04763b3055de4860b"
            },
            "x_aws_vpc": {
                "subnet_id": "subnet-c62a11e8",
                "vpc_id": "vpc-10db926a",
                "security_group_name": "launch-wizard-1",
                "security_group_id": "sg-0aa89ff4646f71594"
            },
            "x_aws_guardduty_finding": {
                "probe_port": 22,
                "id": "9ab6e702ba673b8f1f3323956f0759d9",
                "type": "Recon:EC2/PortProbeUnprotectedPort",
                "severity": 2,
                "title": "Unprotected port on EC2 instance i-0b8fd03ade35c681d is being probed.",
                "timestamp": "2019-10-18T09:45:05.000Z"
            },
            "x_aws": {
                "account_id": "979326520502",
                "region": "us-east-1"
            },
            "first_observed": "2019-10-15T05:50:08Z",
            "last_observed": "2019-10-18T09:20:16Z",
            "number_observed": 1
        }
    }
```

#### VPCFlow STIX observable output:

```
{
            "id": "observed-data--b5cb09d3-5b2a-4ff3-b78d-d86b847d61a6",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-12-23T10:40:15.852Z",
            "modified": "2019-12-23T10:40:15.852Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "172.31.88.63",
                    "x_aws_interface_id": "eni-02e70b8e842c70a2f"
                },
                "1": {
                    "type": "network-traffic",
                    "src_ref": "0",
                    "dst_ref": "2",
                    "src_port": 36834,
                    "dst_port": 443,
                    "protocols": [
                        "tcp"
                    ],
                    "start": "2019-10-20T10:43:09.000Z",
                    "end": "2019-10-20T10:44:08.000Z"
                },
                "2": {
                    "type": "ipv4-addr",
                    "value": "52.46.159.38"
                }
            },
            "first_observed": "2019-10-20T10:43:09.000Z",
            "last_observed": "2019-10-20T10:43:09.000Z",
            "x_aws": {
                "account_id": "979326520502"
            },
            "number_observed": 1
        },
        {
            "id": "observed-data--e5391086-f4ae-4c47-a238-7ae1b20cf1d7",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-12-23T10:40:15.855Z",
            "modified": "2019-12-23T10:40:15.855Z",
            "objects": {
                "0": {
                    "type": "ipv4-addr",
                    "value": "120.192.217.102",
                    "x_aws_interface_id": "eni-02e70b8e842c70a2f"
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
            "x_aws": {
                "account_id": "979326520502"
            },
            "number_observed": 1
        }
```

## Sample 3:

#### STIX patterns:(STIX pattern without resultSizeLimit)

```
([x-aws-api:access_key_id = 'xxxxxxx']) START t'2019-12-01T08:43:10.003Z' STOP t'2019-12-06T10:43:10.003Z'
```

#### Translated query:

```
{"logType": "guardduty", "limit": 10000, "queryString": "fields @timestamp, source, @message | parse detail.resource
.accessKeyDetails.accessKeyId \\"\\" as access_key_id | filter source = \'aws.guardduty\' or strlen (access_key_id) >
 0 | filter (tolower(access_key_id) = tolower(\'xxxxxxxx\'))", "startTime": 1577333751, "endTime": 1577334051}
```

#### Transmit query:

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxx\",\"port\": \"xxxx\",\"cert_verify\":\"xxxx\",\"options\": {\"region\": \"xxxx\",\"log_group_names\":{\"guardduty\":[\"CloudTrail/DefaultLogGroup\",\"/aws/events/guardduty\"], \"vpcflow\":\"USEast1_FlowLogs\"}}}"
"{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
query
"{\"logType\": \"guardduty\", \"limit\": 10000, \"queryString\": \"fields @timestamp, source, @message | parse detail
.resource.accessKeyDetails.accessKeyId \\"\\" as access_key_id | filter source = 'aws.guardduty' or strlen 
(access_key_id) > 0 | filter (tolower(access_key_id) = tolower('xxxxx'))\", \"startTime\": 1577333751, 
\"endTime\": 1577334051}"
```

#### Search id:

```
{'success': True, 'search_id': '50359121-6624-43bf-9ef2-a9f3bf07f5ef:10000'}
```

#### Transmit result:

```
transmit
"aws_cloud_watch_logs"
"{\"host\":\"xxxxxxx.xxxx.xxxxx\",\"port\": \"xxx\",\"cert_verify\":\"xxxx\"}"
"{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"xxxxx\"}}"
results
50359121-6624-43bf-9ef2-a9f3bf07f5ef:10000
0
2
```

#### STIX observable output:
```
{
    "type": "bundle",
    "id": "bundle--4fafbd23-0b25-44c2-982a-bf2ed4999429",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "aws_cloud_watch_logs",
            "identity_class": "events"
        },
        {
            "id": "observed-data--794b5867-6600-419f-b912-0868954c72d3",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2019-12-26T13:21:04.882Z",
            "modified": "2019-12-26T13:21:04.882Z",
            "objects": {
                "0": {
                    "type": "user-account",
                    "user_id": "AIDA6IBDIZS3PHKDTXCSI",
                    "account_login": "karthick.rajagopal@hcl.com"
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "157.46.15.243",
                    "x_aws_remote_city_name": "Chennai",
                    "x_aws_remote_country_name": "India"
                }
            },
            "x_aws_api": {
                "access_key_id": "xxxxxxx",
                "api": "DescribeSecurityGroups",
                "service_name": "ec2.amazonaws.com"
            },
            "x_aws": {
                "account_id": "979326520502",
                "region": "us-east-1"
            },
            "x_aws_guardduty_finding": {
                "id": "14b76d5936d5f302695e67ac500ab78a",
                "type": "Recon:IAMUser/NetworkPermissions",
                "severity": 5,
                "title": "Unusual network permission reconnaissance activity by karthick.rajagopal@hcl.com.",
                "timestamp": "2019-12-06T10:15:05.000Z"
            },
            "first_observed": "2019-12-06T09:51:34Z",
            "last_observed": "2019-12-06T09:51:34Z",
            "number_observed": 1
        }
    ]
}

```

### STIX pattern for custom attributes and sample values
|  Description  |  STIX Pattern  |  Sample Values  |
| --- | --- | --- |
| Network Interface id of the EC2 instance  | ipv4-addr:x_aws_interface_id | [ipv4-addr:x_aws_interface_id = 'eni-0a70b0fa1a9cd3dbe'] |
| City name of Remote Ip address  | ipv4-addr:x_aws_remote_city_name | [ipv4-addr:x_aws_remote_city_name = 'Ashburn'] |
| Country name of Remote Ip address  | ipv4-addr:x_aws_remote_country_name | [ipv4-addr:x_aws_remote_country_name = 'United States'] |
| Network Interface id of the EC2 instance  | ipv6-addr:x_aws_interface_id | [ipv6-addr:x_aws_interface_id = 'eni-0a70b0fa1a9cd3dbe'] |
| AWS Account Id | x-aws:account_id | [x-aws:account_id = '979326520502'] |
| AWS Region | x-aws:aws_region | [x-aws:aws_region = 'us-east-1'] |
| EC2 instance Id  | x-aws-instance:instance_id | [x-aws-instance:instance_id = 'i-091501e21e01d0602'] |
| EC2 instance Image Id  | x-aws-instance:image_id| [x-aws-instance:image_id = 'ami-00068cd7555f543d5'] |
| EC2 instance Availability Zone  | x-aws-instance:availability_zone | [x-aws-instance:availability_zone = 'us-east-1a'] |
| VPC Id associated with EC2 Instance | x-aws-vpc:vpc_id | [x-aws-vpc:vpc_id = 'i-091501e21e01d0602'] |
| Subnet Id associated with EC2 Instance | x-aws-vpc:subnet_id| [x-aws-vpc:subnet_id = 'ami-00068cd7555f543d5'] |
| Security Group Name associated with EC2 Instance  | x-aws-vpc:security_group_name | [x-aws-vpc:security_group_name = 'launch-wizard-1'] |
| Security Group Id associated with EC2 Instance | x-aws-vpc:security_group_id | [x-aws-vpc:security_group_id = 'sg-0aa89ff4646f71594'] |
| AccessKey Id of User | x-aws-api:access_key_id | [x-aws-api:access_key_id = 'AAAABBBBCCCC'] |
| AWS api name | x-aws-api:api | [x-aws-api:api = 'DescribeSecurityGroups'] |
| AWS service name whose api is invoked | x-aws-api:api_service_name | [x-aws-api:api_service_name = 'ec2.amazonaws.com'] |
| Id of guardduty finding | x-aws-guardduty-finding:finding_id | [x-aws-guardduty-finding:finding_id = '14b76d5936d5f302695e67ac500ab78a'] |
| Type of guardduty finding | x-aws-guardduty-finding:finding_type | [x-aws-guardduty-finding:finding_type = 'Recon:IAMUser/NetworkPermissions'] |

###References
Click below link for different types of guardduty finding<br/>
 [Guardduty Finding](https://docs.aws.amazon.com/guardduty/latest/ug/guardduty_finding-types-active.html).