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
        data = {'guardduty': {
            'NETWORK_CONNECTION': {'privateIpAddress': '172.31.88.63', 'privateDnsName': 'ip-172-31-88-63.ec2.internal',
                                   'publicDnsName': 'ec2-54-211-223-78.compute-1.amazonaws.com',
                                   'publicIp': '54.211.223.78', 'localPort': '22', 'remotePort': '33978',
                                   'protocol': 'TCP'}, '@timestamp': '2019-10-30 10:30:06.000', 'region': 'us-east-1',
            'source': 'aws.guardduty', 'account': '979326520502', 'detail.id': '6cb6e99751fcbed76aae1a9a64bb96a8',
            'detail.updatedAt': '2019-10-30T10:17:33.277Z', 'detail.type': 'UnauthorizedAccess:EC2/SSHBruteForce',
            'detail.severity': '2', 'detail.service.resourceRole': 'TARGET',
            'iamInstanceProfileId': 'AIPA6IBDIZS3ES3TI5TNQ', 'imageId': 'ami-04763b3055de4860b',
            'instanceId': 'i-0b8fd03ade35c681d', 'localPortName': 'SSH', 'remotePortName': 'Unknown',
            'groupName': 'launch-wizard-1', 'groupId': 'sg-0aa89ff4646f71594', 'subnetId': 'subnet-c62a11e8',
            'vpcId': 'vpc-10db926a', 'resourceType': 'Instance', 'actionType': 'NETWORK_CONNECTION',
            'network_blocked': '0', 'network_direction': 'INBOUND', 'network_countryName': 'United States',
            'network_asn': '14618', 'network_asnOrg': 'Amazon.com, Inc.',
            '@ptr':
                'CmQKKwonOTc5MzI2NTIwNTAyOi9hd3MvZXZlbnRzL3NlY3VyaXR5aHViYWxsEAQSNRoYAgXKYCpeAAAAAZm7kHAABduWYXAAAAHiI'
                'AEosMfc4eEtMLDH3OHhLTgBQOsVSP1XUJhAEAAYAQ==',
            'event_count': 1}}

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
        assert observed_data['x_com_cwl_timestamp'] is not None
        assert observed_data['created'] is not None
        assert observed_data['modified'] is not None
        assert observed_data['number_observed'] is not None

    def test_vpc_flow_network_json_to_stix(self):
        """to test network stix object properties"""
        data = {
            'vpcflow': {'@timestamp': '2019-10-30 10:43:00.000', 'srcAddr': '159.203.81.129', 'dstAddr': '172.31.88.63',
                        'srcPort': '32773', 'dstPort': '8088', 'protocol': 'tcp', 'start': '1572432180',
                        'end': '1572432229', 'accountId': '979326520502', 'interfaceId': 'eni-02e70b8e842c70a2f',
                        'bytes': '40', 'packets': '1',
                        '@ptr':
                            'CloKIQodOTc5MzI2NTIwNTAyOlVTRWFzdDFfRmxvd0xvZ3MQBBI1GhgCBdlAMFMAAAAAg2EkAgAF25a1cAAAADIgAS'
                            'jwgYji4S0w2NyW4uEtOCxA5zFIySlQyCIQERgB',
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
        assert network_obj['src_port'] == 32773
        assert network_obj['dst_port'] == 8088
        assert network_obj['protocols'] == ['tcp']
        assert network_obj['start'] == '2019-10-30T10:43:00.000Z'
        assert network_obj['end'] == '2019-10-30T10:43:49.000Z'

    def test_vpc_flow_custom_attr_json_to_stix(self):
        """to test network stix object properties"""
        data = {
            'vpcflow': {'@timestamp': '2019-10-30 10:43:00.000', 'srcAddr': '159.203.81.129', 'dstAddr': '172.31.88.63',
                        'srcPort': '32773', 'dstPort': '8088', 'protocol': 'tcp', 'start': '1572432180',
                        'end': '1572432229', 'accountId': '979326520502', 'interfaceId': 'eni-02e70b8e842c70a2f',
                        'bytes': '40', 'packets': '1',
                        '@ptr':
                            'CloKIQodOTc5MzI2NTIwNTAyOlVTRWFzdDFfRmxvd0xvZ3MQBBI1GhgC'
                            'BdlAMFMAAAAAg2EkAgAF25a1cAAAADIgASjwgYji4S0w2NyW4uEtOCxA5zFIySlQyCIQERgB',
                        'event_count': 1}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        custom_object = observed_data['x_com_vpc_flow']

        assert custom_object.keys() == {'account_id', 'interface_id'}
        assert custom_object['account_id'] == '979326520502'
        assert custom_object['interface_id'] == 'eni-02e70b8e842c70a2f'

    def test_guardduty_network_json_to_stix(self):
        """to test network stix object properties"""
        data = {'guardduty': {'NETWORK_CONNECTION': {'version': '0', 'id': 'dfd97470-7b65-4123-3611-894bac10262c',
                                                     'detail-type': 'GuardDuty Finding', 'time': '2019-10-20T10:30:04Z',
                                                     'region': 'us-east-1', 'detail_schemaVersion': '2.0',
                                                     'detail_accountId': '979326520502', 'detail_partition': 'aws',
                                                     'detail_arn': 'arn:aws:guardduty:us-east-1:979326520502:detector'
                                                                   '/6ab6e6ee780ed494f3b7ca56acdc74df/finding/6cb6e9975'
                                                                   '1fcbed76aae1a9a64bb96a8',
                                                     'detail_resource_instanceDetails_instanceId': 'i-0b8fd03ade35c68'
                                                                                                   '1d',
                                                     'detail_resource_instanceDetails_instanceType': 't2.micro',
                                                     'detail_resource_instanceDetails_launchTime': '2019-10-14T12:51'
                                                                                                   ':57Z',
                                                     'detail_resource_instanceDetails_platform': None,
                                                     'detail_resource_instanceDetails_iamInstanceProfile_arn':
                                                         'arn:aws:iam::979326520502:instance-profile/EC2_Instances_Full'
                                                         '_'
                                                         'Access', 'detail_resource_instanceDetails_iamInstanceProfile_'
                                                                   'id': 'AIPA6IBDIZS3ES3TI5TNQ',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_networkInter'
                                                     'faceId': 'eni-02e70b8e842c70a2f',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_privateD'
                                                     'nsName': 'ip-172-31-88-63.ec2.internal',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_privateIpAddr'
                                                     'ess': '172.31.88.63', 'detail_resource_instanceDetails_networkIn'
                                                                            'terfaces_0_privateIpAddresses_0_privateDn'
                                                                            'sName': 'ip-172-31-88-63.ec2.internal',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_privateIpAddr'
                                                     'e'
                                                     'sses_0_privateIpAddress': '172.31.88.63',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_subnetId':
                                                         'subnet-c62a11e8',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_vpcId':
                                                         'vpc-10db926a',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_securityGrou'
                                                     'ps_0_groupName': 'launch-wizard-1',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_securityGro'
                                                     'ups_0_groupId': 'sg-0aa89ff4646f71594',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_publicDnsNa'
                                                     'me': 'ec2-54-211-223-78.compute-1.amazonaws.com',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_publicI'
                                                     'p': '54.211.223.78',
                                                     'detail_resource_instanceDetails_instanceState': 'running',
                                                     'detail_resource_instanceDetails_availabilityZone': 'us-east-1b',
                                                     'detail_resource_instanceDetails_imageId': 'ami-04763b3055de4860b',
                                                     'detail_resource_instanceDetails_imageDescription':
                                                         'Canonical, Ubuntu, 16.04 LTS, amd64 xenial image build on 201'
                                                         '9-09-13', 'detail_service_serviceName': 'guardduty',
                                                     'detail_service_detectorId': '6ab6e6ee780ed494f3b7ca56acdc74df',
                                                     'detail_service_action_networkConnectionAction_'
                                                     'connectionDirection': 'INBOUND',
                                                     'detail_service_action_networkConnectionAction_'
                                                     'remoteIpDetails_ipAddressV4': '54.211.162.49',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_org'
                                                     'anization_asn': '14618',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_asnOrg': 'Amazon.com, Inc.',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_o'
                                                     'rganization_isp': 'Amazon.com',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_org': 'Amazon.com',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_c'
                                                     'ountry_countryName': 'United States',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_cit'
                                                     'y_cityName': 'Ashburn',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_ge'
                                                     'oLocation_lat': 39.0481,
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_g'
                                                     'eoLocation_lon': -77.4728,
                                                     'detail_service_action_networkConnectionAction_remotePortDeta'
                                                     'ils_port': 33972,
                                                     'detail_service_action_networkConnectionAction_remotePortDetails_'
                                                     'portName': 'Unknown',
                                                     'detail_service_action_networkConnectionAction_localPortDetai'
                                                     'ls_port': 22,
                                                     'detail_service_action_networkConnectionAction_localPortDetails_'
                                                     'portName': 'SSH',
                                                     'detail_service_action_networkConnectionAction_protocol': 'TCP',
                                                     'detail_service_action_networkConnectionAction_blocked': False,
                                                     'detail_service_evidence': None}, 'source': 'aws.guardduty',
                              'account': '979326520502', 'detail_region': 'us-east-1', 'detail_id': '6cb6e99751fcbe'
                                                                                                    'd76aae1a9a64bb96a8'
                                                                                                    '',
                              'detail_type': 'UnauthorizedAccess:EC2/SSHBruteForce',
                              'detail_resource_resourceType': 'Instance',
                              'detail_service_action_actionType': 'NETWORK_CONNECTION', 'detail_service_resourceRole':
                                  'TARGET', 'detail_service_eventFirstSeen': '2019-10-16T05:55:25Z',
                              'detail_service_eventLastSeen': '2019-10-20T10:14:08Z', 'detail_service_archived': False,
                              'detail_service_count': 30, 'detail_severity': 2,
                              'detail_createdAt': '2019-10-16T06:08:32.249Z',
                              'detail_updatedAt': '2019-10-20T10:26:06.983Z',
                              'detail_title': '54.211.162.49 is performing SSH brute force attacks against i-'
                                              '0b8fd03ade35c681d. ',
                              'detail_description': '54.211.162.49 is performing SSH brute force attacks again'
                                                    'st i-0b8fd03ade35c681d. Brute force attacks are used to gain una'
                                                    'uthorized access to your instance by guessing the SSH password.',
                              '@timestamp': '2019-10-20 10:30:04.000', 'event_count': 1}}
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
        assert network_obj['dst_port'] == 33972
        assert network_obj['src_ref'] == '1'
        assert network_obj['dst_ref'] == '5'
        assert network_obj['src_port'] == 22
        assert network_obj['protocols'] == ['tcp']

    def test_guardduty_custom_attr_json_to_stix(self):
        """to test network stix object properties"""
        data = {'guardduty': {'NETWORK_CONNECTION': {'version': '0', 'id': '553f211b-bc2b-41a4-2528-2a1325397d00',
                                                     'detail-type': 'GuardDuty Finding', 'time': '2019-11-29T08:00:17Z',
                                                     'region': 'us-east-1', 'detail_schemaVersion': '2.0',
                                                     'detail_accountId': '979326520502', 'detail_partition': 'aws',
                                                     'detail_arn': 'arn:aws:guardduty:us-east-1:979326520502:detecto'
                                                                   '/6ab6e6ee780ed494f3b7ca56acdc74df/finding/60b6ecb3'
                                                                   '9e88c74c25b8fd425289ba88',
                                                     'detail_resource_instanceDetails_instanceId': 'i-99999999',
                                                     'detail_resource_instanceDetails_instanceType': 'm3.xlarge',
                                                     'detail_resource_instanceDetails_launchTime': '2016-08-02T02:0'
                                                                                                   '5:06Z',
                                                     'detail_resource_instanceDetails_productCodes_0_productCodeId':
                                                         'GeneratedFindingProductCodeId',
                                                     'detail_resource_instanceDetails_productCodes_0_productCodeType':
                                                         'GeneratedFindingProductCodeType',
                                                     'detail_resource_instanceDetails_iamInstanceProfile_arn':
                                                         'GeneratedFindingInstanceProfileArn',
                                                     'detail_resource_instanceDetails_iamInstanceProfile_id':
                                                         'GeneratedFindingInstanceProfileId',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_networkInt'
                                                     'erfaceId': 'eni-bfcffe88',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_privateDnsNam'
                                                     'e': 'GeneratedFindingPrivateDnsName',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_privateIpAd'
                                                     'dress': '10.0.0.1',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_privateIpAdd'
                                                     'resses_0_privateDnsName': 'GeneratedFindingPrivateName',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_privateIpAdd'
                                                     'resses_0_privateIpAddress': '10.0.0.1',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_subnetId':
                                                         'GeneratedFindingSubnetId',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_vpcId':
                                                         'GeneratedFindingVPCId',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_securityGr'
                                                     'oups_0_groupName': 'GeneratedFindingSecurityGroupName',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_securityGr'
                                                     'oups_0_groupId': 'GeneratedFindingSecurityId',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_publicDn'
                                                     'sName': 'GeneratedFindingPublicDNSName',
                                                     'detail_resource_instanceDetails_networkInterfaces_0_publicIp':
                                                         '198.51.100.0',
                                                     'detail_resource_instanceDetails_tags_0_key':
                                                         'GeneratedFindingInstaceTag1',
                                                     'detail_resource_instanceDetails_tags_0_value':
                                                         'GeneratedFindingInstaceValue1',
                                                     'detail_resource_instanceDetails_tags_1_key':
                                                         'GeneratedFindingInstaceTag2',
                                                     'detail_resource_instanceDetails_tags_1_value':
                                                         'GeneratedFindingInstaceTagValue2',
                                                     'detail_resource_instanceDetails_tags_2_key':
                                                         'GeneratedFindingInstaceTag3',
                                                     'detail_resource_instanceDetails_tags_2_value':
                                                         'GeneratedFindingInstaceTagValue3',
                                                     'detail_resource_instanceDetails_tags_3_key':
                                                         'GeneratedFindingInstaceTag4',
                                                     'detail_resource_instanceDetails_tags_3_value':
                                                         'GeneratedFindingInstaceTagValue4',
                                                     'detail_resource_instanceDetails_tags_4_key':
                                                         'GeneratedFindingInstaceTag5',
                                                     'detail_resource_instanceDetails_tags_4_value':
                                                         'GeneratedFindingInstaceTagValue5',
                                                     'detail_resource_instanceDetails_tags_5_key':
                                                         'GeneratedFindingInstaceTag6',
                                                     'detail_resource_instanceDetails_tags_5_value':
                                                         'GeneratedFindingInstaceTagValue6',
                                                     'detail_resource_instanceDetails_tags_6_key':
                                                         'GeneratedFindingInstaceTag7',
                                                     'detail_resource_instanceDetails_tags_6_value':
                                                         'GeneratedFindingInstaceTagValue7',
                                                     'detail_resource_instanceDetails_tags_7_key':
                                                         'GeneratedFindingInstaceTag8',
                                                     'detail_resource_instanceDetails_tags_7_value':
                                                         'GeneratedFindingInstaceTagValue8',
                                                     'detail_resource_instanceDetails_tags_8_key':
                                                         'GeneratedFindingInstaceTag9',
                                                     'detail_resource_instanceDetails_tags_8_value':
                                                         'GeneratedFindingInstaceTagValue9',
                                                     'detail_resource_instanceDetails_instanceState': 'running',
                                                     'detail_resource_instanceDetails_availabilityZone':
                                                         'GeneratedFindingInstaceAvailabilityZone',
                                                     'detail_resource_instanceDetails_imageId': 'ami-99999999',
                                                     'detail_resource_instanceDetails_imageDescription':
                                                         'GeneratedFindingInstaceImageDescription',
                                                     'detail_service_serviceName': 'guardduty',
                                                     'detail_service_detectorId': '6ab6e6ee780ed494f3b7ca56acdc74df',
                                                     'detail_service_action_networkConnectionAction_'
                                                     'connectionDirection': 'OUTBOUND',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetai'
                                                     'ls_ipAddressV4': '198.51.100.0',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetail'
                                                     's_organization_asn': '-1',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetai'
                                                     'ls_organization_asnOrg': 'GeneratedFindingASNOrg',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails'
                                                     '_organization_isp': 'GeneratedFindingISP',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'organization_org': 'GeneratedFindingORG',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'country_countryName': 'United States',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'city_cityName': 'GeneratedFindingCityName',
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_geo'
                                                     'Location_lat': 0,
                                                     'detail_service_action_networkConnectionAction_remoteIpDetails_'
                                                     'geoLocation_lon': 0,
                                                     'detail_service_action_networkConnectionAction_remotePortDetails'
                                                     '_port': 22,
                                                     'detail_service_action_networkConnectionAction_remotePortDetail'
                                                     's_portName': 'SSH',
                                                     'detail_service_action_networkConnectionAction_localPortDetails'
                                                     '_port': 2000,
                                                     'detail_service_action_networkConnectionAction_localPortDetail'
                                                     's_portName': 'Unknown',
                                                     'detail_service_action_networkConnectionAction_protocol': 'TCP',
                                                     'detail_service_action_networkConnectionAction_blocked': 'false',
                                                     'detail_service_additionalInfo_unusualProtocol': 'UDP',
                                                     'detail_service_additionalInfo_threatListName':
                                                         'GeneratedFindingThreatListName',
                                                     'detail_service_additionalInfo_unusual': 22,
                                                     'detail_service_additionalInfo_sample': True,
                                                     'detail_service_evidence_threatIntelligenceDetails_0_threatL'
                                                     'istName': 'GeneratedFindingThreatListName',
                                                     'detail_service_evidence_threatIntelligenceDetails_0_threatNam'
                                                     'es_0': 'GeneratedFindingThreatName'},
                              'source': 'aws.guardduty', 'account': '979326520502', 'detail_region': 'us-east-1',
                              'detail_id': '60b6ecb39e88c74c25b8fd425289ba88', 'detail_type': 'Trojan:EC2/DropPoint',
                              'detail_resource_resourceType': 'Instance',
                              'detail_service_action_actionType': 'NETWORK_CONNECTION',
                              'detail_service_resourceRole': 'TARGET',
                              'detail_service_eventFirstSeen': '2019-10-17T11:08:04.753Z',
                              'detail_service_eventLastSeen': '2019-11-29T07:58:47.043Z',
                              'detail_service_archived': 'false', 'detail_service_count': 2, 'detail_severity': 5,
                              'detail_createdAt': '2019-10-17T11:08:04.753Z',
                              'detail_updatedAt': '2019-11-29T07:58:47.043Z',
                              'detail_title': 'EC2 instance i-99999999 is communicating with a Drop Point.',
                              'detail_description': 'EC2 instance i-99999999 is communicating with a remote host 198.'
                                                    '51.100.0 that is known to hold credentials and other stolen data'
                                                    ' captured by malware.',
                              '@timestamp': '2019-11-29 08:00:17.000', 'event_count': 1}}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], transformers.get_all_transformers(), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        custom_object = observed_data['x_com_guardduty_findings']

        assert custom_object.keys() == {'resource', 'service', 'region', 'source', 'account_id',
                                        'id', 'updated_at',
                                        'type', 'severity', 'title'}
        assert custom_object['resource'] == {'instance_details': {'instance_id': 'i-99999999', 'iam_instance_profile': {
            'id': 'GeneratedFindingInstanceProfileId'}, 'network_interfaces_0': {'network_interface_id': 'eni-bfcffe88',
                                                                                 'private_dns_name_ref':
                                                                                     'GeneratedFindingPrivateDnsName',
                                                                                 'private_ip_address_ref': '0',
                                                                                 'subnet_id': 'GeneratedFindingSubnetId',
                                                                                 'vpc_id': 'GeneratedFindingVPCId',
                                                                                 'security_groups': {
                                                                                     'group_name':
                                                                                         'GeneratedFindingSecurityGroupName',
                                                                                     'group_id':
                                                                                         'GeneratedFindingSecurityId'},
                                                                                 'public_dns_name_ref': 'GeneratedFindingPublicDNSName',
                                                                                 'public_ip_ref': '3'},
                                                                  'tags_0': {'key': 'GeneratedFindingInstaceTag1',
                                                                             'value': 'GeneratedFindingInstaceValue1'},
                                                                  'image_id': 'ami-99999999'},
                                             'resource_type': 'Instance'}

        assert custom_object['service'] == {'action': {'network_connection_action': {'connection_direction': 'OUTBOUND',
                                                                                     'remote_ip_details': {
                                                                                         'ip_addressv4': {
                                                                                             'remote_ip_ref': '5'},
                                                                                         'organization': {'asn': '-1',
                                                                                                          'asn_org': 'GeneratedFindingASNOrg'},
                                                                                         'country': {
                                                                                             'country_name': 'United States'}},
                                                                                     'remote_port_details': {
                                                                                         'port_ref': '1',
                                                                                         'port_name': 'SSH'},
                                                                                     'local_port_details': {
                                                                                         'port_ref': '1',
                                                                                         'port_name': 'Unknown'},
                                                                                     'protocol_ref': '1',
                                                                                     'blocked': 'false'},
                                                       'action_type': 'NETWORK_CONNECTION'}, 'resource_role': 'TARGET'}
        assert custom_object['region'] == 'us-east-1'
        assert custom_object['source'] == 'aws.guardduty'
        assert custom_object['account_id'] == '979326520502'
        assert custom_object['id'] == '60b6ecb39e88c74c25b8fd425289ba88'
        assert custom_object['updated_at'] == '2019-11-29T07:58:47.043Z'
        assert custom_object['type'] == 'Trojan:EC2/DropPoint'
        assert custom_object['severity'] == 5
        assert custom_object['title'] == 'EC2 instance i-99999999 is communicating with a Drop Point.'
