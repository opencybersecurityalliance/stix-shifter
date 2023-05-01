# Amazon Athena

## Supported STIX Mappings

See the [table of mappings](aws_athena_supported_stix.md) for the STIX objects and operators supported by this connector.

### Data Source: 
Amazon Athena is an interactive query service that makes it easy to analyze data in Amazon S3 using standard SQL. 
Athena is serverless, so there is no infrastructure to manage, and you pay only for the queries that you run.

### Supported Amazon schema

1. [OCSF Schema](https://github.com/ocsf/ocsf-schema): Currently supports partial OCSF schema that includes the base events and few objecs such as api, cloud, identity, enrichments, http_request, identity, metadata, observables and resources.

2. [VPC Flow logs](https://docs.aws.amazon.com/athena/latest/ug/vpc-flow-logs.html)

3. [GuardDuty findings](https://docs.aws.amazon.com/athena/latest/ug/querying-guardduty.html)

##### Amazon Athena API Endpoints:
|  Connector Method  |  Boto3 library API Methods  |  
| --- | --- |
| Ping | list_work_groups() |
| Query | start_query_execution() |
| Status | get_query_execution() |
| Results | get_query_results() |
| Delete | stop_query_execution() |

#####Reference - [Athena Boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html)

### AWS Authentication Types

##### This connector supports two types of datasource authentication:

   1. Using user's security credentials (Access and Secret keys)
       ##### Sample Input:
        ```
        transmit
        "aws_athena"
        "{\"region\": \"<athena configured region>\", \"s3_bucket_location\":\"s3://<path to output bucket>/\",
        \"vpcflow_database_name\":\"flow_logs_db\", \"vpcflow_table_name\":\"vpc_flow_log\", 
        \"guardduty_database_name\":\"guardduty_logs_db\",\"guardduty_table_name\":\"gd_logs\"}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"yyyy\"}}"
        query <translated_query>
        ``` 
   
   2. Using user's security credentials (Access and Secret keys) and IAM role (ARN value of the IAM role)
       ##### Sample Input:
        ```
        transmit
        "aws_athena"
        "{\"region\": \"<athena configured region>\", \"s3_bucket_location\":\"s3://<path to output bucket>/\", 
        \"vpcflow_database_name\":\"flow_logs_db\", \"vpcflow_table_name\":\"vpc_flow_log\", 
        \"guardduty_database_name\":\"guardduty_logs_db\",\"guardduty_table_name\":\"gd_logs\"}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": 
        \"yyyy\",\"aws_iam_role\":\"zzzz\"}}"
        query <translated_query>
        ```

### Query Service Types

##### This connector supports following search support 

   1. Data search with all optional values.
      ##### Sample Input:
        ```
        transmit
        "{"region": "<athena configured region>", "s3_bucket_location":"s3://<path to output bucket>/",
        "vpcflow_database_name":"flow_logs_db", "vpcflow_table_name":"vpc_flow_logs", 
        "guardduty_database_name":"guardduty_logs_db","guardduty_table_name":"gd_logs",
        "ocsf_database_name": "ocsf_db",
        "ocsf_table_name": "ocsf_table"}"
        "{"auth":{"aws_access_key_id": "xxxx", "aws_secret_access_key": "yyyy"}}"
        query <translated_query>
        ```
   2. Data search with service based optional values.
      ##### Sample Input:
        ```
        "aws_athena"
        "{"region": "<athena configured region>", "s3_bucket_location":"s3://<path to output bucket>/",
        "guardduty_database_name":"guardduty_logs_db","guardduty_table_name":"gd_logs"}"
        "{"auth":{"aws_access_key_id": "xxxx", "aws_secret_access_key": "yyyy"}}"
        query <translated_query>
        ```

## Sample 1:(Pattern expression with STIX Attributes)

#### STIX patterns:(multiple queries will be formed based on mapping)

```
translate aws_athena query '{}' "[ipv4-addr:value = '172.31.76.105'] START t'2020-05-01T08:43:10.003Z' 
STOP t'2020-11-30T10:43:10.003Z'"
```

#### Translated query:

```
{
    "queries": [
        {
            "vpcflow": "((lower(sourceaddress) = lower('172.31.76.105') OR lower(destinationaddress) = lower('172.31.76.105')) AND start BETWEEN 1588322590 AND 1606732990)"
        },
        {
            "guardduty": "((lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.0.privateipaddress')) = lower('172.31.76.105') OR lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.1.privateipaddress')) = lower('172.31.76.105') OR lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.0.publicip')) = lower('172.31.76.105') OR lower(json_extract_scalar(service,'$.action.networkconnectionaction.remoteipdetails.ipaddressv4')) = lower('172.31.76.105') OR lower(json_extract_scalar(service,'$.action.portprobeaction.remoteipdetails.ipaddressv4')) = lower('172.31.76.105') OR lower(json_extract_scalar(service,'$.action.awsapicallaction.remoteipdetails.ipaddressv4')) = lower('172.31.76.105')) AND updatedat BETWEEN '2020-05-01T08:43:10.003Z' AND '2020-11-30T10:43:10.003Z')"
        },
        {
            "ocsf": "(lower(src_endpoint.intermediate_ips) = lower('172.31.76.105') AND _time BETWEEN 1588322590000 AND 1606732990000)"
        }
    ]
}
```

#### Transmit query: GuardDuty query is passed to STIX transmission module

```
 transmit aws_athena "{\"region\": \"us-east-1\", \"s3_bucket_location\": \"s3://queryresults-athena-s3/\", 
 \"vpcflow_database_name\":\"logs_db\", \"vpcflow_table_name\":\"vpc_flow_log\", 
 \"guardduty_database_name\":\"logs_db\",\"guardduty_table_name\":\"gd_logs\"}" "{\"auth\":{\"aws_access_key_id\": 
 \"xxxx\", 
 \"aws_secret_access_key\": \"yyyy\"}}" query "{\"guardduty\": \"((lower(json_extract_scalar(resource,'$
 .instancedetails.networkinterfaces.0.privateipaddress')) = lower('172.31.76.105') OR lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.1.privateipaddress')) = lower('172.31.76.105') OR lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.0.publicip')) = lower('172.31.76.105') OR lower(json_extract_scalar(service,'$.action.networkconnectionaction.remoteipdetails.ipaddressv4')) = lower('172.31.76.105') OR lower(json_extract_scalar(service,'$.action.portprobeaction.remoteipdetails.ipaddressv4')) = lower('172.31.76.105') OR lower(json_extract_scalar(service,'$.action.awsapicallaction.remoteipdetails.ipaddressv4')) = lower('172.31.76.105')) AND updatedat BETWEEN '2020-05-01T08:43:10.003Z' AND '2020-11-30T10:43:10.003Z')\"}"
```

#### Transmit query: VPCFlow query is passed to STIX transmission module

```
transmit aws_athena "{\"region\": \"us-east-1\", \"s3_bucket_location\": \"s3://queryresults-athena-s3/\", 
\"vpcflow_database_name\":\"logs_db\", \"vpcflow_table_name\":\"vpc_flow_log\", 
\"guardduty_database_name\":\"logs_db\",\"guardduty_table_name\":\"gd_logs\"}" "{\"auth\":{\"aws_access_key_id\": \"xxxx\", 
\"aws_secret_access_key\": \"yyyy\"}}" query "{\"vpcflow\": \"((lower(sourceaddress) = lower('172.31.76.105') OR lower
(destinationaddress) = lower('172.31.76.105')) AND starttime BETWEEN 1588322590 AND 1606732990)\"}"
```

#### GuardDuty Search id: 

```
 {'success': True, 'search_id': 'd512d194-396e-4afb-9e38-4011c2472edc:guardduty'}
```

#### VPCFlow Search id:

```
{'success': True, 'search_id': 'c3be3246-8b2b-4be7-b2de-d5d475c0ed8a:vpcflow'}
```

#### GuardDuty Transmit result: (provide search id in transmit result with offset and length)

```
 transmit aws_athena "{\"region\": \"us-east-1\", \"s3_bucket_location\": \"s3://queryresults-athena-s3/\", 
 \"vpcflow_database_name\":\"logs_db\", \"vpcflow_table_name\":\"vpc_flow_log\", 
 \"guardduty_database_name\":\"logs_db\",\"guardduty_table_name\":\"gd_logs\"}" "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"yyyy\"}}" 
 results "d512d194-396e-4afb-9e38-4011c2472edc:guardduty" 0 2
```

#### VPCFlow Transmit result : (provide search id in transmit result with offset and length)

```
transmit aws_athena "{\"region\": \"us-east-1\", \"s3_bucket_location\": \"s3://queryresults-athena-s3/\", 
\"vpcflow_database_name\":\"logs_db\", \"vpcflow_table_name\":\"vpc_flow_log\", 
\"guardduty_database_name\":\"logs_db\",\"guardduty_table_name\":\"gd_logs\"}" "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"yyyy\"}}" 
results "19b3ad96-a8de-4894-bb9d-f63c50c99b0a:vpcflow" 0 2
```

#### GuardDuty STIX observable output:

```json
 {
    "type": "bundle",
    "id": "bundle--0b9321b6-deba-4b89-a4dc-44f50ec3cf8c",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "aws_athena",
            "identity_class": "events"
        },
        {
            "id": "observed-data--3e13aa4b-2047-4082-8ff5-94ff9178f2f7",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2020-11-16T16:04:11.955Z",
            "modified": "2020-11-16T16:04:11.955Z",
            "objects": {
                "0": {
                    "type": "x-aws-details",
                    "account_id": 979326520502,
                    "region": "us-east-1"
                },
                "1": {
                    "type": "x-ibm-finding",
                    "finding_type": "UnauthorizedAccess:EC2/RDPBruteForce",
                    "src_ip_ref": "3",
                    "src_os_ref": "9",
                    "start": "2020-11-16T00:33:13Z",
                    "dst_ip_ref": "10",
                    "dst_geolocation": "Germany",
                    "end": "2020-11-16T05:13:15Z",
                    "severity": 2,
                    "name": "213.202.233.193 is performing RDP brute force attacks against i-0707634d9134ecada.",
                    "description": "213.202.233.193 is performing RDP brute force attacks against i-0707634d9134ecada. Brute force attacks are used to gain unauthorized access to your instance by guessing the RDP password."
                },
                "2": {
                    "type": "domain-name",
                    "value": "ip-172-31-76-105.ec2.internal",
                    "resolves_to_refs": [
                        "3"
                    ]
                },
                "3": {
                    "type": "ipv4-addr",
                    "value": "172.31.76.105",
                    "x_aws_interface_id": "eni-0b96a84d6a8cadfb2",
                    "x_aws_ip_type": "private"
                },
                "4": {
                    "type": "network-traffic",
                    "src_ref": "3",
                    "protocols": [
                        "tcp"
                    ],
                    "dst_port": 1081,
                    "dst_ref": "10",
                    "src_port": 3389
                },
                "5": {
                    "type": "x-aws-vpc",
                    "subnet_id": "subnet-4b662675",
                    "vpc_id": "vpc-10db926a",
                    "security_group_id": "sg-0bda1d30e86632484",
                    "security_group_name": "launch-wizard-12"
                },
                "6": {
                    "type": "domain-name",
                    "value": "ec2-52-87-235-83.compute-1.amazonaws.com",
                    "resolves_to_refs": [
                        "7"
                    ]
                },
                "7": {
                    "type": "ipv4-addr",
                    "value": "52.87.235.83",
                    "x_aws_interface_id": "eni-0b96a84d6a8cadfb2",
                    "x_aws_ip_type": "public"
                },
                "8": {
                    "type": "x-aws-instance",
                    "image_id": "ami-04a0ee204b44cc91a",
                    "instance_id": "i-0707634d9134ecada",
                    "availability_zone": "us-east-1e"
                },
                "9": {
                    "type": "software",
                    "name": "windows"
                },
                "10": {
                    "type": "ipv4-addr",
                    "value": "213.202.233.193",
                    "x_aws_remote_city_name": "D\u00fcsseldorf",
                    "x_aws_remote_country_name": "Germany"
                },
                "11": {
                    "type": "x-aws-athena",
                    "arn": "arn:aws:guardduty:us-east-1:979326520502:detector/6ab6e6ee780ed494f3b7ca56acdc74df/finding/24bae74503647e535aa16eeb246de329",
                    "createdat": "2020-11-16T00:52:33.609Z",
                    "partition": "aws",
                    "finding_id": "7ab9d1cb6248e05a0e419a79528761cb",
                    "resource": {
                        "instancedetails": {
                            "instancestate": "running",
                            "instancetype": "t2.large",
                            "launchtime": "2020-11-13T05:34:50Z",
                            "resourcetype": "Instance"
                    },
                    "schemaversion": 2.0,
                    "service": {
                        "action": {
                            "actiontype": "NETWORK_CONNECTION",
                            "networkconnectionaction": {
                                "connectiondirection": "INBOUND",
                                "localportdetails": {
                                    "portname": "RDP"
                              }
                            }
                          }
                       },
                        "servicename": "guardduty"
                    },
                    "updatedat": "2020-11-16T05:25:41.862Z"
                }
            },
            "first_observed": "2020-11-16T00:33:13Z",
            "last_observed": "2020-11-16T05:13:15Z",
            "number_observed": 1
        }]
    } 
```

#### VPCFlow STIX observable output:

```json
{
    "type": "bundle",
    "id": "bundle--a98322c2-1016-49e9-b6ba-5744c79f146c",
    "spec_version": "2.0",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "aws_athena",
            "identity_class": "events"
        },
        {
            "id": "observed-data--75084cc5-2694-4843-99dc-c5fe2ab510a6",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2020-11-17T04:03:09.720Z",
            "modified": "2020-11-17T04:03:09.720Z",
            "objects": {
                "0": {
                    "type": "x-aws-details",
                    "account_id": 979326520502
                },
                "1": {
                    "type": "ipv4-addr",
                    "value": "172.31.62.249",
                    "x_aws_interface_id": "eni-04b762de832716892"
                },
                "2": {
                    "type": "network-traffic",
                    "src_ref": "1",
                    "dst_ref": "4",
                    "src_port": 8443,
                    "dst_port": 49715,
                    "protocols": [
                        "tcp"
                    ],
                    "start": "2020-06-19T07:59:08.000Z",
                    "end": "2020-06-19T07:59:24.000Z"
                },
                "3": {
                    "type": "x-ibm-finding",
                    "src_ip_ref": "1",
                    "dst_ip_ref": "4",
                    "start": "2020-06-19T07:59:08.000Z",
                    "end": "2020-06-19T07:59:24.000Z",
                    "finding_type": "network-traffic-accept",
                    "name": "VPC flow log"
                },
                "4": {
                    "type": "ipv4-addr",
                    "value": "172.31.76.105"
                },
                "5": {
                    "type": "x-aws-athena",
                    "logstatus": "OK",
                    "numbytes": 64662,
                    "numpackets": 61,
                    "version": 2
                }
            },
            "first_observed": "2020-06-19T07:59:08.000Z",
            "last_observed": "2020-06-19T07:59:24.000Z",
            "number_observed": 1
        }
    ]
}
```

## Sample 2:(Pattern expression with Custom IBM finding Attributes)

#### STIX patterns:

```
translate aws_athena query '{}' "[x-ibm-finding:name = '146.168.246.36 is performing SSH brute force attacks against i-03d7e6195920aa4c0.'] START t'2020-05-01T08:43:10.003Z' STOP t'2020-11-30T10:43:10.003Z'"
```

#### Translated query:

```
{
    "queries": [
        {
            "guardduty": "(lower(title) = lower('146.168.246.36 is performing SSH brute force attacks against i-03d7e6195920aa4c0.') AND updatedat BETWEEN '2020-05-01T08:43:10.003Z' AND '2020-11-30T10:43:10.003Z')"
        },
        {
            "ocsf": "(lower(observables.name) = lower('146.168.246.36 is performing SSH brute force attacks against i-03d7e6195920aa4c0.') AND _time BETWEEN 1588322590000 AND 1606732990000)"
        }
    ]
}
```

## Sample 3:(Multiple observation expression with OR operator)

#### STIX patterns:

```
translate aws_athena query '{}' "([network-traffic:src_port = '3389'] OR [domain-name:value = 'guarddutyc2activityb.com']) START t'2020-05-01T08:43:10.003Z' STOP t'2020-11-30T10:43:10.003Z'"
```

#### Translated query:

```
{
    "queries": [
        {
            "vpcflow": "(CAST(sourceport AS varchar) = '3389' AND start BETWEEN 1588322590 AND 1606732990)"
        },
        {
            "guardduty": "(((CAST(json_extract_scalar(service,'$.action.networkconnectionaction.localportdetails.port') AS varchar) = '3389' OR CAST(json_extract_scalar(service,'$.action.portprobeaction.localportdetails.port') AS varchar) = '3389') AND updatedat BETWEEN '2020-05-01T08:43:10.003Z' AND '2020-11-30T10:43:10.003Z') UNION ((lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.0.privatednsname')) = lower('guarddutyc2activityb.com') OR lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.1.privatednsname')) = lower('guarddutyc2activityb.com') OR lower(json_extract_scalar(resource,'$.instancedetails.networkinterfaces.0.publicdnsname')) = lower('guarddutyc2activityb.com') OR lower(json_extract_scalar(service,'$.action.dnsrequestaction.domain')) = lower('guarddutyc2activityb.com')) AND updatedat BETWEEN '2020-05-01T08:43:10.003Z' AND '2020-11-30T10:43:10.003Z'))"
        }
    ]
}
```

## Sample 4:(Multiple observation expression with AND operator)

#### STIX patterns:

```
translate aws_athena query '{}' "([x-aws-details:account_id = '979326520502'] AND [x-ibm-finding:finding_type = 'accept']) START t'2020-05-01T08:43:10.003Z' STOP t'2020-11-30T10:43:10.003Z'"
```

#### Translated query:

```
{
    "queries": [
        {
            "vpcflow": "((CAST(account AS varchar) = '979326520502' AND start BETWEEN 1588322590 AND 1606732990) INTERSECT (lower(action) = lower('accept') AND start BETWEEN 1588322590 AND 1606732990))"
        },
        {
            "guardduty": "((CAST(accountid AS varchar) = '979326520502' AND updatedat BETWEEN '2020-05-01T08:43:10.003Z' AND '2020-11-30T10:43:10.003Z') INTERSECT (lower(type) = lower('accept') AND updatedat BETWEEN '2020-05-01T08:43:10.003Z' AND '2020-11-30T10:43:10.003Z'))"
        },
        {
            "ocsf": "(lower(observables.type) = lower('accept') AND _time BETWEEN 1588322590000 AND 1606732990000)"
        }
    ]
}
```

### Exclusions 
Athena does not provide operator support for the following attributes,

`LIKE Operator`

* 'LIKE' Operator is not supported for vpcflow protocol field with wildcard characters.

`MATCHES Operator`

* 'MATCHES' Operator is not supported for vpcflow protocol field with regular expressions in the search query.

### STIX pattern for custom attributes and sample values
|  Description  |  STIX Pattern  |  Sample Values  |
| --- | --- | --- |
| Network Interface id of the EC2 instance  | ipv4-addr:x_aws_interface_id | [ipv4-addr:x_aws_interface_id = 'eni-0a70b0fa1a9cd3dbe'] |
| City name of Remote Ip address  | ipv4-addr:x_aws_remote_city_name | [ipv4-addr:x_aws_remote_city_name = 'Ashburn'] |
| Country name of Remote Ip address  | ipv4-addr:x_aws_remote_country_name | [ipv4-addr:x_aws_remote_country_name = 'United States'] |
| Network Interface id of the EC2 instance  | ipv6-addr:x_aws_interface_id | [ipv6-addr:x_aws_interface_id = 'eni-0a70b0fa1a9cd3dbe'] |
| AWS Account Id | x-aws-details:account_id | [x-aws:account_id = '979326520502'] |
| AWS Region | x-aws-details:aws_region | [x-aws:aws_region = 'us-east-1'] |
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
| Name of ibm finding | x-ibm-finding:name | [x-ibm-finding:name = '146.168.246.36 is performing SSH brute force attacks against i-03d7e6195920aa4c0.'] |
| Type of ibm finding | x-ibm-finding:finding_type | [x-ibm-finding:finding_type = 'Recon:IAMUser/NetworkPermissions'] |
| Description of ibm finding | x-ibm-finding:description | [x-ibm-finding:description = 'EC2 instance i-99999999 is generating unusually large amounts of network traffic to remote host 198.51.100.0.'] |
| Country name of Remote Ip address | x-ibm-finding:dst_geolocation | [x-ibm-finding:dst_geolocation = 'Russia'] |