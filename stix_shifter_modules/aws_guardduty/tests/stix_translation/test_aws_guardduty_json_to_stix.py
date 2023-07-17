""" test script to perform unit test case for aws_guardduty translate results """
import unittest
from stix_shifter_modules.aws_guardduty.entry_point import EntryPoint
from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers

MODULE = "aws_guardduty"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "aws_guardduty",
    "identity_class": "events"
}
options = {}

aws_guardduty_sample_response = {
    "AccountId": "12345678910",
    "Arn": "arn:aws:guardduty:us-east-1:12345678910:detector/123abc456def789ghi/finding/"
           "123abc456def789ghi123456",
    "CreatedAt": "2023-05-05T06:12:49.891Z",
    "Description": "15.116.116.115 is performing RDP brute force attacks against i-0bc12345678910. "
                   "Brute force attacks are used to gain unauthorized access to your instance "
                   "by guessing the RDP password.",
    "Id": "123abc456def789ghi123456",
    "Partition": "aws",
    "Region": "us-east-1",
    "Resource": {
        "InstanceDetails": {
            "AvailabilityZone": "us-east-1c",
            "ImageId": "ami-0b12345678910",
            "InstanceId": "i-0bc12345678910",
            "InstanceState": "running",
            "InstanceType": "t2.medium",
            "LaunchTime": "2023-05-04T04:18:46.000Z",
            "NetworkInterfaces": [
                {
                    "Ipv6Addresses": [],
                    "NetworkInterfaceId": "eni-025723cd79287c910",
                    "PrivateDnsName": "ip-11-111-111-111.ec2.internal",
                    "PrivateIpAddress": "11.111.111.111",
                    "PrivateIpAddresses": [
                        {
                            "PrivateDnsName": "ip-11-111-111-111.ec2.internal"
                        }
                    ],
                    "PublicDnsName": "ec2-22-112-112-112.compute-1.amazonaws.com",
                    "PublicIp": "22.112.112.112",
                    "SecurityGroups": [
                        {
                            "GroupId": "sg-07a9c258f2c08e2a3",
                            "GroupName": "launch-wizard-31"
                        }
                    ],
                    "SubnetId": "subnet-11111",
                    "VpcId": "vpc-11111"
                }
            ],
            "Platform": "windows",
            "ProductCodes": [],
            "Tags": [
                {
                    "Key": "Name",
                    "Value": "cp4s_proofpoint_development"
                }
            ]
        },
        "ResourceType": "Instance"
    },
    "SchemaVersion": "2.0",
    "Service": {
        "Action": {
            "ActionType": "NETWORK_CONNECTION",
            "NetworkConnectionAction": {
                "Blocked": 'false',
                "ConnectionDirection": "INBOUND",
                "LocalPortDetails": {
                    "Port": 3389,
                    "PortName": "RDP"
                },
                "Protocol": "TCP",
                "LocalIpDetails": {
                    "IpAddressV4": "11.111.111.111"
                },
                "RemoteIpDetails": {
                    "City": {
                        "CityName": "Berlin"
                    },
                    "Country": {
                        "CountryName": "Germany"
                    },
                    "GeoLocation": {
                        "Lat": 52.5196,
                        "Lon": 13.4069
                    },
                    "IpAddressV4": "15.116.116.115",
                    "Organization": {
                        "Asn": "174",
                        "AsnOrg": "COGENT-174",
                        "Isp": "Cogent Communications",
                        "Org": "Cogent Communications"
                    }
                },
                "RemotePortDetails": {
                    "Port": 49163,
                    "PortName": "Unknown"
                }
            }
        },
        "Archived": 'false',
        "Count": 43,
        "DetectorId": "abcdefghij123456",
        "EventFirstSeen": "2023-05-05T05:59:51.000Z",
        "EventLastSeen": "2023-05-05T13:08:11.000Z",
        "ResourceRole": "TARGET",
        "ServiceName": "guardduty",
        "AdditionalInfo": {
            "Value": "{}",
            "Type": "default"
        }
    },
    "Severity": 2,
    "Title": "15.116.116.115 is performing RDP brute force attacks against i-0bc12345678910.",
    "Type": "UnauthorizedAccess:EC2/RDPBruteForce",
    "UpdatedAt": "2023-05-05T13:13:02.364Z",
    "FindingType": "alert"
}

