from stix_shifter.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter.stix_translation.src.utils import transformers
from stix_shifter.stix_translation.src.modules.aws_cloud_watch_logs import aws_cloud_watch_logs_translator
import json
import unittest

interface = aws_cloud_watch_logs_translator.Translator()
map_file = open(interface.mapping_filepath).read()

map_data = json.loads(map_file)
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "aws_cloud_watch_logs",
    "identity_class": "events"
}
options = {}


class TestAwsResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for aws cloudwatch logs translate results
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
        return TestAwsResultsToStix.get_first(itr, lambda o: isinstance(o, dict) and o.get('type') == typ)

    def test_common_prop(self):
        """
        to test the common stix object properties
        """
        data = {'guardduty': {'NETWORK_CONNECTION': {'version': '0', 'id': '1fbec093-9e30-3ca6-073e-c648580845e0',
                                                     'detail-type': 'GuardDuty Finding', 'time': '2019-10-18T03:00:05Z',
                                                     'region': 'us-east-1', 'detail_schemaVersion': '2.0',
                                                     'detail_accountId': '979326520502', 'detail_partition': 'aws',
                                                     'detail_arn':
                                                         'arn:aws:guardduty:us-east-1:979326520502:detector/'
                                                         '6ab6e6ee780ed494f3b7ca56acdc74df/finding/6cb6e99751fcbe'
                                                         'd76aae1a9a64bb96a8',
                                                     'detail_resource_instanceDetails_instanceId':
                                                         'i-0b8fd03ade35c681d',
                                                     'detail_resource_instanceDetails_instanceType': 't2.micro',
                                                     'detail_resource_instanceDetails_launchTime':
                                                         '2019-10-14T12:51:57Z',
                                                     'detail_resource_instanceDetails_iamInstanceProfile_arn':
                                                         'arn:aws:iam::979326520502:instance-profile/EC2_'
                                                         'Instances_Full_Access',
                                                     'detail_resource_instanceDetails_iamInstanceProfile_id':
                                                         'AIPA6IBDIZS3ES3TI5TNQ',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'networkInterfaceId': 'eni-02e70b8e842c70a2f',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateDnsName': 'ip-172-31-88-63.ec2.internal',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateIpAddress': '172.31.88.63',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateIpAddresses_0_privateDnsName':
                                                         'ip-172-31-88-63.ec2.internal',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateIpAddresses_0_privateIpAddress': '172.31.88.63',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_subnetId':
                                                         'subnet-c62a11e8',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_vpcId':
                                                         'vpc-10db926a',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'securityGroups_0_groupName': 'launch-wizard-1',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'securityGroups_0_groupId': 'sg-0aa89ff4646f71594',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'publicDnsName': 'ec2-54-211-223-78.compute-1.amazonaws.com',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_publicIp':
                                                         '54.211.223.78',
                                                     'detail_resource_instanceDetails_instanceState': 'running',
                                                     'detail_resource_instanceDetails_availabilityZone': 'us-east-1b',
                                                     'detail_resource_instanceDetails_imageId': 'ami-04763b3055de4860b',
                                                     'detail_resource_instanceDetails_imageDescription': 'Canonical, '
                                                                                                         'Ubuntu, '
                                                                                                         '16.04 LTS, '
                                                                                                         'amd64 '
                                                                                                         'xenial '
                                                                                                         'image build '
                                                                                                         'on '
                                                                                                         '2019-09-13',
                                                     'detail_service_serviceName': 'guardduty',
                                                     'detail_service_detectorId': '6ab6e6ee780ed494f3b7ca56acdc74df',
                                                     'detail_service_action_networkConnectionAction_connectionDirection'
                                                     : 'INBOUND',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'ipAddressV4': '54.211.162.49',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_asn': '14618',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_asnOrg': 'Amazon.com, Inc.',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_isp': 'Amazon.com',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_org': 'Amazon.com',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'country_countryName': 'United States',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'city_cityName': 'Ashburn',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'geoLocation_lat': 39.0481,
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'geoLocation_lon': -77.4728,
                                                     'detail_service_action_networkConnectionAction_remotePortDetails_'
                                                     'port': 34042,
                                                     'detail_service_action_networkConnectionAction_remotePortDetails_'
                                                     'portName': 'Unknown',
                                                     'detail_service_action_networkConnectionAction_localPortDetails_'
                                                     'port': 22,
                                                     'detail_service_action_networkConnectionAction_localPortDetails_'
                                                     'portName': 'SSH',
                                                     'detail_service_action_networkConnectionAction_protocol': 'TCP',
                                                     'detail_service_action_networkConnectionAction_blocked': 'false',
                                                     'detail_service_additionalInfo': {}}, 'source': 'aws.guardduty',
                              'account': '979326520502', 'detail_region': 'us-east-1',
                              'detail_id': '6cb6e99751fcbed76aae1a9a64bb96a8',
                              'detail_type': 'UnauthorizedAccess:EC2/SSHBruteForce',
                              'detail_resource_resourceType': 'Instance',
                              'detail_service_action_actionType': 'NETWORK_CONNECTION',
                              'detail_service_resourceRole': 'TARGET',
                              'detail_service_eventFirstSeen': '2019-10-16T05:55:25Z',
                              'detail_service_eventLastSeen': '2019-10-18T02:30:09Z',
                              'detail_service_archived': 'false', 'detail_service_count': 23, 'detail_severity': 2,
                              'detail_createdAt': '2019-10-16T06:08:32.249Z',
                              'detail_updatedAt': '2019-10-18T02:50:01.450Z',
                              'detail_title': '54.211.162.49 is performing SSH brute force attacks against '
                                              'i-0b8fd03ade35c681d. ',
                              'detail_description': '54.211.162.49 is performing SSH brute force attacks against '
                                                    'i-0b8fd03ade35c681d. Brute force attacks are used to gain '
                                                    'unauthorized access to your instance by guessing the SSH '
                                                    'password.',
                              '@timestamp': '2019-10-18 03:00:05.000', 'event_count': 1}}

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        assert result_bundle['type'] == 'bundle'
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']
        assert result_bundle_identity['id'] == data_source['id']
        assert result_bundle_identity['name'] == data_source['name']
        assert result_bundle_identity['identity_class'] == data_source['identity_class']

        observed_data = result_bundle_objects[1]
        assert observed_data['id'] is not None
        assert observed_data['type'] == "observed-data"
        assert observed_data['created_by_ref'] == result_bundle_identity['id']
        assert observed_data['x_com_aws_guardduty_finding'] is not None
        assert observed_data['x_com_aws'] is not None
        assert observed_data['created'] is not None
        assert observed_data['modified'] is not None
        assert observed_data['number_observed'] is not None

    def test_vpc_flow_network_json_to_stix(self):
        """to test network stix object properties"""
        data = {
            'vpcflow': {'@timestamp': '2019-10-20 10:43:09.000', 'srcAddr': '54.239.29.61', 'dstAddr': '172.31.88.63',
                        'srcPort': '443', 'dstPort': '53866', 'protocol': 'tcp', 'start': '1571568189',
                        'end': '1571568248', 'accountId': '979326520502', 'interfaceId': 'eni-02e70b8e842c70a2f',
                        '@ptr':
                            'CloKIQodOTc5MzI2NTIwNTAyOlVTRWFzdDFfRmxvd0xvZ3MQBxI1GhgCBc2q4EYAAAACFMuFggAF2sO4QAAAAWIgA'
                            'SjoyP/F3i0wyPyNxt4tOCxA7TFI0ClQzyIQJRgB',
                        'event_count': 1}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        network_obj = TestAwsResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert network_obj is not None, 'network-traffic object type not found'
        assert network_obj.keys() == {'type', 'src_ref', 'dst_ref', 'src_port', 'dst_port', 'protocols', 'start', 'end'}
        assert network_obj['type'] == 'network-traffic'
        assert network_obj['src_ref'] == '0'
        assert network_obj['dst_ref'] == '2'
        assert network_obj['src_port'] == 443
        assert network_obj['dst_port'] == 53866
        assert network_obj['protocols'] == ['tcp']
        assert network_obj['start'] == '2019-10-20T10:43:09.000Z'
        assert network_obj['end'] == '2019-10-20T10:44:08.000Z'

    def test_vpc_flow_custom_attr_json_to_stix(self):
        """to test network stix object properties"""
        data = {
            'vpcflow': {'@timestamp': '2019-10-20 10:43:09.000', 'srcAddr': '54.239.29.61', 'dstAddr': '172.31.88.63',
                        'srcPort': '443', 'dstPort': '53866', 'protocol': 'tcp', 'start': '1571568189',
                        'end': '1571568248', 'accountId': '979326520502', 'interfaceId': 'eni-02e70b8e842c70a2f',
                        '@ptr':
                            'CloKIQodOTc5MzI2NTIwNTAyOlVTRWFzdDFfRmxvd0xvZ3MQBxI1GhgCBc2q4EYAAAACFMuFggAF2sO4QAAAAWIg'
                            'ASjoyP/F3i0wyPyNxt4tOCxA7TFI0ClQzyIQJRgB',
                        'event_count': 1}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        custom_object = observed_data['x_com_aws']

        assert custom_object.keys() == {'account_id'}
        assert custom_object['account_id'] == '979326520502'

    def test_guardduty_network_json_to_stix(self):
        """to test network stix object properties"""
        data = {'guardduty': {'NETWORK_CONNECTION': {'version': '0', 'id': '617628ca-ae74-5875-6e9c-be4cd2e9e267',
                                                     'detail-type': 'GuardDuty Finding', 'time': '2019-10-17T09:30:05Z',
                                                     'region': 'us-east-1', 'detail_schemaVersion': '2.0',
                                                     'detail_accountId': '979326520502', 'detail_partition': 'aws',
                                                     'detail_arn':
                                                         'arn:aws:guardduty:us-east-1:979326520502:detector/6ab6e6ee7'
                                                         '80ed494f3b7ca56acdc74df/finding/6cb6e99751fcbed76aae1a9'
                                                         'a64bb96a8',
                                                     'detail_resource_instanceDetails_instanceId':
                                                         'i-0b8fd03ade35c681d',
                                                     'detail_resource_instanceDetails_instanceType': 't2.micro',
                                                     'detail_resource_instanceDetails_launchTime':
                                                         '2019-10-14T12:51:57Z',
                                                     'detail_resource_instanceDetails_iamInstanceProfile_arn':
                                                         'arn:aws:iam::979326520502:instance-profile/EC2_Instances_'
                                                         'Full_Access',
                                                     'detail_resource_instanceDetails_iamInstanceProfile_id':
                                                         'AIPA6IBDIZS3ES3TI5TNQ',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'networkInterfaceId': 'eni-02e70b8e842c70a2f',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateDnsName': 'ip-172-31-88-63.ec2.internal',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateIpAddress': '172.31.88.63',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateIpAddresses_0_privateDnsName':
                                                         'ip-172-31-88-63.ec2.internal',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateIpAddresses_0_privateIpAddress': '172.31.88.63',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_subnetId':
                                                         'subnet-c62a11e8',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_vpcId':
                                                         'vpc-10db926a',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'securityGroups_0_groupName': 'launch-wizard-1',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'securityGroups_0_groupId': 'sg-0aa89ff4646f71594',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'publicDnsName': 'ec2-54-211-223-78.compute-1.amazonaws.com',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_publicIp':
                                                         '54.211.223.78',
                                                     'detail_resource_instanceDetails_instanceState': 'running',
                                                     'detail_resource_instanceDetails_availabilityZone': 'us-east-1b',
                                                     'detail_resource_instanceDetails_imageId': 'ami-04763b3055de4860b',
                                                     'detail_resource_instanceDetails_imageDescription': 'Canonical, '
                                                                                                         'Ubuntu, '
                                                                                                         '16.04 LTS, '
                                                                                                         'amd64 '
                                                                                                         'xenial '
                                                                                                         'image build '
                                                                                                         'on '
                                                                                                         '2019-09-13',
                                                     'detail_service_serviceName': 'guardduty',
                                                     'detail_service_detectorId': '6ab6e6ee780ed494f3b7ca56acdc74df',
                                                     'detail_service_action_networkConnectionAction_'
                                                     'connectionDirection': 'INBOUND',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'ipAddressV4': '54.211.162.49',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_asn': '14618',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_asnOrg': 'Amazon.com, Inc.',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_isp': 'Amazon.com',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_org': 'Amazon.com',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'country_countryName': 'United States',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'city_cityName': 'Ashburn',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'geoLocation_lat': 39.0481,
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'geoLocation_lon': -77.4728,
                                                     'detail_service_action_networkConnectionAction_remotePortDetails_'
                                                     'port': 32820,
                                                     'detail_service_action_networkConnectionAction_remotePortDetails_'
                                                     'portName': 'Unknown',
                                                     'detail_service_action_networkConnectionAction_localPortDetails_'
                                                     'port': 22,
                                                     'detail_service_action_networkConnectionAction_localPortDetails_'
                                                     'portName': 'SSH',
                                                     'detail_service_action_networkConnectionAction_protocol': 'TCP',
                                                     'detail_service_action_networkConnectionAction_blocked': 'false',
                                                     'detail_service_additionalInfo': {}}, 'source': 'aws.guardduty',
                              'account': '979326520502', 'detail_region': 'us-east-1',
                              'detail_id': '6cb6e99751fcbed76aae1a9a64bb96a8',
                              'detail_type': 'UnauthorizedAccess:EC2/SSHBruteForce',
                              'detail_resource_resourceType': 'Instance',
                              'detail_service_action_actionType': 'NETWORK_CONNECTION',
                              'detail_service_resourceRole': 'TARGET',
                              'detail_service_eventFirstSeen': '2019-10-16T05:55:25Z',
                              'detail_service_eventLastSeen': '2019-10-17T09:05:51Z',
                              'detail_service_archived': 'false', 'detail_service_count': 16, 'detail_severity': 2,
                              'detail_createdAt': '2019-10-16T06:08:32.249Z',
                              'detail_updatedAt': '2019-10-17T09:20:25.038Z',
                              'detail_title': '54.211.162.49 is performing SSH brute force attacks against '
                                              'i-0b8fd03ade35c681d. ',
                              'detail_description': '54.211.162.49 is performing SSH brute force attacks against '
                                                    'i-0b8fd03ade35c681d. Brute force attacks are used to gain '
                                                    'unauthorized access to your instance by guessing the SSH '
                                                    'password.',
                              '@timestamp': '2019-10-17 09:30:05.000', 'event_count': 1}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']

        network_obj = TestAwsResultsToStix.get_first_of_type(objects.values(), 'network-traffic')
        assert network_obj is not None, 'network-traffic object type not found'
        assert network_obj.keys() == {'type', 'dst_port', 'src_ref', 'dst_ref', 'src_port', 'protocols'}
        assert network_obj['type'] == 'network-traffic'
        assert network_obj['dst_port'] == 32820
        assert network_obj['src_ref'] == '1'
        assert network_obj['dst_ref'] == '5'
        assert network_obj['src_port'] == 22
        assert network_obj['protocols'] == ['tcp']

    def test_guardduty_custom_attr_json_to_stix(self):
        """to test network stix object properties"""
        data = {'guardduty': {'NETWORK_CONNECTION': {'version': '0', 'id': '617628ca-ae74-5875-6e9c-be4cd2e9e267',
                                                     'detail-type': 'GuardDuty Finding', 'time': '2019-10-17T09:30:05Z',
                                                     'region': 'us-east-1', 'detail_schemaVersion': '2.0',
                                                     'detail_accountId': '979326520502', 'detail_partition': 'aws',
                                                     'detail_arn': 'arn:aws:guardduty:us-east-1:979326520502:detector'
                                                                   '/6ab6e6ee780ed494f3b7ca56acdc74df/finding/6cb6e9975'
                                                                   '1fcbed76aae1a9a64bb96a8',
                                                     'detail_resource_instanceDetails_instanceId': 'i-0b8fd03ade35c'
                                                                                                   '681d',
                                                     'detail_resource_instanceDetails_instanceType': 't2.micro',
                                                     'detail_resource_instanceDetails_launchTime': '2019-10-14T12:51:'
                                                                                                   '57Z',
                                                     'detail_resource_instanceDetails_iamInstanceProfile'
                                                     '_arn': 'arn:aws:iam::979326520502:instance-profile/EC2_Instances_'
                                                             'Full_Access',
                                                     'detail_resource_instanceDetails_iamInstanceProfile_id':
                                                         'AIPA6IBDIZS3ES3TI5TNQ',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'networkInterfaceId': 'eni-02e70b8e842c70a2f',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateDnsName': 'ip-172-31-88-63.ec2.internal',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateIpAddress': '172.31.88.63',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateIpAddresses_0_privateDnsName':
                                                         'ip-172-31-88-63.ec2.internal',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'privateIpAddresses_0_privateIpAddress': '172.31.88.63',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_subnetId':
                                                         'subnet-c62a11e8',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_vpcId':
                                                         'vpc-10db926a',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'securityGroups_0_groupName': 'launch-wizard-1',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'securityGroups_0_groupId': 'sg-0aa89ff4646f71594',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'publicDnsName': 'ec2-54-211-223-78.compute-1.amazonaws.com',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_'
                                                     'publicIp': '54.211.223.78',
                                                     'detail_resource_instanceDetails_instanceState': 'running',
                                                     'detail_resource_instanceDetails_availabilityZone': 'us-east-1b',
                                                     'detail_resource_instanceDetails_imageId': 'ami-04763b3055de4860b',
                                                     'detail_resource_instanceDetails_imageDescription':
                                                         'Canonical, Ubuntu, 16.04 LTS, amd64 xenial image build on '
                                                         '2019-09-13',
                                                     'detail_service_serviceName': 'guardduty',
                                                     'detail_service_detectorId': '6ab6e6ee780ed494f3b7ca56acdc74df',
                                                     'detail_service_action_networkConnectionAction_'
                                                     'connectionDirection': 'INBOUND',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'ipAddressV4': '54.211.162.49',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_asn': '14618',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_asnOrg': 'Amazon.com, Inc.',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_isp': 'Amazon.com',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_org': 'Amazon.com',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'country_countryName': 'United States',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'city_cityName': 'Ashburn',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'geoLocation_lat': 39.0481,
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'geoLocation_lon': -77.4728,
                                                     'detail_service_action_networkConnectionAction_remotePortDetails_'
                                                     'port': 32820,
                                                     'detail_service_action_networkConnectionAction_remotePortDetails_'
                                                     'portName': 'Unknown',
                                                     'detail_service_action_networkConnectionAction_localPortDetails_'
                                                     'port': 22,
                                                     'detail_service_action_networkConnectionAction_localPortDetails_'
                                                     'portName': 'SSH',
                                                     'detail_service_action_networkConnectionAction_protocol': 'TCP',
                                                     'detail_service_action_networkConnectionAction_blocked': 'false',
                                                     'detail_service_additionalInfo': {}}, 'source': 'aws.guardduty',
                              'account': '979326520502', 'detail_region': 'us-east-1',
                              'detail_id': '6cb6e99751fcbed76aae1a9a64bb96a8',
                              'detail_type': 'UnauthorizedAccess:EC2/SSHBruteForce',
                              'detail_resource_resourceType': 'Instance',
                              'detail_service_action_actionType': 'NETWORK_CONNECTION',
                              'detail_service_resourceRole': 'TARGET',
                              'detail_service_eventFirstSeen': '2019-10-16T05:55:25Z',
                              'detail_service_eventLastSeen': '2019-10-17T09:05:51Z',
                              'detail_service_archived': 'false', 'detail_service_count': 16, 'detail_severity': 2,
                              'detail_createdAt': '2019-10-16T06:08:32.249Z',
                              'detail_updatedAt': '2019-10-17T09:20:25.038Z',
                              'detail_title': '54.211.162.49 is performing SSH brute force attacks against i-0b8fd03'
                                              'ade35c681d. ',
                              'detail_description': '54.211.162.49 is performing SSH brute force attacks against '
                                                    'i-0b8fd03ade35c681d. Brute force attacks are used to gain '
                                                    'unauthorized access to your instance by guessing the SSH '
                                                    'password.',
                              '@timestamp': '2019-10-17 09:30:05.000', 'event_count': 1}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        custom_object = observed_data['x_com_aws_guardduty_finding']

        assert custom_object.keys() == {'severity', 'id', 'type', 'title', 'timestamp'}
        assert custom_object['id'] == '6cb6e99751fcbed76aae1a9a64bb96a8'
        assert custom_object['type'] == 'UnauthorizedAccess:EC2/SSHBruteForce'
        assert custom_object['severity'] == 2
        assert custom_object['timestamp'] == '2019-10-17T09:30:05.000Z'
        assert custom_object[
                   'title'] == '54.211.162.49 is performing SSH brute force attacks against i-0b8fd03ade35c681d. '
