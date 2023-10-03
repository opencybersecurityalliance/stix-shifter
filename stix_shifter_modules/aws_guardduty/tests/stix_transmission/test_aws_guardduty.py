from stix_shifter_modules.aws_guardduty.entry_point import EntryPoint
from unittest.mock import patch
import unittest
from stix_shifter.stix_transmission import stix_transmission
from stix_shifter_utils.utils.async_utils import run_in_thread
from tests.utils.async_utils import get_aws_mock_response
from botocore.exceptions import EndpointConnectionError, ParamValidationError, ClientError, InvalidRegionError, \
    ReadTimeoutError, ConnectTimeoutError


class TestAWSConnection(unittest.TestCase, object):
    detector_response = {
        'ResponseMetadata': {
            'RequestId': 'e1a0bc13-24fe-4494-8022-dc9d45d41fda',
            'HTTPStatusCode': 200,
            'RetryAttempts': 0
        },
        'data': ['6ab6e6dd780ed494f3b7ca50acdc04tg']
    }

    findings_response = {
        'ResponseMetadata': {
            'RequestId': '09a1e4a4-b6b9-4e60-8f4b-6bfac2a829b3',
            'HTTPStatusCode': 200,
            'RetryAttempts': 0
        },
        'data': ['sss3f545573182s44d6442s7s7s2s420'], 'next_token': ''
    }

    results_response = {

        'ResponseMetadata': {
            'RequestId': 'af993b02-dc27-4c2c-8ea0-8d4ca80f1985',
            'HTTPStatusCode': 200,
        },
        "Findings": [{
            "AccountId": "9799797979797",
            "Arn": "arn:aws:guardduty:us-east-1:979326520502:detector/6ab6e6dd780ed494f3b7ca50acdc04tg/"
                   "finding/c2c40bf921b79794d9bd0f4559ec6ace",
            "CreatedAt": "2023-05-14T01:48:52.975Z",
            "Description": "10.11.111.112 is performing RDP brute force attacks against i-0999999999999999. "
                           "Brute force attacks are used to gain unauthorized access to your instance "
                           "by guessing the RDP password.",
            "Id": "c2c40bf921b79794d9bd0f4559ec6ace",
            "Partition": "aws",
            "Region": "us-east-1",
            "Resource": {
                "InstanceDetails": {
                    "AvailabilityZone": "us-east-1c",
                    "ImageDescription": "Microsoft Windows Server 2022 Full Locale English AMI provided by Amazon",
                    "ImageId": "ami-1c2b0h3fa02924d63",
                    "InstanceId": "i-0999999999999999",
                    "InstanceState": "running",
                    "InstanceType": "t2.large",
                    "LaunchTime": "2023-05-11T07:47:06.000Z",
                    "NetworkInterfaces": [
                        {
                            "Ipv6Addresses": [],
                            "NetworkInterfaceId": "eni-013b37911da60cc09",
                            "PrivateDnsName": "ip-111-11-11-11.ec2.internal",
                            "PrivateIpAddress": "111.11.11.11",
                            "PrivateIpAddresses": [
                                {
                                    "PrivateDnsName": "ip-111-11-11-11.ec2.internal",
                                    "PrivateIpAddress": "111.11.11.11"
                                }
                            ],
                            "PublicDnsName": "ec2-12-12-112-112.compute-1.amazonaws.com",
                            "PublicIp": "12.12.112.112",
                            "SecurityGroups": [
                                {
                                    "GroupId": "aw-0000d71d3c30933f",
                                    "GroupName": "launch-wizard-180"
                                }
                            ],
                            "SubnetId": "subnet-ooss011f",
                            "VpcId": "vpc-10ss926a"
                        }
                    ],
                    "Platform": "windows",
                    "ProductCodes": [],
                    "Tags": [
                        {
                            "Key": "Name",
                            "Value": "cp4s-splunk-enterprise-large-2"
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
                            "IpAddressV4": "111.11.11.11"
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
                            "IpAddressV4": "10.11.111.112",
                            "Organization": {
                                "Asn": "174",
                                "AsnOrg": "COGENT-174",
                                "Isp": "Cogent Communications",
                                "Org": "Cogent Communications"
                            }
                        },
                        "RemotePortDetails": {
                            "Port": 49222,
                            "PortName": "Unknown"
                        }
                    }
                },
                "Archived": 'false',
                "Count": 21,
                "DetectorId": "6db6d6dd780dd494f3b7dd56ddddd74df",
                "EventFirstSeen": "2023-05-14T01:34:39.000Z",
                "EventLastSeen": "2023-05-14T05:44:35.000Z",
                "ResourceRole": "TARGET",
                "ServiceName": "guardduty",
                "AdditionalInfo": {
                    "Value": "{}",
                    "Type": "default"
                }
            },
            "Severity": 2,
            "Title": "10.11.111.112 is performing RDP brute force attacks against i-0999999999999999.",
            "Type": "UnauthorizedAccess:EC2/RDPBruteForce",
            "UpdatedAt": "2023-05-14T05:48:48.485Z"
        }
        ],
        "metadata": {
            "result_count": 1,
            "next_page_token": "",
            "detector_ids": []
        }
    }

    @staticmethod
    def connection():
        """format for connection"""
        return {
            "region": "us-east-1"
        }

    @staticmethod
    def configuration():
        """format for configuration"""
        return {
            "auth": {
                "aws_access_key_id": "abc",
                "aws_secret_access_key": "xyx"
            }
        }

    @staticmethod
    def iam_config():
        return {
            "auth": {
                "aws_access_key_id": "abc",
                "aws_secret_access_key": "xyz",
                "aws_iam_role": "ABC"
            }
        }

    @staticmethod
    def get_client_error():
        response = {'Error': {'Message': 'The request was rejected because the parameter findingCriteria has '
                                         'an invalid value.', 'Code': 'BadRequestException'},
                    'ResponseMetadata': {'HTTPStatusCode': 400}}
        return ClientError(error_response=response, operation_name='ListFindings')

    @staticmethod
    def get_client_error_for_invalid_credentials():
        response = {'Error': {'Message': 'The security token included in the request is invalid',
                              'Code': 'UnrecognizedClientException'},
                    'ResponseMetadata': {'HTTPStatusCode': 403}}
        return ClientError(error_response=response, operation_name='ListFindings')

    @staticmethod
    def get_invalid_region_error():
        return InvalidRegionError(region_name='us-east-')

    @staticmethod
    def get_read_timeout_error():
        return ReadTimeoutError(endpoint_url='https://guardduty.us-eaat-1.amazonaws.com/detector')

    @staticmethod
    def get_connect_timeout_error():
        return ConnectTimeoutError(endpoint_url='https://guardduty.us-east-1.amazonaws.com/detector')

    @staticmethod
    def get_parameter_validations_error():
        return ParamValidationError(report='Parameter validation failed:Unknown parameter in FindingCriteria')

    @staticmethod
    def get_endpoint_connection_error():
        return EndpointConnectionError(endpoint_url='https://guardduty.us-eaat-1.amazonaws.com/detector')

    def test_is_async(self):
        """check for synchronous or asynchronous"""
        entry_point = EntryPoint(TestAWSConnection.connection(), TestAWSConnection.configuration())
        check_async = entry_point.is_async()
        assert check_async is False

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_ping_connection(self, mock_results):
        """test ping connection"""
        mock_results.return_value = get_aws_mock_response(TestAWSConnection.detector_response)
        entry_point = EntryPoint(TestAWSConnection.connection(), TestAWSConnection.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is True

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_results_connections(self, mock_results_2, mock_results_1):
        """test success result response"""
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response),
                                      get_aws_mock_response(TestAWSConnection.findings_response)]
        mock_results_2.return_value = get_aws_mock_response(TestAWSConnection.results_response)

        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        connection_with_limit = {
            "region": "us-east-1",
            "options": {"result_limit": 3}
        }
        transmission = stix_transmission.StixTransmission('aws_guardduty', connection_with_limit,
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert results_response['data'] is not None
        assert 'PrivateIpAddress' not in \
               results_response['data'][0]['Resource']['InstanceDetails']['NetworkInterfaces'][0]['PrivateIpAddresses'][
                   0]
        assert 'metadata' in results_response
        assert results_response['metadata']['result_count'] == 1

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_results_connections_with_detector_id(self, mock_results_2, mock_results_1):
        """test success result response with detector id as input"""
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response),
                                      get_aws_mock_response(TestAWSConnection.findings_response)]
        mock_results_2.return_value = get_aws_mock_response(TestAWSConnection.results_response)

        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        connection_with_detector_id = {
            "region": "us-east-1",
            "detector_ids": "6ab6e6dd780ed494f3b7ca50acdc04tg"
        }
        transmission = stix_transmission.StixTransmission('aws_guardduty', connection_with_detector_id,
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_results_connections_to_test_kubernetes_api_call(self, mock_results_2, mock_results_1):
        """test success result response to test the protocol value in kubernetes api call"""
        response = {
            'ResponseMetadata': {
                'RequestId': 'af993b02-dc27-4c2c-8ea0-8d4ca80f1985',
                'HTTPStatusCode': 200,
            },
            "Findings": [{
                "Service": {
                    "Action": {
                        "ActionType": "KUBERNETES_API_CALL",
                        "KubernetesApiCallAction": {
                            "RequestUri": "GeneratedFindingRequestURI",
                            "Verb": "create",
                            "UserAgent": "",
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
            }]
        }
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response),
                                      get_aws_mock_response(TestAWSConnection.findings_response)]
        mock_results_2.return_value = get_aws_mock_response(response)

        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        transmission = stix_transmission.StixTransmission('aws_guardduty', TestAWSConnection.connection(),
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert results_response['data'] is not None
        assert results_response['data'][0]['Service']['Action']['KubernetesApiCallAction']['Protocol'] == 'http'

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_results_connections_to_test_ebs_volume_hash_format(self, mock_results_2, mock_results_1):
        """test success result response with ebs volume"""
        results_response = {

            'ResponseMetadata': {
                'RequestId': 'af993b02-dc27-4c2c-8ea0-8d4ca80f1985',
                'HTTPStatusCode': 200,
            },
            "Findings": [
                {
                    "SchemaVersion": "2.0",
                    "Service": {
                        "Archived": 'false',
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
                                                    "Hash": "a021bbfb6489e54d471899f7dbaaa9d1663fc345ec2fe2a2c4538aab"
                                                            "f651fd0f",
                                                    "FileName": "eicar.com"
                                                },
                                                {
                                                    "FilePath": "tmp/eicar-2.txt",
                                                    "VolumeArn": "arn:aws:ec2:us-west-2:12345678910:volume/"
                                                                 "vol-09d5050dea915943d",
                                                    "Hash": "a021bbfb6489e54d471899f7db9d2363fc345ec2fe2a2c4538aabf"
                                                            "651ad0x",
                                                    "FileName": "eicar-2.txt"
                                                },
                                                {
                                                    "FilePath": "tmp/eicar-2.txt",
                                                    "VolumeArn": "arn:aws:ec2:us-west-2:12345678910:volume/"
                                                                 "vol-09d5050dea915943d",
                                                    "Hash": "202cb962ac59075b964b07152d234b70",
                                                    "FileName": "eicar-3.txt"
                                                },
                                                {
                                                    "FilePath": "tmp/eicar-2.txt",
                                                    "VolumeArn": "arn:aws:ec2:us-west-2:12345678910:volume/"
                                                                 "vol-09d5050dea915943d",
                                                    "Hash": "40bd001563085fc35165329ea1ff5c5ecbdbbeef",
                                                    "FileName": "eicar-4.txt"
                                                },
                                            ]
                                        }
                                    ]
                                }
                            },
                            "ScanType": "ON_DEMAND"
                        }
                    }
                }
            ],
            "metadata": {
                "result_count": 1,
                "next_page_token": "",
                "detector_ids": []
            }
        }
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response),
                                      get_aws_mock_response(TestAWSConnection.findings_response)]
        mock_results_2.return_value = get_aws_mock_response(results_response)

        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        transmission = stix_transmission.StixTransmission('aws_guardduty', TestAWSConnection.connection(),
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is True
        assert results_response['data'] is not None
        assert results_response['data'][0]['Service']['EbsVolumeScanDetails']['ScanDetections'][
                   'ThreatDetectedByName']['ThreatNames'][0]['FilePaths'][0]['FileSha256'] == \
               "a021bbfb6489e54d471899f7dbaaa9d1663fc345ec2fe2a2c4538aabf651fd0f"
        assert results_response['data'][0]['Service']['EbsVolumeScanDetails']['ScanDetections'][
                   'ThreatDetectedByName']['ThreatNames'][0]['FilePaths'][1][
                   'UnknownHash'] == "a021bbfb6489e54d471899f7db9d2363fc345ec2fe2a2c4538aabf651ad0x"

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_results_connections_using_metadata(self, mock_results_2, mock_results_1):
        """test success result response with metadata"""
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response),
                                      get_aws_mock_response(TestAWSConnection.findings_response)]
        mock_results_2.return_value = get_aws_mock_response(TestAWSConnection.results_response)
        metadata = {"result_count": 2, "next_page_token": '123', "detector_ids": ['1234abc']}
        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        connection_with_limit = {
            "region": "us-east-1",
            "options": {"result_limit": 3}
        }
        transmission = stix_transmission.StixTransmission('aws_guardduty', connection_with_limit,
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length, metadata)
        assert results_response is not None
        assert results_response['success'] is True
        assert results_response['data'] is not None

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_results_connections_client_error(self, mock_results_2, mock_results_1):
        """test Bad Request in result response"""
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response),
                                      TestAWSConnection.get_client_error()]
        mock_results_2.return_value = get_aws_mock_response(TestAWSConnection.results_response)
        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceTyp\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        transmission = stix_transmission.StixTransmission('aws_guardduty', TestAWSConnection.connection(),
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'invalid_parameter'
        assert 'An error occurred (BadRequestException) when calling the ListFindings operation' in \
               results_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_ping_connection_with_client_error(self, mock_results):
        """test ping connection with invalid credentials"""
        mock_results.side_effect = TestAWSConnection.get_client_error_for_invalid_credentials()
        entry_point = EntryPoint(TestAWSConnection.connection(), TestAWSConnection.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == 'authentication_fail'
        assert 'The security token included in the request is invalid' in \
               ping_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_results_connections_parameter_validations_error(self, mock_results_2, mock_results_1):
        """test results with invalid parameter"""
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response),
                                      TestAWSConnection.get_parameter_validations_error()]
        mock_results_2.return_value = get_aws_mock_response(TestAWSConnection.results_response)
        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourcetype\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        transmission = stix_transmission.StixTransmission('aws_guardduty', TestAWSConnection.connection(),
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'invalid_parameter'
        assert 'Parameter validation failed:Unknown parameter in FindingCriteria' in \
               results_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_ping_connection_with_invalid_region_error(self, mock_results):
        """test ping connection with invalid region"""
        mock_results.side_effect = TestAWSConnection.get_invalid_region_error()
        connection_with_invalid_region = {
            "region": "us-east-"
        }
        entry_point = EntryPoint(connection_with_invalid_region, TestAWSConnection.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == 'authentication_fail'
        assert "Provided region_name 'us-east-' doesn't match a supported format." in \
               ping_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    def test_results_connections_with_invalid_region(self, mock_results_1):
        """test results with invalid region"""
        mock_results_1.side_effect = [TestAWSConnection.get_invalid_region_error()]
        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        connection_with_invalid_region = {
            "region": "us-east-"
        }
        transmission = stix_transmission.StixTransmission('aws_guardduty', connection_with_invalid_region,
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'authentication_fail'
        assert "Provided region_name 'us-east-' doesn't match a supported format." in \
               results_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_results_connections_endpoint_connection_error(self, mock_results_2, mock_results_1):
        """test endpoint connection error for results"""
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response),
                                      TestAWSConnection.get_endpoint_connection_error()]
        mock_results_2.return_value = get_aws_mock_response(TestAWSConnection.results_response)
        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        transmission = stix_transmission.StixTransmission('aws_guardduty', TestAWSConnection.connection(),
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'service_unavailable'
        assert 'Could not connect to the endpoint URL: ' \
               '"https://guardduty.us-eaat-1.amazonaws.com/detector"' in results_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_ping_connection_with_endpoint_connection_error(self, mock_results):
        """test endpoint connection error for ping"""
        mock_results.side_effect = TestAWSConnection.get_endpoint_connection_error()
        entry_point = EntryPoint(TestAWSConnection.connection(), TestAWSConnection.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == 'service_unavailable'
        assert 'Could not connect to the endpoint URL: "https://guardduty.us-eaat-1.amazonaws.com/detector"' in \
               ping_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    def test_results_key_error_with_invalid_token(self, mock_results_1):
        """test results with invalid token in IAM type config"""
        mock_results_1.side_effect = [KeyError('An error occurred (InvalidClientTokenId) when calling the AssumeRole '
                                               'operation: The security token included in the request is invalid')]
        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        transmission = stix_transmission.StixTransmission('aws_guardduty', TestAWSConnection.connection(),
                                                          TestAWSConnection.iam_config())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'authentication_fail'
        assert 'InvalidClientTokenId' in results_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_ping_key_error_with_invalid_token(self, mock_results_1):
        """test ping with invalid token in IAM type config"""
        mock_results_1.side_effect = [KeyError('An error occurred (InvalidClientTokenId) when calling the AssumeRole '
                                               'operation: The security token included in the request is invalid')]
        entry_point = EntryPoint(TestAWSConnection.connection(), TestAWSConnection.iam_config())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == 'authentication_fail'
        assert 'InvalidClientTokenId' in ping_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    def test_results_with_endpoint_connection_using_key_error(self, mock_results_1):
        """test results with endpoint connection from key error"""
        mock_results_1.side_effect = [KeyError('Could not connect to endpoint URL')]
        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        transmission = stix_transmission.StixTransmission('aws_guardduty', TestAWSConnection.connection(),
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'service_unavailable'
        assert 'Could not connect to endpoint URL' in results_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_ping_key_error_with_endpoint_connection(self, mock_results_1):
        """test ping with endpoint connection from Key Error"""
        mock_results_1.side_effect = [KeyError('Could not connect to endpoint URL')]
        entry_point = EntryPoint(TestAWSConnection.connection(), TestAWSConnection.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == 'service_unavailable'
        assert 'Could not connect to endpoint URL' in ping_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    def test_results_Parameter_key_error(self, mock_results_1):
        """test endpoint connection error for results"""
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response)]
        query = "{\"findingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        transmission = stix_transmission.StixTransmission('aws_guardduty', TestAWSConnection.connection(),
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert results_response['code'] == 'invalid_parameter'
        assert 'FindingCriteria' in results_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_results_connections_using_invalid_metadata(self, mock_results_2, mock_results_1):
        """test result response with invalid metadata"""
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response),
                                      get_aws_mock_response(TestAWSConnection.findings_response)]
        mock_results_2.return_value = get_aws_mock_response(TestAWSConnection.results_response)
        metadata = {"result_count": 2, "next_page_token": '123'}
        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        transmission = stix_transmission.StixTransmission('aws_guardduty', TestAWSConnection.connection(),
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length, metadata)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'Invalid Metadata' in results_response['error']
        assert results_response['code'] == 'invalid_parameter'

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_results_connections_with_connect_timeout(self, mock_results_2, mock_results_1):
        """test connect timeout for results"""
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response),
                                      TestAWSConnection.get_connect_timeout_error()]
        mock_results_2.return_value = get_aws_mock_response(TestAWSConnection.results_response)
        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        transmission = stix_transmission.StixTransmission('aws_guardduty', TestAWSConnection.connection(),
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'Connect timeout on endpoint URL' in results_response['error']
        assert results_response['code'] == 'service_unavailable'

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.get_paginated_result')
    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_results_connections_with_read_timeout(self, mock_results_2, mock_results_1):
        """test read timeout for results"""
        mock_results_1.side_effect = [get_aws_mock_response(TestAWSConnection.detector_response),
                                      TestAWSConnection.get_read_timeout_error()]
        mock_results_2.return_value = get_aws_mock_response(TestAWSConnection.results_response)
        query = "{\"FindingCriteria\":{\"Criterion\":{\"resource.resourceType\":" \
                "{\"Equals\":[\"Instance\"]},\"updatedAt\":{\"GreaterThanOrEqual\":1676460035000," \
                "\"LessThanOrEqual\":1686394800003}}}}"
        offset = 0
        length = 4
        transmission = stix_transmission.StixTransmission('aws_guardduty', TestAWSConnection.connection(),
                                                          TestAWSConnection.configuration())
        results_response = transmission.results(query, offset, length)
        assert results_response is not None
        assert results_response['success'] is False
        assert 'Read timeout' in results_response['error']
        assert results_response['code'] == 'service_unavailable'

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_ping_with_read_timeout_error(self, mock_results_1):
        """test read timeout for ping"""
        mock_results_1.side_effect = [TestAWSConnection.get_read_timeout_error()]
        entry_point = EntryPoint(TestAWSConnection.connection(), TestAWSConnection.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == 'service_unavailable'
        assert 'Read timeout' in ping_response['error']

    @patch('stix_shifter_modules.aws_guardduty.stix_transmission.boto3_client.BOTO3Client.make_request')
    def test_ping_with_connect_timeout_error(self, mock_results_1):
        """test connect timeout for ping"""
        mock_results_1.side_effect = [TestAWSConnection.get_connect_timeout_error()]
        entry_point = EntryPoint(TestAWSConnection.connection(), TestAWSConnection.configuration())
        ping_response = run_in_thread(entry_point.ping_connection)
        assert ping_response is not None
        assert ping_response['success'] is False
        assert ping_response['code'] == 'service_unavailable'
        assert 'Connect timeout on endpoint URL' in ping_response['error']
