# AWS GuardDuty

## Supported STIX Mappings

See the [table of mappings](aws_guardduty_supported_stix.md) for the STIX objects and operators supported by this connector.

**Table of Contents**
- [AWS GuardDuty API Endpoints](#AWSGuardDuty-api-endpoints)
- [Format of calling Stix shifter from Command Line](#format-for-calling-stix-shifter-from-the-command-line)
- [AWS Authentication Types](#aws-authentication-types)
- [AWS GuardDuty data search methods](#aws-guardduty-data-search-methods)
- [Pattern expression with STIX attributes - Single Observation](#single-observation)
- [Pattern expression with STIX and CUSTOM attributes - Multiple Observation](#multiple-observation)
- [STIX Execute Query](#stix-execute-query)
- [Observations](#observations)
- [Limitations](#limitations)
- [References](#references)

### AWSGuardDuty API Endpoints

   | Connector Method | AWS Guardduty API Endpoint                                                                                                                | Method |
   |-------------------------------------------------------------------------------------------------------------------------------------------|------|   ------|
   | Ping Endpoint    | List detector: /detector                                                                                                                  | GET|
   | Results Endpoint | 1. List Detector: /detector <br/> 2. List Findings: /detector/detectorId/findings<br/> 3. Get Findings: /detector/detectorId/findings/get | GET , POST |

### Format for calling stix-shifter from the command line
```
python main.py `<translator_module>` `<query or result>` `<STIX identity object>` `<data>`

```
### AWS Authentication Types

##### This connector supports two types of datasource authentication:

   1. Using user's security credentials (Access and Secret keys)
       ##### Sample Input:
        ```
        transmit
        "aws_guardduty"
        "{\"region\": \"<guardduty configured region>\"}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"yyyy\"}}"
        results <translated_query> offset length
        ``` 
   
   2. Using user's security credentials (Access and Secret keys) and IAM role (ARN value of the IAM role)
       ##### Sample Input:
        ```
        transmit
        "aws_guardduty"
        "{\"region\": \"<guardduty configured region>\"}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": 
        \"yyyy\",\"aws_iam_role\":\"zzzz\"}}"
        results <translated_query> offset length
        ```
### AWS GuardDuty Data search Methods
   1. Input without detector id
       #### Sample Input:
        ```
        transmit
        "aws_guardduty"
        "{\"region\": \"<guardduty configured region>\"}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"yyyy\"}}"
        results <translated_query> offset length
        ```

   2. Input with one or more Detector ids separated by comma as delimiter
        #### Sample Input:
        ```
        transmit
        "aws_guardduty"
        "{\"region\": \"<guardduty configured region>\",\"detector_ids\":\"123,456\"}"
        "{\"auth\":{\"aws_access_key_id\": \"xxxx\", \"aws_secret_access_key\": \"yyyy\"}}"
        results <translated_query> offset length
        

### Pattern expression with STIX and CUSTOM attributes

#### Single Observation

#### STIX Translate query 
```shell
translate aws_guardduty query "{}" "[network-traffic:src_port != 1234 AND autonomous-system:number < 50] START t'2023-01-15T00:00:00.000Z' STOP t'2023-06-30T00:00:00.000Z'"
```
#### STIX Translate query - Output
```json
{
    "queries": [
        {
            "FindingCriteria": {
                "Criterion": {
                    "service.action.networkConnectionAction.remoteIpDetails.organization.asn": {
                        "LessThan": 50
                    },
                    "updatedAt": {
                        "GreaterThanOrEqual": 1673740800000,
                        "LessThanOrEqual": 1688083200000
                    },
                    "service.action.networkConnectionAction.localPortDetails.port": {
                        "NotEquals": [
                            "1234"
                        ]
                    }
                }
            }
        },
        {
            "FindingCriteria": {
                "Criterion": {
                    "service.action.awsApiCallAction.remoteIpDetails.organization.asn": {
                        "LessThan": 50
                    },
                    "updatedAt": {
                        "GreaterThanOrEqual": 1673740800000,
                        "LessThanOrEqual": 1688083200000
                    },
                    "service.action.networkConnectionAction.localPortDetails.port": {
                        "NotEquals": [
                            "1234"
                        ]
                    }
                }
            }
        }
    ]
}
```
#### STIX Transmit results - Query
```shell
transmit
aws_guardduty
"{\"region\":\"xxxx\"}"
"{\"auth\":{\"aws_access_key_id\": \"abc\",\"aws_secret_access_key\":\"xyz\",\"aws_iam_role\":\"123zxy\"}}"
results
"{ \"queries\": [ { \"FindingCriteria\": { \"Criterion\": { \"service.action.networkConnectionAction.remoteIpDetails.organization.asn\": { \"LessThan\": 50 }, \"updatedAt\": { \"GreaterThanOrEqual\": 1673740800000, \"LessThanOrEqual\": 1688083200000 }, \"service.action.networkConnectionAction.localPortDetails.port\": { \"NotEquals\": [ \"1234\" ] } } } }, { \"FindingCriteria\": { \"Criterion\": { \"service.action.awsApiCallAction.remoteIpDetails.organization.asn\": { \"LessThan\": 50 }, \"updatedAt\": { \"GreaterThanOrEqual\": 1673740800000, \"LessThanOrEqual\": 1688083200000 }, \"service.action.networkConnectionAction.localPortDetails.port\": { \"NotEquals\": [ \"1234\" ] } } } } ] }"
0
1

```
#### STIX Transmit results - Output
```json
{
    "success": true,
    "data": [{
       "AccountId": "912345678901",
       "Arn": "arn:aws:guardduty:us-east-1:912345678901:detector/abcdefghijklmn/finding/12345678910abcdef",
       "CreatedAt": "2023-06-05T04:48:34.491Z",
       "Description": "EC2 instance i-0b123456abcdefghi is communicating with an Unusual DNS Resolver 8.8.8.8.",
       "Id": "12345678910abcdef",
       "Partition": "aws",
       "Region": "us-east-1",
       "Resource": {
           "InstanceDetails": {
               "AvailabilityZone": "us-east-1c",
               "ImageId": "ami-0b123456789abcde",
               "InstanceId": "i-0b123456abcdefghi",
               "InstanceState": "running",
               "InstanceType": "t2.medium",
               "OutpostArn": null,
               "LaunchTime": "2023-06-05T03:50:36.000Z",
               "NetworkInterfaces": [{
                   "Ipv6Addresses": [],
                   "NetworkInterfaceId": "eni-055726ef79287c018",
                   "PrivateDnsName": "ip-1-1-1-1.ec2.internal",
                   "PrivateIpAddress": "1.1.1.1",
                   "PrivateIpAddresses": [{
                       "PrivateDnsName": "ip-1-1-1-1.ec2.internal"
                   }],
                   "PublicDnsName": "ec2-2-2-2-2.compute-1.amazonaws.com",
                   "PublicIp": "2.2.2.2",
                   "SecurityGroups": [{
                       "GroupId": "sg-07a9c2h8f2f18e7a6",
                       "GroupName": "launch-wizard-31"
                   }],
                   "SubnetId": "subnet-58ch16f",
                   "VpcId": "vpc-10db926a"
               }],
               "Platform": "windows",
               "ProductCodes": [],
               "Tags": [{
                   "Key": "Name",
                   "Value": "local-machine"
               }]
           },
           "ResourceType": "Instance"
       },
       "SchemaVersion": "2.0",
       "Service": {
           "Action": {
               "ActionType": "NETWORK_CONNECTION",
               "NetworkConnectionAction": {
                   "Blocked": false,
                   "ConnectionDirection": "OUTBOUND",
                   "LocalPortDetails": {
                       "Port": 51923,
                       "PortName": "Unknown"
                   },
                   "Protocol": "UDP",
                   "LocalIpDetails": {
                       "IpAddressV4": "1.1.1.1"
                   },
                   "RemoteIpDetails": {
                       "City": {
                           "CityName": "Los Angeles"
                       },
                       "Country": {
                           "CountryName": "United States"
                       },
                       "GeoLocation": {
                           "Lat": 34.0544,
                           "Lon": -118.2441
                       },
                       "IpAddressV4": "8.8.8.8",
                       "Organization": {
                           "Asn": "15169",
                           "AsnOrg": "GOOGLE",
                           "Isp": "Google",
                           "Org": "Google"
                       }
                   },
                   "RemotePortDetails": {
                       "Port": 53,
                       "PortName": "DNS"
                   }
               }
           },
           "Archived": false,
           "Count": 1,
           "DetectorId": "abcdefghijklmn",
           "EventFirstSeen": "2023-06-05T04:46:40.000Z",
           "EventLastSeen": "2023-06-05T04:47:36.000Z",
           "ResourceRole": "ACTOR",
           "ServiceName": "guardduty",
           "AdditionalInfo": {
               "Value": "{\"inBytes\":\"152\",\"outBytes\":\"56\",\"unusual\":\"GOOGLE\"}",
               "Type": "default"
           }
       },
       "Severity": 5,
       "Title": "EC2 instance i-0b123456abcdefghi is communicating with an Unusual DNS Resolver 8.8.8.8.",
       "Type": "DefenseEvasion:EC2/UnusualDNSResolver",
       "UpdatedAt": "2023-06-05T04:48:34.491Z",
       "FindingType": "alert"
    }],
    "metadata": {
        "result_count": 1,
        "next_page_token": "abc",
        "detector_ids": []
    }
}
```
#### STIX Translate results
```json
{
    "type": "bundle",
    "id": "bundle--46aa4c44-9ba5-4977-a00f-725759392a56",
    "objects": [
        {
            "type": "identity",
            "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "name": "aws_guardduty",
            "identity_class": "events",
            "created": "2023-07-05T10:22:50.336Z",
            "modified": "2023-07-05T10:22:50.336Z"
        },
        {
            "id": "observed-data--a4919982-48c2-4ee9-bcb9-f7376a62930e",
            "type": "observed-data",
            "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
            "created": "2023-06-05T10:26:40.410Z",
            "modified": "2023-06-05T10:26:40.410Z",
            "objects": {
                "0": {
                    "type": "x-aws-resource",
                    "account_id": "912345678901",
                    "partition": "aws",
                    "region": "us-east-1",
                    "instance_ref": "2",
                    "resource_type": "Instance",
                    "resource_role": "ACTOR"
                },
                "1": {
                    "type": "x-ibm-finding",
                    "x_resource_ref": "0",
                    "x_arn": "arn:aws:guardduty:us-east-1:912345678901:detector/abcdefghijklmn/finding/12345678910abcdef",
                    "description": "EC2 instance i-0b123456abcdefghi is communicating with an Unusual DNS Resolver 8.8.8.8.",
                    "alert_id": "12345678910abcdef",
                    "x_schema_version": "2.0",
                    "x_service_ref": "8",
                    "x_archived": false,
                    "event_count": 1,
                    "x_detector_id": "abcdefghijklmn",
                    "severity": 5,
                    "x_title": "EC2 instance i-0b123456abcdefghi is communicating with an Unusual DNS Resolver 8.8.8.8.",
                    "name": "DefenseEvasion:EC2/UnusualDNSResolver",
                    "time_observed": "2023-06-05T04:48:34.491Z",
                    "finding_type": "alert"
                },
                "2": {
                    "type": "x-aws-instance",
                    "availability_zone": "us-east-1c",
                    "image_id": "ami-0b123456789abcde",
                    "instance_id": "i-0b123456abcdefghi",
                    "state": "running",
                    "instance_type": "t2.medium",
                    "launch_time": "2023-06-05T03:50:36.000Z",
                    "x_network_interface_refs": [
                        "3"
                    ],
                    "os_ref": "7",
                    "tags": [
                        {
                            "Key": "Name",
                            "Value": "local-machine"
                        }
                    ]
                },
                "3": {
                    "type": "x-aws-network-interface",
                    "interface_id": "eni-055726ef79287c018",
                    "private_domain_refs": [
                        "4"
                    ],
                    "public_domain_ref": "5",
                    "security_groups": [
                        {
                            "GroupId": "sg-07a9c2h8f2f18e7a6",
                            "GroupName": "launch-wizard-31"
                        }
                    ],
                    "subnet_id": "subnet-58ch16f",
                    "vpc_id": "vpc-10db926a"
                },
                "4": {
                    "type": "domain-name",
                    "value": "ip-1-1-1-1.ec2.internal"
                },
                "5": {
                    "type": "domain-name",
                    "value": "ec2-2-2-2-2.compute-1.amazonaws.com",
                    "resolves_to_refs": [
                        "6"
                    ]
                },
                "6": {
                    "type": "ipv4-addr",
                    "value": "2.2.2.2"
                },
                "7": {
                    "type": "software",
                    "name": "windows"
                },
                "8": {
                    "type": "x-aws-finding-service",
                    "action": {
                        "action_type": "NETWORK_CONNECTION",
                        "network_ref": "9"
                    },
                    "event_first_seen": "2023-06-05T04:46:40.000Z",
                    "event_last_seen": "2023-06-05T04:47:36.000Z",
                    "additional_info": {
                        "Value": "{\"inBytes\":\"152\",\"outBytes\":\"56\",\"unusual\":\"GOOGLE\"}",
                        "Type": "default"
                    }
                },
                "9": {
                    "type": "network-traffic",
                    "x_is_target_port_blocked": false,
                    "x_direction": "OUTBOUND",
                    "src_port": 51923,
                    "x_src_port_name": "Unknown",
                    "protocols": [
                        "udp"
                    ],
                    "src_ref": "10",
                    "dst_ref": "12",
                    "dst_port": 53,
                    "x_dst_port_name": "DNS"
                },
                "10": {
                    "type": "ipv4-addr",
                    "value": "1.1.1.1"
                },
                "11": {
                    "type": "x-oca-geo",
                    "city_name": "Los Angeles",
                    "country_name": "United States",
                    "location": {
                        "Lat": 34.0544,
                        "Lon": -118.2441
                    }
                },
                "12": {
                    "type": "ipv4-addr",
                    "x_geo_ref": "11",
                    "value": "8.8.8.8",
                    "belongs_to_refs": [
                        "13"
                    ]
                },
                "13": {
                    "type": "autonomous-system",
                    "number": 15169,
                    "name": "GOOGLE",
                    "x_isp": "Google",
                    "x_organisation": "Google"
                }
            },
            "first_observed": "2023-06-05T04:48:34.491Z",
            "last_observed": "2023-06-05T04:48:34.491Z",
            "number_observed": 1
        }
    ],
    "spec_version": "2.0"
}
```
#### Multiple Observation
```shell
translate aws_guardduty query {} "([x-aws-finding-service:action.action_type = 'AWS_API_CALL' AND user-account:display_name = 'awsathenauser' OR x-aws-s3-bucket:bucket_type = 'Destination'] AND [network-traffic:protocols[*] = 'UDP']) START t'2022-01-01T16:43:26.000Z' STOP t'2023-06-20T16:43:26.003Z'"  
```
#### STIX Multiple observation - Output
```json
{
    "queries": [
        {
            "FindingCriteria": {
                "Criterion": {
                    "resource.s3BucketDetails.type": {
                        "Equals": [
                            "Destination"
                        ]
                    },
                    "updatedAt": {
                        "GreaterThanOrEqual": 1641055406000,
                        "LessThanOrEqual": 1687279406003
                    }
                }
            }
        },
        {
            "FindingCriteria": {
                "Criterion": {
                    "service.action.actionType": {
                        "Equals": [
                            "AWS_API_CALL"
                        ]
                    },
                    "updatedAt": {
                        "GreaterThanOrEqual": 1641055406000,
                        "LessThanOrEqual": 1687279406003
                    }
                }
            }
        },
        {
            "FindingCriteria": {
                "Criterion": {
                    "resource.accessKeyDetails.userName": {
                        "Equals": [
                            "awsathenauser"
                        ]
                    },
                    "updatedAt": {
                        "GreaterThanOrEqual": 1641055406000,
                        "LessThanOrEqual": 1687279406003
                    }
                }
            }
        },
        {
            "FindingCriteria": {
                "Criterion": {
                    "resource.kubernetesDetails.kubernetesUserDetails.username": {
                        "Equals": [
                            "awsathenauser"
                        ]
                    },
                    "updatedAt": {
                        "GreaterThanOrEqual": 1641055406000,
                        "LessThanOrEqual": 1687279406003
                    }
                }
            }
        },
        {
            "FindingCriteria": {
                "Criterion": {
                    "service.action.networkConnectionAction.protocol": {
                        "Equals": [
                            "UDP"
                        ]
                    },
                    "updatedAt": {
                        "GreaterThanOrEqual": 1641055406000,
                        "LessThanOrEqual": 1687279406003
                    }
                }
            }
        }
    ]
}
```
### STIX Execute query
```shell
execute
aws_guardduty
aws_guardduty
"{\"type\":\"identity\",\"id\":\"identity--f431f809-377b-45e0-aa1c-6a4751cae5ff\",\"name\":\"aws_guardduty\",\"identity_class\":\"system\",\"created\":\"2023-07-05T13:22:50.336Z\",\"modified\":\"2023-07-05T13:22:50.336Z\"}"
"{\"region\":\"us-east-1\"}"
"{\"auth\":{\"aws_access_key_id\": \"ABC\",\"aws_secret_access_key\":\"xyz\"}}"
"[ipv4-addr:value = '4.5.6.7' AND x-aws-s3-bucket:bucket_type = 'Destination'] START t'2022-01-01T16:43:26.000Z' STOP t'2023-06-20T16:43:26.003Z'"
```

#### STIX Execute query - Output
```json
{
    "id": "observed-data--a618ce27-47e0-48b0-8b7c-b002c9c8bed6",
    "type": "observed-data",
    "created_by_ref": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "created": "2023-07-17T09:26:05.008Z",
    "modified": "2023-07-17T09:26:05.008Z",
    "objects": {
        "0": {
            "type": "x-aws-resource",
            "account_id": "912345678901",
            "partition": "aws",
            "region": "us-east-1",
            "access_key_ref": "2",
            "s3_bucket_refs": [
                "3"
            ],
            "resource_type": "S3Bucket",
            "resource_role": "TARGET"
        },
        "1": {
            "type": "x-ibm-finding",
            "x_resource_ref": "0",
            "x_arn": "arn:aws:guardduty:us-east-1:912345678901:detector/aabbccdd/finding/xyz",
            "description": "An API was used to access a bucket from an IP address on a custom threat list.",
            "alert_id": "xyz",
            "x_schema_version": "2.0",
            "x_service_ref": "4",
            "x_archived": false,
            "event_count": 2,
            "x_detector_id": "aabbccdd",
            "severity": 8,
            "x_title": "API DeleteObjects was invoked from an IP address on a custom threat list.",
            "name": "UnauthorizedAccess:S3/MaliciousIPCaller.Custom",
            "time_observed": "2023-06-08T08:22:11.192Z",
            "finding_type": "alert"
        },
        "2": {
            "type": "user-account",
            "x_access_key_id": "AABBZZ",
            "user_id": "ABCD",
            "display_name": "user@login.com",
            "x_user_type": "IAMUser"
        },
        "3": {
            "type": "x-aws-s3-bucket",
            "arn": "arn:aws:s3:::sampleguardtest",
            "name": "sampleguardtest",
            "bucket_type": "Destination",
            "created_at": "2023-06-08T07:27:58.000Z",
            "canonical_id_of_bucket_owner": "1234",
            "server_side_encryption_type": "AES256",
            "permissions": {
                "bucket_level": {
                    "access_control_policies": {
                        "allows_public_read_access": false,
                        "allows_public_write_access": false
                    },
                    "bucket_policies": {
                        "allows_public_read_access": false,
                        "allows_public_write_access": false
                    },
                    "block_public_access_settings": {
                        "ignore_public_acls": true,
                        "restrict_public_buckets": true,
                        "block_public_acls": true,
                        "block_public_policy": true
                    }
                },
                "account_level": {
                    "ignore_public_acls": false,
                    "restrict_public_buckets": false,
                    "block_public_acls": false,
                    "block_public_policy": false
                }
            },
            "bucket_permission": "NOT_PUBLIC"
        },
        "4": {
            "type": "x-aws-finding-service",
            "action": {
                "action_type": "AWS_API_CALL",
                "api_called": "DeleteObjects",
                "caller_type": "Remote IP",
                "remote_ref": "6",
                "service_name": "s3.amazonaws.com",
                "affected_resources": {}
            },
            "evidence_refs": [
                "8"
            ],
            "event_first_seen": "2023-06-08T08:17:05.000Z",
            "event_last_seen": "2023-06-08T08:17:05.000Z",
            "additional_info": {
                "Value": "{\"threatName\":\"Customer Threat Intel\",\"threatListName\":\"threat-list2\",\"authenticationMethod\":\"AuthHeader\"}",
                "Type": "default"
            }
        },
        "5": {
            "type": "x-oca-geo",
            "city_name": "Ashburn",
            "country_name": "United States",
            "location": {
                "Lat": 39.0469,
                "Lon": -77.4903
            }
        },
        "6": {
            "type": "ipv4-addr",
            "x_geo_ref": "5",
            "value": "4.5.6.7",
            "belongs_to_refs": [
                "7"
            ]
        },
        "7": {
            "type": "autonomous-system",
            "number": 14618,
            "name": "AMAZON-AES",
            "x_isp": "Amazon.com",
            "x_organisation": "Amazon.com"
        },
        "8": {
            "type": "x-aws-evidence",
            "threat_intelligence_list_name": "threat-list2",
            "threat_names": [
                "Customer Threat Intel"
            ]
        }
    },
    "first_observed": "2023-06-08T08:22:10.062Z",
    "last_observed": "2023-06-08T08:22:11.192Z",
    "number_observed": 2
}
```
### Observations
- Since AWS GuardDuty doesn't support OR operator, individual queries will be formed for each stix attribute when the pattern contains either
  only OR operator or combination of AND, OR operator.
- If AND operator is used between same stix attribute, exception will be thrown.
- If AND operator is used between different stix attribute which contains same field mappings(Example: network-traffic:src_ref AND ipv4-addr), 
  exception will be thrown.
- Exception will be thrown when more than 50 values are provided using IN operator in AWS GuardDuty connector.
- Exception will be thrown when more than 50 attributes are present in a single stix translate query in AWS GuardDuty connector.
- As of now, latest version AioBoto3 package is not returning LamdaDetails from AWS GuardDuty.But Boto3 package is returning Lambda details. 
  AioBoto3 may return in updated versions, once it is in compliance with latest Boto3 package.

### Limitations
- AWS GuardDuty Datasource doesn't support OR operator.
- AWS GuardDuty Datasource does not support LIKE/MATCHES operators.
- AWS GuardDuty Datasource can hold a minimum of one attribute and up to a maximum of 50 attributes in a single Finding Criteria.
- AWS GuardDuty Datasource supports maximum of 50 values while using equals and not equals operator.

### References
- [Amazon GuardDuty User Guide](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
- [Amazon GuardDuty API Reference](https://docs.aws.amazon.com/guardduty/latest/APIReference/Welcome.html)
- [Amazon GuardDuty List Finding ](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListFindings.html)
- [Amazon GuardDuty List Detectors ](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_ListDetectors.html)
- [Amazon GuardDuty Get Findings](https://docs.aws.amazon.com/guardduty/latest/APIReference/API_GetFindings.html)