aws_guardduty_sample_response_2 = {
    "AccountId": "12345678910",
    "Arn": "arn:aws:guardduty:us-east-1:12345678910:detector/123abc456def789ghi/"
           "finding/0011c11111404002875f3ab698ae5b9b",
    "CreatedAt": "2023-03-29T07:26:01.797Z",
    "Description": "API GeneratedFindingAPIName was used to access bucket GeneratedFindingS3Bucket "
                   "from Tor exit node IP address 111.11.000.1.",
    "Id": "0011c11111404002875f3ab698ae5b9b",
    "Partition": "aws",
    "Region": "us-east-1",
    "Resource": {
        "AccessKeyDetails": {
            "AccessKeyId": "GeneratedFindingAccessKeyId",
            "PrincipalId": "GeneratedFindingPrincipalId",
            "UserName": "GeneratedFindingUserName",
            "UserType": "IAMUser"
        },
        "S3BucketDetails": [
            {
                "Arn": "arn:aws:s3:::bucketName",
                "Name": "bucketName",
                "Type": "Destination",
                "CreatedAt": "2017-12-18 21:28:11.551000+05:30",
                "Owner": {
                    "Id": "CanonicalId of Owner"
                },
                "Tags": [
                    {
                        "Key": "foo",
                        "Value": "bar"
                    }
                ],
                "DefaultServerSideEncryption": {
                    "EncryptionType": "SSEAlgorithm",
                    "KmsMasterKeyArn": "arn:aws:kms:region:1111111111:key/key-id"
                },
                "PublicAccess": {
                    "PermissionConfiguration": {
                        "BucketLevelPermissions": {
                            "AccessControlList": {
                                "AllowsPublicReadAccess": 'false',
                                "AllowsPublicWriteAccess": 'false'
                            },
                            "BucketPolicy": {
                                "AllowsPublicReadAccess": 'false',
                                "AllowsPublicWriteAccess": 'false'
                            },
                            "BlockPublicAccess": {
                                "IgnorePublicAcls": 'false',
                                "RestrictPublicBuckets": 'false',
                                "BlockPublicAcls": 'false',
                                "BlockPublicPolicy": 'false'
                            }
                        },
                        "AccountLevelPermissions": {
                            "BlockPublicAccess": {
                                "IgnorePublicAcls": 'false',
                                "RestrictPublicBuckets": 'false',
                                "BlockPublicAcls": 'false',
                                "BlockPublicPolicy": 'false'
                            }
                        }
                    },
                    "EffectivePermission": "NOT_PUBLIC"
                }
            }
        ],
        "InstanceDetails": {
            "AvailabilityZone": "GeneratedFindingInstaceAvailabilityZone",
            "IamInstanceProfile": {
                "Arn": "arn:aws:iam::12345678910:example/instance/profile",
                "Id": "GeneratedFindingInstanceProfileId"
            },
            "ImageDescription": "GeneratedFindingInstaceImageDescription",
            "ImageId": "ami-100000000",
            "InstanceId": "i-10000000",
            "InstanceState": "running",
            "InstanceType": "m3.xlarge",
            "OutpostArn": "arn:aws:outposts:us-west-2:123456789000:outpost/op-0fbc006e9abbc73c3",
            "LaunchTime": "2016-08-02T02:05:06.000Z",
            "NetworkInterfaces": [
                {
                    "Ipv6Addresses": [],
                    "NetworkInterfaceId": "eni-aaaaaa88",
                    "PrivateDnsName": "GeneratedFindingPrivateDnsName",
                    "PrivateIpAddress": "10.0.0.1",
                    "PrivateIpAddresses": [
                        {
                            "PrivateDnsName": "GeneratedFindingPrivateName",
                            "PrivateIpAddress": "10.0.0.1"
                        }
                    ],
                    "PublicDnsName": "GeneratedFindingPublicDNSName",
                    "PublicIp": "111.11.000.1",
                    "SecurityGroups": [
                        {
                            "GroupId": "GeneratedFindingSecurityId",
                            "GroupName": "GeneratedFindingSecurityGroupName"
                        }
                    ],
                    "SubnetId": "GeneratedFindingSubnetId",
                    "VpcId": "GeneratedFindingVPCId"
                }
            ],
            "ProductCodes": [
                {
                    "Code": "GeneratedFindingProductCodeId",
                    "ProductType": "GeneratedFindingProductCodeType"
                }
            ],
            "Tags": [
                {
                    "Key": "GeneratedFindingInstaceTag1",
                    "Value": "GeneratedFindingInstaceValue1"
                }
            ]
        },
        "ResourceType": "S3Bucket"
    },
    "SchemaVersion": "2.0",
    "Service": {
        "Action": {
            "ActionType": "AWS_API_CALL",
            "AwsApiCallAction": {
                "Api": "GeneratedFindingAPIName",
                "CallerType": "Remote IP",
                "ErrorCode": "AccessDenied",
                "RemoteIpDetails": {
                    "City": {
                        "CityName": "GeneratedFindingCityName"
                    },
                    "Country": {
                        "CountryName": "GeneratedFindingCountryName"
                    },
                    "GeoLocation": {
                        "Lat": 0,
                        "Lon": 0
                    },
                    "IpAddressV4": "111.11.000.1",
                    "Organization": {
                        "Asn": "-1",
                        "AsnOrg": "GeneratedFindingASNOrg",
                        "Isp": "GeneratedFindingISP",
                        "Org": "GeneratedFindingORG"
                    }
                },
                "ServiceName": "GeneratedFindingAPIServiceName",
                "AffectedResources": {
                    "AWS::S3::Bucket": "GeneratedFindingS3Bucket"
                }
            }
        },
        "Archived": 'false',
        "Count": 4,
        "DetectorId": "123abc456def789ghi",
        "EventFirstSeen": "2023-03-29T07:26:01.000Z",
        "EventLastSeen": "2023-06-01T15:31:39.000Z",
        "ResourceRole": "TARGET",
        "ServiceName": "guardduty",
        "AdditionalInfo": {
            "Value": "{\"unusual\":{\"hoursOfDay\":[1513609200000],\"userNames\":"
                     "[\"GeneratedFindingUserName\"]},\"sample\":true}",
            "Type": "default"
        }
    },
    "Severity": 8,
    "Title": "API GeneratedFindingAPIName was invoked from a Tor exit node.",
    "Type": "UnauthorizedAccess:S3/TorIPCaller",
    "UpdatedAt": "2023-06-01T15:31:39.178Z",
    "FindingType": "alert"
}

