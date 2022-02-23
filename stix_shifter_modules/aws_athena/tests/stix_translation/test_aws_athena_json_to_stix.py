from stix_shifter_utils.stix_translation.src.json_to_stix import json_to_stix_translator
from stix_shifter_utils.stix_translation.src.utils.transformer_utils import get_module_transformers
from stix_shifter_modules.aws_athena.entry_point import EntryPoint
import unittest

MODULE = "aws_athena"
entry_point = EntryPoint()
map_data = entry_point.get_results_translator().map_data
data_source = {
    "type": "identity",
    "id": "identity--f431f809-377b-45e0-aa1c-6a4751cae5ff",
    "name": "aws_athena",
    "identity_class": "events"
}
options = {}


class TestAwsResultsToStix(unittest.TestCase):
    """
    class to perform unit test case for Aws Athena logs translate results
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
        data = {
            "guardduty": {
                "accountid": 979326520502,
                "region": "us-east-1",
                "type": "UnauthorizedAccess:EC2/SSHBruteForce",
                "resource_instancedetails_networkinterfaces_0_privatednsname": "ip-172-31-60-104.ec2.internal",
                "resource_instancedetails_networkinterfaces_0_privateipaddress": "172.31.60.104",
                "resource_instancedetails_networkinterfaces_0_subnetid": "subnet-ea9d6be4",
                "resource_instancedetails_networkinterfaces_0_publicdnsname": "ec2-18-210-22-128.compute-1."
                                                                              "amazonaws.com",
                "resource_instancedetails_networkinterfaces_0_vpcid": "vpc-10db926a",
                "resource_instancedetails_networkinterfaces_0_publicip": "18.210.22.128",
                "resource_instancedetails_networkinterfaces_0_networkinterfaceid": "eni-0203098cca62c3f21",
                "resource_instancedetails_networkinterfaces_0_securitygroups_0_groupid": "sg-018edb43fcc81525f",
                "resource_instancedetails_networkinterfaces_0_securitygroups_0_groupname": "launch-wizard-13",
                "resource_instancedetails_imageid": "ami-0015fcaa5516c75ed",
                "resource_instancedetails_instanceid": "i-031cb81e1f32a36e1",
                "resource_instancedetails_availabilityzone": "us-east-1f",
                "service_eventfirstseen": "2020-07-31T06:19:09Z",
                "service_action_networkconnectionaction_protocol": "TCP",
                "service_action_networkconnectionaction_remoteportdetails_port": "38420",
                "service_action_networkconnectionaction_remoteipdetails_country_countryname": "Sweden",
                "service_action_networkconnectionaction_remoteipdetails_ipaddressv4": "85.224.242.94",
                "service_action_networkconnectionaction_remoteipdetails_city_cityname": "\u00d6rebro",
                "service_action_networkconnectionaction_localportdetails_port": "22",
                "service_eventlastseen": "2020-09-12T09:19:40Z",
                "severity": 2,
                "title": "85.224.242.94 is performing SSH brute force attacks against i-031cb81e1f32a36e1.",
                "arn": "arn:aws:guardduty:us-east-1:979326520502:detector/6ab6e6ee780ed494f3b7ca56acdc74df/finding/"
                       "7ab9d1cb6248e05a0e419a79528761cb",
                "createdat": "2020-07-31T06:37:13.745Z",
                "description": "85.224.242.94 is performing SSH brute force attacks against i-031cb81e1f32a36e1. "
                               "Brute force attacks are used to gain unauthorized access to your instance by "
                               "guessing the SSH password.",
                "finding_id": "7ab9d1cb6248e05a0e419a79528761cb",
                "partition": "aws",
                "resource": {
                    "instancedetails": {
                        "imagedescription": "Provided by Red Hat, Inc.",
                        "instancestate": "running",
                        "instancetype": "t2.large",
                        "launchtime": "2020-09-11T23:16:03Z",
                        "tags": {
                            "0": {
                                "key": "Name",
                                "value": "ArcSight Logger"
                            }
                        }
                    },
                    "resourcetype": "Instance"
                },
                "schemaversion": 2.0,
                "service": {
                    "action": {
                        "actiontype": "NETWORK_CONNECTION",
                        "networkconnectionaction": {
                            "connectiondirection": "INBOUND",
                            "localportdetails": {
                                "portname": "SSH"
                            },
                            "remoteipdetails": {
                                "geolocation": {
                                    "lat": "59.2741",
                                    "lon": "15.2066"
                                },
                                "organization": {
                                    "asn": "2119",
                                    "asnorg": "Telenor Norge AS",
                                    "isp": "Telenor Sverige AB",
                                    "org": "Telenor Sverige AB"
                                }
                            },
                            "remoteportdetails": {
                                "portname": "Unknown"
                            }
                        }
                    },
                    "count": "20",
                    "detectorid": "6ab6e6ee780ed494f3b7ca56acdc74df",
                    "resourcerole": "TARGET",
                    "servicename": "guardduty"
                },
                "updatedat": "2020-09-12T09:25:34.086Z"
            }
        }

        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
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
        assert observed_data['created'] is not None
        assert observed_data['modified'] is not None
        assert observed_data['number_observed'] is not None

    def test_vpc_flow_network_json_to_stix(self):
        """to test network stix object properties"""
        data = {
            "vpcflow": {
                "account": 979326520502,
                "interfaceid": "eni-04b762de832716892",
                "sourceaddress": "89.248.172.85",
                "destinationaddress": "172.31.62.249",
                "sourceport": 58387,
                "destinationport": 51289,
                "protocol": "tcp",
                "starttime": 1592547796,
                "endtime": 1592547798,
                "action": "REJECT",
                "date": "2020-06-19",
                "logstatus": "OK",
                "numbytes": 40,
                "region": "us-east-1",
                "version": 2
            }
        }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
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
        assert network_obj['src_ref'] == '1'
        assert network_obj['dst_ref'] == '4'
        assert network_obj['src_port'] == 58387
        assert network_obj['dst_port'] == 51289
        assert network_obj['protocols'] == ['tcp']
        assert network_obj['start'] == '2020-06-19T06:23:16.000Z'
        assert network_obj['end'] == '2020-06-19T06:23:18.000Z'

    def test_vpc_flow_custom_attr_json_to_stix(self):
        """to test network stix object properties"""
        data = {
            "vpcflow": {
                "account": 979326520502,
                "interfaceid": "eni-04b762de832716892",
                "sourceaddress": "89.248.172.85",
                "destinationaddress": "172.31.62.249",
                "sourceport": 58387,
                "destinationport": 51289,
                "protocol": "tcp",
                "starttime": 1592547796,
                "endtime": 1592547798,
                "action": "REJECT",
                "date": "2020-06-19",
                "logstatus": "OK",
                "numbytes": 40,
                "region": "us-east-1",
                "version": 2
            }
        }
        options = {"unmapped_fallback": True}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        custom_object = TestAwsResultsToStix.get_first_of_type(objects.values(), 'x-aws-athena')

        assert custom_object.keys() == {'type', 'interfaceid', 'date', 'logstatus', 'numbytes', 'region', 'version'}
        assert custom_object['date'] == '2020-06-19'
        assert custom_object['logstatus'] == 'OK'
        assert custom_object['numbytes'] == 40
        assert custom_object['region'] == 'us-east-1'
        assert custom_object['version'] == 2

    def test_guardduty_network_json_to_stix(self):
        """to test network stix object properties"""
        data = {
            "guardduty": {
                "accountid": 979326520502,
                "region": "us-east-1",
                "type": "UnauthorizedAccess:EC2/SSHBruteForce",
                "resource_instancedetails_networkinterfaces_0_privatednsname": "ip-172-31-60-104.ec2.internal",
                "resource_instancedetails_networkinterfaces_0_privateipaddress": "172.31.60.104",
                "resource_instancedetails_networkinterfaces_0_subnetid": "subnet-ea9d6be4",
                "resource_instancedetails_networkinterfaces_0_publicdnsname": "ec2-18-210-22-128.compute-1."
                                                                              "amazonaws.com",
                "resource_instancedetails_networkinterfaces_0_vpcid": "vpc-10db926a",
                "resource_instancedetails_networkinterfaces_0_publicip": "18.210.22.128",
                "resource_instancedetails_networkinterfaces_0_networkinterfaceid": "eni-0203098cca62c3f21",
                "resource_instancedetails_networkinterfaces_0_securitygroups_0_groupid": "sg-018edb43fcc81525f",
                "resource_instancedetails_networkinterfaces_0_securitygroups_0_groupname": "launch-wizard-13",
                "resource_instancedetails_imageid": "ami-0015fcaa5516c75ed",
                "resource_instancedetails_instanceid": "i-031cb81e1f32a36e1",
                "resource_instancedetails_availabilityzone": "us-east-1f",
                "service_eventfirstseen": "2020-07-31T06:19:09Z",
                "service_action_networkconnectionaction_protocol": "TCP",
                "service_action_networkconnectionaction_remoteportdetails_port": "38420",
                "service_action_networkconnectionaction_remoteipdetails_country_countryname": "Sweden",
                "service_action_networkconnectionaction_remoteipdetails_ipaddressv4": "85.224.242.94",
                "service_action_networkconnectionaction_remoteipdetails_city_cityname": "rebro",
                "service_action_networkconnectionaction_localportdetails_port": "22",
                "service_eventlastseen": "2020-09-12T09:19:40Z",
                "severity": 2,
                "title": "85.224.242.94 is performing SSH brute force attacks against i-031cb81e1f32a36e1.",
                "arn": "arn:aws:guardduty:us-east-1:979326520502:detector/6ab6e6ee780ed494f3b7ca56acdc74df/finding"
                       "/7ab9d1cb6248e05a0e419a79528761cb",
                "createdat": "2020-07-31T06:37:13.745Z",
                "description": "85.224.242.94 is performing SSH brute force attacks against i-031cb81e1f32a36e1. "
                               "Brute force attacks are used to gain unauthorized access to your instance by "
                               "guessing the SSH password.",
                "finding_id": "7ab9d1cb6248e05a0e419a79528761cb",
                "partition": "aws",
                "resource": {
                    "instancedetails": {
                        "imagedescription": "Provided by Red Hat, Inc.",
                        "instancestate": "running",
                        "instancetype": "t2.large",
                        "launchtime": "2020-09-11T23:16:03Z",
                        "tags": {
                            "0": {
                                "key": "Name",
                                "value": "ArcSight Logger"
                            }
                        }
                    },
                    "resourcetype": "Instance"
                },
                "schemaversion": 2.0,
                "service": {
                    "action": {
                        "actiontype": "NETWORK_CONNECTION",
                        "networkconnectionaction": {
                            "connectiondirection": "INBOUND",
                            "localportdetails": {
                                "portname": "SSH"
                            },
                            "remoteipdetails": {
                                "geolocation": {
                                    "lat": "59.2741",
                                    "lon": "15.2066"
                                },
                                "organization": {
                                    "asn": "2119",
                                    "asnorg": "Telenor Norge AS",
                                    "isp": "Telenor Sverige AB",
                                    "org": "Telenor Sverige AB"
                                }
                            },
                            "remoteportdetails": {
                                "portname": "Unknown"
                            }
                        }
                    },
                    "count": "20",
                    "detectorid": "6ab6e6ee780ed494f3b7ca56acdc74df",
                    "resourcerole": "TARGET",
                    "servicename": "guardduty"
                },
                "updatedat": "2020-09-12T09:25:34.086Z"
            }
        }
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
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
        assert network_obj['dst_port'] == 38420
        assert network_obj['src_ref'] == '3'
        assert network_obj['dst_ref'] == '9'
        assert network_obj['src_port'] == 22
        assert network_obj['protocols'] == ['tcp']

    def test_guardduty_custom_attr_json_to_stix(self):
        """to test network stix object properties"""
        data = {
            "guardduty": {
                "accountid": 979326520502,
                "region": "us-east-1",
                "type": "UnauthorizedAccess:EC2/SSHBruteForce",
                "resource_instancedetails_networkinterfaces_0_privatednsname": "ip-172-31-60-104.ec2.internal",
                "resource_instancedetails_networkinterfaces_0_privateipaddress": "172.31.60.104",
                "resource_instancedetails_networkinterfaces_0_subnetid": "subnet-ea9d6be4",
                "resource_instancedetails_networkinterfaces_0_publicdnsname": "ec2-18-210-22-128.compute-1."
                                                                              "amazonaws.com",
                "resource_instancedetails_networkinterfaces_0_vpcid": "vpc-10db926a",
                "resource_instancedetails_networkinterfaces_0_publicip": "18.210.22.128",
                "resource_instancedetails_networkinterfaces_0_networkinterfaceid": "eni-0203098cca62c3f21",
                "resource_instancedetails_networkinterfaces_0_securitygroups_0_groupid": "sg-018edb43fcc81525f",
                "resource_instancedetails_networkinterfaces_0_securitygroups_0_groupname": "launch-wizard-13",
                "resource_instancedetails_imageid": "ami-0015fcaa5516c75ed",
                "resource_instancedetails_instanceid": "i-031cb81e1f32a36e1",
                "resource_instancedetails_availabilityzone": "us-east-1f",
                "service_eventfirstseen": "2020-07-31T06:19:09Z",
                "service_action_networkconnectionaction_protocol": "TCP",
                "service_action_networkconnectionaction_remoteportdetails_port": "38420",
                "service_action_networkconnectionaction_remoteipdetails_country_countryname": "Sweden",
                "service_action_networkconnectionaction_remoteipdetails_ipaddressv4": "85.224.242.94",
                "service_action_networkconnectionaction_remoteipdetails_city_cityname": "rebro",
                "service_action_networkconnectionaction_localportdetails_port": "22",
                "service_eventlastseen": "2020-09-12T09:19:40Z",
                "severity": 2,
                "title": "85.224.242.94 is performing SSH brute force attacks against i-031cb81e1f32a36e1.",
                "arn": "arn:aws:guardduty:us-east-1:979326520502:detector/6ab6e6ee780ed494f3b7ca56acdc74df/finding/"
                       "7ab9d1cb6248e05a0e419a79528761cb",
                "createdat": "2020-07-31T06:37:13.745Z",
                "description": "85.224.242.94 is performing SSH brute force attacks against i-031cb81e1f32a36e1."
                               " Brute force attacks are used to gain unauthorized access to your instance by guessing "
                               "the SSH password.",
                "finding_id": "7ab9d1cb6248e05a0e419a79528761cb",
                "partition": "aws",
                "resource": {
                    "instancedetails": {
                        "imagedescription": "Provided by Red Hat, Inc.",
                        "instancestate": "running",
                        "instancetype": "t2.large",
                        "launchtime": "2020-09-11T23:16:03Z",
                        "tags": {
                            "0": {
                                "key": "Name",
                                "value": "ArcSight Logger"
                            }
                        }
                    },
                    "resourcetype": "Instance"
                },
                "schemaversion": 2.0,
                "service": {
                    "action": {
                        "actiontype": "NETWORK_CONNECTION",
                        "networkconnectionaction": {
                            "connectiondirection": "INBOUND",
                            "localportdetails": {
                                "portname": "SSH"
                            },
                            "remoteipdetails": {
                                "geolocation": {
                                    "lat": "59.2741",
                                    "lon": "15.2066"
                                },
                                "organization": {
                                    "asn": "2119",
                                    "asnorg": "Telenor Norge AS",
                                    "isp": "Telenor Sverige AB",
                                    "org": "Telenor Sverige AB"
                                }
                            },
                            "remoteportdetails": {
                                "portname": "Unknown"
                            }
                        }
                    },
                    "count": "20",
                    "detectorid": "6ab6e6ee780ed494f3b7ca56acdc74df",
                    "resourcerole": "TARGET",
                    "servicename": "guardduty"
                },
                "updatedat": "2020-09-12T09:25:34.086Z"
            }
        }
        options = {"unmapped_fallback": True}
        result_bundle = json_to_stix_translator.convert_to_stix(
            data_source, map_data, [data], get_module_transformers(MODULE), options)
        result_bundle_objects = result_bundle['objects']

        result_bundle_identity = result_bundle_objects[0]
        assert result_bundle_identity['type'] == data_source['type']

        observed_data = result_bundle_objects[1]

        assert 'objects' in observed_data
        objects = observed_data['objects']
        custom_object = TestAwsResultsToStix.get_first_of_type(objects.values(), 'x-aws-athena')

        assert custom_object.keys() == {'type', 'service_action_networkconnectionaction_remoteipdetails_country_countryname', 
                                        'finding_id', 'arn', 'createdat', 'partition', 'resource',
                                        'schemaversion', 'service', 'updatedat'}
        assert custom_object['arn'] == 'arn:aws:guardduty:us-east-1:979326520502:detector/6ab6e6ee780ed' \
                                       '494f3b7ca56acdc74df/finding/7ab9d1cb6248e05a0e419a79528761cb'
        assert custom_object['finding_id'] == '7ab9d1cb6248e05a0e419a79528761cb'
        assert custom_object['createdat'] == '2020-07-31T06:37:13.745Z'
        assert custom_object['partition'] == 'aws'
        assert custom_object['schemaversion'] == 2.0
        assert custom_object['updatedat'] == '2020-09-12T09:25:34.086Z'
