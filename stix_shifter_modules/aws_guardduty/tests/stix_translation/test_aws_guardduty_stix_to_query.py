from stix_shifter.stix_translation import stix_translation
import unittest

translation = stix_translation.StixTranslation()


def _remove_timestamp_from_query(query):
    for i in range(len(query['queries'])):
        del (query['queries'][i]['FindingCriteria']['Criterion']['updatedAt'])
    return query


class TestQueryTranslator(unittest.TestCase):
    """
    class to perform unit test case aws_guardduty translate query
    """
    if __name__ == "__main__":
        unittest.main()

    def _test_query_assertions(self, query, queries):
        """
        to assert the each query in the list against expected result
        """
        self.assertIsInstance(queries, dict)
        self.assertIsInstance(query, dict)
        self.assertIsInstance(query['queries'], list)
        self.assertEqual(query, queries)

    def test_ipv4_query(self):
        stix_pattern = "[ipv4-addr:value = '198.51.100.0']"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "resource.instanceDetails.networkInterfaces.privateIpAddresses.privateIpAddress": {
                                "Equals": [
                                    "198.51.100.0"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687074624826,
                                "LessThanOrEqual": 1687074924826
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "resource.instanceDetails.networkInterfaces.publicIp": {
                                "Equals": [
                                    "198.51.100.0"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687074624826,
                                "LessThanOrEqual": 1687074924826
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.networkConnectionAction.remoteIpDetails.ipAddressV4": {
                                "Equals": [
                                    "198.51.100.0"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687074624826,
                                "LessThanOrEqual": 1687074924826
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.awsApiCallAction.remoteIpDetails.ipAddressV4": {
                                "Equals": [
                                    "198.51.100.0"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687074624826,
                                "LessThanOrEqual": 1687074924826
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.kubernetesApiCallAction.remoteIpDetails.ipAddressV4": {
                                "Equals": [
                                    "198.51.100.0"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687074624826,
                                "LessThanOrEqual": 1687074924826
                            }}}}
            ]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_autonomous_system_lt_operator(self):
        stix_pattern = "[autonomous-system:number < 1]"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [
            {
                "FindingCriteria": {
                    "Criterion": {
                        "service.action.networkConnectionAction.remoteIpDetails.organization.asn": {
                            "LessThan": 1
                        },
                        "updatedAt": {
                            "GreaterThanOrEqual": 1688202355837,
                            "LessThanOrEqual": 1688202655837
                        }}}},
            {
                "FindingCriteria": {
                    "Criterion": {
                        "service.action.awsApiCallAction.remoteIpDetails.organization.asn": {
                            "LessThan": 1
                        },
                        "updatedAt": {
                            "GreaterThanOrEqual": 1688202355837,
                            "LessThanOrEqual": 1688202655837
                        }}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_ipv6_not_equal_operator(self):
        stix_pattern = "[ipv6-addr:value != '2001:0db8:85a3:0000:0000:8a2e:0370:7334']"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{
            "FindingCriteria": {
                "Criterion": {
                    "resource.instanceDetails.networkInterfaces.ipv6Addresses": {
                        "NotEquals": [
                            "2001:0db8:85a3:0000:0000:8a2e:0370:7334"
                        ]
                    },
                    "updatedAt": {
                        "GreaterThanOrEqual": 1688202475717,
                        "LessThanOrEqual": 1688202775717
                    }}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_boolean_operator(self):
        stix_pattern = "[x-ibm-finding:x_archived = 0 ]"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"FindingCriteria": {"Criterion": {"service.archived": {"Equals": ["false"]},
                                                                  "updatedAt": {"GreaterThanOrEqual": 1686757300141,
                                                                                "LessThanOrEqual": 1686757600141}}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_oca_geo_query(self):
        stix_pattern = "[x-oca-geo:country_name = 'Germany']"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{
            "FindingCriteria": {
                "Criterion": {
                    "service.action.networkConnectionAction.remoteIpDetails.country.countryName": {
                        "Equals": [
                            "Germany"
                        ]
                    },
                    "updatedAt": {
                        "GreaterThanOrEqual": 1688202899562,
                        "LessThanOrEqual": 1688203199562
                    }}}},
            {
                "FindingCriteria": {
                    "Criterion": {
                        "service.action.awsApiCallAction.remoteIpDetails.country.countryName": {
                            "Equals": [
                                "Germany"
                            ]
                        },
                        "updatedAt": {
                            "GreaterThanOrEqual": 1688202899562,
                            "LessThanOrEqual": 1688203199562
                        }}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_traffic_gt_operator(self):
        stix_pattern = "[network-traffic:src_port > 32794]"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"FindingCriteria": {"Criterion": {"service.action.networkConnectionAction.localPort"
                                                                  "Details." "port": {"GreaterThan": 32794},
                                                                  "updatedAt": {"GreaterThanOrEqual": 1685960443489,
                                                                                "LessThanOrEqual": 1685960743489}}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_user_account_query(self):
        stix_pattern = "[user-account:x_access_key_id='ASIARRRRRRGGGGAAAAAAA']"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{
            "FindingCriteria": {
                "Criterion": {
                    "resource.accessKeyDetails.accessKeyId": {
                        "Equals": [
                            "ASIARRRRRRGGGGAAAAAAA"
                        ]
                    },
                    "updatedAt": {
                        "GreaterThanOrEqual": 1688203091738,
                        "LessThanOrEqual": 1688203391738
                    }
                }}}]}

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_domain_name_query(self):
        stix_pattern = "[domain-name:value ='ec2-1-1-1-1.compute-1.amazonaws.com']"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{
            "FindingCriteria": {
                "Criterion": {
                    "resource.instanceDetails.networkInterfaces.publicDnsName": {
                        "Equals": [
                            "ec2-1-1-1-1.compute-1.amazonaws.com"
                        ]
                    },
                    "updatedAt": {
                        "GreaterThanOrEqual": 1688203150008,
                        "LessThanOrEqual": 1688203450008
                    }}}},
            {
                "FindingCriteria": {
                    "Criterion": {
                        "service.action.dnsRequestAction.domain": {
                            "Equals": [
                                "ec2-1-1-1-1.compute-1.amazonaws.com"
                            ]
                        },
                        "updatedAt": {
                            "GreaterThanOrEqual": 1688203150008,
                            "LessThanOrEqual": 1688203450008
                        }}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_network_traffic_gt_equal_operator(self):
        stix_pattern = "[network-traffic:src_port >= 32794]"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.networkConnectionAction.localPortDetails.port": {
                                "GreaterThanOrEqual": 32794
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1688203233380,
                                "LessThanOrEqual": 1688203533380
                            }}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_ibm_finding_in_operator(self):
        stix_pattern = "[x-ibm-finding:severity IN (8,15)]"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {"queries": [{"FindingCriteria": {"Criterion": {"severity": {"Equals": ["8", "15"]},
                                                                  "updatedAt": {"GreaterThanOrEqual": 1686360236693,
                                                                                "LessThanOrEqual": 1686360536693}}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_enum_type_fields(self):
        stix_pattern = "[x-aws-finding-service:action.action_type = 'NETWORK_CONNECTION']START " \
                       "t'2023-02-10T16:43:26.000Z' STOP t'2023-05-30T16:43:26.003Z'"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [{
                "FindingCriteria": {
                    "Criterion": {
                        "service.action.actionType": {
                            "Equals": [
                                "NETWORK_CONNECTION"
                            ]
                        },
                        "updatedAt": {
                            "GreaterThanOrEqual": 1676047406000,
                            "LessThanOrEqual": 1685465006003
                        }}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_x_ibm_finding_not_in_operator(self):
        stix_pattern = "[x-ibm-finding:severity NOT IN (8,15)]"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "severity": {
                                "NotEquals": [
                                    "8",
                                    "15"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1688206119205,
                                "LessThanOrEqual": 1688206419205
                            }}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_autonomous_system_lt_equal_operator(self):
        stix_pattern = "[autonomous-system:number <= 1]"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.networkConnectionAction.remoteIpDetails.organization.asn": {
                                "LessThanOrEqual": 1
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1688204480628,
                                "LessThanOrEqual": 1688204780628
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.awsApiCallAction.remoteIpDetails.organization.asn": {
                                "LessThanOrEqual": 1
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1688204480628,
                                "LessThanOrEqual": 1688204780628
                            }
                        }}}]}

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_autonomous_system_not_lt_equal_operator(self):
        stix_pattern = "[autonomous-system:number NOT <= 1]"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.networkConnectionAction.remoteIpDetails.organization.asn": {
                                "GreaterThan": 1
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687071785287,
                                "LessThanOrEqual": 1687072085287
                            }
                        }
                    }
                },
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.awsApiCallAction.remoteIpDetails.organization.asn": {
                                "GreaterThan": 1
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687071785287,
                                "LessThanOrEqual": 1687072085287
                            }
                        }
                    }
                }
            ]
        }
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_for_same_stix_attributes_with_different_operators_joined_by_OR(self):
        stix_pattern = "[x-aws-finding-service:action.service_name='ec2.amazonaws.com' " \
                       "OR x-aws-instance:image_id='ami-99999999' OR x-aws-instance:image_id NOT IN ('ami-55555555')]" \
                       "START t'2023-02-10T16:43:26.000Z' STOP t'2023-05-30T16:43:26.003Z'"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "resource.instanceDetails.imageId": {
                                "NotEquals": [
                                    "ami-55555555"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1676047406000,
                                "LessThanOrEqual": 1685465006003
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.awsApiCallAction.serviceName": {
                                "Equals": [
                                    "ec2.amazonaws.com"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1676047406000,
                                "LessThanOrEqual": 1685465006003
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "resource.instanceDetails.imageId": {
                                "Equals": [
                                    "ami-99999999"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1676047406000,
                                "LessThanOrEqual": 1685465006003
                            }}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_for_morethan_two_comparison_expressions_joined_by_AND(self):
        stix_pattern = "[x-aws-finding-service:action.service_name='ec2.amazonaws.com' " \
                       "AND x-aws-instance:image_id='ami-99999999' AND x-aws-s3-bucket:tag_value = 'bar']START " \
                       "t'2023-01-10T16:43:26.000Z' STOP t'2023-05-16T16:43:26.003Z'"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "resource.s3BucketDetails.tags.value": {
                                "Equals": [
                                    "bar"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1673369006000,
                                "LessThanOrEqual": 1684255406003
                            },
                            "resource.instanceDetails.imageId": {
                                "Equals": [
                                    "ami-99999999"
                                ]
                            },
                            "service.action.awsApiCallAction.serviceName": {
                                "Equals": [
                                    "ec2.amazonaws.com"
                                ]
                            }}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_with_multiple_comparison_expressions_with_AND_OR_combinations(self):
        stix_pattern = "[x-aws-s3-bucket:bucket_type='Destination' OR  x-aws-finding-service:action." \
                       "service_name='ec2.amazonaws.com' AND network-traffic:x_direction = 'INBOUND'" \
                       " AND x-aws-resource:resource_role = 'TARGET']"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.resourceRole": {
                                "Equals": [
                                    "TARGET"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687074952666,
                                "LessThanOrEqual": 1687075252666
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "resource.s3BucketDetails.type": {
                                "Equals": [
                                    "Destination"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687074952666,
                                "LessThanOrEqual": 1687075252666
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.awsApiCallAction.serviceName": {
                                "Equals": [
                                    "ec2.amazonaws.com"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687074952666,
                                "LessThanOrEqual": 1687075252666
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.networkConnectionAction.connectionDirection": {
                                "Equals": [
                                    "INBOUND"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687074952666,
                                "LessThanOrEqual": 1687075252666
                            }}}}]}
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_query_for_multiple_observation_with_and_without_qualifier(self):
        stix_pattern = "[network-traffic:src_port >= 32794 OR x-aws-resource:account_id='123456789']" \
                       "AND [x-ibm-finding:alert_id='0ff5ef449377437b9c9c0892d38d5adf' AND  " \
                       "user-account:user_id = 'user1'] OR [x-aws-s3-bucket:bucket_type='Destination']" \
                       "START t'2023-05-10T11:00:00.000Z'STOP t'2023-06-01T11:00:00.003Z'"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "accountId": {
                                "Equals": [
                                    "123456789"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687099841192,
                                "LessThanOrEqual": 1687100141192
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.networkConnectionAction.localPortDetails.port": {
                                "GreaterThanOrEqual": 32794
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687099841192,
                                "LessThanOrEqual": 1687100141192
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "resource.accessKeyDetails.principalId": {
                                "Equals": [
                                    "user1"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1687099841192,
                                "LessThanOrEqual": 1687100141192
                            },
                            "id": {
                                "Equals": [
                                    "0ff5ef449377437b9c9c0892d38d5adf"
                                ]
                            }}}},
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "resource.s3BucketDetails.type": {
                                "Equals": [
                                    "Destination"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1683716400000,
                                "LessThanOrEqual": 1685617200003
                            }}}}]
        }
        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_multiple_observation_with_single_qualifier_with_precedence_bracket(self):
        stix_pattern = "([x-aws-s3-bucket:bucket_type = 'Destination' AND network-traffic:protocols[*] = 'UDP'] " \
                       "OR [x-aws-resource:account_id='123456789' OR x-aws-instance:image_id='ami-99999999'])" \
                       "START t'2023-03-15T11:20:35.000Z'STOP t'2023-05-10T11:00:00.003Z'"
        query = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        query = _remove_timestamp_from_query(query)
        queries = {
            "queries": [
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "service.action.networkConnectionAction.protocol": {
                                "Equals": [
                                    "UDP"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1678879235000,
                                "LessThanOrEqual": 1683716400003
                            },
                            "resource.s3BucketDetails.type": {
                                "Equals": [
                                    "Destination"
                                ]
                            }
                        }
                    }
                },
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "resource.instanceDetails.imageId": {
                                "Equals": [
                                    "ami-99999999"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1678879235000,
                                "LessThanOrEqual": 1683716400003
                            }
                        }
                    }
                },
                {
                    "FindingCriteria": {
                        "Criterion": {
                            "accountId": {
                                "Equals": [
                                    "123456789"
                                ]
                            },
                            "updatedAt": {
                                "GreaterThanOrEqual": 1678879235000,
                                "LessThanOrEqual": 1683716400003
                            }
                        }
                    }
                }
            ]
        }

        queries = _remove_timestamp_from_query(queries)
        self._test_query_assertions(query, queries)

    def test_invalid_qualifier_with_future_timestamp(self):
        stix_pattern = "[network-traffic:src_port >= 32794]START t'2023-01-19T11:00:00.000Z' " \
                       "STOP t'2024-02-07T11:00:00.003Z'"
        result = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert 'Start/Stop time should not be in the future UTC timestamp' in result['error']

    def test_stop_time_lesser_than_start_time(self):
        stix_pattern = "[network-traffic:src_port >= 32794]START t'2023-01-19T11:00:00.000Z' " \
                       "STOP t'2022-02-07T11:00:00.003Z'"
        result = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert 'Start time should be lesser than Stop time' in result['error']

    def test_invalid_value_for_integer_based_field(self):
        stix_pattern = "[autonomous-system:number = 'guardduty']"
        result = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'wrong parameter' in result['error']

    def test_invalid_operator_for_guardduty(self):
        stix_pattern = "[autonomous-system:number LIKE 50]"
        result = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "mapping_error" == result['code']
        assert 'data mapping error : Unable to map the following STIX Operators: [Like] to data source fields' in \
               result['error']

    def test_invalid_operator_for_enum_fields(self):
        stix_pattern = "[network-traffic:protocols[*] > 'TCP']"
        result = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'wrong parameter : GreaterThan operator is not supported for Enum type field ' \
               'network-traffic:protocols[*]. Possible supported operators are  =, !=, IN, NOT IN ' in \
               result['error']

    def test_invalid_operator_for_string_fields(self):
        stix_pattern = "[x-aws-instance:image_id <= 'ami-99999999']"
        result = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'LessThanOrEqual operator is not supported for string type field ' in result['error']

    def test_invalid_value_enum_type_field(self):
        stix_pattern = "[network-traffic:protocols[*] = 'tcp']"
        result = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert "wrong parameter : The input value provided for the field network-traffic:protocols[*] is " \
               "not among the possible values of the field.Suggested values are ['GRE', 'ICMP', 'TCP', 'UDP']" in \
               result['error']

    def test_invalid_value_for_boolean_type_field(self):
        stix_pattern = "[x-ibm-finding:x_archived = 'aws']"
        result = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert ' Invalid boolean type input' in result['error']

    def test_invalid_operator_for_boolean_field(self):
        stix_pattern = "[x-ibm-finding:x_archived NOT IN (false,true)]"
        result = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "not_implemented" == result['code']
        assert 'NOT In operator is not supported for Boolean type' in result['error']

    def test_similar_stix_attributes_for_and_operator(self):
        stix_pattern = "[x-aws-finding-service:action.action_type='NETWORK_CONNECTION' " \
                       "AND x-aws-finding-service:action.action_type='DNS_REQUEST']"
        result = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert 'expression is used in the pattern which has only AND comparison operator. Recommended to Use ' \
               'OR operator for similar STIX attributes' in result['error']

    def test_similar_mapping_fields_in_different_attributes_for_and_operator(self):
        stix_pattern = "[ipv4-addr:value = '1.1.1.1' AND network-traffic:src_ref.value = '2.2.2.2']"
        result = translation.translate('aws_guardduty', 'query', '{}', stix_pattern)
        assert result['success'] is False
        assert "translation_error" == result['code']
        assert 'same data source field mapping with another expression in the pattern which has ' \
               'only AND comparison operator' in result['error']