aws_guardduty_sample_response_3 = {

    "AccountId": "10987654321",
    "Arn": "arn:aws:guardduty:us-east-1:10987654321:detector/2ab2e2ee222ed222f3b2ca22acdc24df/"
           "finding/12c12dd12dc12bf1ad12121ef1212cb",
    "CreatedAt": "2023-06-08T09:23:06.809Z",
    "Description": "AWS CloudTrail trail arn:aws:cloudtrail:us-east-1:10987654321:trail/"
                   "sampleguardtrail was disabled by abc@abc.com calling DeleteTrail under unusual "
                   "circumstances. This can be attackers attempt to cover their tracks by eliminating any "
                   "trace of activity performed while they accessed your account.",
    "Id": "12c12dd12dc12bf1ad12121ef1212cb",
    "Partition": "aws",
    "Region": "us-east-1",
    "Resource": {
        "AccessKeyDetails": {
            "AccessKeyId": "SSSSSSSSSSSSSSS",
            "PrincipalId": "AABBCCDDEEFFGGHHII",
            "UserName": "abc@abc.com",
            "UserType": "IAMUser"
        },
        "ResourceType": "AccessKey"
    },
    "SchemaVersion": "2.0",
    "Service": {
        "Action": {
            "ActionType": "AWS_API_CALL",
            "AwsApiCallAction": {
                "Api": "DeleteTrail",
                "CallerType": "Remote IP",
                "RemoteIpDetails": {
                    "City": {
                        "CityName": "Mumbai"
                    },
                    "Country": {
                        "CountryName": "India"
                    },
                    "GeoLocation": {
                        "Lat": 19.0748,
                        "Lon": 72.8856
                    },
                    "IpAddressV4": "222.22.222.22",
                    "Organization": {
                        "Asn": "396982",
                        "AsnOrg": "GOOGLE-CLOUD-PLATFORM",
                        "Isp": "Symantec Endpoint Protection",
                        "Org": "Symantec Endpoint Protection"
                    }
                },
                "ServiceName": "cloudtrail.amazonaws.com",
                "AffectedResources": {
                    "AWS::CloudTrail::Trail": "arn:aws:cloudtrail:us-east-1:10987654321:trail/"
                                              "sampleguardtrail"
                }
            }
        },
        "Archived": 'false',
        "Count": 1,
        "DetectorId": "2ab2e2ee222ed222f3b2ca22acdc24df",
        "EventFirstSeen": "2023-06-08T09:13:13.000Z",
        "EventLastSeen": "2023-06-08T09:13:13.000Z",
        "ResourceRole": "TARGET",
        "ServiceName": "guardduty",
        "AdditionalInfo": {
            "Value": "{}",
            "Type": "default"
        }
    },
    "Severity": 2,
    "Title": "AWS CloudTrail trail arn:aws:cloudtrail:us-east-1:10987654321:trail/"
             "sampleguardtrail was disabled.",
    "Type": "Stealth:IAMUser/CloudTrailLoggingDisabled",
    "UpdatedAt": "2023-06-08T09:23:06.809Z",
    "FindingType": "alert"
}
aws_guardduty_sample_response_4 = {

    "AccountId": "10987654321",
    "Arn": "arn:aws:guardduty:us-east-1:10987654321:detector/1ab1e6ee111ed111f11ca11acdc11df/"
           "finding/01fc453c5efe4cfd895a83ee6111111",
    "CreatedAt": "2023-03-29T07:26:01.798Z",
    "Description": "IP address 1.2.3.4, that is associated with known malicious activity, "
                   "unsuccessfully attempted to log in to RDS database GeneratedFindingDBInstanceId.",
    "Id": "01fc453c5efe4cfd895a83ee6111111",
    "Partition": "aws",
    "Region": "us-east-1",
    "Resource": {
        "ResourceType": "RDSDBInstance"
    },
    "SchemaVersion": "2.0",
    "Service": {
        "Action": {
            "ActionType": "RDS_LOGIN_ATTEMPT"
        },
        "Evidence": {
            "ThreatIntelligenceDetails": [
                {
                    "ThreatListName": "GeneratedFindingThreatListName",
                    "ThreatNames": [
                        "GeneratedFindingThreatName"
                    ]
                }
            ]
        },
        "Archived": 'false',
        "Count": 4,
        "DetectorId": "1ab1e6ee111ed111f11ca11acdc11df",
        "EventFirstSeen": "2023-03-29T07:26:01.000Z",
        "EventLastSeen": "2023-06-01T15:31:39.000Z",
        "ResourceRole": "TARGET",
        "ServiceName": "guardduty",
        "AdditionalInfo": {
            "Value": "{\"sample\":true}",
            "Type": "default"
        }
    },
    "Severity": 5,
    "Title": "An IP address that is associated with known malicious activity unsuccessfully attempted "
             "to log in to RDS database GeneratedFindingDBInstanceId.",
    "Type": "CredentialAccess:RDS/MaliciousIPCaller.FailedLogin",
    "UpdatedAt": "2023-06-01T15:31:39.180Z",
    "FindingType": "alert"
}


class TestAwsGuarddutyResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for aws_guardduty translate results
    """

    @staticmethod
    def get_first(itr, constraint):
        """
        return the obj in the itr if constraint is true
        """
        return next(
            (obj for obj in itr if constraint(obj)),
            None
        )

    @staticmethod
    def get_first_of_type(itr, typ):
        """
        to check whether the object belongs to respective stix object
        """
        return TestAwsGuarddutyResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    @staticmethod
    def get_observed_data_objects(data):
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        return observed_data['objects']

    def test_ipv4_addr_json_to_stix(self):
        """
        to test ipv4-addr stix object properties
        """
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response)
        ipv4_obj = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'ipv4-addr')
        assert (ipv4_obj.keys() == {'type', 'value'})
        assert ipv4_obj is not None
        assert ipv4_obj['type'] == 'ipv4-addr'
        assert ipv4_obj['value'] == '22.112.112.112'

    def test_network_traffic_json_to_stix(self):
        """
        to test network_traffic stix object properties
        """
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response)
        network_traffic_obj = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert (network_traffic_obj.keys() == {'type', 'x_is_target_port_blocked', 'x_direction',
                                               'src_port', 'x_src_port_name', 'protocols', 'src_ref',
                                               'dst_ref', 'dst_port', 'x_dst_port_name'})
        assert network_traffic_obj is not None
        assert network_traffic_obj['type'] == 'network-traffic'
        assert network_traffic_obj['x_is_target_port_blocked'] == 'false'
        assert network_traffic_obj['src_port'] == 3389
        assert network_traffic_obj['protocols'] == ['tcp']
        assert network_traffic_obj['x_direction'] == 'INBOUND'

        dst_ref = network_traffic_obj['dst_ref']
        assert (dst_ref in objects), f"dst_ref with key {network_traffic_obj['dst_ref']} " \
                                     f"not found"
        dst_obj = objects[dst_ref]
        assert dst_obj['type'] == 'ipv4-addr'
        src_ref = network_traffic_obj['src_ref']
        assert (src_ref in objects), f"src_ref with key {network_traffic_obj['src_ref']} " \
                                     f"not found"
        src_obj = objects[src_ref]
        assert src_obj['type'] == 'ipv4-addr'

    def test_x_aws_instance_json_to_stix(self):
        """
        to test x_aws_instance stix object properties
        """
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response)
        x_aws_instance_obj = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'x-aws-instance')
        assert (x_aws_instance_obj.keys() == {'type', 'availability_zone', 'image_id', 'instance_id', 'state',
                                              'instance_type', 'launch_time', 'x_network_interface_refs', 'os_ref',
                                              'tags'})

        assert x_aws_instance_obj is not None
        assert x_aws_instance_obj['type'] == 'x-aws-instance'
        assert x_aws_instance_obj['image_id'] == 'ami-0b12345678910'
        assert x_aws_instance_obj['instance_id'] == 'i-0bc12345678910'
        assert x_aws_instance_obj['availability_zone'] == 'us-east-1c'
        assert x_aws_instance_obj['state'] == 'running'
        assert x_aws_instance_obj['instance_type'] == 't2.medium'
        assert x_aws_instance_obj['launch_time'] == '2023-05-04T04:18:46.000Z'

        os_ref = x_aws_instance_obj['os_ref']
        assert (os_ref in objects), f"os_ref with key{x_aws_instance_obj['os_ref']}" f"not found"
        os_obj = objects[os_ref]
        assert os_obj['type'] == 'software'

        interface_ref = x_aws_instance_obj['x_network_interface_refs']
        assert (ref_value in objects for ref_value in interface_ref), \
            f"x_network_interface_refs with key {x_aws_instance_obj['x_network_interface_refs']} not found"

    def test_ibm_finding_json_to_stix(self):
        """
        to test x-ibm-finding stix object properties
        """
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response)
        ibm_finding_obj = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'x-ibm-finding')
        assert (ibm_finding_obj.keys() == {'type', 'x_arn', 'description', 'alert_id',
                                           'x_resource_ref', 'x_schema_version', 'x_service_ref',
                                           'x_archived', 'event_count', 'x_detector_id', 'severity', 'x_title',
                                           'name', 'time_observed', 'finding_type'})
        assert ibm_finding_obj is not None
        assert ibm_finding_obj['type'] == 'x-ibm-finding'
        assert ibm_finding_obj['alert_id'] == '123abc456def789ghi123456'
        assert ibm_finding_obj['x_archived'] == 'false'
        assert ibm_finding_obj['severity'] == 2
        assert ibm_finding_obj['event_count'] == 43

        assert ibm_finding_obj['name'] == 'UnauthorizedAccess:EC2/RDPBruteForce'
        assert ibm_finding_obj['description'] == "15.116.116.115 is performing RDP brute force attacks against " \
                                                 "i-0bc12345678910. " \
                                                 "Brute force attacks are used to gain unauthorized " \
                                                 "access to your instance by guessing the RDP password."
        assert ibm_finding_obj['x_detector_id'] == 'abcdefghij123456'

        x_service_ref = ibm_finding_obj['x_service_ref']
        assert (x_service_ref in objects), f"x_service_ref with key {ibm_finding_obj['x_service_ref']} " \
                                           f"not found"
        resource_ref = ibm_finding_obj['x_resource_ref']
        assert (resource_ref in objects), f" resource_ref with key " \
                                          f"{ibm_finding_obj['x_resource_ref']} " \
                                          f"not found"

    def test_autonomous_system_json_to_stix(self):
        """to test autonomous-system stix object properties"""
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response)
        autonomous_system_obj = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(),
                                                                                'autonomous-system')
        assert (autonomous_system_obj.keys() == {'type', 'number', 'name', 'x_isp', 'x_organisation'})
        assert autonomous_system_obj is not None
        assert autonomous_system_obj['type'] == 'autonomous-system'
        assert autonomous_system_obj['number'] == 174
        assert autonomous_system_obj['name'] == 'COGENT-174'
        assert autonomous_system_obj['x_isp'] == 'Cogent Communications'
        assert autonomous_system_obj['x_organisation'] == 'Cogent Communications'

    def test_x_oca_geo_json_to_stix(self):
        """to test x-oca-geo stix object properties"""
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response)
        x_oca_obj = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'x-oca-geo')
        assert (x_oca_obj.keys() == {'type', 'city_name', 'country_name', 'location'})
        assert x_oca_obj is not None
        assert x_oca_obj['type'] == 'x-oca-geo'
        assert x_oca_obj['city_name'] == 'Berlin'
        assert x_oca_obj['country_name'] == 'Germany'
        assert x_oca_obj['location']['Lat'] == 52.5196
        assert x_oca_obj['location']['Lon'] == 13.4069

    def test_resource_type_json_to_stix(self):
        """to test resource-type stix object properties"""
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response)
        resource_type = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'x-aws-resource')
        assert (resource_type.keys() == {'type', 'account_id', 'partition', 'region', 'resource_type',
                                         'resource_role', 'instance_ref'})
        assert resource_type is not None
        assert resource_type['type'] == 'x-aws-resource'
        assert resource_type['resource_type'] == 'Instance'
        assert resource_type['resource_role'] == 'TARGET'
        assert resource_type['account_id'] == '12345678910'

    def test_domain_name_json_to_stix(self):
        """to test domain-name stix object properties"""
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response)
        domain_name = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'domain-name')
        assert (domain_name.keys() == {'type', 'value'})
        assert domain_name is not None
        assert domain_name['type'] == 'domain-name'
        assert domain_name['value'] == 'ip-11-111-111-111.ec2.internal'

    def test_x_aws_network_interface_json_to_stix(self):
        """to test network-interface stix object properties"""
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response)
        x_aws_network_interface = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(),
                                                                                  'x-aws-network-interface')
        assert (x_aws_network_interface.keys() == {'type', 'interface_id', 'private_domain_refs', 'public_domain_ref',
                                                   'security_groups', 'subnet_id', 'vpc_id'})
        assert x_aws_network_interface is not None
        assert x_aws_network_interface['type'] == 'x-aws-network-interface'
        assert x_aws_network_interface['interface_id'] == 'eni-025723cd79287c910'
        assert x_aws_network_interface['subnet_id'] == 'subnet-11111'
        assert x_aws_network_interface['vpc_id'] == 'vpc-11111'
        security_gps = x_aws_network_interface['security_groups']
        assert (security_groups['GroupId'] == 'sg-07a9c258f2c08e2a3' and security_groups['GroupName'] ==
                'launch-wizard-31' for security_groups in security_gps)

        private_domain_refs = x_aws_network_interface['private_domain_refs']
        assert (private_domain in objects for private_domain in
                private_domain_refs), f"private_domain with key {x_aws_network_interface['private_domain_refs']} " \
                                      f"not found"
        public_domain_ref = x_aws_network_interface['public_domain_ref']
        assert (public_domain_ref in objects), f"public_domain_ref with key " \
                                               f"{x_aws_network_interface['public_domain_ref']}" f"not found"

    def test_x_aws_s3_bucket_json_to_stix(self):
        """to test x-aws-s3-bucket stix object properties"""
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response_2)
        x_aws_s3_bucket = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'x-aws-s3-bucket')
        assert (x_aws_s3_bucket.keys() == {'type', 'arn', 'name', 'bucket_type', 'created_at',
                                           'canonical_id_of_bucket_owner', 'tags', 'server_side_encryption_type',
                                           'kms_encryption_key_arn', 'permissions', 'bucket_permission'})
        assert x_aws_s3_bucket is not None
        assert x_aws_s3_bucket['type'] == 'x-aws-s3-bucket'
        assert x_aws_s3_bucket['arn'] == 'arn:aws:s3:::bucketName'
        assert x_aws_s3_bucket['name'] == 'bucketName'
        assert x_aws_s3_bucket['bucket_type'] == 'Destination'
        assert x_aws_s3_bucket['server_side_encryption_type'] == 'SSEAlgorithm'
        assert x_aws_s3_bucket['bucket_permission'] == 'NOT_PUBLIC'
        assert x_aws_s3_bucket['kms_encryption_key_arn'] == 'arn:aws:kms:region:1111111111:key/key-id'
        assert x_aws_s3_bucket['permissions']['bucket_level']['access_control_policies']['allows_public_read_access'] \
               is not True
        assert x_aws_s3_bucket['permissions']['bucket_level']['block_public_access_settings']['block_public_policy'] \
               is not True
        assert x_aws_s3_bucket['permissions']['account_level']['block_public_acls'] is not True

    def test_x_aws_finding_service_with_api_call_action_json_to_stix(self):
        """to test x-aws-finding-service stix object properties"""
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response_3)
        x_aws_finding_service = TestAwsGuarddutyResultsToStix. \
            get_first_of_type(objects.values(), 'x-aws-finding-service')
        assert (x_aws_finding_service.keys() == {'type', 'action', 'event_first_seen',
                                                 'event_last_seen', 'additional_info'})
        assert x_aws_finding_service is not None
        assert x_aws_finding_service['type'] == 'x-aws-finding-service'
        assert x_aws_finding_service['action']['action_type'] == 'AWS_API_CALL'
        assert x_aws_finding_service['action']['api_called'] == 'DeleteTrail'
        assert x_aws_finding_service['action']['caller_type'] == 'Remote IP'
        assert x_aws_finding_service['action']['service_name'] == 'cloudtrail.amazonaws.com'
        assert x_aws_finding_service['event_last_seen'] == '2023-06-08T09:13:13.000Z'
        remote_ref = x_aws_finding_service['action']['remote_ref']
        assert (remote_ref in objects), f"remote references with key " \
                                        f"{x_aws_finding_service['action']['remote_ref']} not found"

    def test_user_account_json_to_stix(self):
        """to test user-account stix object properties"""
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response_3)
        user_account = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'user-account')
        assert (user_account.keys() == {'type', 'x_access_key_id', 'user_id', 'display_name', 'x_user_type'})
        assert user_account is not None
        assert user_account['type'] == 'user-account'
        assert user_account['x_access_key_id'] == 'SSSSSSSSSSSSSSS'
        assert user_account['user_id'] == 'AABBCCDDEEFFGGHHII'
        assert user_account['display_name'] == 'abc@abc.com'
        assert user_account['x_user_type'] == 'IAMUser'

    def test_x_aws_evidence_json_to_stix(self):
        """to test x-aws-evidence stix object properties"""
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(aws_guardduty_sample_response_4)
        x_aws_evidence = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'x-aws-evidence')
        assert (x_aws_evidence.keys() == {'type', 'threat_intelligence_list_name', 'threat_names'})
        assert x_aws_evidence is not None
        assert x_aws_evidence['type'] == 'x-aws-evidence'
        assert x_aws_evidence['threat_intelligence_list_name'] == 'GeneratedFindingThreatListName'
        assert x_aws_evidence['threat_names'] == ["GeneratedFindingThreatName"]

    def test_x_aws_eks_cluster_json_to_stix(self):
        """to test x-aws-eks-cluster-details stix object properties"""
        data = {"Resource": {
            "EksClusterDetails": {
                "Name": "GeneratedFindingEKSClusterName",
                "Arn": "GeneratedFindingEKSClusterArn",
                "VpcId": "GeneratedFindingEKSClusterVpcId",
                "Status": "ACTIVE",
                "Tags": [
                    {
                        "Key": "GeneratedFindingEKSClusterTag1",
                        "Value": "GeneratedFindingEKSClusterTagValue1"
                    }
                ],
                "CreatedAt": "2021-11-11 15:45:55.218000+05:30"
            },
            "KubernetesDetails": {
                "KubernetesUserDetails": {
                    "Username": "GeneratedFindingUserName",
                    "Uid": "GeneratedFindingUID",
                    "Groups": [
                        "GeneratedFindingUserGroup"
                    ]
                },
                "KubernetesWorkloadDetails": {
                    "Name": "GeneratedFindingKubernetesWorkloadName",
                    "Type": "GeneratedFindingKubernetesWorkloadType",
                    "Uid": "GeneratedFindingKubernetesWorkloadUID",
                    "Namespace": "GeneratedFindingKubernetesWorkloadNamespace",
                    "Containers": [
                        {
                            "Name": "GeneratedFindingContainerName",
                            "Image": "GeneratedFindingContainerImage",
                            "ImagePrefix": "GeneratedFindingContainerImagePrefix",
                            "VolumeMounts": [
                                {
                                    "Name": "GeneratedFindingVolumeName",
                                    "MountPath": "GeneratedFindingVolumeMountPath"
                                }
                            ]
                        }
                    ],
                    "Volumes": [
                        {
                            "Name": "GeneratedFindingVolumeName",
                            "HostPath": {
                                "Path": "GeneratedFindingHostPath"
                            }
                        }
                    ]
                }
            },
            "ResourceType": "EKSCluster"
        },
            "SchemaVersion": "2.0",
        }

        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(data)
        resource = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'x-aws-resource')
        assert (resource.keys() == {'type', 'eks_cluster_ref', 'resource_type'})
        assert resource is not None
        eks_cluster_details_ref = resource['eks_cluster_ref']
        assert (eks_cluster_details_ref in objects), f"EKS Cluster details references with " \
                                                     f"key{resource['eks_cluster_ref']} not found"
        eks_cluster_details = objects[eks_cluster_details_ref]
        assert (eks_cluster_details.keys() == {'type', 'name', 'arn', 'vpc_id', 'status', 'tags', 'created_at',
                                               'kubernetes_user_ref', 'kubernetes_workload_ref'})
        assert eks_cluster_details is not None
        assert eks_cluster_details['type'] == 'x-aws-eks-cluster'
        assert eks_cluster_details['name'] == 'GeneratedFindingEKSClusterName'
        assert eks_cluster_details['arn'] == 'GeneratedFindingEKSClusterArn'
        assert eks_cluster_details['vpc_id'] == 'GeneratedFindingEKSClusterVpcId'
        assert eks_cluster_details['status'] == 'ACTIVE'
        kubernetes_workload_ref = eks_cluster_details['kubernetes_workload_ref']
        assert (kubernetes_workload_ref in objects), f"kubernetes_workload_ref with key" \
                                                     f"{eks_cluster_details['kubernetes_workload_ref']}" f"not found"
        kubernetes_user_ref = eks_cluster_details['kubernetes_user_ref']
        assert (kubernetes_user_ref in objects), f"kubernetes_user_ref with key" \
                                                 f"{eks_cluster_details['kubernetes_user_ref']}" f"not found"

        x_aws_kubernetes_workload = objects[kubernetes_workload_ref]
        assert (x_aws_kubernetes_workload.keys() == {'type', 'workload_name', 'workload_type',
                                                     'workload_id', 'workload_namespace', 'container_refs',
                                                     'volumes'})
        assert x_aws_kubernetes_workload is not None
        assert x_aws_kubernetes_workload['type'] == 'x-aws-kubernetes-workload'
        assert x_aws_kubernetes_workload['workload_name'] == 'GeneratedFindingKubernetesWorkloadName'
        assert x_aws_kubernetes_workload['workload_type'] == 'GeneratedFindingKubernetesWorkloadType'
        container_refs = x_aws_kubernetes_workload['container_refs']
        assert (container in objects for container in container_refs), \
            f"container_refs with key{x_aws_kubernetes_workload['container_refs']}" f"not found"

    def test_x_aws_container_json_to_stix(self):
        """to test x-aws-container stix object properties"""
        data = {
            "Resource": {
                "ResourceType": "EKSCluster",
                "ContainerDetails": {
                    "Id": "GeneratedFindingContainerId",
                    "Name": "GeneratedFindingContainerName",
                    "Image": "GeneratedFindingContainerImage",
                    "ImagePrefix": "GeneratedFindingContainerImagePrefix",
                    "VolumeMounts": [
                        {
                            "Name": "GeneratedFindingVolumeName",
                            "MountPath": "GeneratedFindingVolumeMountPath"
                        }
                    ]
                }
            },
            "SchemaVersion": "2.0"
        }
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(data)
        x_aws_container = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'x-aws-container')
        assert (x_aws_container.keys() == {'type', 'container_id', 'name', 'image', 'image_prefix',
                                           'volume_mount_refs'})
        assert x_aws_container is not None
        assert x_aws_container['type'] == 'x-aws-container'
        assert x_aws_container['container_id'] == 'GeneratedFindingContainerId'
        assert x_aws_container['name'] == 'GeneratedFindingContainerName'
        assert x_aws_container['image'] == 'GeneratedFindingContainerImage'
        volume_refs = x_aws_container['volume_mount_refs']
        assert (volume in objects for volume in volume_refs), \
            f"volume_mount_refs with key{x_aws_container['volume_mount_refs']} not found"
        for vol in volume_refs:
            assert (objects[vol].keys() == {'type', 'name', 'path'})

    def test_x_aws_ecs_cluster_details_json_to_stix(self):
        """to test x-aws-ecs-cluster-details stix object properties"""
        data = {
            "Resource": {
                "ResourceType": "ECSCluster",
                "EcsClusterDetails": {
                    "Name": "GeneratedFindingECSClusterName",
                    "Arn": "arn:aws:ecs:region:123456789000:cluster/clusterName",
                    "Status": "ACTIVE",
                    "Tags": [
                        {
                            "Key": "GeneratedFindingECSClusterTag1",
                            "Value": "GeneratedFindingECSClusterTagValue1"
                        }
                    ],
                    "TaskDetails": {
                        "Arn": "arn:aws:ecs:region:123456789000:task/mycluster/043de9ab3",
                        "DefinitionArn": "arn:aws:ecs:region:123456789000:task-definition/mycluster/76f1f1asdf",
                        "Version": "1",
                        "TaskCreatedAt": "2021-12-09 04:53:50+05:30",
                        "StartedAt": "2021-12-09 04:53:50+05:30",
                        "StartedBy": "GeneratedFindingECSTaskStartedBy",
                        "Containers": [
                            {
                                "Name": "GeneratedFindingContainerName",
                                "Image": "GeneratedFindingContainerImage"
                            }
                        ]
                    }
                }
            },
            "SchemaVersion": "2.0",
        }
        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(data)
        x_aws_ecs_cluster_details = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(),
                                                                                    'x-aws-ecs-cluster')
        assert (x_aws_ecs_cluster_details.keys() == {'type', 'name', 'cluster_arn', 'status', 'tags', 'task'})
        assert x_aws_ecs_cluster_details is not None
        assert x_aws_ecs_cluster_details['type'] == 'x-aws-ecs-cluster'
        assert x_aws_ecs_cluster_details['name'] == 'GeneratedFindingECSClusterName'
        assert x_aws_ecs_cluster_details['cluster_arn'] == 'arn:aws:ecs:region:123456789000:cluster/clusterName'
        assert x_aws_ecs_cluster_details['status'] == 'ACTIVE'
        assert x_aws_ecs_cluster_details['task']['arn'] == 'arn:aws:ecs:region:123456789000:task/mycluster/043de9ab3'
        assert x_aws_ecs_cluster_details['task']['definition_arn'] == \
               'arn:aws:ecs:region:123456789000:task-definition/mycluster/76f1f1asdf'
        assert x_aws_ecs_cluster_details['task']['version'] == '1'
        container_refs = x_aws_ecs_cluster_details['task']['container_refs']
        assert (container_ref in objects for container_ref in container_refs), \
            f"container_refs with key{x_aws_ecs_cluster_details['task']['container_refs']}" f"not found"

    def test_process_and_file_details_json_to_stix(self):
        """to test process and file details stix object properties"""
        data = {"Service": {
            "Evidence": {
                "ThreatIntelligenceDetails": [
                    {
                        "ThreatListName": "GeneratedFindingThreatListName",
                        "ThreatNames": [
                            "GeneratedFindingThreatName"
                        ]
                    }
                ]
            },
            "Archived": 'false',
            "Count": 4,
            "DetectorId": "123abc456def456ghij",
            "EventFirstSeen": "2023-06-01T15:31:22.000Z",
            "EventLastSeen": "2023-06-30T11:54:18.000Z",
            "ResourceRole": "TARGET",
            "ServiceName": "guardduty",
            "AdditionalInfo": {
                "Value": "{\"threatListName\":\"GeneratedFindingThreatListName\",\"sample\":true,\"agentDetails\":"
                         "{\"agentVersion\":\"1\",\"agentId\":\"GeneratedFindingAgentId\"}}",
                "Type": "default"
            },
            "FeatureName": "RuntimeMonitoring",
            "RuntimeDetails": {
                "Process": {
                    "Name": "GeneratedFindingProcessName",
                    "ExecutablePath": "GeneratedFindingPath",
                    "ExecutableSha256": "GeneratedFindingHash",
                    "Pwd": "GeneratedFindingPath",
                    "Pid": 1234,
                    "StartTime": "2023-06-01T13:14:57.000Z",
                    "Uuid": "GeneratedFindingUUId",
                    "ParentUuid": "GeneratedFindingUUId",
                    "User": "ec2-user",
                    "UserId": 1000,
                    "Euid": 1000,
                    "Lineage": [
                        {
                            "Pid": 1233,
                            "Uuid": "GeneratedFindingUUId",
                            "ExecutablePath": "GeneratedFindingPath",
                            "Euid": 1000,
                            "ParentUuid": "GeneratedFindingUUId"
                        },
                        {
                            "Pid": 1230,
                            "Uuid": "GeneratedFindingUUId",
                            "ExecutablePath": "GeneratedFindingPath",
                            "Euid": 1000,
                            "ParentUuid": "GeneratedFindingUUId"
                        }
                    ]
                },
                "Context": {
                    "ReleaseAgentPath": "GeneratedFindingPath"
                }
            }
        },
            "Severity": 8,
            "Title": "Container escape via cgroups was detected in EC2 instance i-99999999.",
            "Type": "PrivilegeEscalation:Runtime/CGroupsReleaseAgentModified",
            "UpdatedAt": "2023-06-30T11:54:18.614Z"
        }

        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(data)
        process = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'process')
        assert (process.keys() == {'type', 'name', 'binary_ref', 'cwd', 'pid', 'created',
                                   'x_unique_id', 'x_parent_unique_id', 'creator_user_ref', 'x_lineage_refs'})
        assert process is not None
        assert process['type'] == 'process'
        assert process['name'] == 'GeneratedFindingProcessName'
        assert process['cwd'] == 'GeneratedFindingPath'
        assert process['pid'] == 1234
        assert process['x_unique_id'] == 'GeneratedFindingUUId'
        assert process['x_parent_unique_id'] == 'GeneratedFindingUUId'
        x_lineage_refs = process['x_lineage_refs']
        assert (lineage in objects for lineage in x_lineage_refs), \
            f"x_lineage_refs with key{process['x_lineage_refs']}" f"not found"

        creator_user_ref = process['creator_user_ref']
        assert (creator_user_ref in objects), f"creator_user_ref with key {process['creator_user_ref']} " \
                                              f"not found"
        user = objects[creator_user_ref]
        assert user['type'] == 'user-account'

        binary_ref = process['binary_ref']
        assert (binary_ref in objects), f"binary_ref with key {process['binary_ref']} not found"
        file = objects[binary_ref]
        assert (file.keys() == {'type', 'x_path', 'hashes'})
        assert file['type'] == 'file'
        assert file['x_path'] == 'GeneratedFindingPath'
        assert file['hashes']['SHA-256'] == 'GeneratedFindingHash'

    def test_x_aws_rds_db_user_json_to_stix(self):
        """to test x-aws-rds-db-user stix object properties"""
        data = {
            "Resource": {
                "ResourceType": "RDSDBInstance",
                "RdsDbUserDetails": {
                    "User": "GeneratedFindingUserName",
                    "Application": "GeneratedFindingApplicationName",
                    "Database": "GeneratedFindingDatabaseName",
                    "Ssl": "GeneratedFindingSSLValue",
                    "AuthMethod": "GeneratedFindingAuthMethod"
                }
            }}

        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(data)
        rds_db_user = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'x-aws-rds-db-user')
        assert (rds_db_user.keys() == {'type', 'user_name', 'application_name', 'database_name',
                                       'ssl', 'authentication_method'})
        assert rds_db_user is not None
        assert rds_db_user['type'] == 'x-aws-rds-db-user'
        assert rds_db_user['user_name'] == 'GeneratedFindingUserName'
        assert rds_db_user['application_name'] == 'GeneratedFindingApplicationName'
        assert rds_db_user['database_name'] == 'GeneratedFindingDatabaseName'
        assert rds_db_user['ssl'] == 'GeneratedFindingSSLValue'
        assert rds_db_user['authentication_method'] == 'GeneratedFindingAuthMethod'

    def test_x_aws_rds_db_instance_json_to_stix(self):
        """to test x-aws-rds-db-instance stix object properties"""
        data = {
            "Resource": {
                "ResourceType": "RDSDBInstance",
                "RdsDbInstanceDetails": {
                    "DbInstanceIdentifier": "GeneratedFindingDBInstanceId",
                    "Engine": "GeneratedFindingEngine",
                    "EngineVersion": "13.6",
                    "DbClusterIdentifier": "GeneratedFindingDBClusterId",
                    "DbInstanceArn": "arn:aws:rds:us-east-1:12345678910:db:GeneratedFindingDBInstanceId",
                    "Tags": [
                        {
                            "Key": "GeneratedFindingRDSDBInstanceTag1",
                            "Value": "GeneratedFindingRDSDBInstanceValue1"
                        }
                    ]
                }
            }
        }

        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(data)
        rds_db_instance = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'x-aws-rds-db-instance')
        assert (rds_db_instance.keys() == {'type', 'instance_id', 'engine', 'engine_version',
                                           'cluster_id', 'instance_arn', 'tags'})
        assert rds_db_instance is not None
        assert rds_db_instance['type'] == 'x-aws-rds-db-instance'
        assert rds_db_instance['instance_id'] == 'GeneratedFindingDBInstanceId'
        assert rds_db_instance['engine'] == 'GeneratedFindingEngine'
        assert rds_db_instance['engine_version'] == '13.6'
        assert rds_db_instance['cluster_id'] == 'GeneratedFindingDBClusterId'
        assert rds_db_instance['instance_arn'] == 'arn:aws:rds:us-east-1:12345678910:db:GeneratedFindingDBInstanceId'

    def test_ebs_volume_details_json_to_stix(self):
        """to test EbsVolumeDetails stix object properties"""
        data = {
            "Resource": {
                "ResourceType": "Container",
                "EbsVolumeDetails": {
                    "ScannedVolumeDetails": [
                        {
                            "VolumeArn": "arn:aws:ec2:us-west-2:12345678910:volume/vol-09d5050dea915943d",
                            "VolumeType": "GeneratedScannedVolumeType",
                            "DeviceName": "GeneratedScannedDeviceName",
                            "VolumeSizeInGB": 8,
                            "EncryptionType": "UNENCRYPTED",
                            "SnapshotArn": "arn:aws:ec2:us-east-2:12345678910:snapshot/snap-12345678901234567",
                            "KmsKeyArn": 'null'
                        }
                    ]
                },
                "ContainerDetails": {
                    "Id": "abcdefghijklmn",
                    "Name": "GeneratedFindingContainerName",
                    "Image": "GeneratedFindingContainerImage"
                }
            },
            "SchemaVersion": "2.0",
            "Service": {
                "Archived": 'false',
                "Count": 6,
                "DetectorId": "abcdefghijklmn",
                "EventFirstSeen": "2023-03-29T07:26:01.000Z",
                "EventLastSeen": "2023-06-30T11:54:18.000Z",
                "ServiceName": "guardduty",
                "AdditionalInfo": {
                    "Value": "{\"sample\":true}",
                    "Type": "default"
                },
                "FeatureName": "EbsVolumeScan",
                "EbsVolumeScanDetails": {
                    "ScanId": "12345",
                    "ScanStartedAt": "2021-12-09T00:45:03.000Z",
                    "ScanCompletedAt": "2021-12-09T00:53:46.000Z",
                    "TriggerFindingId": "xyz",
                    "Sources": [
                        "Bitdefender"
                    ],
                    "ScanDetections": {
                        "ScannedItemCount": {
                            "TotalGb": 1,
                            "Files": 65226,
                            "Volumes": 1
                        },
                        "ThreatsDetectedItemCount": {
                            "Files": 2
                        },
                        "HighestSeverityThreatDetails": {
                            "Severity": "HIGH",
                            "ThreatName": "EICAR-Test-File",
                            "Count": 2
                        },
                        "ThreatDetectedByName": {
                            "ItemCount": 2,
                            "UniqueThreatNameCount": 1,
                            "Shortened": 'false',
                            "ThreatNames": [
                                {
                                    "Name": "EICAR-Test-File",
                                    "Severity": "HIGH",
                                    "ItemCount": 2,
                                    "FilePaths": [
                                        {
                                            "FilePath": "tmp/eicar.com",
                                            "VolumeArn": "arn:aws:ec2:us-west-2:12345678910:"
                                                         "volume/vol-09d5050dea915943d",
                                            "FileSha256": "a021bbfb6489e54d471899f7dbaaa9d1663fc345ec2fe2a2c4538aabf65"
                                                          "1fd0f",
                                            "FileName": "eicar.com"
                                        },
                                        {
                                            "FilePath": "tmp/eicar-2.txt",
                                            "VolumeArn": "arn:aws:ec2:us-west-2:12345678910:volume/"
                                                         "vol-09d5050dea915943d",
                                            "UnknownHash": "a021bbfb6489e54d471899f7db9d2363fc345ec2fe2a2c4538aabf651"
                                                           "ad0x",
                                            "FileName": "eicar-2.txt"
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                    "ScanType": "ON_DEMAND"
                }
            }
        }

        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(data)
        ebs_volume = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'x-aws-ebs-volume-malware-scan')
        assert (ebs_volume.keys() == {'type', 'scan_id', 'scan_started_time', 'scan_completed_at',
                                      'triggered_finding_id', 'sources', 'scanned_items', 'total_infected_files',
                                      'highest_severity_threat', 'threat_detected_by_name', 'scan_type'})
        assert ebs_volume is not None
        assert ebs_volume['type'] == 'x-aws-ebs-volume-malware-scan'
        assert ebs_volume['scan_id'] == '12345'
        assert ebs_volume['triggered_finding_id'] == 'xyz'
        assert ebs_volume['sources'] == ['Bitdefender']
        assert ebs_volume['scanned_items']['total_files_scanned_in_gb'] == 1
        assert ebs_volume['scanned_items']['total_scanned_files'] == 65226
        assert ebs_volume['scanned_items']['total_volumes_scanned'] == 1
        assert ebs_volume['total_infected_files'] == 2
        assert ebs_volume['highest_severity_threat']['severity'] == 'HIGH'
        assert ebs_volume['highest_severity_threat']['name'] == 'EICAR-Test-File'
        assert ebs_volume['highest_severity_threat']['total_infected_files'] == 2
        assert ebs_volume['threat_detected_by_name']['infected_files_count'] == 2
        assert ebs_volume['scan_type'] == 'ON_DEMAND'
        assert ebs_volume['threat_detected_by_name']['unique_threats_count_based_on_name'] == 1
        assert ebs_volume['threat_detected_by_name']['is_finding_shortened'] == 'false'
        threat_details_ref = ebs_volume['threat_detected_by_name']['threat_refs']
        assert (threat_details in objects for threat_details in threat_details_ref), \
            f"container_refs with key{ebs_volume['threat_detected_by_name']['threat_refs']}" f"not found"

    def test_kubernetes_api_call_json_to_stix(self):
        """to test kubernetes api call stix object properties"""
        data = {
            "Service": {
                "Action": {
                    "ActionType": "KUBERNETES_API_CALL",
                    "KubernetesApiCallAction": {
                        "Protocol": "http",
                        "RequestUri": "GeneratedFindingRequestURI",
                        "Verb": "create",
                        "UserAgent": "",
                        "RemoteIpDetails": {
                            "City": {
                                "CityName": "GeneratedFindingCityName"
                            },
                            "Country": {
                                "CountryName": "GeneratedFindingCountryName"
                            },
                            "GeoLocation": {
                                "Lat": 0,
                                "Lon": 0
                            },
                            "IpAddressV4": "111.11.100.0",
                            "Organization": {
                                "Asn": "0",
                                "AsnOrg": "GeneratedFindingASNOrg",
                                "Isp": "GeneratedFindingISP",
                                "Org": "GeneratedFindingORG"
                            }
                        },
                        "StatusCode": 201,
                        "Parameters": "GeneratedFindingActionParameters"
                    }
                },
                "Archived": 'false',
                "Count": 6,
                "DetectorId": "abcdefghijklmn",
                "EventFirstSeen": "2023-03-29T07:26:01.000Z",
                "EventLastSeen": "2023-06-30T11:54:18.000Z",
                "ResourceRole": "TARGET",
                "ServiceName": "guardduty",
                "AdditionalInfo": {
                    "Value": "{\"sample\":true}",
                    "Type": "default"
                }
            }
        }

        objects = TestAwsGuarddutyResultsToStix.get_observed_data_objects(data)
        kubernetes_api_call = TestAwsGuarddutyResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert (kubernetes_api_call.keys() == {'type', 'extensions', 'dst_ref', 'protocols'})
        assert kubernetes_api_call is not None
        assert kubernetes_api_call['protocols'] == ["http"]
        assert kubernetes_api_call['extensions']['http-request-ext']['request_value'] == 'GeneratedFindingRequestURI'
        assert kubernetes_api_call['extensions']['http-request-ext']['request_method'] == 'create'
        assert kubernetes_api_call['extensions']['http-request-ext']['request_header']['User-Agent'] == ''
        assert kubernetes_api_call['extensions']['http-request-ext']['x_status_code'] == 201
        assert kubernetes_api_call['extensions']['http-request-ext']['x_parameters'] == 'GeneratedFindingAct' \
                                                                                        'ionParameters'
